#!/usr/bin/env python3
"""Construit communes-cp.json : pour chaque code postal, les communes et leur prix de l'eau.

Entrées (dossier passé en argument, par défaut "eau-sources") :
  - 019HexaSmal.csv           Base officielle des codes postaux (La Poste, data.gouv.fr), ISO-8859-1, séparateur ;
  - tarifs_AEP_<année>.csv    Feuille « Zones tarifaires » du fichier tarifs eau potable (SISPEA), exportée en CSV UTF-8
  - tarifs_AC_<année>.csv     idem pour l'assainissement collectif
  - detail_AEP_<année>.csv, detail_AC_<année>.csv   feuille « Détail tarifaire » des mêmes fichiers (part fixe = abonnement :
                              variables VP.190 délégataire + VP.191 collectivité, en € HT par an, TVA = VP.213)
  - zones_gn.json (optionnel) noms de communes avec accents par code postal (GeoNames)
Sortie : communes-cp.json  {code_postal: "insee~nom~prix~flag~abonnement~eau_potable~assainissement|..."}
  abonnement = part fixe annuelle TTC eau potable + assainissement (€ par an), vide si inconnu
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
    out = collections.defaultdict(list); names = {}; pops = {}; svc = collections.defaultdict(list)
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
            if v is not None:
                out[ins].append(v)
                svc[ins].append((v, "".join(ch for ch in r.get("Identifiant SISPEA de l'entité de gestion à laquelle la commune adhère", "") if ch.isdigit())))
    return names, {k: sum(v) / len(v) for k, v in out.items()}, pops, svc

def read_abo(path, tva_def):
    """Identifiant du service -> part fixe annuelle TTC (€), valeurs hors 0-400 € écartées."""
    out = {}
    try: f = open(path, encoding="utf-8", newline="")
    except OSError: return out
    with f:
        for r in csv.DictReader(f):
            a, b = to_f(r.get("VP.190")), to_f(r.get("VP.191"))
            if a is None and b is None: continue
            tva = to_f(r.get("VP.213"))
            if not tva: tva = tva_def           # TVA absente ou 0 : taux courant
            ttc = ((a or 0) + (b or 0)) * (1 + tva / 100)
            sid = "".join(ch for ch in r.get("Id SISPEA de l'entité de gestion", "") if ch.isdigit())
            if sid and 0 < ttc <= 400: out[sid] = ttc
    return out

def commune_abo(svc, abos, price):
    """Abonnement du service dont le prix est le plus proche du prix de la commune."""
    best = None
    for v, sid in svc:
        if sid in abos and (best is None or abs(v - price) < best[0]): best = (abs(v - price), abos[sid])
    return best[1] if best else None

def main():
    src = sys.argv[1] if len(sys.argv) > 1 else "eau-sources"
    dst = sys.argv[2] if len(sys.argv) > 2 else "communes-cp.json"
    year = sys.argv[3] if len(sys.argv) > 3 else "2025"
    names, ep, pops, svc_ep = read_zones("%s/tarifs_AEP_%s.csv" % (src, year))
    names2, ac, _, svc_ac = read_zones("%s/tarifs_AC_%s.csv" % (src, year))
    abo_ep = read_abo("%s/detail_AEP_%s.csv" % (src, year), 5.5)
    abo_ac = read_abo("%s/detail_AC_%s.csv" % (src, year), 10.0)
    names.update({k: v for k, v in names2.items() if k not in names})
    ep = {k: v for k, v in ep.items() if 0.8 <= v <= 8}   # valeurs aberrantes écartées
    ac = {k: v for k, v in ac.items() if 0.3 <= v <= 8}
    dep_ac = collections.defaultdict(list)
    for k, v in ac.items(): dep_ac[k[:2] if not k.startswith("2") else k[:2]].append(v)
    med = {d: statistics.median(v) for d, v in dep_ac.items() if len(v) >= 3}
    ca = {}  # abonnement assainissement par commune
    for k in ac:
        v = commune_abo(svc_ac.get(k, []), abo_ac, ac[k])
        if v: ca[k] = v
    dep_abo = collections.defaultdict(list)
    for k, v in ca.items(): dep_abo[k[:2]].append(v)
    med_abo = {d: statistics.median(v) for d, v in dep_abo.items() if len(v) >= 3}
    all_abo = statistics.median(ca.values()) if ca else 0
    try: gn = json.load(open("%s/zones_gn.json" % src, encoding="utf-8"))
    except OSError: gn = {}
    out = collections.OrderedDict(); n_p = n_e = n_s = n_a = 0
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
            price = ""; flag = ""; abo = ""; pe = ""; pa = ""
            if ins in ep:
                a = ac.get(ins)
                if a is None:
                    # assainissement non renseigné : estimé (médiane du département) pour les communes de 2 000 habitants et plus,
                    # sinon eau potable seule (petites communes souvent en assainissement individuel)
                    if pops.get(ins, 0) >= 2000 and ins[:2] in med: a = med[ins[:2]]; flag = "e"
                    else: a = 0.0; flag = "s"
                pe = "%.2f" % ep[ins]; pa = "" if flag == "s" else "%.2f" % a
                price = "%.2f" % (ep[ins] + a); n_p += 1; n_e += flag == "e"; n_s += flag == "s"
                ae = commune_abo(svc_ep.get(ins, []), abo_ep, ep[ins])
                if ae is not None:
                    aa = ca.get(ins) if flag == "" else (med_abo.get(ins[:2], all_abo) if flag == "e" else 0)
                    if aa is not None and 10 <= ae + aa < 0.6 * 120 * (ep[ins] + a): abo = "%.0f" % (ae + aa); n_a += 1
            ent = "~".join([ins, nom.replace("~", " ").replace("|", " "), price, flag, abo, pe, pa]).rstrip("~")
            lst = out.setdefault(cp, [])
            if ent not in lst and not any(e.startswith(ins + "~") for e in lst): lst.append(ent)
    js = {cp: "|".join(v) for cp, v in sorted(out.items())}
    open(dst, "w", encoding="utf-8").write(json.dumps(js, ensure_ascii=False, separators=(",", ":")))
    print("codes postaux :", len(js), "· communes avec prix :", n_p, "(dont assainissement estimé :", n_e, ", eau potable seule :", n_s, ") · avec abonnement :", n_a)

if __name__ == "__main__":
    main()
