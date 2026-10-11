#!/usr/bin/env python3
"""Met à jour data.json à partir des pages listées dans sources.json.

Principe : une IA (par défaut Gemini, offre gratuite) lit le texte d'une page et renvoie les chiffres
AVEC la phrase exacte où elle les a trouvés. Le script ne retient un chiffre que si :
  1. la phrase existe vraiment dans la page (contre les inventions de l'IA) ;
  2. le chiffre figure dans cette phrase ;
  3. il reste dans une fourchette plausible ;
  4. il ne s'écarte pas trop de la valeur précédente (sinon : à relire, non appliqué).
Rien n'est publié sans relecture : le workflow ouvre une demande de fusion (pull request).

Usage : python scripts/update_prices.py [--dry-run] [--only elec,gaz,primes,refs]
Variables : GEMINI_API_KEY (par défaut, gratuit), ou MISTRAL_API_KEY / ANTHROPIC_API_KEY selon PROVIDER ; MODEL et CONTACT facultatifs.
"""
import argparse, unicodedata, datetime, hashlib, html.parser, json, os, re, sys, time, urllib.error, urllib.parse, urllib.request, urllib.robotparser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data.json")
SOURCES = os.path.join(ROOT, "sources.json")
STATE = os.path.join(ROOT, "state", "hashes.json")
REPORT = os.path.join(ROOT, "report.md")
MONTHS = ["janv.", "févr.", "mars", "avr.", "mai", "juin", "juil.", "août", "sept.", "oct.", "nov.", "déc."]
BOUNDS = {"elec_kwh": (0.10, 0.45), "elec_abo": (100, 450), "gas_kwh": (0.08, 0.30), "gas_abo": (80, 700), "prime": (0, 200)}


# ---------- lecture des pages ----------
class _Text(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(); self.out = []; self.skip = 0
    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style", "noscript", "svg"): self.skip += 1
        if tag in ("p", "div", "br", "li", "tr", "h1", "h2", "h3", "h4", "td", "th"): self.out.append("\n")
    def handle_endtag(self, tag):
        if tag in ("script", "style", "noscript", "svg") and self.skip: self.skip -= 1
    def handle_data(self, data):
        if not self.skip: self.out.append(data)

def norm(t):
    t = t.replace(" ", " ").replace(" ", " ").replace("’", "'")
    return re.sub(r"\s+", " ", t).strip().lower()

def fold(t):
    """Minuscules sans accents, pour comparer « Électricité » et « Electricité »."""
    return "".join(c for c in unicodedata.normalize("NFD", norm(t)) if unicodedata.category(c) != "Mn")

def html_to_text(raw):
    p = _Text(); p.feed(raw)
    return re.sub(r"[ \t]+", " ", re.sub(r"\n\s*\n+", "\n", "".join(p.out))).strip()

def pdf_to_text(raw):
    try: import pypdf, io
    except ImportError: raise RuntimeError("PDF : installez pypdf (pip install pypdf)")
    rd = pypdf.PdfReader(io.BytesIO(raw))
    return re.sub(r"[ \t]+", " ", "\n".join((pg.extract_text() or "") for pg in rd.pages[:40])).strip()

_robots = {}
def allowed(url, ua):
    host = urllib.parse.urlsplit(url)
    base = f"{host.scheme}://{host.netloc}"
    if base not in _robots:
        rp = urllib.robotparser.RobotFileParser(); rp.set_url(base + "/robots.txt")
        try: rp.read()
        except Exception: rp = None
        _robots[base] = rp
    rp = _robots[base]
    return True if rp is None else rp.can_fetch(ua, url)

def fetch_text(url):
    ua = "ComparateurEnergieBot/1.0 (+" + os.environ.get("CONTACT", "mise a jour mensuelle, non lucratif") + ")"
    if not allowed(url, ua): raise RuntimeError("interdit par robots.txt")
    last = None
    for attempt in range(2):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": ua, "Accept-Language": "fr"})
            with urllib.request.urlopen(req, timeout=30) as r:
                raw, ctype = r.read(), (r.headers.get("Content-Type", "") if getattr(r, "headers", None) else "")
            if "pdf" in ctype.lower() or url.lower().split("?")[0].endswith(".pdf") or raw[:5] == b"%PDF-":
                return pdf_to_text(raw)
            return html_to_text(raw.decode("utf-8", "replace"))
        except Exception as e:
            last = e; time.sleep(3)
    raise RuntimeError(str(last))

def window(text, needle, size=6000, maxlen=40000):
    """Garde les passages autour du nom de l'offre si la page est très longue."""
    if len(text) <= maxlen or not needle: return text[:maxlen]
    low, key, parts, pos = text.lower(), needle.lower(), [text[:2000]], 0
    for _ in range(3):
        i = low.find(key, pos)
        if i < 0: break
        parts.append(text[max(0, i - 500): i + size]); pos = i + size
    return "\n[...]\n".join(parts)


# ---------- appel de l'IA ----------
SYSTEM = ("Tu extrais des chiffres de tarifs d'énergie depuis le texte brut d'une page web française. "
          "Réponds par un unique objet JSON, sans autre texte. Pour chaque champ demandé, renvoie "
          '{"value": nombre ou null, "quote": phrase copiée MOT POUR MOT depuis la page, ou null}. '
          "Ne déduis rien, ne calcule rien, n'arrondis pas : si le chiffre n'est pas écrit dans la page pour le cas demandé, mets null. "
          "Les prix sont en euros TTC ; les prix du kWh en euros par kWh (ex. 0,2330), pas en centimes.")

def _post(url, headers, body, tries=4):
    """POST JSON avec attente et nouvel essai en cas de limite de débit (429) ou d'erreur serveur."""
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, data=json.dumps(body).encode(), method="POST", headers={"content-type": "application/json", **headers})
            with urllib.request.urlopen(req, timeout=120) as r: return json.load(r)
        except urllib.error.HTTPError as e:
            last = e
            if e.code in (429, 500, 502, 503, 504) and i < tries - 1: time.sleep(float(os.environ.get("RETRY_WAIT", "30")) * (i + 1)); continue
            raise RuntimeError(f"HTTP {e.code} : " + e.read().decode("utf-8", "replace")[:200])
    raise RuntimeError(str(last))

def _json_from(txt):
    m = re.search(r"\{.*\}", txt, re.S)
    if not m: raise RuntimeError("réponse sans JSON")
    return json.loads(m.group(0))

def call_llm(prompt):
    """Fournisseur choisi par PROVIDER (ou sources.json) : gemini (gratuit), mistral (gratuit, compatible OpenAI) ou anthropic (payant)."""
    cfg = load(SOURCES)
    provider = os.environ.get("PROVIDER") or cfg.get("provider", "gemini")
    model = os.environ.get("MODEL") or cfg.get("model", "gemini-3.1-flash-lite")
    time.sleep(float(os.environ.get("LLM_DELAY", "6")))   # reste sous les limites par minute des offres gratuites
    if provider == "gemini":
        key = os.environ.get("GEMINI_API_KEY")
        if not key: raise RuntimeError("GEMINI_API_KEY absente")
        out = _post(f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent", {"x-goog-api-key": key},
                    {"systemInstruction": {"parts": [{"text": SYSTEM}]}, "contents": [{"role": "user", "parts": [{"text": prompt}]}],
                     "generationConfig": {"temperature": 0, "responseMimeType": "application/json"}})
        parts = (((out.get("candidates") or [{}])[0].get("content") or {}).get("parts") or [])
        return _json_from("".join(x.get("text", "") for x in parts))
    if provider == "mistral":
        key = os.environ.get("MISTRAL_API_KEY")
        if not key: raise RuntimeError("MISTRAL_API_KEY absente")
        out = _post("https://api.mistral.ai/v1/chat/completions", {"authorization": "Bearer " + key},
                    {"model": model, "temperature": 0, "response_format": {"type": "json_object"},
                     "messages": [{"role": "system", "content": SYSTEM}, {"role": "user", "content": prompt}]})
        return _json_from(out["choices"][0]["message"]["content"])
    if provider == "anthropic":
        key = os.environ.get("ANTHROPIC_API_KEY")
        if not key: raise RuntimeError("ANTHROPIC_API_KEY absente")
        out = _post("https://api.anthropic.com/v1/messages", {"x-api-key": key, "anthropic-version": "2023-06-01"},
                    {"model": model, "max_tokens": 1500, "temperature": 0, "system": SYSTEM, "messages": [{"role": "user", "content": prompt}]})
        return _json_from("".join(b.get("text", "") for b in out.get("content", []) if b.get("type") == "text"))
    raise RuntimeError(f"fournisseur inconnu : {provider}")


# ---------- contrôles ----------
def number_forms(v):
    """Écritures exactes du nombre (virgule ou point), sans arrondi : 0.24 -> 0,24 / 0,240 / 0,2400."""
    forms = set()
    for nd in range(0, 5):
        s = f"{v:.{nd}f}"
        if abs(float(s) - v) < 1e-9: forms.add(s); forms.add(s.replace(".", ","))
    return forms

def check_field(f, page_norm, lo, hi):
    """Renvoie (valeur, None) si le champ est fiable, sinon (None, raison)."""
    if not isinstance(f, dict) or f.get("value") is None: return None, "non trouvé dans la page"
    v, q = f.get("value"), f.get("quote")
    if not isinstance(v, (int, float)) or isinstance(v, bool): return None, "valeur non numérique"
    if not q or norm(q) not in page_norm: return None, "phrase citée absente de la page"
    qn = norm(q).replace(" ", "")
    if not any(re.search(r"(?<![\d,.])" + re.escape(x) + r"(?!\d|[,.]\d)", qn) for x in number_forms(float(v))): return None, "chiffre absent de la phrase citée"
    if not (lo <= v <= hi): return None, f"hors fourchette plausible ({lo} à {hi})"
    return float(v), None

def too_far(new, old, rel):
    return old and abs(new - old) / old > rel


# ---------- état, rapport ----------
def load(path, default=None):
    try:
        with open(path, encoding="utf-8") as fh: return json.load(fh)
    except FileNotFoundError: return default

def save(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh: json.dump(obj, fh, ensure_ascii=False, indent=1); fh.write("\n")

class Report:
    def __init__(self): self.applied, self.review, self.failed, self.same, self.url_fail = [], [], [], [], {}
    def md(self, today):
        grouped = [f"{u} : page illisible ({why}). Concerne : " + ", ".join(sorted(set(ls))) for u, (why, ls) in self.url_fail.items()]
        failed = grouped + self.failed
        def sec(t, rows): return f"## {t} ({len(rows)})\n\n" + ("\n".join("- " + r for r in rows) if rows else "Aucun.") + "\n\n"
        return (f"# Mise à jour des données du {today}\n\n"
                "Relisez chaque ligne avant de fusionner : l'IA peut se tromper, les contrôles automatiques limitent les erreurs sans les exclure.\n\n"
                + sec("Changements appliqués", self.applied) + sec("À relire : valeur proposée mais non appliquée", self.review)
                + sec("Sources en échec", failed) + sec("Inchangé", self.same))


# ---------- mise à jour ----------
def pagetext(url, cache, state, rep, label, needle=None):
    if url in cache:
        if cache[url] is None and url in rep.url_fail: rep.url_fail[url][1].append(label)
        return cache[url]
    try:
        time.sleep(float(os.environ.get("FETCH_DELAY", "2")))
        t = fetch_text(url)
    except Exception as e:
        rep.url_fail.setdefault(url, [str(e), []])[1].append(label); cache[url] = None; return None
    cache[url] = t
    return t

def ask(label, url, text, needle, fields, state, rep, extra=""):
    """fields : {nom: description}. Renvoie le JSON de l'IA ou None. Saute l'appel si la page n'a pas changé."""
    body = window(text, needle)
    h = hashlib.sha256((body + "|" + needle + "|" + ",".join(fields)).encode()).hexdigest()[:16]
    key = f"{url}|{needle}"
    if state.get(key) == h and not os.environ.get("FORCE"):
        rep.same.append(f"{label} : page inchangée depuis la dernière lecture"); return None, None
    prompt = (f"Page : {url}\n{extra}\nChamps demandés :\n" + "\n".join(f"- {k} : {v}" for k, v in fields.items())
              + '\n\nRéponds par {"fields": {"<nom>": {"value": ..., "quote": ...}, ...}}.\n\n=== TEXTE DE LA PAGE ===\n' + body)
    try:
        out = call_llm(prompt)
    except Exception as e:
        rep.failed.append(f"{label} : appel à l'IA en échec ({e})"); return None, None
    commit = lambda: state.__setitem__(key, h)   # mémorisé seulement si les contrôles passent
    return (out.get("fields", {}) if isinstance(out, dict) else None), commit

def update_offers(data, src, state, rep, kinds, cache):
    rel = src["max_rel_change"]; today = data["updated_label"]
    for kind, rows in (("elec", data["elec"]), ("gaz", data["gas"])):
        if kind not in kinds: continue
        for r in rows:
            url = src["tarifs_pages"].get(r["k"]); label = f"{kind} · {r['name']} ({r['offer']})"
            raison = src.get("manuel", {}).get(kind, {}).get(r["k"])
            if raison: rep.same.append(f"{label} : à vérifier à la main ({raison})"); continue
            if not url: rep.failed.append(f"{label} : aucune page dans sources.json"); continue
            text = pagetext(url, cache, state, rep, label)
            if not text: continue
            fields = {"offre": f"le nom de l'offre « {r['offer']} » tel qu'écrit dans la page (value = 1 si présent, sinon null)"}
            if kind == "elec":
                fields["kwh"] = "prix du kWh TTC, option Base, compteur 6 kVA (ou 3 à 6 kVA), pour cette offre, en €/kWh"
                fields["abo"] = "abonnement annuel TTC, option Base, 6 kVA, pour cette offre, en €/an (si l'abonnement est mensuel, laisse null)"
                fields["kwh9"] = "prix du kWh TTC, option Base, 9 kVA, pour cette offre (null si absent)"
            else:
                fields["kwh"] = "prix du kWh TTC de gaz, profil chauffage (B1), pour cette offre, en €/kWh"
            got, commit = ask(label, url, text, r["offer"], fields, state, rep, f"Offre cherchée : {r['offer']} ({r['name']}), {'électricité' if kind == 'elec' else 'gaz'}.")
            if got is None: continue
            pn = norm(text)
            q = (got.get("offre") or {}).get("quote")
            if not q or norm(q) not in pn or fold(r["offer"]).split(" ")[0] not in fold(q): rep.failed.append(f"{label} : offre non retrouvée dans la page"); continue
            lk, la = ("elec_kwh", "elec_abo") if kind == "elec" else ("gas_kwh", "gas_abo")
            kwh, e1 = check_field(got.get("kwh"), pn, *BOUNDS[lk])
            if kind == "gaz": abo, e2 = r.get("abo_skip", True), None  # abonnement gaz : non lu (les pages mélangent B0/B1), valeur conservée
            else: abo, e2 = check_field(got.get("abo"), pn, *BOUNDS[la])
            changed = []
            if kwh is None and e1 == "non trouvé dans la page":
                i = text.lower().find(r["offer"].lower().split(",")[0][:12]); print(f"[diagnostic] {label} : texte lu autour de l'offre : " + repr(text[max(0, i): i + 700] if i >= 0 else "(nom de l'offre absent du texte)"), file=sys.stderr)
            if kwh is None: rep.review.append(f"{label} : kWh refusé ({e1})")
            elif too_far(kwh, r["a"], rel["kwh"]): rep.review.append(f"{label} : kWh {r['a']} → {kwh} (écart > {int(rel['kwh']*100)} %, non appliqué)")
            elif abs(kwh - r["a"]) > 1e-9:
                if kind == "elec" and "b" in r: r["b"] = round(r["b"] + (kwh - r["a"]), 4)
                changed.append(f"kWh {r['a']} → {kwh}"); r["a"] = kwh
            if kind == "elec" and kwh is not None:
                k9, _ = check_field(got.get("kwh9"), pn, *BOUNDS["elec_kwh"])
                if k9 is not None and not too_far(k9, r.get("b"), rel["kwh"]): r["b"] = k9
            amap = data["abo_e"] if kind == "elec" else data["abo_g"]
            if kind == "gaz": pass
            elif abo is None: rep.review.append(f"{label} : abonnement refusé ({e2})")
            elif too_far(abo, amap.get(r["k"]), rel["abo"]): rep.review.append(f"{label} : abonnement {amap.get(r['k'])} → {abo} (écart > {int(rel['abo']*100)} %, non appliqué)")
            elif abs(abo - amap.get(r["k"], -1)) > 1e-9:
                changed.append(f"abonnement {amap.get(r['k'])} → {abo}"); amap[r["k"]] = abo
            if kwh is not None and abo is not None:
                commit(); r["d"] = today; r["s"] = [urllib.parse.urlsplit(url).netloc.replace("www.", ""), url]
                if kind == "elec": data.setdefault("abo_d", {})[r["k"]] = today
            if changed: rep.applied.append(f"{label} : " + ", ".join(changed))
            elif kwh is not None and abo is not None: rep.same.append(f"{label} : vérifié, identique")

def update_primes(data, src, state, rep, cache):
    today = data["updated_label"]
    for k, p in data["primes"].items():
        if not p.get("s"): continue
        url, label = src.get("primes_pages", {}).get(k) or p["s"][1], f"prime · {p['name']}"
        raison = src.get("manuel", {}).get("primes", {}).get(k)
        if raison: rep.same.append(f"{label} : à vérifier à la main ({raison})"); continue
        text = pagetext(url, cache, state, rep, label)
        if not text: continue
        fields = {"parrain": f"montant de la prime du parrain chez {p['name']}, en euros (null si ce n'est pas une somme en euros)",
                  "filleul": f"montant de la prime du filleul chez {p['name']}, en euros (null si ce n'est pas une somme en euros)"}
        got, commit = ask(label, url, text, p["name"], fields, state, rep, f"Fournisseur : {p['name']}. Plusieurs fournisseurs peuvent figurer dans la page : ne retiens que {p['name']}.")
        if got is None: continue
        pn = norm(text); changes = []; confirmed = 0
        for fld, txt, num in (("parrain", "p", "pn"), ("filleul", "f", "fn")):
            v, why = check_field(got.get(fld), pn, *BOUNDS["prime"])
            if v is None: rep.review.append(f"{label} : {fld} non confirmé ({why})"); continue
            confirmed += 1
            if int(v) != p[num] and not (p[num] <= 0 and v == 0):
                changes.append(f"{fld} {p[txt]} → {int(v)} €"); p[txt] = f"{int(v)} €"; p[num] = int(v)
        if confirmed == 2: commit(); p["s"] = [urllib.parse.urlsplit(url).netloc.replace("www.", ""), url]
        if changes:
            p["st"] = "check"; p["d"] = f"relevé le {today}"
            rep.applied.append(f"{label} : " + ", ".join(changes) + " (passé en « à vérifier »)")
        else: rep.same.append(f"{label} : montants identiques ou non confirmés")

def update_refs(data, src, state, rep, cache):
    today = data["updated_label"]; rel = src["max_rel_change"]
    url = src["references"]["trv"]; label = "référence · tarif réglementé"
    text = pagetext(url, cache, state, rep, label)
    if text:
        f = {"kwh_3_6": "prix du kWh TTC du tarif réglementé Bleu, option Base, 3 à 6 kVA (€/kWh)",
             "kwh_9": "prix du kWh TTC du tarif réglementé Bleu, option Base, 9 kVA et plus (€/kWh)"}
        got, commit = ask(label, url, text, "tarif réglementé", f, state, rep)
        if got:
            pn = norm(text); ref = data["elec_ref"]
            for fld, key, old, lo_hi, setter in (("kwh_3_6", "a", ref["a"], "elec_kwh", lambda v: ref.__setitem__("a", v)),
                                                 ("kwh_9", "b", ref["b"], "elec_kwh", lambda v: ref.__setitem__("b", v))):
                v, why = check_field(got.get(fld), pn, *BOUNDS[lo_hi])
                if v is not None and fld == "kwh_3_6": ref["s"] = [urllib.parse.urlsplit(url).netloc.replace("www.", ""), url]
                if v is None: rep.review.append(f"{label} : {fld} refusé ({why})")
                elif too_far(v, old, rel["kwh"]): rep.review.append(f"{label} : {fld} {old} → {v} (écart important, non appliqué)")
                elif abs(v - old) > 1e-9: setter(v); rep.applied.append(f"{label} : {fld} {old} → {v}")
    url = src["references"]["gas_ref"]; label = "référence · prix repère du gaz (CRE)"
    text = pagetext(url, cache, state, rep, label)
    if text:
        f = {"b1_kwh": "prix repère CRE du gaz, option B1 (chauffage), €/kWh TTC", "b0_kwh": "prix repère CRE du gaz, option B0 (cuisson et eau chaude), €/kWh TTC"}
        got, commit = ask(label, url, text, "prix repère", f, state, rep)
        if got:
            pn = norm(text)
            for fld, tgt, key, b in (("b1_kwh", data["gas_b1"], "a", "gas_kwh"), ("b0_kwh", data["gas_b0"], "a", "gas_kwh")):
                v, why = check_field(got.get(fld), pn, *BOUNDS[b])
                if v is not None and fld == "b1_kwh": data["gas_ref"]["s"] = [urllib.parse.urlsplit(url).netloc.replace("www.", ""), url]
                if v is None: rep.review.append(f"{label} : {fld} refusé ({why})")
                elif too_far(v, tgt[key], rel["kwh"]): rep.review.append(f"{label} : {fld} {tgt[key]} → {v} (écart important, non appliqué)")
                elif abs(v - tgt[key]) > 1e-9:
                    rep.applied.append(f"{label} : {fld} {tgt[key]} → {v}"); tgt[key] = v
                    if fld == "b1_kwh": data["gas_ref"]["a"] = v

def maintenant():
    """Date et heure de Paris (le serveur GitHub est en heure UTC)."""
    try:
        from zoneinfo import ZoneInfo
        return datetime.datetime.now(ZoneInfo("Europe/Paris"))
    except Exception:
        return datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=2)


def main(argv=None):
    ap = argparse.ArgumentParser(); ap.add_argument("--dry-run", action="store_true"); ap.add_argument("--only", default="elec,gaz,primes,refs")
    a = ap.parse_args(argv); kinds = set(a.only.split(","))
    data, src = load(DATA), load(SOURCES); state = load(STATE, {}) or {}
    now = maintenant(); data["updated"] = now.date().isoformat(); data["updated_label"] = f"{now.day} {MONTHS[now.month-1]} {now.year}"; data["updated_time"] = now.strftime("%H:%M")
    rep, cache = Report(), {}
    if kinds & {"elec", "gaz"}: update_offers(data, src, state, rep, kinds, cache)
    if "primes" in kinds: update_primes(data, src, state, rep, cache)
    if "refs" in kinds: update_refs(data, src, state, rep, cache)
    md = rep.md(data["updated_label"]); print(md)
    if not a.dry_run:
        # la date globale ne change que si au moins une valeur a été vérifiée avec succès
        if not (rep.applied or rep.same):
            old = load(DATA); data["updated"], data["updated_label"] = old["updated"], old["updated_label"]
            if "updated_time" in old: data["updated_time"] = old["updated_time"]
            else: data.pop("updated_time", None)
        save(DATA, data); save(STATE, state)
        with open(REPORT, "w", encoding="utf-8") as fh: fh.write(md)
    return 0 if (rep.applied or rep.same) else 1

if __name__ == "__main__":
    sys.exit(main())
