#!/usr/bin/env python3
"""Classement des 3 communes où l'eau est la moins chère, par région : donnees/eau/classement.json.

Lit les fichiers par département (donnees/eau/cp/NN.json). Ne retient que les communes dont le prix est complet (eau potable ET assainissement relevés,
champ « drapeau » vide), au prix plausible (au moins 2 €/m³ : en dessous, la donnée est suspecte et n'est pas classée). Une commune n'est comptée qu'une fois
même si elle a plusieurs codes postaux. Le rattachement département → région est lu dans index.html (une seule source dans le dépôt)."""
import datetime, json, os, re, sys
DEPOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SEUIL = 2.0

def regions_depuis_html(html):
    m = re.search(r'var DEPT_RAW = (.*?);\s*\nvar CITY_RAW', html, re.S)
    brut = "".join(re.findall(r'"([^"]*)"', m.group(1)))
    return {c: r for c, _, r in (x.split("|") for x in brut.split(";") if x)}

def classement(dossier_cp, region_de, n=3, seuil=SEUIL):
    """-> {région: [[insee, nom, prix, code postal], …]} : les n moins chères, prix croissants."""
    vus, par = {}, {}
    for nom in sorted(os.listdir(dossier_cp)):
        if not nom.endswith(".json"): continue
        for cp, s in json.load(open(os.path.join(dossier_cp, nom), encoding="utf-8")).items():
            for item in s.split("|"):
                p = item.split("~")
                try: ins, ville, prix, drap = p[0], p[1], float(p[2]), p[3]
                except (IndexError, ValueError): continue
                if drap != "" or prix < seuil or ins in vus: continue
                reg = region_de.get(ins[:2])
                if not reg: continue
                vus[ins] = 1; par.setdefault(reg, []).append([ins, ville, round(prix, 2), cp])
    return {r: sorted(v, key=lambda x: (x[2], x[1]))[:n] for r, v in sorted(par.items())}

def main(depot=DEPOT, today=None):
    html = open(os.path.join(depot, "index.html"), encoding="utf-8").read()
    out = {"mis_a_jour": (today or datetime.date.today()).isoformat(), "seuil": SEUIL,
           "regions": classement(os.path.join(depot, "donnees", "eau", "cp"), regions_depuis_html(html))}
    chemin = os.path.join(depot, "donnees", "eau", "classement.json")
    ancien = json.load(open(chemin, encoding="utf-8")) if os.path.exists(chemin) else {}
    if ancien.get("regions") == out["regions"]: print("Classement de l'eau : aucun changement."); return 0
    with open(chemin, "w", encoding="utf-8") as fh: json.dump(out, fh, ensure_ascii=False, indent=1); fh.write("\n")
    print("Classement de l'eau écrit : %d régions." % len(out["regions"])); return 0

if __name__ == "__main__": sys.exit(main())
