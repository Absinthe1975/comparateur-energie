#!/usr/bin/env python3
"""Historique des prix : séries officielles de la CRE (aucune IA) et relevés de nos propres offres.

  elec/historique.json         tarif réglementé de vente (base, 6 kVA) : kWh TTC et abonnement TTC à chaque changement
  gaz/historique.json          prix repère du gaz : grilles B0 et B1 par date, et prix repère moyen mensuel (€/MWh TTC)
  elec|gaz/historique-offres.json   prix de chaque offre relevé par ce programme, ajouté seulement quand il change

Les dates du jeu de données du tarif réglementé sont écrites de façon incohérente (jour/mois inversés dans DATE_DEBUT) :
on reconstruit donc chaque début de période à partir de la fin de la précédente (DATE_FIN, toujours en fin de mois) et
on ne garde la série que si DATE_DEBUT concorde. Sinon rien n'est écrit : on préfère pas d'historique à un faux."""
import datetime, json, os, re, sys, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cre_open as c, donnees

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
API = "https://tabular-api.data.gouv.fr/api/resources/{rid}/data/?P_SOUSCRITE__exact={kva}&page_size=100"


def _date(s, ordre):
    """'2026-07-31', '31/07/2026' (ordre 'jm') ou '07/31/2026' (ordre 'mj') -> date, ou None."""
    s = str(s or "").strip()
    if s.lower() in ("", "nul", "null", "none", "nan"): return None
    m = re.match(r"^(\d{4})-(\d\d)-(\d\d)", s)
    try:
        if m:   # le jeu de données écrit parfois aaaa-jj-mm (2013-01-08 pour le 1er août 2013) : on essaie les deux ordres
            x, y = int(m.group(2)), int(m.group(3))
            return datetime.date(int(m.group(1)), x, y) if ordre == "mj" else datetime.date(int(m.group(1)), y, x)
        m = re.match(r"^(\d\d)/(\d\d)/(\d{4})$", s)
        if not m: return None
        a, b, y = int(m.group(1)), int(m.group(2)), int(m.group(3))
        return datetime.date(y, b, a) if ordre == "jm" else datetime.date(y, a, b)
    except ValueError: return None


def serie_trv(rows, kva=6):
    """[(date_debut, kwh_ttc, abo_ttc)] triée, ou ValueError si les périodes ne s'enchaînent pas."""
    rs = [r for r in rows if c.num(r.get("P_SOUSCRITE")) == kva]
    if len(rs) < 3: raise ValueError(f"TRV {kva} kVA : {len(rs)} périodes seulement")
    def fin(r):
        """Fin de période : toujours un dernier jour de mois (28 à 31), donc jamais ambiguë entre jour et mois."""
        c = [d for d in (_date(r.get("DATE_FIN"), o) for o in ("jm", "mj")) if d and (d + datetime.timedelta(days=1)).day == 1]
        return c[0] if c else None
    fermees = sorted([r for r in rs if fin(r)], key=fin); ouvertes = [r for r in rs if not fin(r)]
    if len(ouvertes) != 1: raise ValueError(f"TRV {kva} kVA : {len(ouvertes)} périodes ouvertes (une attendue)")
    ordre = fermees + ouvertes
    # début de la première période : DATE_DEBUT, lu jour/mois puis mois/jour, doit précéder sa fin
    f0 = fin(ordre[0]); debut = [d for d in (_date(ordre[0].get("DATE_DEBUT"), o) for o in ("mj", "jm")) if d and d <= f0]
    if not debut: raise ValueError("TRV : début de la première période illisible")
    d = next((x for x in debut if x.day == 1), debut[0]); out = []   # une période commence normalement le 1er du mois
    for r in ordre:
        if out:
            d = fin_prec + datetime.timedelta(days=1)
            lus = {_date(r.get("DATE_DEBUT"), o) for o in ("jm", "mj")}
            if d not in lus: raise ValueError(f"TRV : les périodes ne s'enchaînent pas à {d} (DATE_DEBUT {r.get('DATE_DEBUT')})")
        kwh, abo = c.num(r.get("PART_VARIABLE_TTC")), c.num(r.get("PART_FIXE_TTC"))
        if kwh is None or abo is None or not (0.05 <= kwh <= 0.60) or not (30 <= abo <= 400): raise ValueError(f"TRV : prix incohérent {kwh} / {abo} au {d}")
        out.append((d, round(kwh, 5), round(abo, 2)))
        fin_prec = fin(r) or d
    return out


def trv_historique(rid, kva=6, get=c._get):
    url, rows = API.format(rid=rid, kva=kva), []
    for _ in range(20):
        j = json.loads(get(url).decode("utf-8")); rows += j.get("data", [])
        url = (j.get("links") or {}).get("next")
        if not url: break
    return serie_trv(rows, kva)


def gaz_historique(raw, today):
    grilles = [(d, g) for d, g in c.gaz_grilles(raw) if d <= today]
    prvg = [(d, v) for d, v in c.prvg_moyen(raw) if d <= today]
    if len(grilles) < 3 or len(prvg) < 12: raise ValueError(f"gaz : historique trop court ({len(grilles)} grilles, {len(prvg)} mois)")
    return sorted(grilles, key=lambda x: x[0]), prvg


def instantane(offres, jour, ancien):
    """Ajoute à ancien {'k|offre': [[jour, a, b], …]} le prix du jour, seulement s'il a changé."""
    for r in offres:
        k = f"{r['k']}|{r['offer']}"; hist = ancien.setdefault(k, []); val = [r.get("a"), r.get("b")]
        if not hist or hist[-1][1:] != val: hist.append([jour] + val)
    return ancien


def _lire(chemin):
    try: return json.load(open(chemin, encoding="utf-8"))
    except FileNotFoundError: return {}


def _ecrire(chemin, obj):
    os.makedirs(os.path.dirname(chemin), exist_ok=True)
    with open(chemin, "w", encoding="utf-8") as fh: json.dump(obj, fh, ensure_ascii=False, separators=(",", ":")); fh.write("\n")


def _ecrire_serie(chemin, obj):
    """Réécrit le fichier seulement si la série a changé (la date de mise à jour seule ne compte pas), pour ne pas ouvrir de demande pour rien."""
    avant = _lire(chemin)
    if {k: v for k, v in avant.items() if k != "mis_a_jour"} == {k: v for k, v in obj.items() if k != "mis_a_jour"}: return
    _ecrire(chemin, obj)


def main(racine=RACINE, get=c._get, today=None):
    today = today or datetime.date.today(); iso = lambda d: d.isoformat(); code = 0
    src = json.load(open(os.path.join(racine, "sources.json"), encoding="utf-8")); od = src["open_data"]
    try:
        s = trv_historique(od["trv_base_rid"], 6, get)
        _ecrire_serie(os.path.join(racine, "elec", "historique.json"), {"source": "CRE, tarif réglementé de vente d'électricité, option Base, 6 kVA (data.gouv.fr)", "mis_a_jour": iso(today), "trv6": [[iso(d), k, a] for d, k, a in s]})
        print(f"Tarif réglementé : {len(s)} périodes depuis le {s[0][0]}.")
    except Exception as e: print("Historique du tarif réglementé non mis à jour :", e); code = 1
    try:
        page = get(od["gas_page"]).decode("utf-8", "replace")
        grilles, prvg = gaz_historique(get(c.trouver_xlsx(page)), today)
        _ecrire_serie(os.path.join(racine, "gaz", "historique.json"), {"source": "CRE, prix repère de vente de gaz naturel (data CRE)", "mis_a_jour": iso(today),
            "b0": [[iso(d), g["b0_kwh"], g["b0_abo"]] for d, g in grilles], "b1": [[iso(d), g["b1_kwh"], g["b1_abo"]] for d, g in grilles], "prvg": [[iso(d), round(v, 2)] for d, v in prvg]})
        print(f"Prix repère du gaz : {len(grilles)} grilles, {len(prvg)} mois depuis le {prvg[0][0]}.")
    except Exception as e: print("Historique du prix repère du gaz non mis à jour :", e); code = 1
    d = donnees.charger(racine)
    for dossier, cle in (("elec", "elec"), ("gaz", "gas")):
        chemin = os.path.join(racine, dossier, "historique-offres.json")
        _ecrire(chemin, instantane(d[cle], d.get("updated") or iso(today), _lire(chemin)))
    return code


if __name__ == "__main__":
    sys.exit(main())
