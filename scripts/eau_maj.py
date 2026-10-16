#!/usr/bin/env python3
"""Met à jour communes-cp.json (prix de l'eau par code postal) de façon automatique.

1. Télécharge la base La Poste des codes postaux (data.gouv.fr) et les fichiers « tarifs » du SISPEA
   de la dernière année disponible (liste dans eau-config.json).
2. Convertit les feuilles Excel en CSV, lance build_eau.py.
3. Garde-fous : refuse le résultat s'il perd trop de codes postaux ou si les prix bougent trop.
   Si l'année la plus récente est vide (en-têtes seuls), on garde l'année précédente.
Utilisation : python3 scripts/eau_maj.py [eau-config.json] [communes-cp.json]
Code de sortie 0 = rien à signaler ou fichier mis à jour ; 1 = échec (le fichier existant est conservé).
"""
import csv, json, os, subprocess, sys, tempfile, urllib.request

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UA = {"User-Agent": "comparateur-energie (association loi 1901; contact via GitHub Absinthe1975)"}

def telecharger(url, dest, ouvrir=urllib.request.urlopen):
    req = urllib.request.Request(url, headers=UA)
    with ouvrir(req, timeout=120) as r, open(dest, "wb") as f:
        f.write(r.read())

def xls_vers_csv(src, feuille, dest):
    """Exporte une feuille d'un classeur .xls/.xlsx en CSV UTF-8 ; renvoie le nombre de lignes de données."""
    import pandas as pd
    df = pd.read_excel(src, sheet_name=feuille, dtype=str)
    df.to_csv(dest, index=False, encoding="utf-8", sep=";")
    return len(df)

def prix_valides(com):
    """{cp: [(insee, prix)]} depuis communes-cp.json (dict déjà chargé)."""
    out = {}
    for cp, s in com.items():
        for item in s.split("|"):
            p = item.split("~")
            try: out.setdefault(cp, []).append((p[0], float(p[2])))
            except (IndexError, ValueError): pass
    return out

def comparer(ancien, nouveau, max_perte=0.03, max_ecart=0.25):
    """Liste de problèmes (vide = acceptable) entre l'ancien et le nouveau contenu."""
    pb = []
    if not nouveau: return ["fichier vide"]
    if ancien:
        if len(nouveau) < len(ancien) * (1 - max_perte):
            pb.append("codes postaux : %d au lieu de %d" % (len(nouveau), len(ancien)))
        a, n = prix_valides(ancien), prix_valides(nouveau)
        def moy(d):
            v = [p for l in d.values() for _, p in l]
            return sum(v) / len(v) if v else 0
        ma, mn = moy(a), moy(n)
        if ma and abs(mn - ma) / ma > 0.10:
            pb.append("prix moyen %.2f → %.2f €/m³ (écart > 10 %%)" % (ma, mn))
        commun = [(cp, a[cp][0][1], n[cp][0][1]) for cp in a if cp in n]
        bouge = [c for c in commun if c[1] and abs(c[2] - c[1]) / c[1] > max_ecart]
        if commun and len(bouge) / len(commun) > 0.15:
            pb.append("%d codes postaux sur %d changent de plus de %d %%" % (len(bouge), len(commun), int(max_ecart * 100)))
    return pb

def suspects(com, seuil=2.0):
    """Communes dont le prix eau potable + assainissement (complet, non estimé) est sous le seuil : à vérifier à la main."""
    out = {}
    for cp, s in com.items():
        for item in s.split("|"):
            p = item.split("~")
            try:
                if len(p) > 3 and p[3] == "" and float(p[2]) < seuil: out[p[0]] = (p[1], float(p[2]))
            except (IndexError, ValueError): pass
    return out

def annee_disponible(cfg, dossier, telecharger=telecharger, convertir=xls_vers_csv):
    """Essaie les années de la plus récente à la plus ancienne ; renvoie l'année dont les 4 feuilles ont des données."""
    for an in sorted(cfg["annees"], reverse=True):
        ok = True
        for code, nom in (("AEP", "tarifs_AEP"), ("AC", "tarifs_AC")):
            url = cfg["sispea"][code].replace("{an}", str(an))
            tmp = os.path.join(dossier, "%s_%s.xls" % (nom, an))
            try:
                telecharger(url, tmp)
                n = convertir(tmp, "Zones tarifaires", os.path.join(dossier, "%s_%s.csv" % (nom, an)))
                d = convertir(tmp, "Détail tarifaire", os.path.join(dossier, "detail_%s_%s.csv" % (code, an)))
            except Exception as e:
                print("année %s %s : %s" % (an, code, e)); ok = False; break
            if n < 100 or d < 100:
                print("année %s %s : fichier vide (%d / %d lignes)" % (an, code, n, d)); ok = False; break
        if ok: return str(an)
    return None

def main():
    cfg_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(RACINE, "eau-config.json")
    dst = sys.argv[2] if len(sys.argv) > 2 else os.path.join(RACINE, "communes-cp.json")
    cfg = json.load(open(cfg_path, encoding="utf-8"))
    if any("A_COMPLETER" in u for u in cfg["sispea"].values()):
        print("eau-config.json : adresses des fichiers SISPEA à renseigner."); return 1
    ancien = json.load(open(dst, encoding="utf-8")) if os.path.exists(dst) else {}
    with tempfile.TemporaryDirectory() as dossier:
        telecharger(cfg["laposte"], os.path.join(dossier, "019HexaSmal.csv"))
        an = annee_disponible(cfg, dossier)
        if not an:
            print("Aucune année SISPEA exploitable : communes-cp.json conservé."); return 0
        # noms avec accents : repris du fichier actuel (la base La Poste est en majuscules sans accents)
        gn = {cp: "|".join(i.split("~")[1] if "~" in i else i for i in v.split("|")) for cp, v in ancien.items()}
        json.dump(gn, open(os.path.join(dossier, "zones_gn.json"), "w", encoding="utf-8"), ensure_ascii=False)
        sortie = os.path.join(dossier, "communes-cp.json")
        subprocess.run([sys.executable, os.path.join(RACINE, "scripts", "build_eau.py"), dossier, sortie, an], check=True)
        nouveau = json.load(open(sortie, encoding="utf-8"))
        pb = comparer(ancien, nouveau)
        if pb:
            print("Résultat refusé :", "; ".join(pb)); return 1
        for ins, (nom, pr) in sorted(suspects(nouveau).items()):
            print("À vérifier : %s (%s) à %.2f €/m³ eau + assainissement, très bas" % (nom, ins, pr))
        if nouveau == ancien:
            print("Prix de l'eau %s : aucun changement." % an); return 0
        with open(dst, "w", encoding="utf-8") as f:
            json.dump(nouveau, f, ensure_ascii=False, separators=(",", ":"))
        print("Prix de l'eau mis à jour (SISPEA %s) : %d codes postaux." % (an, len(nouveau)))
    return 0

if __name__ == "__main__":
    sys.exit(main())
