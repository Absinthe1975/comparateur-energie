#!/usr/bin/env python3
"""Test de bout en bout : ouvre le site, parcourt les onglets, vérifie l'absence d'erreur, des tableaux remplis et l'absence de débordement horizontal.
Usage : python3 tests/e2e/smoke.py   (nécessite playwright et chromium ; lance son propre serveur local)"""
import os, sys, subprocess, time, socket
from playwright.sync_api import sync_playwright
RACINE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TABS = ["home", "logt", "elec", "gaz", "duo", "eau", "abo", "marche", "prime", "memo", "methode", "sources", "legal"]

def port_libre():
    with socket.socket() as s: s.bind(("127.0.0.1", 0)); return s.getsockname()[1]

def main():
    port = port_libre()
    srv = subprocess.Popen([sys.executable, "-m", "http.server", str(port), "--bind", "127.0.0.1"], cwd=RACINE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1); echecs = []
    try:
        with sync_playwright() as p:
            b = p.chromium.launch()
            for largeur in (375, 1280):
                pg = b.new_page(viewport={"width": largeur, "height": 800}); erreurs = []
                pg.on("pageerror", lambda e: erreurs.append(str(e)))
                pg.goto("http://127.0.0.1:%d/index.html" % port); pg.wait_for_timeout(1500)
                for t in TABS:
                    pg.click("#tab-" + t); pg.wait_for_timeout(120)
                    if not pg.is_visible("#p-" + t): echecs.append("%d px : onglet %s non affiché" % (largeur, t))
                    exces = pg.evaluate("document.documentElement.scrollWidth - innerWidth")
                    if exces > 1: echecs.append("%d px : onglet %s déborde de %d px" % (largeur, t, exces))
                for t, tableau in (("elec", "#t-elec"), ("gaz", "#t-gaz")):
                    pg.click("#tab-" + t); pg.wait_for_timeout(200)
                    if pg.locator(tableau + " tbody tr").count() < 5: echecs.append("%d px : tableau %s presque vide" % (largeur, t))
                pg.click("#tab-elec"); pg.select_option("#kva", "9"); pg.wait_for_timeout(200)
                if pg.locator("#t-elec tbody tr").count() < 5: echecs.append("%d px : tableau électricité vide à 9 kVA" % largeur)
                echecs += ["%d px : erreur JavaScript : %s" % (largeur, e) for e in erreurs]
                pg.close()
            b.close()
    finally:
        srv.terminate()
    for e in echecs: print("ÉCHEC :", e)
    print("OK" if not echecs else "%d échec(s)" % len(echecs))
    return 1 if echecs else 0

if __name__ == "__main__": sys.exit(main())
