"""Publie sur la Page Facebook du site un court message quand des prix OFFICIELS changent.
Compare donnees/*/data.json entre deux versions git (AVANT et APRÈS). Ne publie jamais les offres « à confirmer ».
Sans FB_PAGE_ID et FB_PAGE_TOKEN, affiche seulement le message (aucune publication).
Lancer : python scripts/facebook.py AVANT_SHA [APRES_SHA]"""
import json, os, subprocess, sys, urllib.parse, urllib.request

SITE = "https://absinthe1975.github.io/comparateur-energie/"
FICHIERS = (("donnees/elec/data.json", "elec"), ("donnees/gaz/data.json", "gas"))

def lire(sha, chemin):
    try:
        return json.loads(subprocess.check_output(["git", "show", f"{sha}:{chemin}"], stderr=subprocess.DEVNULL))
    except Exception:
        return None

def officielles(d, cle):
    return {(o["k"], o["offer"]): o for o in (d or {}).get(cle, []) if o.get("niv") == "officiel"}

def changements(avant, apres):
    """Offres officielles dont le prix du kWh a changé (nouvelles offres ignorées)."""
    res = []
    for chemin, cle in FICHIERS:
        a, b = officielles(lire(avant, chemin), cle), officielles(lire(apres, chemin), cle)
        for ident, o in b.items():
            if ident in a and o.get("a") != a[ident].get("a"):
                res.append((o["name"], o["offer"], a[ident].get("a"), o.get("a")))
    return res

def message(ch):
    if not ch: return None
    lignes = ["Mise à jour des prix sur le comparateur :"]
    for nom, offre, x, y in ch[:8]:
        lignes.append(f"• {nom}, {offre} : {x:.4f} → {y:.4f} €/kWh".replace(".", ","))
    if len(ch) > 8: lignes.append(f"… et {len(ch) - 8} autres offres")
    lignes.append("Prix issus des grilles officielles des fournisseurs.")
    lignes.append(SITE)
    return "\n".join(lignes)

def publier(texte):
    pid, tok = os.environ.get("FB_PAGE_ID"), os.environ.get("FB_PAGE_TOKEN")
    if not (pid and tok):
        print("FB_PAGE_ID / FB_PAGE_TOKEN absents : aucune publication."); return
    data = urllib.parse.urlencode({"message": texte, "link": SITE, "access_token": tok}).encode()
    with urllib.request.urlopen(f"https://graph.facebook.com/v21.0/{pid}/feed", data, timeout=30) as r:
        print("Publié :", r.read().decode())

if __name__ == "__main__":
    avant = sys.argv[1]; apres = sys.argv[2] if len(sys.argv) > 2 else "HEAD"
    if os.environ.get("FB_TEST") == "1":
        t = "Test de publication automatique (ignorez ce message) : le comparateur publiera ici ses mises à jour de prix officielles.\n" + SITE
    else:
        t = message(changements(avant, apres))
    if not t: print("Aucun changement de prix officiel : rien à publier.")
    else: print(t); publier(t)
