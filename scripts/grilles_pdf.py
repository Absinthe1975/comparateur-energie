#!/usr/bin/env python3
"""Détection automatique des PDF de grilles tarifaires, téléchargement et lecture.

Le nom d'un PDF change souvent (date, numéro de version). On ne garde donc pas son adresse : on lit la page du
fournisseur qui le propose, on repère le lien par son TEXTE (« Grille tarifaire », « Mon gaz naturel »…) et par des
mots du nom de fichier, puis on télécharge ce que le lien désigne ce jour-là.

Règles de sécurité : robots.txt respecté ; si aucun lien ou plusieurs liens différents correspondent, on ne devine pas
(l'entrée est signalée dans le rapport) ; un fichier trop différent du précédent n'est pas appliqué.
Entrée de sources.json, rubrique « grilles » :
  {"k": "alterna", "offre": "Mon gaz naturel indexé", "page": "https://…", "type": "cp-gaz",
   "contient": ["grille"], "un_de": ["gaz naturel"], "exclut": ["biogaz"]}
  Au lieu de « page », une entrée peut donner « url » : adresse stable du PDF, ou adresse qui redirige vers le PDF du moment.
  type « cp-gaz » : grille par code postal, intégrée automatiquement (fichier prix-cp/…, offre de data.json) ;
  type « info »   : PDF seulement détecté ; le rapport signale qu'il a changé, pour une intégration à la main."""
import hashlib, html.parser, json, os, re, subprocess, tempfile, urllib.parse
import cp_prix

class _Liens(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(); self.liens = []; self._h = None; self._t = []
    def handle_starttag(self, tag, attrs):
        if tag == "a":
            self._h = dict(attrs).get("href"); self._t = []
    def handle_data(self, d):
        if self._h is not None: self._t.append(d)
    def handle_endtag(self, tag):
        if tag == "a" and self._h is not None:
            self.liens.append((self._h, " ".join("".join(self._t).split()))); self._h = None

def _f(t):
    import unicodedata
    t = t.lower().replace("’", "'").replace("_", " ").replace("-", " ").replace("%20", " ")
    return "".join(c for c in unicodedata.normalize("NFD", t) if unicodedata.category(c) != "Mn")

def liens_pdf(html_page, base):
    p = _Liens(); p.feed(html_page)
    vus, out = set(), []
    for h, t in p.liens:
        if not h or h.startswith(("#", "javascript:", "mailto:")): continue
        u = urllib.parse.urljoin(base, h.strip())
        if not re.search(r"\.pdf($|[?#])", u.lower()) or u in vus: continue
        vus.add(u); out.append((u, t))
    # sites dont les liens sont dans des données intégrées à la page (JSON : adresses avec « \\/ » ou « \\u002F ») : on lit aussi les adresses .pdf du texte brut
    brut = html_page.replace("\\u002F", "/").replace("\\u002f", "/").replace("\\/", "/")
    for m in re.finditer(r"""https?://[^"'\s<>\\]+?\.pdf(?:\?[^"'\s<>\\]*)?""", brut):
        u = m.group(0)
        if u not in vus: vus.add(u); out.append((u, ""))
    return out

def choisir(liens, regle):
    """-> (url, None) ou (None, raison). Le texte du lien et le nom du fichier sont examinés ensemble."""
    cont = [_f(x) for x in regle.get("contient", [])]
    un_de = [_f(x) for x in regle.get("un_de", [])]
    excl = [_f(x) for x in regle.get("exclut", [])]
    bons = []
    for u, t in liens:
        s = _f(t + " " + urllib.parse.unquote(u.rsplit("/", 1)[-1]))
        if all(c in s for c in cont) and (not un_de or any(x in s for x in un_de)) and not any(x in s for x in excl): bons.append((u, t))
    if not bons: return None, f"aucun lien PDF ne correspond ({len(liens)} PDF sur la page)"
    if len({u for u, _ in bons}) > 1: return None, "plusieurs PDF correspondent : " + " ; ".join(sorted({u for u, _ in bons}))
    return bons[0][0], None

def texte_pdf(raw):
    """Texte du PDF entier (pdftotext si disponible, sinon pypdf)."""
    with tempfile.NamedTemporaryFile(suffix=".pdf") as f:
        f.write(raw); f.flush()
        try:
            r = subprocess.run(["pdftotext", "-layout", f.name, "-"], capture_output=True, timeout=300)
            if r.returncode == 0 and r.stdout.strip(): return r.stdout.decode("utf-8", "replace")
        except Exception: pass
    import pypdf, io
    return "\n".join((pg.extract_text() or "") for pg in pypdf.PdfReader(io.BytesIO(raw)).pages)

def lire_date(txt):
    m = re.search(r"applicables?\s+au\s+(\d\d/\d\d/\d{4})", txt) or re.search(r"(?:en vigueur|valables?)\s+(?:à partir du|au|depuis le)\s+(\d\d/\d\d/\d{4})", txt)
    return m.group(1) if m else None

def _telecharger(url, allowed):
    import urllib.request, os
    ua = "ComparateurEnergieBot/1.0 (+" + os.environ.get("CONTACT", "mise a jour mensuelle, non lucratif") + ")"
    if not allowed(url, ua): raise RuntimeError("interdit par robots.txt")
    req = urllib.request.Request(url, headers={"User-Agent": ua, "Accept-Language": "fr"})
    with urllib.request.urlopen(req, timeout=60) as r: return r.read()

def update_grilles(data, src, state, rep, now, allowed=None, get=None, racine=None, to_text=None):
    """get(url) -> octets (page ou PDF). to_text(octets) -> texte. Injectables pour les tests."""
    entrees = src.get("grilles") or []
    if not entrees: return
    if get is None:
        import update_prices; allowed = allowed or update_prices.allowed
        get = lambda u: _telecharger(u, allowed)
    to_text = to_text or texte_pdf
    racine = racine or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    mem = state.setdefault("grilles", {})
    for e in entrees:
        nom = f"{e['k']} · {e['offre']}"
        try:
            if e.get("url"):
                # adresse stable (le PDF garde son adresse, ou l'adresse redirige vers le PDF du moment) : pas de page à fouiller
                url = e["url"]; raw = get(url)
                if raw[:5] != b"%PDF-":   # une page plutôt qu'un PDF : on cherche le lien dedans
                    u2, why = choisir(liens_pdf(raw.decode("utf-8", "replace"), url), e)
                    if not u2: rep.failed.append(f"{nom} : {url} n'est pas un PDF et aucun lien PDF n'y a été trouvé ({why})"); continue
                    url = u2; raw = get(url)
            else:
                page = get(e["page"]).decode("utf-8", "replace")
                url, why = choisir(liens_pdf(page, e["page"]), e)
                if not url: rep.failed.append(f"{nom} : PDF non trouvé sur {e['page']} ({why})"); continue
                raw = get(url)
            if raw[:5] != b"%PDF-": rep.failed.append(f"{nom} : {url} n'est pas un PDF"); continue
            h = hashlib.sha256(raw).hexdigest()
            if mem.get(nom, {}).get("sha") == h: rep.same.append(f"{nom} : PDF inchangé ({url})"); continue
            if e.get("type") != "cp-gaz":
                if nom not in mem:   # première vue : enregistré comme référence (grille déjà intégrée à la main), pas de fausse alerte
                    mem[nom] = {"sha": h, "url": url}; rep.same.append(f"{nom} : PDF enregistré comme référence ({url})"); continue
                rep.review.append(f"{nom} : PDF nouveau ou modifié, à intégrer à la main : {url}"); mem[nom] = {"sha": h, "url": url}; continue
            txt = to_text(raw)
            date = lire_date(txt)
            if not date: rep.review.append(f"{nom} : date de la grille introuvable dans {url}, non appliqué"); continue
            offre = next((r for r in data["gas"] if r["k"] == e["k"] and r["offer"] == e["offre"] and r.get("cpf")), None)
            if not offre: rep.failed.append(f"{nom} : offre absente de data.json ou sans champ cpf"); continue
            f = cp_prix.construire(e["k"], e["offre"], date, e.get("page") or e["url"], txt)
            chemin = os.path.join(racine, offre["cpf"])
            ancien = None
            try: ancien = json.load(open(chemin, encoding="utf-8"))
            except Exception: pass
            n = lambda t: sum(len(v.split()) for v in t["niv"].values()) + len(t["mixte"])
            if ancien and n(f["b1"]) < 0.8 * n(ancien["b1"]):
                rep.review.append(f"{nom} : {n(f['b1'])} codes postaux lus contre {n(ancien['b1'])} avant, non appliqué ({url})"); continue
            if ancien and abs(f["b1"]["moy"] - ancien["b1"]["moy"]) > 0.12 * ancien["b1"]["moy"]:
                rep.review.append(f"{nom} : prix moyen {f['b1']['moy']} contre {ancien['b1']['moy']} avant, écart trop grand, non appliqué ({url})"); continue
            json.dump(f, open(chemin, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
            niv = sorted(float(x) for x in f["b1"]["niv"])
            offre["a"] = niv[0]
            if len(f["b0"]["niv"]) == 1: offre["b0"] = float(next(iter(f["b0"]["niv"])))
            if len(niv) == 6: offre["zones"] = {"b1": niv, "b0": [offre["b0"]] * 6}
            offre["niv"], offre["nivd"] = "officiel", date
            mem[nom] = {"sha": h, "url": url}
            rep.applied.append(f"{nom} : grille par code postal du {date} ({n(f['b1'])} codes postaux) lue dans {url}")
        except Exception as ex:
            rep.failed.append(f"{nom} : {ex}")
