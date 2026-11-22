#!/usr/bin/env python3
"""Test de bout en bout : ouvre le site, parcourt les onglets, vérifie l'absence d'erreur, des tableaux remplis et l'absence de débordement horizontal.
Tolérance : attentes sur condition (et non durées fixes), serveur attendu jusqu'à ce qu'il réponde, une seule marge de 2 px
pour le débordement, et un second essai complet avant de déclarer un échec (un échec n'est retenu que s'il se répète).
Usage : python3 tests/e2e/smoke.py   (nécessite playwright et chromium ; lance son propre serveur local)"""
import os, sys, subprocess, time, socket
from playwright.sync_api import sync_playwright
RACINE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TABS = ["home", "logt", "elec", "gaz", "duo", "eau", "abo", "marche", "prime", "methode", "sources", "legal"]

def port_libre():
    with socket.socket() as s: s.bind(("127.0.0.1", 0)); return s.getsockname()[1]

def attendre_serveur(port, delai=15):
    fin = time.time() + delai
    while time.time() < fin:
        try:
            with socket.create_connection(("127.0.0.1", port), timeout=0.5): return True
        except OSError: time.sleep(0.2)
    return False

def lignes_ok(pg, tableau, minimum=5, delai=6000):
    """Attend (jusqu'à `delai` ms) que le tableau contienne au moins `minimum` lignes."""
    try:
        pg.wait_for_function("([s, n]) => document.querySelectorAll(s + ' tbody tr').length >= n", arg=[tableau, minimum], timeout=delai)
        return True
    except Exception:
        return False

def une_passe(port):
    echecs = []
    if True:
        with sync_playwright() as p:
            b = p.chromium.launch()
            for largeur in (375, 1280):
                pg = b.new_page(viewport={"width": largeur, "height": 800}); erreurs = []
                pg.set_default_timeout(10000)
                pg.on("pageerror", lambda e: erreurs.append(str(e)))
                pg.goto("http://127.0.0.1:%d/index.html" % port, wait_until="load")
                try: pg.wait_for_selector("#tab-elec", state="visible", timeout=10000)
                except Exception: pass
                pg.wait_for_timeout(500)
                def aller(t):  # ouvre la rubrique : change de mode (particulier / pro) et ouvre « Plus » si besoin
                    if not pg.is_visible("#tab-" + t):
                        pg.click("#mode-pro" if t == "pro" else "#mode-part"); pg.wait_for_timeout(100)
                        if not pg.is_visible("#tab-" + t):
                            pg.click("#tab-plus"); pg.wait_for_timeout(100)
                    pg.click("#tab-" + t)
                for t in TABS:
                    aller(t)
                    try: pg.wait_for_selector("#p-" + t, state="visible", timeout=5000)
                    except Exception: echecs.append("%d px : onglet %s non affiché" % (largeur, t))
                    pg.wait_for_timeout(150)
                    exces = pg.evaluate("document.documentElement.scrollWidth - innerWidth")
                    if exces > 2: echecs.append("%d px : onglet %s déborde de %d px" % (largeur, t, exces))
                for t, tableau in (("elec", "#t-elec"), ("gaz", "#t-gaz")):
                    aller(t)
                    if not lignes_ok(pg, tableau): echecs.append("%d px : tableau %s presque vide" % (largeur, t))
                aller("elec"); pg.select_option("#kva", "9")
                if not lignes_ok(pg, "#t-elec"): echecs.append("%d px : tableau électricité vide à 9 kVA" % largeur)
                echecs += ["%d px : erreur JavaScript : %s" % (largeur, e) for e in erreurs]
                pg.close()
            b.close()
    return echecs

def main():
    port = port_libre()
    srv = subprocess.Popen([sys.executable, "-m", "http.server", str(port), "--bind", "127.0.0.1"], cwd=RACINE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        if not attendre_serveur(port): print("ÉCHEC : le serveur local ne répond pas"); return 1
        echecs = une_passe(port)
        if echecs:
            print("Premier essai : %d échec(s), nouvel essai complet…" % len(echecs))
            for e in echecs: print("  (1er essai)", e)
            echecs = une_passe(port)
    finally:
        srv.terminate()
    for e in echecs: print("ÉCHEC :", e)
    print("OK" if not echecs else "%d échec(s)" % len(echecs))
    return 1 if echecs else 0

if __name__ == "__main__": sys.exit(main())
