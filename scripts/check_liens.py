#!/usr/bin/env python3
"""Vérifie que les liens fournisseur de data.json répondent (rubrique « liens » et champ « url » des offres).
Ne bloque jamais la mise à jour : les liens en échec sont ajoutés au rapport (report.md) pour correction.
Un site qui refuse les robots (403/429) n'est pas compté comme cassé."""
import json, os, sys, urllib.error, urllib.request
DEPOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # racine du dépôt
RACINE = os.path.join(DEPOT, "donnees")      # dossier des données
UA = "ComparateurEnergieBot/1.0 (+" + os.environ.get("CONTACT", "verification des liens, non lucratif") + ")"

def liens(d):
    out = {}
    for k, u in d.get("liens", {}).items(): out[u] = f"fournisseur {k}"
    for r in d["elec"] + d["gas"] + [d.get("elec_ref", {}), d.get("gas_ref", {})]:
        if r.get("url"): out[r["url"]] = f"{r.get('name', '')} · {r.get('offer', '')}"
    return out

def etat(url, ouvrir=urllib.request.urlopen):
    try:
        with ouvrir(urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "fr"}), timeout=30) as r:
            return None if r.status < 400 else f"code {r.status}"
    except urllib.error.HTTPError as e:
        return None if e.code in (401, 403, 405, 429) else f"code {e.code}"
    except Exception as e:
        return str(e)[:80]

def main():
    import donnees
    d = donnees.charger_complet(RACINE)
    ko = [f"{u} ({qui}) : {why}" for u, qui in sorted(liens(d).items()) for why in [etat(u)] if why]
    texte = f"## Liens fournisseur en échec ({len(ko)})\n\n" + ("\n".join("- " + x for x in ko) if ko else "Aucun.") + "\n"
    print(texte)
    rapport = os.path.join(DEPOT, "report.md")
    if os.path.exists(rapport): open(rapport, "a", encoding="utf-8").write("\n" + texte)
    return 0
if __name__ == "__main__": sys.exit(main())
