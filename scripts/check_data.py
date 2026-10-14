#!/usr/bin/env python3
"""Vérifie que data.json est complet et plausible. Code de sortie 1 si une erreur est trouvée."""
import json, os, sys
d = json.load(open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data.json"), encoding="utf-8"))
err = []
def need(c, m):
    if not c: err.append(m)
need(d.get("schema") == 1, "schema doit valoir 1")
need(isinstance(d.get("updated"), str) and len(d["updated"]) == 10, "updated doit être une date AAAA-MM-JJ")
need("updated_time" not in d or (isinstance(d["updated_time"], str) and len(d["updated_time"]) == 5 and d["updated_time"][2] == ":"), "updated_time doit être HH:MM")
for r in d["elec"]:
    need(0.10 <= r["a"] <= 0.45 and 0.10 <= r["b"] <= 0.45, f"kWh électricité hors fourchette : {r['name']}")
    need(isinstance(d["abo_e"].get(r["k"]), (int, float)) and 100 <= d["abo_e"][r["k"]] <= 450, f"abonnement électricité manquant ou hors fourchette : {r['name']}")
for r in d["gas"]:
    need(0.08 <= r["a"] <= 0.30, f"kWh gaz hors fourchette : {r['name']}")
    need(isinstance(d["abo_g"].get(r["k"]), (int, float)) and 80 <= d["abo_g"][r["k"]] <= 700, f"abonnement gaz manquant ou hors fourchette : {r['name']}")
    need(isinstance(d["abo_g0"].get(r["k"]), (int, float)), f"abonnement gaz B0 manquant : {r['name']}")
    need(r.get("niv", "confirmer") in ("officiel", "confirmer"), f"niveau de fiabilité invalide : {r['name']}")
    if "zones" in r:
        for o, z in r["zones"].items():
            need(isinstance(z, list) and len(z) == 6 and all(0.08 <= x <= 0.35 for x in z) and all(z[i + 1] >= z[i] - 0.0005 for i in range(5)), f"prix par zone invalides (6 valeurs à peu près croissantes) : {r['name']} {o}")
        need(abs(r["zones"].get("b1", [r["a"]])[0] - r["a"]) < 1e-9, f"le prix de la zone 1 doit égaler le prix affiché : {r['name']}")
    if "b0" in r: need(r["a"] < r["b0"] <= 0.35, f"kWh gaz B0 incohérent (doit dépasser le B1) : {r['name']}")
RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for r in d["gas"]:
    if "cpf" not in r: continue
    need(isinstance(r["cpf"], str) and r["cpf"].startswith("prix-cp/") and r["cpf"].endswith(".json") and ".." not in r["cpf"], f"cpf invalide : {r['name']}")
    try: f = json.load(open(os.path.join(RACINE, r["cpf"]), encoding="utf-8"))
    except Exception: need(False, f"fichier par code postal introuvable : {r['cpf']}"); continue
    need(f.get("type") == "prix-par-code-postal" and f.get("energie") == "gaz", f"{r['cpf']} : type ou énergie invalide")
    need(f.get("k") == r["k"] and f.get("offre") == r["offer"], f"{r['cpf']} : fournisseur ou offre différents de data.json ({r['k']} / {r['offer']})")
    need(bool(f.get("date")) and bool(f.get("source")), f"{r['cpf']} : date ou source manquante")
    for o in ("b0", "b1"):
        t = f.get(o) or {}
        cps = [c for v in t.get("niv", {}).values() for c in v.split()] + list(t.get("mixte", {}))
        need(len(cps) > 100 and all(len(c) == 5 and c.isdigit() for c in cps) and len(cps) == len(set(cps)), f"{r['cpf']} {o} : codes postaux invalides ou en double")
        px = [float(x) for x in t.get("niv", {})] + list(t.get("mixte", {}).values()) + list(t.get("dep", {}).values()) + [t.get("moy", 0)]
        need(all(0.08 <= x <= 0.35 for x in px), f"{r['cpf']} {o} : prix hors fourchette")
    if "zones" in r: need(abs(float(sorted(f["b1"]["niv"])[0]) - r["a"]) < 1e-9, f"{r['cpf']} : le plus bas prix doit égaler le prix zone 1 de data.json")
for k, p in d["primes"].items():
    need(p.get("st") in ("ok", "check", "none"), f"statut de prime invalide : {k}")
for r in d.get("duo", []):
    need(0.10 <= r["ea"] <= 0.45 and 100 <= r["eabo"] <= 450, f"offre duo : électricité hors fourchette : {r['name']}")
    need(0.08 <= r["ga"] <= 0.30 and 80 <= r["gabo"] <= 700, f"offre duo : gaz hors fourchette : {r['name']}")
    need(0 <= r.get("promo", 0) <= 200, f"offre duo : promotion hors fourchette : {r['name']}")
for t in ("3", "6", "9"): need(t in d["trv_abo"], f"abonnement du tarif réglementé manquant : {t} kVA")
if err: print("\n".join("ERREUR : " + e for e in err)); sys.exit(1)
print("data.json : OK")
