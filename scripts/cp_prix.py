#!/usr/bin/env python3
"""Construit prix-cp.json : prix du gaz par code postal, lus dans les grilles des fournisseurs
(texte extrait du PDF : une ligne par commune « CP COMMUNE abo_B0 kWh_B0 abo_B1 kWh_B1 », TTC).
Un fichier par offre, dans gaz/prix-cp/ ; l'offre de data.json y renvoie par son champ « cpf »."""
import json, re, sys, collections
LIGNE = re.compile(r"^(\d{4,5})\s+(.+?)\s+(\d+,\d\d)\s+(\d,\d{4})\s+(\d+,\d\d)\s+(\d,\d{4})\s*$", re.M)
f = lambda s: float(s.replace(",", "."))

def lire(txt):
    rows = [(m[1].zfill(5), f(m[3]), f(m[4]), f(m[5]), f(m[6])) for m in LIGNE.findall(txt) for m in [(None,) + m]]
    if not rows: raise ValueError("aucune ligne lue")
    if re.search(r"Tarifs HT", txt) and not re.search(r"Tarifs TTC", txt): raise ValueError("grille en HT seulement : les prix TTC sont nécessaires")
    top = max(r[3] for r in rows)          # fichier HT + TTC : on garde le TTC (abonnement le plus élevé)
    return [r for r in rows if r[3] == top]

def table(par_cp):
    """par_cp : {cp: [prix de chaque commune]} -> table compacte (niveaux, codes mixtes, moyennes)."""
    moy = {cp: sum(v) / len(v) for cp, v in par_cp.items()}
    niv, mixte = collections.defaultdict(list), {}
    for cp, v in sorted(par_cp.items()):
        if len(set(v)) == 1: niv["%.4f" % v[0]].append(cp)
        else: mixte[cp] = round(moy[cp], 4)
    dep = collections.defaultdict(list)
    for cp, m in moy.items(): dep[cp[:2]].append(m)
    return {"niv": {k: " ".join(v) for k, v in sorted(niv.items())}, "mixte": mixte,
            "dep": {d: round(sum(v) / len(v), 4) for d, v in sorted(dep.items())},
            "moy": round(sum(moy.values()) / len(moy), 4)}

def slug(t):
    t = re.sub(r"[^a-z0-9]+", "-", t.lower().translate(str.maketrans("éèêëàâîïôöùûüç", "eeeeaaiioouuuc"))).strip("-")
    return t

def construire(k, offre, date, source, txt):
    rows = lire(txt)
    o = {"schema": 1, "type": "prix-par-code-postal", "energie": "gaz", "k": k, "offre": offre, "date": date, "source": source}
    for opt, i in (("b0", 2), ("b1", 4)):
        par = collections.defaultdict(list)
        for r in rows: par[r[0]].append(r[i])
        o[opt] = table(par)
    return o

def main(dossier, k, offre, date, source, fichier_txt):
    """cp_prix.py DOSSIER k "Nom exact de l'offre" jj/mm/aaaa URL grille.txt -> DOSSIER/<k>-<offre>.json"""
    o = construire(k, offre, date, source, open(fichier_txt, encoding="utf-8").read())
    nom = "%s-%s.json" % (k, slug(offre))
    import os; os.makedirs(dossier, exist_ok=True)
    json.dump(o, open(os.path.join(dossier, nom), "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    print(os.path.join(os.path.basename(dossier.rstrip("/")), nom), sum(len(v.split()) for v in o["b1"]["niv"].values()) + len(o["b1"]["mixte"]), "codes postaux")
if __name__ == "__main__": main(*sys.argv[1:])
