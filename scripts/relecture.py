#!/usr/bin/env python3
"""Relecture automatique d'une PR : compare les données avant / après et signale ce qui mérite un coup d'œil.

Usage : python3 scripts/relecture.py BASE HEAD [rapport.md]
BASE et HEAD sont des références git. Le script lit les fichiers avec « git show » (il n'exécute jamais le code de la PR).
Code de sortie : 0 = rien à signaler, 1 = à relire (la fusion automatique ne doit pas avoir lieu).
"""
import json
import subprocess
import sys

FICHIERS = ["donnees/data.json", "donnees/elec/data.json", "donnees/gaz/data.json",
            "donnees/manuel/tarifs_manuels.json"]
PRIX = ["a", "b", "b0", "hp", "hc", "hpb", "hcb"]
SEUIL_PRIX = 0.15     # variation de prix jugée suspecte
SEUIL_ABO = 0.25      # variation d'abonnement jugée suspecte
SEUIL_PRIME = 0.5


def lire(ref, chemin):
    try:
        r = subprocess.run(["git", "show", "%s:%s" % (ref, chemin)], capture_output=True, text=True, check=True)
        return json.loads(r.stdout)
    except Exception:
        return None


def offres(d, chemin, chemin_liste=""):
    """Rend {(liste, k, offre): objet} pour toutes les listes d'offres d'un fichier."""
    out = {}
    if not isinstance(d, dict):
        return out
    for nom, v in d.items():
        if isinstance(v, list):
            for o in v:
                if isinstance(o, dict) and "k" in o and "offer" in o:
                    out[(chemin + ":" + nom, o["k"], o["offer"])] = o
    return out


def variation(x, y):
    if not isinstance(x, (int, float)) or not isinstance(y, (int, float)) or not x:
        return None
    return (y - x) / x


def comparer(base, tete):
    notes = []
    for f in FICHIERS:
        b, t = lire(base, f), lire(tete, f)
        if t is None:
            if b is not None:
                notes.append("Fichier supprimé ou illisible : %s" % f)
            continue
        ob, ot = offres(b, f), offres(t, f)
        for cle, o in ot.items():
            nom = "%s – %s" % (cle[1], cle[2])
            av = ob.get(cle)
            if av == o:
                continue
            if o.get("niv") == "officiel" and not (o.get("s") and len(o["s"]) > 1 and str(o["s"][1]).startswith("http")):
                notes.append("%s : marquée officielle sans lien de source." % nom)
            if o.get("niv") == "officiel" and not o.get("nivd"):
                notes.append("%s : marquée officielle sans date de grille." % nom)
            if not av:
                continue
            for c in PRIX:
                v = variation(av.get(c), o.get(c))
                if v is not None and abs(v) > SEUIL_PRIX:
                    notes.append("%s : prix « %s » %+.0f %% (%s → %s)." % (nom, c, v * 100, av.get(c), o.get(c)))
            for c in ("ab6", "ab9"):
                v = variation(av.get(c), o.get(c))
                if v is not None and abs(v) > SEUIL_ABO:
                    notes.append("%s : abonnement « %s » %+.0f %% (%s → %s)." % (nom, c, v * 100, av.get(c), o.get(c)))
            if av.get("niv") == "officiel" and o.get("niv") != "officiel":
                notes.append("%s : repasse de officiel à %s." % (nom, o.get("niv")))
        for cle in ob:
            if cle not in ot:
                notes.append("Offre retirée : %s – %s (%s)." % (cle[1], cle[2], cle[0].split(":")[1]))
    # primes
    b, t = lire(base, "donnees/data.json") or {}, lire(tete, "donnees/data.json") or {}
    pb, pt = b.get("primes"), t.get("primes")
    if isinstance(pb, dict) and isinstance(pt, dict):
        for k, p in pt.items():
            a = pb.get(k)
            if not isinstance(a, dict) or not isinstance(p, dict):
                continue
            for c in ("p", "f"):
                v = variation(a.get(c), p.get(c))
                if v is not None and abs(v) > SEUIL_PRIME:
                    notes.append("Prime %s « %s » %+.0f %% (%s → %s)." % (k, c, v * 100, a.get(c), p.get(c)))
            if a.get("st") == "ok" and p.get("st") != "ok":
                notes.append("Prime %s : n'est plus confirmée (%s)." % (k, p.get("st")))
    return notes


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        return 2
    notes = comparer(sys.argv[1], sys.argv[2])
    if notes:
        txt = "### 🔎 Relecture automatique : à regarder avant de fusionner\n\n" + "\n".join("- " + n for n in notes)
        txt += "\n\nLa fusion automatique est suspendue (étiquette `ne-pas-fusionner`). Si tout est normal, retire l'étiquette puis fusionne."
    else:
        txt = "### 🔎 Relecture automatique : rien à signaler\n\nAucune variation de prix anormale, aucune source manquante."
    if len(sys.argv) > 3:
        open(sys.argv[3], "w", encoding="utf-8").write(txt + "\n")
    print(txt)
    return 1 if notes else 0


if __name__ == "__main__":
    sys.exit(main())
