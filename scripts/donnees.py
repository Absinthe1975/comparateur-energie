#!/usr/bin/env python3
"""Lecture et écriture des données des offres, réparties sur trois fichiers :
  donnees/elec/data.json : offres d'électricité, tarif réglementé, abonnements
  donnees/gaz/data.json  : offres de gaz, prix repère, abonnements
  donnees/data.json      : ce qui est commun (dates, primes, liens, offres combinées)
En mémoire, le programme travaille toujours sur un seul dictionnaire ; cette rubrique les sépare ou les réunit."""
import json, os

ELEC = ("elec_ref", "elec", "hphc", "abo_e", "abo_d", "trv_abo")
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

MANUELS = os.path.join("manuel", "tarifs_manuels.json")
LISTES = ("elec", "gas", "duo", "hphc")        # offres : repérées par (k, offer)
TABLES = ("abo_e", "abo_g", "abo_g0")  # abonnements par fournisseur : repérés par k

def fusionner_manuels(d, manuels):
    """Ajoute à d (sans le modifier) les grilles saisies à la main : une offre déjà présente (même k et même offer)
    est complétée champ par champ par la version manuelle, sinon elle est ajoutée. Les clés qui commencent par « _ » sont des notes."""
    out = json.loads(json.dumps(d))
    for cle in LISTES:
        if not manuels.get(cle): continue
        rows = out.setdefault(cle, [])
        for m in manuels.get(cle, []):
            cible = next((r for r in rows if r.get("k") == m.get("k") and r.get("offer") == m.get("offer")), None)
            if cible is None: rows.append(dict(m))
            else: cible.update(m)
    for cle in TABLES:
        out.setdefault(cle, {}).update({k: v for k, v in manuels.get(cle, {}).items() if not k.startswith("_")})
    return out

def charger_complet(racine):
    """Données automatiques + grilles manuelles (donnees/manuel/tarifs_manuels.json, absent = rien à ajouter). Lecture seule : ne pas réenregistrer."""
    d = charger(racine)
    chemin = os.path.join(racine, MANUELS)
    return fusionner_manuels(d, _lire(chemin)) if os.path.exists(chemin) else d

def _ecrire(chemin, obj):
    with open(chemin, "w", encoding="utf-8") as fh: json.dump(obj, fh, ensure_ascii=False, indent=1); fh.write("\n")
