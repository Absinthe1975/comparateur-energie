#!/usr/bin/env python3
"""Publie sur la Page Facebook un brouillon de docs/FACEBOOK-BROUILLONS.md (titre « ## ... »).

Usage : python3 scripts/facebook_manuel.py "Parrainage EDF" [--publier]
Sans --publier : aperçu seulement (rien n'est envoyé). Utilise FB_PAGE_ID et FB_PAGE_TOKEN comme scripts/facebook.py.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import facebook

FICHIER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "docs", "FACEBOOK-BROUILLONS.md")


def brouillons(texte):
    """{titre: texte} d'après les sections « ## titre »."""
    out = {}
    for m in re.finditer(r"^## ([^\n]+)\n(.*?)(?=^## |\Z)", texte, re.S | re.M):
        out[m.group(1).strip()] = m.group(2).strip()
    return out


def main(argv):
    args = [a for a in argv[1:] if not a.startswith("--")]
    if len(args) != 1:
        print(__doc__)
        return 2
    b = brouillons(open(FICHIER, encoding="utf-8").read())
    if args[0] not in b:
        print("Brouillon introuvable : %s. Disponibles : %s" % (args[0], ", ".join(b)))
        return 2
    print("---\n" + b[args[0]] + "\n---")
    if "--publier" not in argv:
        print("Aperçu seulement : rien n'a été publié.")
        print("::notice title=Facebook::Aperçu seulement, rien n'a été publié.")
        return 0
    return 0 if facebook.publier(b[args[0]]) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
