import datetime, json, os, shutil, sys, tempfile, unittest
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))
import historique as h
DEPOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.join(DEPOT, "donnees")

def ligne(debut, fin, kwh, abo): return {"DATE_DEBUT": debut, "DATE_FIN": fin, "P_SOUSCRITE": 6, "PART_VARIABLE_TTC": kwh, "PART_FIXE_TTC": abo}
# DATE_DEBUT écrite mois/jour, DATE_FIN jour/mois : cas réel observé
ROWS = [ligne("08/01/2025", "31/01/2026", "0,2016", "157,0"), ligne("02/01/2026", "31/07/2026", "0,1952", "190,8"), ligne("08/01/2026", None, "0,2001", "192,3"),
        {"DATE_DEBUT": "08/01/2026", "DATE_FIN": None, "P_SOUSCRITE": 9, "PART_VARIABLE_TTC": "0,2001", "PART_FIXE_TTC": "250"}]

class T(unittest.TestCase):
    def test_dates_reconstruites(self):
        s = h.serie_trv(ROWS)
        self.assertEqual([x[0] for x in s], [datetime.date(2025, 8, 1), datetime.date(2026, 2, 1), datetime.date(2026, 8, 1)])
        self.assertEqual(s[-1][1:], (0.2001, 192.3))
    def test_dates_iso_inversees(self):
        iso = [ligne("2025-01-08", "2026-01-31", "0,2016", "157,0"), ligne("2026-01-02", "2026-07-31", "0,1952", "190,8"), ligne("2026-01-08", None, "0,2001", "192,3")]
        self.assertEqual([x[0] for x in h.serie_trv(iso)], [datetime.date(2025, 8, 1), datetime.date(2026, 2, 1), datetime.date(2026, 8, 1)])
        iso2 = [ligne("2025-08-01", "2026-01-31", "0,2016", "157,0"), ligne("2026-02-01", "2026-07-31", "0,1952", "190,8"), ligne("2026-08-01", None, "0,2001", "192,3")]
        self.assertEqual(len(h.serie_trv(iso2)), 3)   # dates normales aussi acceptées
    def test_refuse_si_les_periodes_ne_s_enchainent_pas(self):
        mauvais = [dict(r) for r in ROWS]; mauvais[1]["DATE_DEBUT"] = "03/15/2026"
        with self.assertRaises(ValueError): h.serie_trv(mauvais)
    def test_refuse_prix_absurde(self):
        mauvais = [dict(r) for r in ROWS]; mauvais[0]["PART_VARIABLE_TTC"] = "2,016"
        with self.assertRaises(ValueError): h.serie_trv(mauvais)
    def test_instantane_n_ajoute_que_les_changements(self):
        o = [{"k": "x", "offer": "Y", "a": 0.2, "b": 0.21}]; hist = h.instantane(o, "2026-10-01", {})
        h.instantane(o, "2026-10-08", hist); self.assertEqual(hist["x|Y"], [["2026-10-01", 0.2, 0.21]])
        o[0]["a"] = 0.19; h.instantane(o, "2026-11-01", hist); self.assertEqual(len(hist["x|Y"]), 2)
    def test_main_ecrit_elec_et_survit_a_un_echec_gaz(self):
        with tempfile.TemporaryDirectory() as t:
            for f in ("data.json", "sources.json"): shutil.copy(os.path.join(ROOT, f), t)
            for dos in ("elec", "gaz"): os.makedirs(os.path.join(t, dos)); shutil.copy(os.path.join(ROOT, dos, "data.json"), os.path.join(t, dos))
            def get(u):
                if "tabular-api" in u: return json.dumps({"data": ROWS, "links": {}}).encode()
                raise OSError("réseau coupé")
            self.assertEqual(h.main(t, get, datetime.date(2026, 10, 17)), 1)
            j = json.load(open(os.path.join(t, "elec", "historique.json"), encoding="utf-8")); self.assertEqual(len(j["trv6"]), 3)
            self.assertTrue(os.path.exists(os.path.join(t, "gaz", "historique-offres.json")))
            self.assertFalse(os.path.exists(os.path.join(t, "gaz", "historique.json")))
            chemin = os.path.join(t, "elec", "historique.json"); avant = open(chemin, encoding="utf-8").read()
            h.main(t, get, datetime.date(2026, 10, 24)); self.assertEqual(open(chemin, encoding="utf-8").read(), avant)   # même série : fichier inchangé
    def test_gaz_historique_depuis_le_classeur_cre(self):
        import io, openpyxl
        wb = openpyxl.Workbook(); ws = wb.active; ws.title = "Historique grilles"
        for m in range(1, 6):
            d = datetime.datetime(2026, m, 1)
            ws.append([d, "Cuisson/eau chaude", None, "Chauffage"]); ws.append([None, "HT", "TTC", "HT", "TTC"])
            ws.append(["Abonnement (€/an)", 112.8, 152.4, 252.0, 360.7]); ws.append(["Part variable moyenne (€/kWh)", 0.12, 0.15 + m / 1000, 0.10, 0.13 + m / 1000])
        pv = wb.create_sheet("Historique PRVG moyen"); pv.append(["Date", "HT", "TTC"])
        for m in range(1, 13): pv.append([datetime.datetime(2025, m, 1), 100 + m, 120 + m])
        b = io.BytesIO(); wb.save(b)
        grilles, prvg = h.gaz_historique(b.getvalue(), datetime.date(2026, 10, 17))
        self.assertEqual(len(grilles), 5); self.assertEqual(len(prvg), 12); self.assertEqual(prvg[0], (datetime.date(2025, 1, 1), 121.0))
        with self.assertRaises(ValueError): h.gaz_historique(b.getvalue(), datetime.date(2026, 2, 17))

if __name__ == "__main__": unittest.main()
