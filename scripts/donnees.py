#!/usr/bin/env python3
"""Lecture et écriture des données des offres, réparties sur trois fichiers :
  elec/data.json : offres d'électricité, tarif réglementé, abonnements
  gaz/data.json  : offres de gaz, prix repère, abonnements
  data.json      : ce qui est commun (dates, primes, liens, offres combinées)
En mémoire, le programme travaille toujours sur un seul dictionnaire ; cette rubrique les sépare ou les réunit."""
import json, os

ELEC = ("elec_ref", "elec", "abo_e", "abo_d", "trv_abo")
GAZ = ("gas_ref", "gas", "abo_g", "abo_g0", "gas_b0", "gas_b1")
FICHIERS = {"elec": ELEC, "gaz": GAZ}

def _lire(chemin):
    with open(chemin, encoding="utf-8") as fh: return json.load(fh)

def charger(racine):
    d = _lire(os.path.join(racine, "data.json"))
    for dossier in FICHIERS:
        chemin = os.path.join(racine, dossier, "data.json")
        if os.path.exists(chemin): d.update(_lire(chemin))
    return d

def enregistrer(racine, d):
    pris = set()
    for dossier, cles in FICHIERS.items():
        part = {k: d[k] for k in cles if k in d}; pris |= set(part)
        os.makedirs(os.path.join(racine, dossier), exist_ok=True)
        _ecrire(os.path.join(racine, dossier, "data.json"), part)
    _ecrire(os.path.join(racine, "data.json"), {k: v for k, v in d.items() if k not in pris})

def _ecrire(chemin, obj):
    with open(chemin, "w", encoding="utf-8") as fh: json.dump(obj, fh, ensure_ascii=False, indent=1); fh.write("\n")
