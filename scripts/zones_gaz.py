#!/usr/bin/env python3
"""Construit les fichiers donnees/gaz/zones/NN.json : zone tarifaire gaz (1 à 6, zones historiques de GRDF)
par commune (code INSEE) et par code postal.

Sources (à fournir en arguments) :
  - le zip produit par outils/telecharger_zones_gaz.py (pages de départements d'observatoires.net, une zone par commune) ;
  - le fichier « Base officielle des codes postaux » de La Poste (CSV « 019HexaSmal », séparateur ;, ISO-8859-1).

Usage : python3 scripts/zones_gaz.py zones_gaz.zip 019HexaSmal.csv
        python3 scripts/zones_gaz.py zones_gaz.zip 019HexaSmal.csv zones_gaz_communes.zip   (zones par fournisseur)
Un fichier par début de code postal (comme donnees/eau/cp/) : seul celui du visiteur est téléchargé par le site.
Format : {"i": {"1": "01004 01007 ...", "2": "..."}, "c": {"1": "01400 ...", ...}}
  i : codes INSEE des communes, regroupés par zone ; c : codes postaux dont toutes les communes sont dans la même zone.
"""
import collections
import csv
import glob
import html
import io
import json
import os
import re
import sys
import unicodedata
import zipfile

ART = {"LE", "LES", "LA", "L", "AU", "AUX", "DE", "DES", "DU", "D", "EN", "SUR", "SOUS", "ET", "A"}


def norm(s):
    s = html.unescape(s).replace("œ", "oe").replace("Œ", "OE").replace("æ", "ae").replace("Æ", "AE")
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().upper()
    s = re.sub(r"[-'’./]", " ", s)
    s = re.sub(r"\bSAINTE\b", "STE", s)
    s = re.sub(r"\bSAINT\b", "ST", s)
    return " ".join(w for w in s.split() if w not in ART)


def lire_pages(zf):
    """[(département, commune, nom, zone)] d'après les pages de départements."""
    out = {}
    for n in zf.namelist():
        if not re.fullmatch(r"zone-gaz__[a-z0-9-]+\.html", n):
            continue
        t = zf.read(n).decode("utf-8", "replace")
        for m in re.finditer(r'<a href="/zone-gaz/([a-z0-9-]+)/([a-z0-9-]+)"\s+data-k="[^"]*"[^>]*>(.*?)</a>', t, re.S):
            d, c, body = m.groups()
            nom = re.search(r"<span>([^<]*)</span>", body)
            z = re.search(r"Zone[\s\xa0]*([1-6])", body)
            if z:
                out[(d, c)] = (html.unescape(nom.group(1).strip()) if nom else c, int(z.group(1)))
    return [(d, c, v[0], v[1]) for (d, c), v in sorted(out.items())]


def lire_poste(chemin):
    lignes = []
    with open(chemin, encoding="latin-1", newline="") as f:
        for r in csv.reader(f, delimiter=";"):
            if r and not r[0].startswith("#"):
                lignes.append((r[0], r[1], r[2], r[3] if len(r) > 3 else r[1]))
    return lignes


def rapprocher(pages, poste, ids=None):
    """Associe chaque commune des pages à un code INSEE. Rend (zone par INSEE, communes non rapprochées, codes postaux).
    Si `ids` est un dict, il reçoit aussi {(département, commune): INSEE} (pour relier les pages de communes)."""
    parnom = collections.defaultdict(set)
    parinsee = collections.defaultdict(list)
    cp = collections.defaultdict(set)
    for insee, nom, c, lib in poste:
        parnom[norm(nom)].add(insee)
        parnom[norm(lib)].add(insee)
        cp[insee].add(c)
        parinsee[insee[:3] if insee[:2] == "97" else insee[:2]].append((insee, nom, lib))
    votes = collections.defaultdict(collections.Counter)
    for d, c, nom, z in pages:
        cs = parnom.get(norm(nom), set())
        if len(cs) == 1:
            i = next(iter(cs))
            votes[d][i[:3] if i[:2] == "97" else i[:2]] += 1
    dep = {d: v.most_common(1)[0][0] for d, v in votes.items()}
    res, manque = {}, []
    for d, c, nom, z in pages:
        p, n = dep.get(d), norm(nom)
        cs = {i for i in parnom.get(n, set()) if p and i.startswith(p)}
        if not cs and p and n:  # commune nouvelle : nom contenu dans l'ancien nom ou l'inverse
            cs = {i for i, nm, lib in parinsee[p] if n in norm(nm) or norm(nm) in n or n in norm(lib)}
            if len(cs) > 1:
                cs = set()
        if len(cs) == 1:
            res[next(iter(cs))] = z
            if ids is not None:
                ids[(d, c)] = next(iter(cs))
        else:
            manque.append((d, c, nom))
    return res, manque, cp


# Codes INSEE utilisés par la base de l'eau pour les villes à arrondissements (même zone pour tous les arrondissements)
ALIAS = {"75056": [str(75100 + i) for i in range(1, 21)], "13055": [str(13200 + i) for i in range(1, 17)],
         "69123": [str(69380 + i) for i in range(1, 10)]}


def construire(res, cp):
    for alias, arrs in ALIAS.items():
        zs = {res[a] for a in arrs if a in res}
        if len(zs) == 1:
            res[alias] = zs.pop()
            cp[alias] = set().union(*[cp[a] for a in arrs if a in cp])
    parcp = collections.defaultdict(set)
    for insee, z in res.items():
        for c in cp.get(insee, ()):
            parcp[c].add(z)
    fich = collections.defaultdict(lambda: {"i": collections.defaultdict(set), "c": collections.defaultdict(set)})
    for insee, z in res.items():
        for pre in {c[:2] for c in cp.get(insee, ())}:
            fich[pre]["i"][z].add(insee)
    for c, zs in parcp.items():
        if len(zs) == 1:
            fich[c[:2]]["c"][next(iter(zs))].add(c)
    out = {}
    for pre, v in fich.items():
        out[pre] = {k: {str(z): " ".join(sorted(s)) for z, s in sorted(v[k].items())} for k in ("i", "c")}
    return out


# --- Zones propres à chaque fournisseur (pages de communes d'observatoires.net, outils/telecharger_zones_gaz.py --communes) ---

FOURNISSEURS = {"grille par defaut grdf engie": "grdf", "ilek": "ilek", "totalenergies": "total", "engie": "engie6",
                "alterna": "alterna", "engie 8 zones": "engie8", "geg fixe": "geg", "ntr": "ntr"}
ORDRE = ["ilek", "total", "engie8", "alterna", "geg"]  # colonnes gardées dans les fichiers du site


def lire_communes(zf):
    """{(département, commune): {fournisseur: zone}} d'après les pages (ou tableaux) de communes du zip."""
    out = {}
    for n in zf.namelist():
        m = re.fullmatch(r"(?:.*/)?zone-gaz__([a-z0-9-]+)__([a-z0-9-]+)\.html", n)
        if not m:
            continue
        t = zf.read(n).decode("utf-8", "replace")
        zones = {}
        for four, zone in re.findall(r'<td data-label="Fournisseur"[^>]*>(.*?)</td>\s*<td data-label="Zone tarifaire"[^>]*>(.*?)</td>', t, re.S):
            nom = norm(re.sub(r"<[^>]+>", " ", four)).lower()
            nom = nom.replace("(", "").replace(")", "")
            z = re.sub(r"<[^>]+>", " ", html.unescape(zone))
            z = re.sub(r"^\s*Zone\s+", "", z.replace("\xa0", " ").strip())
            z = " ".join(z.split())
            cle = FOURNISSEURS.get(nom)
            if cle and z:
                zones[cle] = z
        if zones:
            out[(m.group(1), m.group(2))] = zones
    return out


def lire_communes_csv(chemin):
    """Même résultat que lire_communes, depuis le CSV produit par outils/reduire_communes.py."""
    out = {}
    with open(chemin, encoding="utf-8", newline="") as f:
        lignes = csv.reader(f, delimiter=";")
        cols = next(lignes)[2:]
        for r in lignes:
            z = {c: v for c, v in zip(cols, r[2:]) if v}
            if z:
                out[(r[0], r[1])] = z
    return out


# Villes à arrondissements : (département, commune) des pages → code INSEE « ville » de ALIAS
VILLES = {("paris", "paris"): "75056", ("bouches-du-rhone", "marseille"): "13055", ("rhone", "lyon"): "69123"}


def completer(ids, communes, poste):
    """Rapproche les communes des pages de communes que les pages de départements n'ont pas fournies (nom seul, dans le
    département déjà identifié) et étend Paris, Marseille et Lyon à tous leurs arrondissements. Modifie `ids`."""
    pref = collections.defaultdict(collections.Counter)
    for (d, c), i in ids.items():
        pref[d][i[:3] if i[:2] == "97" else i[:2]] += 1
    parnom = collections.defaultdict(set)
    for insee, nom, c, lib in poste:
        parnom[norm(nom)].add(insee)
        parnom[norm(lib)].add(insee)
    ajoutes = 0
    for dc in communes:
        if dc in ids or dc in VILLES:
            continue
        d, c = dc
        if not pref.get(d):
            continue
        p = pref[d].most_common(1)[0][0]
        cs = {i for i in parnom.get(norm(c), set()) if i.startswith(p)}
        if len(cs) == 1:
            ids[dc] = next(iter(cs))
            ajoutes += 1
    arr = {}
    for dc, alias in VILLES.items():
        if dc in communes:
            for a in ALIAS[alias]:
                arr[(dc, a)] = a
    return ajoutes, arr


def construire_fournisseurs(ids, communes, cp, arr=None):
    """Un fichier par début de code postal : {"t": ["I|5|D|6|NTR 8-10", ...], "i": {INSEE: n° de ligne de t}, "c": {code postal: n°}}.
    Une ligne de t = zones ilek | TotalEnergies | ENGIE 8 zones | Alterna | GEG (vide si le fournisseur n'a pas de zone ici)."""
    parinsee = {}
    for dc, zones in communes.items():
        i = ids.get(dc)
        if i:
            parinsee[i] = "|".join(zones.get(k, "") for k in ORDRE)
    for (dc, a), i in (arr or {}).items():
        parinsee[i] = "|".join(communes[dc].get(k, "") for k in ORDRE)
    parcp = collections.defaultdict(set)
    for i, ligne in parinsee.items():
        for c in cp.get(i, ()):
            parcp[c].add(ligne)
    fich = collections.defaultdict(lambda: {"t": [], "i": {}, "c": {}})
    def idx(f, ligne):
        if ligne not in f["t"]:
            f["t"].append(ligne)
        return f["t"].index(ligne)
    for i, ligne in sorted(parinsee.items()):
        for pre in {c[:2] for c in cp.get(i, ())}:
            f = fich[pre]
            f["i"][i] = idx(f, ligne)
    for c, lignes in sorted(parcp.items()):
        if len(lignes) == 1:
            f = fich[c[:2]]
            f["c"][c] = idx(f, next(iter(lignes)))
    return dict(fich)


def main(argv):
    if len(argv) == 4:  # zones par fournisseur : zip de départements, CSV de La Poste, zip de communes
        pages = lire_pages(zipfile.ZipFile(argv[1]))
        ids = {}
        res, manque, cp = rapprocher(pages, lire_poste(argv[2]), ids)
        communes = lire_communes_csv(argv[3]) if argv[3].endswith(".csv") else lire_communes(zipfile.ZipFile(argv[3]))
        poste = lire_poste(argv[2])
        ajoutes, arr = completer(ids, communes, poste)
        out = construire_fournisseurs(ids, communes, cp, arr)
        dossier = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "donnees", "gaz", "zones-fournisseurs")
        os.makedirs(dossier, exist_ok=True)
        for f in glob.glob(os.path.join(dossier, "*.json")):
            os.remove(f)
        for pre, v in out.items():
            with open(os.path.join(dossier, pre + ".json"), "w", encoding="utf-8") as f:
                json.dump(v, f, ensure_ascii=False, separators=(",", ":"))
        print("%d communes avec zones par fournisseur sur %d pages lues, %d fichiers." % (sum(len(v["i"]) for v in out.values()), len(communes), len(out)))
        return 0
    if len(argv) != 3:
        print(__doc__)
        return 2
    pages = lire_pages(zipfile.ZipFile(argv[1]))
    res, manque, cp = rapprocher(pages, lire_poste(argv[2]))
    out = construire(res, cp)
    dossier = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "donnees", "gaz", "zones")
    os.makedirs(dossier, exist_ok=True)
    for f in glob.glob(os.path.join(dossier, "*.json")):
        os.remove(f)
    for pre, v in out.items():
        with open(os.path.join(dossier, pre + ".json"), "w", encoding="utf-8") as f:
            json.dump(v, f, ensure_ascii=False, separators=(",", ":"))
    print("%d communes rapprochées, %d non rapprochées, %d fichiers." % (len(res), len(manque), len(out)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
