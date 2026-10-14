"""Prix repère du gaz par zone, tel que publié par Mint Énergie (sans IA).

La page https://informations.mint-energie.com/Pages/Informations/prix-repere-gaz.aspx republie le prix repère de la CRE
pour chacune des 6 zones tarifaires. C'est un formulaire ASP.NET : on rejoue ce que fait le navigateur
(champs cachés + mois, année, zone + clic sur « Voir le Prix Repère »).
Les offres Mint « indexées au prix repère » (Biogaz Online) sont au niveau de ce prix : on en tire leurs prix par zone.
Tout est strict : si la page ne répond pas à la zone ou au mois demandés, on lève une erreur plutôt que de deviner.
"""
import html, http.cookiejar, re, urllib.parse, urllib.request

UA = "ComparateurEnergieBot/1.0 (donnees publiques, non lucratif)"
CHAMPS = {"b1_kwh": "LBL_PriceKwh_B1_TTC", "b0_kwh": "LBL_PriceKwh_B0_TTC", "b1_abo": "LBL_PriceAbo_B1_TTC", "b0_abo": "LBL_PriceAbo_B0_TTC"}
MOIS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"]


def _num(s):
    return float(s.replace("\xa0", "").replace(" ", "").replace(",", "."))


def champs_caches(page):
    """Tous les <input type="hidden"> du formulaire (VIEWSTATE, EVENTVALIDATION…), à renvoyer tels quels."""
    out = {}
    for m in re.finditer(r"<input\b[^>]*>", page, re.I):
        tag = m.group(0)
        if not re.search(r'type="hidden"', tag, re.I): continue
        n, v = re.search(r'name="([^"]*)"', tag), re.search(r'value="([^"]*)"', tag)
        if n: out[n.group(1)] = html.unescape(v.group(1)) if v else ""
    return out


def _span(page, ident):
    m = re.search(r'<span id="' + re.escape(ident) + r'">([^<]*)</span>', page)
    if not m: raise ValueError(f"champ absent de la page : {ident}")
    return m.group(1).strip()


def lire_prix(page, zone, mois, annee):
    """Prix de la page, après contrôle que le titre correspond bien à la zone et au mois demandés."""
    z, d = _span(page, "LBL_Zone"), _span(page, "LBL_DatePrice")
    if z.lower() != f"zone {zone}": raise ValueError(f"la page répond « {z} » au lieu de « Zone {zone} »")
    if d.lower() != f"{MOIS[mois - 1]} {annee}": raise ValueError(f"la page répond « {d} » au lieu de « {MOIS[mois - 1]} {annee} »")
    out = {k: _num(_span(page, i)) for k, i in CHAMPS.items()}
    if not (0.08 <= out["b1_kwh"] < out["b0_kwh"] <= 0.35): raise ValueError(f"prix incohérents : {out}")
    return out


def zones(get, post, url, mois, annee):
    """get(url) -> html ; post(url, dict) -> html. Retourne {"b1": [6 prix], "b0": [6 prix], "b1_abo": x, "b0_abo": y}."""
    base = get(url); caches = champs_caches(base)
    if "__VIEWSTATE" not in caches: raise ValueError("formulaire introuvable (page modifiée ?)")
    res = []
    for z in range(1, 7):
        form = dict(caches, __EVENTTARGET="LB_Valid", __EVENTARGUMENT="", DDL_Month=f"{mois:02d}", DDL_Year=str(annee), DDL_Zone=str(z))
        res.append(lire_prix(post(url, form), z, mois, annee))
    b1 = [r["b1_kwh"] for r in res]
    if any(b1[i + 1] < b1[i] - 1e-9 for i in range(5)): raise ValueError(f"prix par zone non croissants : {b1}")
    return {"b1": b1, "b0": [r["b0_kwh"] for r in res], "b1_abo": res[0]["b1_abo"], "b0_abo": res[0]["b0_abo"]}


def reseau(allowed):
    """Fonctions get/post réelles. `allowed(url, ua)` applique le robots.txt du site."""
    jar = http.cookiejar.CookieJar(); op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
    def go(url, data=None):
        if not allowed(url, UA): raise RuntimeError("interdit par robots.txt")
        body = urllib.parse.urlencode(data).encode() if data is not None else None
        req = urllib.request.Request(url, data=body, headers={"User-Agent": UA, "Accept-Language": "fr"})
        with op.open(req, timeout=40) as r: return r.read().decode("utf-8", "replace")
    return (lambda u: go(u)), (lambda u, d: go(u, d))
