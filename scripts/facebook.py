"""Publie sur la Page Facebook du site, par rubrique, ce qui a changé entre deux versions git.
Cinq publications au plus par exécution, chacune seulement s'il y a un changement :
électricité, gaz, offres combinées, parrainages, abonnements.
Ne publie que des données fiables : offres au niveau « officiel », parrainages « ok ».
Sans FB_PAGE_ID et FB_PAGE_TOKEN, affiche seulement les messages (aucune publication).
Lancer : python scripts/facebook.py AVANT_SHA [APRES_SHA]"""
import json, os, subprocess, sys, time, urllib.error, urllib.parse, urllib.request

SITE = "https://absinthe1975.github.io/comparateur-energie/"
MAX_LIGNES = 8

def lire(sha, chemin):
    try:
        return json.loads(subprocess.check_output(["git", "show", f"{sha}:{chemin}"], stderr=subprocess.DEVNULL))
    except Exception:
        return None

def fr(x, n=4):
    return f"{x:.{n}f}".replace(".", ",")

def officielles(d, cle):
    return {(o["k"], o["offer"]): o for o in (d or {}).get(cle, []) if o.get("niv") == "officiel"}

def ch_offres(a, b, cle):
    """Prix du kWh (clé « a ») des offres officielles présentes avant et après."""
    A, B = officielles(a, cle), officielles(b, cle)
    return [f"• {o['name']}, {o['offer']} : {fr(A[i]['a'])} → {fr(o['a'])} €/kWh"
            for i, o in B.items() if i in A and o.get("a") != A[i].get("a")]

def ch_duo(a, b):
    def idx(d): return {(o["k"], o["offer"]): o for o in (d or {}).get("duo", []) if o.get("niv") == "officiel"}
    A, B = idx(a), idx(b)
    res = []
    for i, o in B.items():
        if i not in A: continue
        p = []
        for cle, lib in (("ea", "électricité"), ("ga", "gaz")):
            if o.get(cle) != A[i].get(cle) and A[i].get(cle) is not None and o.get(cle) is not None:
                p.append(f"{lib} {fr(A[i][cle])} → {fr(o[cle])} €/kWh")
        if p: res.append(f"• {o['name']}, {o['offer']} : " + " ; ".join(p))
    return res

def ch_primes(a, b):
    A, B = (a or {}).get("primes", {}), (b or {}).get("primes", {})
    res = []
    for k, v in B.items():
        w = A.get(k)
        if not w or v.get("st") != "ok" or w.get("st") != "ok": continue
        if (v.get("pn"), v.get("fn")) != (w.get("pn"), w.get("fn")):
            res.append(f"• {v['name']} : parrain {w.get('p')} → {v.get('p')}, filleul {w.get('f')} → {v.get('f')}")
    return res

def ch_abo(ae, be, ag, bg):
    """Abonnements par an : électricité à 6 kVA, gaz (base et cuisson/eau chaude), selon le fournisseur."""
    noms = {k: v["name"] for k, v in (be.get("primes") or {}).items()}
    res = []
    for (x, y, lib) in ((ae.get("abo_e", {}), be.get("abo_e", {}), "électricité 6 kVA"), (ag.get("abo_g", {}), bg.get("abo_g", {}), "gaz"), (ag.get("abo_g0", {}), bg.get("abo_g0", {}), "gaz sans chauffage")):
        for k, v in y.items():
            if k in x and isinstance(v, (int, float)) and isinstance(x[k], (int, float)) and v != x[k]:
                res.append(f"• {noms.get(k, k)}, abonnement {lib} : {fr(x[k], 2)} → {fr(v, 2)} € par an")
    return res

def messages(avant, apres):
    g = lambda ch: (lire(avant, ch) or {}, lire(apres, ch) or {})
    ea, eb = g("donnees/elec/data.json")
    ga, gb = g("donnees/gaz/data.json")
    da, db = g("donnees/data.json")
    rub = [
        ("Électricité : mise à jour des prix du kWh", ch_offres(ea, eb, "elec"), "Prix issus des grilles officielles des fournisseurs."),
        ("Gaz : mise à jour des prix du kWh", ch_offres(ga, gb, "gas"), "Prix issus des grilles officielles des fournisseurs."),
        ("Offres combinées électricité + gaz : mise à jour des prix", ch_duo(da, db), "Prix issus des grilles officielles des fournisseurs."),
        ("Parrainages : ça change", ch_primes(da, db), "Montants relevés chez les fournisseurs, à vérifier sur leur site avant de s'inscrire."),
        ("Abonnements : mise à jour des prix", ch_abo(ea, {**eb, "primes": db.get("primes", {})}, ga, gb), "Prix de l'abonnement par an, taxes comprises."),
    ]
    out = []
    for titre, lignes, pied in rub:
        if not lignes: continue
        l = lignes[:MAX_LIGNES]
        if len(lignes) > MAX_LIGNES: l.append(f"… et {len(lignes) - MAX_LIGNES} autres")
        out.append("\n".join([titre + " :"] + l + [pied, SITE]))
    return out

def publier(texte):
    pid, tok = os.environ.get("FB_PAGE_ID"), os.environ.get("FB_PAGE_TOKEN")
    if not (pid and tok):
        print("FB_PAGE_ID / FB_PAGE_TOKEN absents : aucune publication."); return True
    data = urllib.parse.urlencode({"message": texte, "link": SITE, "access_token": tok}).encode()
    try:
        with urllib.request.urlopen(f"https://graph.facebook.com/v21.0/{pid}/feed", data, timeout=30) as r:
            print("Publié :", r.read().decode()); return True
    except urllib.error.HTTPError as e:
        corps = e.read().decode("utf-8", "replace").replace(tok, "***")
        print(f"ERREUR Facebook {e.code} : {corps}"); return False

if __name__ == "__main__":
    avant = sys.argv[1]; apres = sys.argv[2] if len(sys.argv) > 2 else "HEAD"
    if os.environ.get("FB_TEST") == "1":
        textes = ["Test de publication automatique (ignorez ce message) : le comparateur publiera ici ses mises à jour de prix officielles.\n" + SITE]
    else:
        textes = messages(avant, apres)
    if not textes: print("Aucun changement à publier.")
    ok = True
    for i, t in enumerate(textes):
        print("---\n" + t)
        if i: time.sleep(5)
        ok = publier(t) and ok
    sys.exit(0 if ok else 1)
