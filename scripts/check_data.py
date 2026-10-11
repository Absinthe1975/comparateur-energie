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
for k, p in d["primes"].items():
    need(p.get("st") in ("ok", "check", "none"), f"statut de prime invalide : {k}")
for t in ("3", "6", "9"): need(t in d["trv_abo"], f"abonnement du tarif réglementé manquant : {t} kVA")
if err: print("\n".join("ERREUR : " + e for e in err)); sys.exit(1)
print("data.json : OK")
