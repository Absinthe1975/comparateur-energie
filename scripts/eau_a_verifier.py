#!/usr/bin/env python3
"""Liste des communes à prix très bas (moins de 2 €/m³, prix complet) à vérifier à la main : docs/EAU-A-VERIFIER.md.
Ne modifie aucune donnée ; lancé à la demande."""
import glob, json, os
RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SEUIL = 2.0

def communes_basses(dossier_cp, seuil=SEUIL):
    vus, out = set(), []
    for f in sorted(glob.glob(os.path.join(dossier_cp, "*.json"))):
        with open(f, encoding="utf-8") as fh: d = json.load(fh)
        for cp, chaine in d.items():
            for c in chaine.split("|"):
                p = c.split("~")
                if len(p) < 7 or p[3] != "" or p[0] in vus: continue
                try: prix = float(p[2])
                except ValueError: continue
                if prix < seuil: vus.add(p[0]); out.append((p[1], cp, p[0], prix))
    return sorted(out, key=lambda x: x[3])

def main():
    L = communes_basses(os.path.join(RACINE, "donnees", "eau", "cp"))
    h = ["# Communes à prix d'eau très bas, à vérifier", "",
         "Prix complet (eau potable + assainissement) sous %.0f €/m³ : souvent un prix incomplet (assainissement absent) ou une erreur de saisie. Pour chaque commune : ouvrir la recherche SISPEA, chercher la commune, comparer avec le prix ci-dessous, puis noter « confirmé » ou « erreur » (et la bonne valeur)." % SEUIL, "",
         "Recherche : https://www.services.eaufrance.fr/donnees/recherche", "",
         "| Commune | Code postal | INSEE | Prix par m³ | Résultat |", "|---|---|---|---|---|"]
    for nom, cp, insee, prix in L: h.append("| %s | %s | %s | %.2f € |  |" % (nom, cp, insee, prix))
    with open(os.path.join(RACINE, "docs", "EAU-A-VERIFIER.md"), "w", encoding="utf-8") as fh: fh.write("\n".join(h) + "\n")
    print(len(L), "communes")
if __name__ == "__main__": main()
