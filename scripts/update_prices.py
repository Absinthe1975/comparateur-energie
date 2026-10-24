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
import donnees

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DONNEES = os.path.join(ROOT, "donnees")   # toutes les données du site
DATA = os.path.join(DONNEES, "data.json")
SOURCES = os.path.join(DONNEES, "sources.json")
STATE = os.path.join(DONNEES, "etat", "hashes.json")
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

_dernier = {}   # dernier appel par site (pour ne pas enchaîner les requêtes vers le même serveur)

def espacer(url, delai=None, maintenant=time.monotonic, dormir=time.sleep):
    """Attend, si besoin, pour qu'au moins `delai` secondes (HOST_DELAY, 10 par défaut) séparent deux requêtes vers le même site."""
    delai = float(os.environ.get("HOST_DELAY", "10")) if delai is None else delai
    h = urllib.parse.urlsplit(url).netloc
    reste = _dernier.get(h, -1e9) + delai - maintenant()
    if reste > 0: dormir(reste)
    _dernier[h] = maintenant()

def attente_serveur(e, essai):
    """Durée d'attente après un « trop de requêtes » (429) ou une panne passagère (503) : Retry-After si le site l'indique (plafonné à 120 s), sinon 30 s, 60 s…"""
    try: ra = float(e.headers.get("Retry-After")) if getattr(e, "headers", None) and e.headers.get("Retry-After") else None
    except (TypeError, ValueError): ra = None
    return min(ra, 120.0) if ra is not None else 30.0 * (essai + 1)

def fetch_text(url):
    ua = "ComparateurEnergieBot/1.0 (+" + os.environ.get("CONTACT", "mise a jour mensuelle, non lucratif") + ")"
    if not allowed(url, ua): raise RuntimeError("interdit par robots.txt")
    last = None
    for attempt in range(3):
        try:
            espacer(url)
            req = urllib.request.Request(url, headers={"User-Agent": ua, "Accept-Language": "fr"})
            with urllib.request.urlopen(req, timeout=30) as r:
                raw, ctype = r.read(), (r.headers.get("Content-Type", "") if getattr(r, "headers", None) else "")
            if "pdf" in ctype.lower() or url.lower().split("?")[0].endswith(".pdf") or raw[:5] == b"%PDF-":
                return pdf_to_text(raw)
            return html_to_text(raw.decode("utf-8", "replace"))
        except urllib.error.HTTPError as e:
            last = e
            if e.code in (429, 503) and attempt < 2: time.sleep(attente_serveur(e, attempt))
            elif e.code not in (429, 503): break
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
    if os.path.basename(path) == "data.json" and os.path.dirname(path) == os.path.dirname(DATA):
        try: return donnees.charger(os.path.dirname(path))
        except FileNotFoundError: return default
    try:
        with open(path, encoding="utf-8") as fh: return json.load(fh)
    except FileNotFoundError: return default

def save(path, obj):
    if os.path.basename(path) == "data.json" and os.path.dirname(path) == os.path.dirname(DATA): return donnees.enregistrer(os.path.dirname(path), obj)
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

def ask(label, url, text, needle, fields, state, rep, extra="", nocache=False):
    """fields : {nom: description}. Renvoie le JSON de l'IA ou None. Saute l'appel si la page n'a pas changé."""
    body = window(text, needle)
    h = hashlib.sha256((body + "|" + needle + "|" + ",".join(fields)).encode()).hexdigest()[:16]
    key = f"{url}|{needle}"
    if state.get(key) == h and not nocache and not os.environ.get("FORCE"):
        rep.same.append(f"{label} : page inchangée depuis la dernière lecture"); return None, "inchangee"
    prompt = (f"Page : {url}\n{extra}\nChamps demandés :\n" + "\n".join(f"- {k} : {v}" for k, v in fields.items())
              + '\n\nRéponds par {"fields": {"<nom>": {"value": ..., "quote": ...}, ...}}.\n\n=== TEXTE DE LA PAGE ===\n' + body)
    try:
        out = call_llm(prompt)
    except Exception as e:
        rep.failed.append(f"{label} : appel à l'IA en échec ({e})"); return None, None
    commit = lambda: state.__setitem__(key, h)   # mémorisé seulement si les contrôles passent
    return (out.get("fields", {}) if isinstance(out, dict) else None), commit

def second_urls(src, k):
    v = src.get("tarifs_pages_2", {}).get(k)
    return [v] if isinstance(v, str) else list(v or [])

def confirm_offer(src, r, kind, kwh, cache, state, rep, label):
    """Relit l'offre sur les secondes sources. True : une seconde source donne le même kWh (à 0,0002 près) ;
    False : une seconde source lit un autre chiffre ; None : aucune seconde source exploitable."""
    verdict = None
    for url in second_urls(src, r["k"]):
        text = pagetext(url, cache, state, rep, f"{label} (second site)")
        if not text: continue
        fields = {"offre": f"le nom de l'offre « {r['offer']} » tel qu'écrit dans la page (value = 1 si présent, sinon null)",
                  "kwh": ("prix du kWh TTC, option Base, 6 kVA, pour cette offre, en €/kWh" if kind == "elec" else "prix du kWh TTC de gaz, profil chauffage (B1), pour cette offre, en €/kWh")}
        got, _ = ask(label + " (second site)", url, text, r["offer"], fields, state, rep, f"Offre cherchée : {r['offer']} ({r['name']}).", nocache=True)
        if not got: continue
        pn = norm(text); q = (got.get("offre") or {}).get("quote")
        if not q or norm(q) not in pn or fold(r["offer"]).split(" ")[0] not in fold(q): continue
        v, _ = check_field(got.get("kwh"), pn, *BOUNDS["elec_kwh" if kind == "elec" else "gas_kwh"])
        if v is None: continue
        if abs(v - kwh) <= 0.0002: return True
        verdict = False
    return verdict

def update_offers(data, src, state, rep, kinds, cache):
    rel = src["max_rel_change"]; today = data["updated_label"]
    for kind, rows in (("elec", data["elec"]), ("gaz", data["gas"])):
        if kind not in kinds: continue
        for r in rows:
            url = src["tarifs_pages"].get(r["k"]); label = f"{kind} · {r['name']} ({r['offer']})"
            raison = src.get("manuel", {}).get(kind, {}).get(r["k"])
            if raison: rep.same.append(f"{label} : à vérifier à la main ({raison})"); continue
            if r.get("niv") == "officiel":   # grille du fournisseur lue à la main ou par code : l'IA ne la retouche jamais
                rep.same.append(f"{label} : grille officielle{' du ' + r['nivd'] if r.get('nivd') else ''}, non relue par l'IA"); continue
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
            if got is None:
                if commit == "inchangee":   # même texte que la dernière lecture vérifiée : le prix est confirmé aujourd'hui
                    r["d"] = today
                    if kind == "elec": data.setdefault("abo_d", {})[r["k"]] = today
                continue
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
                conf = confirm_offer(src, r, kind, kwh, cache, state, rep, label)
                if conf is True:
                    if kind == "elec" and "b" in r: r["b"] = round(r["b"] + (kwh - r["a"]), 4)
                    changed.append(f"kWh {r['a']} → {kwh} (confirmé par un second site)"); r["a"] = kwh
                    if r.get("niv") == "officiel" or "zones" in r or "b0" in r:
                        r["niv"] = "confirmer"; r.pop("nivd", None); rep.review.append(f"{label} : prix modifié, le niveau « grille officielle », le B0 et les zones sont à revoir sur la grille du fournisseur")
                elif conf is False: rep.review.append(f"{label} : kWh {r['a']} → {kwh} contredit par un second site, non appliqué")
                else: rep.review.append(f"{label} : kWh {r['a']} → {kwh} vu sur un seul site, à confirmer sur un second (non appliqué)"); kwh = None
            elif os.environ.get("CROSSCHECK"):
                conf = confirm_offer(src, r, kind, r["a"], cache, state, rep, label)
                if conf is False: rep.review.append(f"{label} : kWh {r['a']} vérifié sur un site mais un second site donne une autre valeur : à contrôler")
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

def _urls(v):
    return [v] if isinstance(v, str) else list(v or [])

def _host(url):
    return urllib.parse.urlsplit(url).netloc.replace("www.", "")

def consensus(label, urls, needle, fields, bounds, cache, state, rep, extra=""):
    """Lit plusieurs sites. Pour chaque champ renvoie (valeur, [sites d'accord], [sites en désaccord]) ou None.
    Une valeur n'est retenue que si au moins DEUX sites indépendants donnent le même chiffre (à 0,0002 près)."""
    seen = {k: [] for k in fields}; ok_sites = 0
    for url in urls:
        text = pagetext(url, cache, state, rep, f"{label} ({_host(url)})")
        if not text: continue
        got, commit = ask(f"{label} ({_host(url)})", url, text, needle, fields, state, rep, extra, nocache=True)
        if not got: continue
        pn = norm(text); ok_sites += 1
        for k in fields:
            v, why = check_field(got.get(k), pn, *bounds)
            if v is not None: seen[k].append((v, url))
        if commit: commit()
    out = {}
    for k, vals in seen.items():
        best = None
        for v, _ in vals:
            grp = [(w, u) for w, u in vals if abs(w - v) <= 0.0002]
            if best is None or len(grp) > len(best): best = grp
        if not best: out[k] = None; continue
        agree = {u for _, u in best}; other = [u for _, u in vals if u not in agree]
        val = round(sum(w for w, _ in best) / len(best), 5)
        out[k] = (val, sorted(_host(u) for u in agree), sorted(_host(u) for u in other))
    return out, ok_sites

def apply_consensus(label, fld, res, old, rel, setter, rep, urls_count):
    r = res.get(fld)
    if not r: rep.review.append(f"{label} : {fld} introuvable sur les sites lus"); return None
    v, agree, other = r
    if other: rep.review.append(f"{label} : {fld} sites en désaccord ({', '.join(agree)} : {v} ; {', '.join(other)} : autre valeur), non appliqué"); return None
    if len(agree) < 2:
        if abs(v - old) > 1e-9: rep.review.append(f"{label} : {fld} {old} → {v} proposé par un seul site ({agree[0]}), à confirmer sur un second site (non appliqué)")
        else: rep.same.append(f"{label} : {fld} identique ({old}), vu sur un seul site ({agree[0]})")
        return None
    if too_far(v, old, rel): rep.review.append(f"{label} : {fld} {old} → {v} (écart important, non appliqué ; sites d'accord : {', '.join(agree)})"); return None
    if abs(v - old) > 1e-9: setter(v); rep.applied.append(f"{label} : {fld} {old} → {v} (confirmé par {', '.join(agree)})")
    else: rep.same.append(f"{label} : {fld} vérifié sur {len(agree)} sites ({', '.join(agree)})")
    return v

def update_refs(data, src, state, rep, cache):
    today = data["updated_label"]; rel = src["max_rel_change"]
    urls = _urls(src["references"]["trv"]); label = "référence · tarif réglementé"
    f = {"kwh_3_6": "prix du kWh TTC du tarif réglementé Bleu, option Base, 3 à 6 kVA (€/kWh)",
         "kwh_9": "prix du kWh TTC du tarif réglementé Bleu, option Base, 9 kVA et plus (€/kWh)"}
    res, n = consensus(label, urls, "tarif réglementé", f, BOUNDS["elec_kwh"], cache, state, rep)
    if n:
        ref = data["elec_ref"]
        v = apply_consensus(label, "kwh_3_6", res, ref["a"], rel["kwh"], lambda x: ref.__setitem__("a", x), rep, len(urls))
        apply_consensus(label, "kwh_9", res, ref["b"], rel["kwh"], lambda x: ref.__setitem__("b", x), rep, len(urls))
        if res.get("kwh_3_6") and len(res["kwh_3_6"][1]) >= 2: ref["s"] = [_host(urls[0]), urls[0]]
    urls = _urls(src["references"]["gas_ref"]); label = "référence · prix repère du gaz (CRE)"
    f = {"b1_kwh": "prix repère CRE du gaz, option B1 (CHAUFFAGE), €/kWh TTC, zone GRDF. Ne pas confondre avec B0.",
         "b0_kwh": "prix repère CRE du gaz, option B0 (CUISSON et eau chaude seulement), €/kWh TTC, zone GRDF. Plus élevé que B1."}
    res, n = consensus(label, urls, "prix repère", f, BOUNDS["gas_kwh"], cache, state, rep)
    if n:
        b1, b0 = res.get("b1_kwh"), res.get("b0_kwh")
        if b1 and b0 and b0[0] <= b1[0]:
            rep.review.append(f"{label} : valeurs incohérentes (B0 {b0[0]} doit être supérieur à B1 {b1[0]}), rien d'appliqué"); return
        def set_b1(x): data["gas_b1"]["a"] = x; data["gas_ref"]["a"] = x
        v = apply_consensus(label, "b1_kwh", res, data["gas_b1"]["a"], rel["kwh"], set_b1, rep, len(urls))
        apply_consensus(label, "b0_kwh", res, data["gas_b0"]["a"], rel["kwh"], lambda x: data["gas_b0"].__setitem__("a", x), rep, len(urls))
        if b1 and len(b1[1]) >= 2: data["gas_ref"]["s"] = [_host(urls[0]), urls[0]]

def maintenant():
    """Date et heure de Paris (le serveur GitHub est en heure UTC)."""
    try:
        from zoneinfo import ZoneInfo
        return datetime.datetime.now(ZoneInfo("Europe/Paris"))
    except Exception:
        return datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=2)


MOIS = ["janvier", "fevrier", "mars", "avril", "mai", "juin", "juillet", "aout", "septembre", "octobre", "novembre", "decembre"]

def update_trend(data, src, state, rep, cache, avant, now, officiel=None):
    """Compare la variation du prix repère annoncée par le médiateur (energie-info.fr) avec celle de notre prix B1.
    Information seulement : ne modifie aucun prix."""
    tpl = src.get("references", {}).get("gas_trend_template")
    if not tpl: return
    url = tpl.format(mois=MOIS[now.month - 1], annee=now.year); label = "contrôle · variation du prix repère du gaz (médiateur)"
    text = pagetext(url, cache, state, rep, label)
    if not text: return
    f = {"variation": "variation annoncée du prix repère du gaz en pourcentage TTC pour le mois en cours, en valeur absolue (ex. 6,3)"}
    got, commit = ask(label, url, text, "prix repère", f, state, rep)
    if not got: return
    pn = norm(text); v, why = check_field(got.get("variation"), pn, 0, 50)
    if v is None: rep.review.append(f"{label} : valeur refusée ({why})"); return
    q = norm(got["variation"]["quote"]); sens = 1 if "hausse" in q or "augment" in q else (-1 if "baisse" in q or "diminu" in q else 0)
    if not sens: rep.review.append(f"{label} : sens (hausse ou baisse) non confirmé dans la phrase citée"); return
    commit(); annonce = sens * v
    if officiel is not None:
        ok = abs(annonce - officiel) <= 0.3
        (rep.same if ok else rep.review).append(f"{label} : annoncé {annonce:+.1f} % TTC, la CRE donne {officiel:+.1f} % entre les deux derniers mois" + (" : cohérent" if ok else " : écart à vérifier"))
        return
    olds = avant if isinstance(avant, tuple) else (avant, None)
    news = (data["gas_b1"]["a"], data["gas_b0"]["a"])
    vars_ = [(n - o) / o * 100 for o, n in zip(olds, news) if o and abs(n - o) > 1e-9]
    if vars_:
        lo, hi = min(vars_), max(vars_); ok = lo - 2 <= annonce <= hi + 2
        msg = f"{label} : annoncé {annonce:+.1f} % TTC (moyenne), nos prix B1/B0 varient de " + " / ".join(f"{x:+.1f} %" for x in vars_)
        (rep.same if ok else rep.review).append(msg + (" : cohérent" if ok else " : écart à vérifier"))
    else:
        rep.review.append(f"{label} : annoncé {annonce:+.1f} % TTC, mais nos prix B1 et B0 du kWh sont inchangés : à vérifier à la main")

def update_official(data, src, rep, now, get=None):
    """Sources officielles de la CRE : elles font foi et l'emportent sur les sites lus par l'IA."""
    od = src.get("open_data"); info = {}
    if not od: return info
    import cre_open
    get = get or cre_open._get; today = now.date()
    def poser(label, old, new, setter, lo, hi, where, maxrel=0.25):
        if not (lo <= new <= hi) or abs(new - old) / old > maxrel:
            rep.review.append(f"{label} : {old} → {new} hors limites, non appliqué (source officielle : {where})"); return
        if abs(new - old) > 1e-9: setter(new); rep.applied.append(f"{label} : {old} → {new} (source officielle CRE : {where})")
        else: rep.same.append(f"{label} : {old} confirmé par la CRE ({where})")
    try:
        rid = od["trv_base_rid"]; ref = data["elec_ref"]
        t6, how = cre_open.trv(rid, 6, get); t9, _ = cre_open.trv(rid, 9, get)
        poser("CRE · tarif réglementé 3-6 kVA (kWh TTC)", ref["a"], t6["PART_VARIABLE_TTC"], lambda x: ref.__setitem__("a", x), *BOUNDS["elec_kwh"], "data.gouv.fr")
        poser("CRE · tarif réglementé 9 kVA et plus (kWh TTC)", ref["b"], t9["PART_VARIABLE_TTC"], lambda x: ref.__setitem__("b", x), *BOUNDS["elec_kwh"], "data.gouv.fr")
        for k, t in (("6", t6), ("9", t9)):
            ecart = abs(t["PART_FIXE_TTC"] - data["trv_abo"][k])
            if ecart > 2: rep.review.append(f"CRE · abonnement tarif réglementé {k} kVA : {t['PART_FIXE_TTC']} € (CRE) contre {data['trv_abo'][k]} € chez nous : à vérifier")
    except Exception as e:
        rep.failed.append(f"CRE · tarif réglementé (data.gouv.fr) : {e}")
    # abonnement du tarif réglementé pour les autres puissances du menu (12 à 36 kVA). Le fichier Base de la CRE n'a pas de ligne en vigueur
    # pour toutes (18 kVA et plus) et ses valeurs à 12 et 15 kVA diffèrent de la grille d'EDF : ces valeurs sont saisies d'après la grille
    # officielle d'EDF et la CRE ne fait que les confronter ; elle ne les remplit que si elles manquent.
    for k in ("12", "15", "18", "24", "30", "36"):
        old = data["trv_abo"].get(k)
        try:
            t, _ = cre_open.trv(od["trv_base_rid"], int(k), get); new = t["PART_FIXE_TTC"]
        except Exception as e:
            if old is None: rep.failed.append(f"CRE · abonnement tarif réglementé {k} kVA : {e}")
            continue
        if old is None:
            if 100 <= new <= 1500:
                data["trv_abo"][k] = new; rep.applied.append(f"CRE · abonnement tarif réglementé {k} kVA : relevé {new} € (source officielle CRE : data.gouv.fr)")
        elif abs(new - old) > 2:
            rep.review.append(f"CRE · abonnement tarif réglementé {k} kVA : {new} € (CRE) contre {old} € chez nous (grille EDF) : à vérifier")
    try:
        page = get(od["gas_page"]).decode("utf-8", "replace")
        raw = get(cre_open.trouver_xlsx(page))
        grilles = cre_open.gaz_grilles(raw)
        try: info["var_pct"] = cre_open.variation_mensuelle(cre_open.prvg_moyen(raw), today)
        except Exception: pass
        d, g = cre_open.gaz_en_vigueur(grilles, today)
        lab = f"CRE · prix repère gaz du {d.strftime('%d/%m/%Y')}"
        b1, b0 = data["gas_b1"], data["gas_b0"]
        def s1(x): b1["a"] = x; data["gas_ref"]["a"] = x
        poser(lab + " B1 (kWh TTC)", b1["a"], g["b1_kwh"], s1, *BOUNDS["gas_kwh"], "Excel cre.fr")
        poser(lab + " B0 (kWh TTC)", b0["a"], g["b0_kwh"], lambda x: b0.__setitem__("a", x), *BOUNDS["gas_kwh"], "Excel cre.fr")
        poser(lab + " B1 (abonnement TTC/an)", b1["abo"], g["b1_abo"], lambda x: b1.__setitem__("abo", x), *BOUNDS["gas_abo"], "Excel cre.fr")
        poser(lab + " B0 (abonnement TTC/an)", b0["abo"], g["b0_abo"], lambda x: b0.__setitem__("abo", x), *BOUNDS["gas_abo"], "Excel cre.fr")
    except Exception as e:
        rep.failed.append(f"CRE · prix repère gaz (cre.fr) : {e}")
    return info

def update_mint_zones(data, src, rep, now, get=None, post=None):
    """Prix par zone des offres indexées au prix repère (Mint Biogaz Online), lus sur la page de prix repère de Mint."""
    page = src.get("mint_prg")
    cibles = [r for r in data["gas"] if r.get("prg")]
    if not page or not cibles: return
    import mint_prg
    try:
        if get is None: get, post = mint_prg.reseau(allowed)
        z = mint_prg.zones(get, post, page, now.month, now.year)
        ref = data["gas_b1"]["a"]
        if abs(z["b1"][0] - ref) > 0.0006:
            rep.review.append(f"Mint · prix repère zone 1 : {z['b1'][0]} (page Mint) contre {ref} (CRE) : écart trop grand, non appliqué"); return
        if not all(0.08 <= x <= 0.30 for x in z["b1"] + z["b0"]): raise ValueError("prix hors limites")
        d1 = f"01/{now.month:02d}/{now.year}"
        for r in cibles:
            neuf = {"b1": [round(x, 4) for x in z["b1"]], "b0": [round(z["b0"][0], 4)] * 6}
            if r.get("zones") != neuf or r.get("a") != neuf["b1"][0]:
                r["zones"] = neuf; r["a"] = neuf["b1"][0]; r["b0"] = neuf["b0"][0]
                rep.applied.append(f"Mint · {r['offer']} : prix par zone du prix repère de {MONTHS[now.month-1]} {now.year} (page Mint)")
            else: rep.same.append(f"Mint · {r['offer']} : prix par zone confirmés (page Mint)")
            r["niv"], r["nivd"] = "officiel", d1
    except Exception as e:
        rep.failed.append(f"Mint · prix repère par zone : {e}")

def main(argv=None):
    ap = argparse.ArgumentParser(); ap.add_argument("--dry-run", action="store_true"); ap.add_argument("--only", default="elec,gaz,primes,refs,grilles")
    a = ap.parse_args(argv); kinds = set(a.only.split(","))
    data, src = load(DATA), load(SOURCES); state = load(STATE, {}) or {}
    now = maintenant(); data["updated"] = now.date().isoformat(); data["updated_label"] = f"{now.day} {MONTHS[now.month-1]} {now.year}"; data["updated_time"] = now.strftime("%H:%M")
    rep, cache = Report(), {}
    if kinds & {"elec", "gaz"}: update_offers(data, src, state, rep, kinds, cache)
    if "primes" in kinds: update_primes(data, src, state, rep, cache)
    avant_b1 = (data["gas_b1"]["a"], data["gas_b0"]["a"])
    if "refs" in kinds: update_refs(data, src, state, rep, cache); off = update_official(data, src, rep, now); update_mint_zones(data, src, rep, now); update_trend(data, src, state, rep, cache, avant_b1, now, off.get("var_pct"))
    if "grilles" in kinds:
        import grilles_pdf; grilles_pdf.update_grilles(data, src, state, rep, now)
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
