#!/usr/bin/env python3
"""Réduit les pages de communes téléchargées à un petit fichier CSV (quelques Mo au lieu de plusieurs centaines).

À lancer sur VOTRE ordinateur, dans le dossier qui contient zones_gaz_pages :
    python3 reduire_communes.py
Résultat : zones_gaz_communes.csv (une ligne par commune), à envoyer à Claude.
Aucune connexion internet : le programme lit seulement les fichiers déjà téléchargés.
"""
import html
import os
import re
import sys

DOSSIER = sys.argv[1] if len(sys.argv) > 1 else os.path.join("zones_gaz_pages", "communes")
COLS = ["grdf", "ilek", "total", "engie6", "alterna", "engie8", "geg", "ntr"]
NOMS = {"grille par defaut (grdf/engie)": "grdf", "ilek": "ilek", "totalenergies": "total", "engie": "engie6",
        "alterna": "alterna", "engie 8 zones": "engie8", "geg fixe": "geg", "ntr": "ntr"}


def sans_accents(s):
    import unicodedata
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()


def lire(chemin):
    t = open(chemin, encoding="utf-8", errors="replace").read()
    zones = {}
    for four, zone in re.findall(r'<td data-label="Fournisseur"[^>]*>(.*?)</td>\s*<td data-label="Zone tarifaire"[^>]*>(.*?)</td>', t, re.S):
        nom = " ".join(sans_accents(html.unescape(re.sub(r"<[^>]+>", " ", four))).split())
        z = " ".join(re.sub(r"<[^>]+>", " ", html.unescape(zone)).replace("\xa0", " ").split())
        z = re.sub(r"^Zone\s+", "", z)
        if nom in NOMS and z:
            zones[NOMS[nom]] = z
    return zones


def main():
    if not os.path.isdir(DOSSIER):
        print("Dossier introuvable : %s (lancez ce programme à côté de zones_gaz_pages)." % DOSSIER)
        return 2
    n = vides = 0
    with open("zones_gaz_communes.csv", "w", encoding="utf-8", newline="") as out:
        out.write(";".join(["dep", "commune"] + COLS) + "\n")
        for f in sorted(os.listdir(DOSSIER)):
            m = re.fullmatch(r"zone-gaz__([a-z0-9-]+)__([a-z0-9-]+)\.html", f)
            if not m:
                continue
            z = lire(os.path.join(DOSSIER, f))
            if not z:
                vides += 1
                continue
            out.write(";".join([m.group(1), m.group(2)] + [z.get(c, "") for c in COLS]) + "\n")
            n += 1
    print("%d communes écrites, %d pages sans tableau. Envoyez zones_gaz_communes.csv à Claude." % (n, vides))
    print("Taille : %.1f Mo" % (os.path.getsize("zones_gaz_communes.csv") / 1e6))
    return 0


if __name__ == "__main__":
    sys.exit(main())
