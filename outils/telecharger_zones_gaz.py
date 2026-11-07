#!/usr/bin/env python3
"""Télécharge les pages « zone gaz » par département d'observatoires.net, poliment, et les range dans un zip.

À lancer sur VOTRE ordinateur (Python 3, rien à installer) :
    python3 telecharger_zones_gaz.py            # tout télécharger (environ 100 pages, 3 s entre chaque)
    python3 telecharger_zones_gaz.py --test     # seulement 2 départements, pour vérifier
    python3 telecharger_zones_gaz.py --communes --departement ain   # pages de communes d'un département (essai)
    python3 telecharger_zones_gaz.py --communes                     # toutes les communes (plusieurs heures, reprend où il s'est arrêté)

Avec --communes, seuls les tableaux « zone par fournisseur » de chaque page de commune sont gardés (quelques ko
par commune au lieu de 300 ko) : le zip reste petit. Il faut d'abord avoir lancé le programme sans option, pour
avoir les pages de départements dans le dossier zones_gaz_pages.

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


def liens_communes(dossier, base, departement=None):
    """Adresses des pages de communes, lues dans les pages de départements déjà téléchargées."""
    site = urllib.parse.urlparse(base)
    racine = "%s://%s" % (site.scheme, site.netloc)
    chemin = site.path.rstrip("/")
    urls = []
    for f in sorted(os.listdir(dossier)):
        m = re.fullmatch(r"zone-gaz__([a-z0-9-]+)\.html", f)
        if not m or (departement and m.group(1) != departement):
            continue
        t = open(os.path.join(dossier, f), encoding="utf-8", errors="replace").read()
        for c in re.findall(r'<a href="(' + re.escape(chemin) + r'/' + re.escape(m.group(1)) + r'/[a-z0-9-]+)"', t):
            u = racine + c
            if u not in urls:
                urls.append(u)
    return urls


def tableau_fournisseurs(html):
    """Garde seulement le tableau « zones tarifaires gaz par fournisseur » (quelques ko)."""
    m = re.search(r"<table[^>]*>\s*<caption[^>]*>[^<]*par fournisseur.*?</table>", html, re.S)
    return m.group(0) if m else None


def liens_sitemap(base, rp):
    """Adresses /zone-gaz/... trouvées dans les sitemaps du site (sitemap.xml et ses sous-fichiers)."""
    site = urllib.parse.urlparse(base)
    racine = "%s://%s" % (site.scheme, site.netloc)
    chemin = site.path.rstrip("/")
    a_lire = [racine + "/sitemap.xml"]
    vus, urls = set(), []
    while a_lire and len(vus) < 20:
        s = a_lire.pop(0)
        if s in vus or not rp.can_fetch(AGENT, s):
            continue
        vus.add(s)
        try:
            xml = lire(s)
        except Exception as e:
            print("sitemap illisible (%s) : %s" % (s, e))
            continue
        for loc in re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", xml):
            if loc.endswith(".xml"):
                a_lire.append(loc)
            elif urllib.parse.urlparse(loc).path.startswith(chemin + "/"):
                u = loc.split("#")[0].rstrip("/")
                if u not in urls:
                    urls.append(u)
        time.sleep(1)
    return urls


def telecharger_communes(a, rp):
    urls = liens_communes(a.dossier, a.base, a.departement)
    if not urls:
        print("Aucune commune trouvée : lancez d'abord le programme sans option (pages de départements dans %s)." % a.dossier)
        return 2
    if a.test:
        urls = urls[:3]
    sous = os.path.join(a.dossier, "communes")
    os.makedirs(sous, exist_ok=True)
    delai = rp.crawl_delay(AGENT) or rp.crawl_delay("*")
    if delai:
        a.pause = max(a.pause, float(delai))
    restantes = [u for u in urls if not os.path.exists(os.path.join(sous, urllib.parse.urlparse(u).path.strip("/").replace("/", "__") + ".html"))]
    print("%d communes, dont %d restent à télécharger. Durée estimée : environ %d minutes." % (len(urls), len(restantes), len(restantes) * (a.pause + 0.5) / 60))
    faits = refus = 0
    for u in urls:
        nom = urllib.parse.urlparse(u).path.strip("/").replace("/", "__") + ".html"
        chemin = os.path.join(sous, nom)
        if os.path.exists(chemin):
            continue
        if not rp.can_fetch(AGENT, u):
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
        t = tableau_fournisseurs(html)
        open(chemin, "w", encoding="utf-8").write("<!-- %s -->\n%s\n" % (u, t or "<!-- pas de tableau -->"))
        faits += 1
        if faits % 50 == 0:
            print("%d pages faites" % faits)
        time.sleep(a.pause)
    with zipfile.ZipFile(a.zip.replace(".zip", "_communes.zip"), "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(os.listdir(sous)):
            z.write(os.path.join(sous, f), f)
    print("Terminé : %d pages téléchargées, %d interdites par robots.txt. Envoyez %s à Claude." % (faits, refus, a.zip.replace(".zip", "_communes.zip")))
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default="https://observatoires.net/zone-gaz")
    ap.add_argument("--pause", type=float, default=3.0)
    ap.add_argument("--test", action="store_true", help="2 pages seulement")
    ap.add_argument("--departements", action="store_true", help="seulement les pages de départements (environ 95), sans les pages de communes")
    ap.add_argument("--dossier", default="zones_gaz_pages")
    ap.add_argument("--communes", action="store_true", help="télécharger les pages de communes (tableau par fournisseur)")
    ap.add_argument("--departement", default=None, help="avec --communes : un seul département (ex. ain)")
    ap.add_argument("--zip", default="zones_gaz.zip")
    a = ap.parse_args(argv)

    site = urllib.parse.urlparse(a.base)
    rp = urllib.robotparser.RobotFileParser()
    url_robots = "%s://%s/robots.txt" % (site.scheme, site.netloc)
    try:
        # robots.txt est lu avec notre propre identité (le lecteur par défaut de Python se présente comme
        # « Python-urllib », que certains sites refusent, et le module en conclurait à tort « tout est interdit »)
        txt = lire(url_robots)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            txt = ""  # pas de robots.txt : aucune restriction annoncée
            print("Pas de robots.txt (404) : aucune restriction annoncée.")
        else:
            print("robots.txt : le site répond %s. Je n'ai donc aucune autorisation claire : j'arrête." % e.code)
            print("Ouvrez %s dans votre navigateur et envoyez-moi son contenu." % url_robots)
            return 2
    except Exception as e:
        print("robots.txt illisible (%s) : j'arrête, par prudence." % e)
        return 2
    rp.parse(txt.splitlines())
    print("robots.txt lu (%d lignes)." % len(txt.splitlines()))
    if not rp.can_fetch(AGENT, a.base):
        print("robots.txt interdit la page d'accueil de l'outil à ce programme : j'arrête.")
        print("Contenu de robots.txt :")
        print(txt[:1500])
        return 2

    os.makedirs(a.dossier, exist_ok=True)
    if a.communes:
        return telecharger_communes(a, rp)
    try:
        accueil = lire(a.base)
    except Exception as e:
        print("Impossible de lire %s : %s" % (a.base, e))
        return 2
    open(os.path.join(a.dossier, "_accueil.html"), "w", encoding="utf-8").write(accueil)
    urls = liens_departements(accueil, a.base)
    for u in liens_sitemap(a.base, rp):
        if u not in urls:
            urls.append(u)
    print("%d pages trouvées (page d'accueil + sitemaps)." % len(urls))
    if not urls:
        print("Aucun lien trouvé : la page d'accueil est enregistrée dans %s, envoyez-la à Claude." % a.dossier)
    if a.departements:
        base_p = urllib.parse.urlparse(a.base).path.rstrip("/")
        urls = [u for u in urls if u.count("/") == (base_p + "/x").count("/") + 2]
        print("%d pages de départements retenues." % len(urls))
    if a.test:
        urls = urls[:2]
    delai = rp.crawl_delay(AGENT) or rp.crawl_delay("*")
    if delai:
        a.pause = max(a.pause, float(delai))
        print("Crawl-delay demandé par le site : %s s entre deux pages." % a.pause)
    print("Durée estimée : environ %d minutes." % (len(urls) * (a.pause + 0.5) / 60))
    faits = refus = 0
    for u in urls:
        nom = urllib.parse.urlparse(u).path.strip("/").replace("/", "__") + ".html"
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
