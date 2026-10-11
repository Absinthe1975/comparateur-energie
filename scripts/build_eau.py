#!/usr/bin/env python3
"""Construit communes-cp.json : pour chaque code postal, les communes et leur prix de l'eau.

Entrées (dossier passé en argument, par défaut "eau-sources") :
  - 019HexaSmal.csv           Base officielle des codes postaux (La Poste, data.gouv.fr), ISO-8859-1, séparateur ;
  - tarifs_AEP_<année>.csv    Feuille « Zones tarifaires » du fichier tarifs eau potable (SISPEA), exportée en CSV UTF-8
  - tarifs_AC_<année>.csv     idem pour l'assainissement collectif
  - zones_gn.json (optionnel) noms de communes avec accents par code postal (GeoNames)
Sortie : communes-cp.json  {code_postal: "insee~nom~prix~flag|..."}
  prix = eau potable + assainissement collectif, € TTC par m³, pour 120 m³ (indicateur « tarif » du SISPEA)
  flag "e" = assainissement non renseigné, estimé par la médiane du département (communes de 2 000 habitants et plus)
  flag "s" = assainissement non renseigné : prix de l'eau potable seule (petites communes)
Utilisation : python3 scripts/build_eau.py eau-sources communes-cp.json 2025
"""
import csv, json, sys, unicodedata, statistics, collections

def fold(s):
    s = unicodedata.normalize("NFD", s).encode("ascii", "ignore").decode().lower()
    t = s.replace("-", " ").replace("'", " ").replace("’", " ").split()
    return " ".join({"st": "saint", "ste": "sainte"}.get(w, w) for w in t)

def to_f(v):
    try: return float(str(v).replace(",", "."))
    except (TypeError, ValueError): return None

def base_insee(c):  # arrondissements -> commune
    if c.startswith("751") and len(c) == 5: return "75056"
    if c.startswith("6938") and len(c) == 5 and c[4] != "0": return "69123"
    if c.startswith("132") and len(c) == 5 and 13201 <= int(c) <= 13216: return "13055"
    return c

def read_zones(path):
    """INSEE -> (nom, prix moyen) à partir de la feuille « Zones tarifaires »."""
    out = collections.defaultdict(list); names = {}; pops = {}
    with open(path, encoding="utf-8", newline="") as f:
        for r in csv.DictReader(f):
            ins = r["Code INSEE de la commune adhérente"]; names[ins] = r["Nom de la commune adhérente"]
            try: pops[ins] = int(float(r["Population de la commune"]))
            except (TypeError, ValueError): pass
            cands = []
            for i in range(1, 6):
                v = to_f(r.get("Tarif zone tarifaire %d" % i)); lab = r.get("Zone tarifaire %d" % i)
                if v is not None: cands.append((lab, v))
            ind = [v for l, v in cands if l == "Indicateur tarif"]
            v = ind[0] if ind else (cands[0][1] if cands else None)
            if v is not None: out[ins].append(v)
    return names, {k: sum(v) / len(v) for k, v in out.items()}, pops

def main():
    src = sys.argv[1] if len(sys.argv) > 1 else "eau-sources"
    dst = sys.argv[2] if len(sys.argv) > 2 else "communes-cp.json"
    year = sys.argv[3] if len(sys.argv) > 3 else "2025"
    names, ep, pops = read_zones("%s/tarifs_AEP_%s.csv" % (src, year))
    names2, ac, _ = read_zones("%s/tarifs_AC_%s.csv" % (src, year))
    names.update({k: v for k, v in names2.items() if k not in names})
    ep = {k: v for k, v in ep.items() if 0.8 <= v <= 8}   # valeurs aberrantes écartées
    ac = {k: v for k, v in ac.items() if 0.3 <= v <= 8}
    dep_ac = collections.defaultdict(list)
    for k, v in ac.items(): dep_ac[k[:2] if not k.startswith("2") else k[:2]].append(v)
    med = {d: statistics.median(v) for d, v in dep_ac.items() if len(v) >= 3}
    try: gn = json.load(open("%s/zones_gn.json" % src, encoding="utf-8"))
    except OSError: gn = {}
    out = collections.OrderedDict(); n_p = n_e = n_s = 0
    with open("%s/019HexaSmal.csv" % src, encoding="latin-1", newline="") as f:
        for r in csv.reader(f, delimiter=";"):
            if not r or r[0].startswith("#"): continue
            ins0, nom0, cp = r[0], r[1], r[2]
            if cp[:2] in ("97", "98"): continue      # hors métropole
            ins = base_insee(ins0)
            nom = names.get(ins)
            if not nom:
                cands = [g for g in gn.get(cp, "").split("|") if fold(g) == fold(nom0)]
                nom = cands[0] if cands else nom0.title()
            price = ""; flag = ""
            if ins in ep:
                a = ac.get(ins)
                if a is None:
                    # assainissement non renseigné : estimé (médiane du département) pour les communes de 2 000 habitants et plus,
                    # sinon eau potable seule (petites communes souvent en assainissement individuel)
                    if pops.get(ins, 0) >= 2000 and ins[:2] in med: a = med[ins[:2]]; flag = "e"
                    else: a = 0.0; flag = "s"
                price = "%.2f" % (ep[ins] + a); n_p += 1; n_e += flag == "e"; n_s += flag == "s"
            ent = "~".join([ins, nom.replace("~", " ").replace("|", " "), price, flag]).rstrip("~")
            lst = out.setdefault(cp, [])
            if ent not in lst and not any(e.startswith(ins + "~") for e in lst): lst.append(ent)
    js = {cp: "|".join(v) for cp, v in sorted(out.items())}
    open(dst, "w", encoding="utf-8").write(json.dumps(js, ensure_ascii=False, separators=(",", ":")))
    print("codes postaux :", len(js), "· communes avec prix :", n_p, "(dont assainissement estimé :", n_e, ", eau potable seule :", n_s, ")")

if __name__ == "__main__":
    main()
