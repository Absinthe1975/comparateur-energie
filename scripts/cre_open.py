"""Lecture des données ouvertes de la CRE (sources officielles, sans IA).

- Tarif réglementé de l'électricité : API tabulaire de data.gouv.fr (repli : le CSV du jeu de données).
- Prix repère du gaz : fichier Excel publié sur cre.fr.
Tout est tolérant au format (virgule ou point décimal, dates jj/mm/aaaa ou aaaa-mm-jj) et strict sur le sens :
une valeur incohérente lève une erreur, jamais une valeur « devinée ».
"""
import csv, datetime, io, json, re, urllib.request

UA = "ComparateurEnergieBot/1.0 (donnees ouvertes CRE, non lucratif)"
API = "https://tabular-api.data.gouv.fr/api/resources/{rid}/data/?P_SOUSCRITE__exact={kva}&page_size=50"
MOIS_FR = {"janvier": 1, "fevrier": 2, "février": 2, "mars": 3, "avril": 4, "mai": 5, "juin": 6, "juillet": 7,
           "aout": 8, "août": 8, "septembre": 9, "octobre": 10, "novembre": 11, "decembre": 12, "décembre": 12}


def num(x):
    """'0,2001' ou '0.2001' ou 0.2001 -> 0.2001 ; vide / nul / null -> None."""
    if x is None or isinstance(x, bool): return None
    if isinstance(x, (int, float)): return float(x)
    s = str(x).strip().replace(" ", "").replace(" ", "")
    if s.lower() in ("", "nul", "null", "none", "nan"): return None
    return float(s.replace(",", "."))


def trv_courant(rows, kva):
    """Ligne en vigueur = celle dont DATE_FIN est vide. On ne s'appuie pas sur les dates : l'API a déjà
    été vue inversant jour et mois (01/08/2026 lu comme 8 janvier). Exactement une ligne doit répondre."""
    cand = [r for r in rows if num(r.get("P_SOUSCRITE")) == kva and str(r.get("DATE_FIN") or "").strip().lower() in ("", "nul", "null", "none")]
    if len(cand) != 1: raise ValueError(f"TRV {kva} kVA : {len(cand)} lignes en vigueur (une seule attendue)")
    r = cand[0]
    out = {k: num(r.get(k)) for k in ("PART_VARIABLE_TTC", "PART_VARIABLE_HT", "PART_FIXE_TTC", "PART_FIXE_HT")}
    if None in out.values(): raise ValueError(f"TRV {kva} kVA : colonne manquante")
    if not (0.10 <= out["PART_VARIABLE_TTC"] <= 0.45) or out["PART_VARIABLE_HT"] >= out["PART_VARIABLE_TTC"]:
        raise ValueError(f"TRV {kva} kVA : prix incohérents {out}")
    return out


def _get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "fr"})
    with urllib.request.urlopen(req, timeout=40) as r: return r.read()


def trv_depuis_api(rid, kva, get=_get):
    return trv_courant(json.loads(get(API.format(rid=rid, kva=kva)).decode("utf-8"))["data"], kva)


def trv_depuis_csv(rid, kva, get=_get):
    raw = get(f"https://www.data.gouv.fr/fr/datasets/r/{rid}").decode("utf-8-sig")
    return trv_courant(list(csv.DictReader(io.StringIO(raw), delimiter=";")), kva)


def trv(rid, kva, get=_get):
    """API d'abord, CSV ensuite ; les deux doivent donner la même chose si les deux répondent."""
    err = []
    for f in (trv_depuis_api, trv_depuis_csv):
        try: return f(rid, kva, get), f.__name__
        except Exception as e: err.append(f"{f.__name__} : {e}")
    raise RuntimeError(" ; ".join(err))


def gaz_grilles(path_or_bytes):
    """Renvoie [(date, {'b0_abo','b0_kwh','b1_abo','b1_kwh'})] : l'historique des grilles TTC moyennes
    + la grille à venir (onglet « Grille tarifaire TTC », daté dans son titre)."""
    import openpyxl
    src = io.BytesIO(path_or_bytes) if isinstance(path_or_bytes, (bytes, bytearray)) else path_or_bytes
    wb = openpyxl.load_workbook(src, read_only=True, data_only=True)
    out = []
    ws = wb["Historique grilles"]; cur = None; blk = {}
    def flush():
        if cur and len(blk) == 4: out.append((cur, dict(blk)))
    for row in ws.iter_rows(values_only=True):
        a = row[0]
        if isinstance(a, datetime.datetime): flush(); cur, blk = a.date(), {}; continue
        vals = [num(c) for c in row[1:] if isinstance(c, (int, float))]
        if isinstance(a, str) and a.startswith("Abonnement") and len(vals) >= 4: blk["b0_abo"], blk["b1_abo"] = vals[1], vals[3]
        if isinstance(a, str) and a.startswith("Part variable moyenne") and len(vals) >= 4: blk["b0_kwh"], blk["b1_kwh"] = vals[1], vals[3]
    flush()
    try:
        ws = wb["Grille tarifaire TTC"]; title = ""; nums = {}
        for row in ws.iter_rows(values_only=True):
            cells = [c for c in row if c is not None]
            if cells and isinstance(cells[0], str) and "au 1er" in cells[0] and not title: title = cells[0]
            if cells and cells[0] in ("Cuisson/eau chaude", "Chauffage") and len(cells) >= 5: nums[cells[0]] = cells
        m = re.search(r"au 1er (\w+) (\d{4})", title)
        if m and m.group(1).lower() in MOIS_FR and len(nums) == 2:
            c0, c1 = nums["Cuisson/eau chaude"], nums["Chauffage"]
            out.append((datetime.date(int(m.group(2)), MOIS_FR[m.group(1).lower()], 1),
                        {"b0_abo": round(num(c0[1]), 2), "b0_kwh": round(num(c0[3]) / 1000, 5),
                         "b1_abo": round(num(c1[1]), 2), "b1_kwh": round(num(c1[3]) / 1000, 5)}))
    except KeyError: pass
    if not out: raise ValueError("aucune grille gaz lue dans le fichier")
    return out


def gaz_en_vigueur(grilles, today):
    ok = [g for g in grilles if g[0] <= today]
    if not ok: raise ValueError("aucune grille gaz à cette date")
    d, g = max(ok, key=lambda x: x[0])
    if not (0.08 <= g["b1_kwh"] < g["b0_kwh"] <= 0.35) or not (80 <= g["b1_abo"] <= 700) or not (50 <= g["b0_abo"] < g["b1_abo"]):
        raise ValueError(f"grille gaz incohérente {g}")
    return d, {k: round(v, 4 if k.endswith("kwh") else 2) for k, v in g.items()}


def trouver_xlsx(page_html, base="https://www.cre.fr"):
    m = re.search(r'href="([^"]+\.xlsx?[^"]*)"', page_html, re.I) or re.search(r'href="([^"]*/content/download/[^"]+)"', page_html, re.I)
    if not m: raise ValueError("lien du fichier Excel introuvable sur la page de la CRE")
    u = m.group(1).replace("&amp;", "&")
    return u if u.startswith("http") else base + (u if u.startswith("/") else "/" + u)


def prvg_moyen(path_or_bytes):
    """Série mensuelle du prix repère moyen TTC (€/MWh), onglet « Historique PRVG moyen » : [(date, valeur)]."""
    import openpyxl
    src = io.BytesIO(path_or_bytes) if isinstance(path_or_bytes, (bytes, bytearray)) else path_or_bytes
    ws = openpyxl.load_workbook(src, read_only=True, data_only=True)["Historique PRVG moyen"]
    out = []
    for row in ws.iter_rows(values_only=True):
        if isinstance(row[0], datetime.datetime) and isinstance(row[2], (int, float)): out.append((row[0].date(), float(row[2])))
    return sorted(out)


def variation_mensuelle(serie, today):
    """Variation en % entre le mois en vigueur et le précédent, ou None."""
    ok = [x for x in serie if x[0] <= today]
    if len(ok) < 2 or not ok[-2][1]: return None
    return (ok[-1][1] / ok[-2][1] - 1) * 100
