#!/usr/bin/env python3
"""Télécharge les pages « zone gaz » par département d'observatoires.net, poliment, et les range dans un zip.

À lancer sur VOTRE ordinateur (Python 3, rien à installer) :
    python3 telecharger_zones_gaz.py            # tout télécharger (environ 100 pages, 3 s entre chaque)
    python3 telecharger_zones_gaz.py --test     # seulement 2 départements, pour vérifier

Règles respectées : lecture de robots.txt avant chaque page (une page interdite est sautée), pause entre
deux demandes, arrêt immédiat en cas de refus (403 / 429), aucun contournement. Le programme reprend où il
s'est arrêté si on le relance. Résultat : le fichier zones_gaz.zip, à envoyer à Claude.
"""
import argparse
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import urllib.robotparser
import zipfile

AGENT = "ComparateurEnergieBot/1.0 (site associatif sans but lucratif, lecture ponctuelle)"


def lire(url):
    req = urllib.request.Request(url, headers={"User-Agent": AGENT, "Accept-Language": "fr"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "replace")


def liens_departements(html, base):
    """Adresses de la forme /zone-gaz/<département> trouvées dans la page d'accueil de l'outil."""
    chemin = urllib.parse.urlparse(base).path.rstrip("/")
    trouves = []
    for h in re.findall(r'href="([^"#]+)"', html):
        u = urllib.parse.urljoin(base, h)
        p = urllib.parse.urlparse(u)
        if p.netloc != urllib.parse.urlparse(base).netloc:
            continue
        m = re.fullmatch(re.escape(chemin) + r"/([a-z0-9-]+)/?", p.path)
        if m and u.split("#")[0] not in trouves:
            trouves.append(u.split("#")[0].rstrip("/"))
    return trouves


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default="https://observatoires.net/zone-gaz")
    ap.add_argument("--pause", type=float, default=3.0)
    ap.add_argument("--test", action="store_true", help="2 départements seulement")
    ap.add_argument("--dossier", default="zones_gaz_pages")
    ap.add_argument("--zip", default="zones_gaz.zip")
    a = ap.parse_args(argv)

    site = urllib.parse.urlparse(a.base)
    rp = urllib.robotparser.RobotFileParser()
    rp.set_url("%s://%s/robots.txt" % (site.scheme, site.netloc))
    try:
        rp.read()
    except Exception as e:
        print("robots.txt illisible (%s) : j'arrête, par prudence." % e)
        return 2
    if not rp.can_fetch(AGENT, a.base):
        print("robots.txt interdit la page d'accueil de l'outil : j'arrête.")
        return 2

    os.makedirs(a.dossier, exist_ok=True)
    try:
        accueil = lire(a.base)
    except Exception as e:
        print("Impossible de lire %s : %s" % (a.base, e))
        return 2
    open(os.path.join(a.dossier, "_accueil.html"), "w", encoding="utf-8").write(accueil)
    urls = liens_departements(accueil, a.base)
    print("%d pages de départements trouvées." % len(urls))
    if not urls:
        print("Aucun lien trouvé : la page d'accueil est enregistrée dans %s, envoyez-la à Claude." % a.dossier)
    if a.test:
        urls = urls[:2]
    faits = refus = 0
    for u in urls:
        nom = u.rsplit("/", 1)[-1] + ".html"
        chemin = os.path.join(a.dossier, nom)
        if os.path.exists(chemin):
            faits += 1
            continue
        if not rp.can_fetch(AGENT, u):
            print("interdit par robots.txt, sauté : " + u)
            refus += 1
            continue
        try:
            html = lire(u)
        except urllib.error.HTTPError as e:
            print("%s : erreur %s" % (u, e.code))
            if e.code in (403, 429):
                print("Le site refuse : j'arrête immédiatement (rien n'est contourné).")
                break
            continue
        except Exception as e:
            print("%s : %s" % (u, e))
            continue
        open(chemin, "w", encoding="utf-8").write(html)
        faits += 1
        print("ok %s" % nom)
        time.sleep(a.pause)
    with zipfile.ZipFile(a.zip, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(os.listdir(a.dossier)):
            z.write(os.path.join(a.dossier, f), f)
    print("Terminé : %d pages, %d interdites par robots.txt. Envoyez %s à Claude." % (faits, refus, a.zip))
    return 0


if __name__ == "__main__":
    sys.exit(main())
