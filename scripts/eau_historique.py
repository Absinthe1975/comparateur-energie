#!/usr/bin/env python3
"""Historique du prix de l'eau par commune, année par année, à partir des fichiers « tarifs » du SISPEA.

Écrit, dans eau/historique/ :
  NN.json         {code INSEE: [[année, eau potable €/m³, assainissement €/m³ ou null], …]}, un fichier par département
  national.json   {année: {"ep": médiane eau potable, "ac": médiane assainissement, "n": communes}}
  annees.json     années déjà traitées
Seules les années manquantes et les deux plus récentes (les valeurs sont parfois corrigées) sont téléchargées.
Une année dont le fichier est absent, vide ou de format différent est ignorée et signalée : aucune valeur n'est devinée.
Utilisation : python3 scripts/eau_historique.py"""
import datetime, json, os, statistics, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import eau_maj as em, build_eau as be

DEPOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # racine du dépôt
RACINE = os.path.join(DEPOT, "donnees")      # dossier des données
PREMIERE = 2009


def prix_annee(csv_aep, csv_ac):
    """({insee: eau potable}, {insee: assainissement}) pour une année, valeurs aberrantes écartées (mêmes bornes que build_eau)."""
    _, ep, _, _ = be.read_zones(csv_aep)
    _, ac, _, _ = be.read_zones(csv_ac)
    return {k: v for k, v in ep.items() if 0.8 <= v <= 8}, {k: v for k, v in ac.items() if 0.3 <= v <= 8}


def lire(dossier):
    """{insee: {année: (ep, ac)}} relu depuis les fichiers par département."""
    d = {}
    if os.path.isdir(dossier):
        for nom in os.listdir(dossier):
            if nom.endswith(".json") and nom not in ("national.json", "annees.json"):
                for ins, pts in json.load(open(os.path.join(dossier, nom), encoding="utf-8")).items():
                    d[ins] = {int(a): (e, c) for a, e, c in pts}
    return d


def ecrire(dossier, d, national, annees, jour):
    os.makedirs(dossier, exist_ok=True)
    parts = {}
    for ins, ys in d.items(): parts.setdefault(ins[:2], {})[ins] = [[a, round(e, 2), None if c is None else round(c, 2)] for a, (e, c) in sorted(ys.items())]
    for nom in os.listdir(dossier):
        if nom.endswith(".json") and nom not in ("national.json", "annees.json") and nom[:-5] not in parts: os.remove(os.path.join(dossier, nom))
    for p, part in parts.items():
        with open(os.path.join(dossier, p + ".json"), "w", encoding="utf-8") as f: json.dump(dict(sorted(part.items())), f, separators=(",", ":"))
    for nom, obj in (("national.json", national), ("annees.json", {"annees": sorted(annees), "mis_a_jour": jour})):
        with open(os.path.join(dossier, nom), "w", encoding="utf-8") as f: json.dump(obj, f, ensure_ascii=False, separators=(",", ":"))


def main(racine=RACINE, telecharger=em.telecharger, convertir=em.xls_vers_csv, today=None):
    today = today or datetime.date.today()
    cfg = json.load(open(os.path.join(racine, "eau", "eau-config.json"), encoding="utf-8"))
    dossier = os.path.join(racine, "eau", "historique")
    d = lire(dossier)
    try: faites = set(json.load(open(os.path.join(dossier, "annees.json"), encoding="utf-8"))["annees"])
    except (OSError, KeyError, ValueError): faites = set()
    try: national = json.load(open(os.path.join(dossier, "national.json"), encoding="utf-8"))
    except (OSError, ValueError): national = {}
    toutes = list(range(PREMIERE, today.year + 1))
    a_faire = [a for a in toutes if a not in faites or a >= today.year - 1]
    nouvelles, ignorees = [], []
    with tempfile.TemporaryDirectory() as tmp:
        for an in sorted(a_faire):
            try:
                fic = {}
                for code in ("AEP", "AC"):
                    x = os.path.join(tmp, "%s_%s.xls" % (code, an)); em.premier_qui_marche(cfg["sispea"][code], an, x, telecharger)
                    c = os.path.join(tmp, "%s_%s.csv" % (code, an)); n = convertir(x, "Zones tarifaires", c)
                    if n < 100: raise ValueError("fichier vide (%d lignes)" % n)
                    fic[code] = c
                ep, ac = prix_annee(fic["AEP"], fic["AC"])
                if len(ep) < 3000: raise ValueError("%d communes avec un prix seulement" % len(ep))
                med = statistics.median(ep.values())
                if not (1.0 <= med <= 4.0): raise ValueError("prix médian incohérent (%.2f €/m³)" % med)
            except Exception as e:
                ignorees.append(an); print("année %s ignorée : %s" % (an, str(e)[:150])); continue
            for ins in d: d[ins].pop(an, None)
            for ins, v in ep.items(): d.setdefault(ins, {})[an] = (v, ac.get(ins))
            national[str(an)] = {"ep": round(med, 2), "ac": round(statistics.median(ac.values()), 2) if ac else None, "n": len(ep)}
            faites.add(an); nouvelles.append(an); print("année %s : %d communes, médiane %.2f €/m³ (eau potable)" % (an, len(ep), med))
    d = {k: v for k, v in d.items() if v}
    if not nouvelles: print("Historique de l'eau : rien de nouveau."); return 0 if faites else 1
    ecrire(dossier, d, dict(sorted(national.items())), faites, today.isoformat())
    print("Historique de l'eau : %d années (%s à %s), %d communes." % (len(faites), min(faites), max(faites), len(d)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
