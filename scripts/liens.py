#!/usr/bin/env python3
"""Rassemble dans LIENS-RECUS.md tous les liens utilisés par le comparateur (sources, grilles, pages de prix, primes, références).

La partie entre les repères AUTO est réécrite à chaque lancement ; le reste du fichier (liens reçus par message) est conservé.
Usage : python3 scripts/liens.py"""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import donnees

DEB, FIN = "<!-- AUTO:DEBUT -->", "<!-- AUTO:FIN -->"

def collecter(racine="."):
    d = donnees.charger(racine)
    s = json.load(open(os.path.join(racine, "sources.json"), encoding="utf-8"))
    noms = {}
    for r in d.get("elec", []) + d.get("gas", []) + d.get("duo", []):
        noms.setdefault(r["k"], r["name"])
    for k, p in (d.get("primes") or {}).items(): noms.setdefault(k, p.get("name", k))
    par = {}
    def ajout(k, lib, url):
        if url and url.startswith("http"): par.setdefault(k, {}).setdefault(url, lib)
    for k, u in (d.get("liens") or {}).items(): ajout(k, "site du fournisseur", u)
    for g in s.get("grilles", []):
        ajout(g["k"], "grille : " + g.get("offre", ""), g.get("url") or g.get("page"))
    for cle, lib in (("tarifs_pages", "page de prix (comparateur)"), ("tarifs_pages_2", "page de prix (second comparateur)"), ("primes_pages", "page de parrainage")):
        for k, v in (s.get(cle) or {}).items():
            for u in (v if isinstance(v, list) else [v]): ajout(k, lib, u)
    for r in d.get("elec", []) + d.get("gas", []) + d.get("duo", []):
        if r.get("s"): ajout(r["k"], "source : " + r["s"][0] + " (" + r.get("offer", r.get("name", "")) + ")", r["s"][1])
    for k, p in (d.get("primes") or {}).items():
        if p.get("s"): ajout(k, "parrainage : " + p["s"][0], p["s"][1])
    return noms, par, s

def texte(racine="."):
    noms, par, s = collecter(racine)
    L = [DEB, "## Liens utilisés par le comparateur (généré automatiquement, ne pas modifier à la main)", ""]
    for k in sorted(par, key=lambda x: noms.get(x, x).lower()):
        L.append(f"### {noms.get(k, k)}")
        for u, lib in par[k].items(): L.append(f"- {lib} : {u}")
        L.append("")
    L.append("### Références (tarif réglementé, prix repère du gaz)")
    for cle in ("trv", "gas_ref"):
        for u in s.get("references", {}).get(cle, []): L.append(f"- {cle} : {u}")
    L.append("- gas_trend_template : " + str(s.get("references", {}).get("gas_trend_template", "")))
    od = s.get("open_data", {})
    L.append("- CRE, prix repère du gaz (données ouvertes) : " + od.get("gas_page", ""))
    L.append("- CRE, tarif réglementé électricité (data.gouv.fr, ressource) : https://www.data.gouv.fr/fr/datasets/r/" + od.get("trv_base_rid", ""))
    L.append("- Mint, prix repère gaz : " + str(s.get("mint_prg", "")))
    try:
        c = json.load(open(os.path.join(racine, "eau", "eau-config.json"), encoding="utf-8"))
        L += ["", "### Eau", "- Codes postaux (La Poste, data.gouv.fr) : " + c["laposte"]]
        L += [f"- SISPEA {t} : {u}" for t, u in c["sispea"].items()]
    except Exception: pass
    L += ["", FIN]
    return "\n".join(L)

def ecrire(racine="."):
    p = os.path.join(racine, "LIENS-RECUS.md")
    cur = open(p, encoding="utf-8").read() if os.path.exists(p) else ""
    bloc = texte(racine)
    if DEB in cur and FIN in cur:
        cur = cur[:cur.index(DEB)] + bloc + cur[cur.index(FIN) + len(FIN):]
    else:
        cur = cur.rstrip("\n") + "\n\n" + bloc + "\n"
    open(p, "w", encoding="utf-8").write(cur)

if __name__ == "__main__":
    ecrire(sys.argv[1] if len(sys.argv) > 1 else ".")
