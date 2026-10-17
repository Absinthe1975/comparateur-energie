import os, sys, unittest
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))
import eau_maj as e

def base(n=200, prix=4.0):
    return {"%05d" % i: "%05d~Ville %d~%.2f~~100~2~2" % (i, i, prix) for i in range(1000, 1000 + n)}

class Garde_fous(unittest.TestCase):
    def test_identique(self): self.assertEqual(e.comparer(base(), base()), [])
    def test_vide(self): self.assertTrue(e.comparer(base(), {}))
    def test_perte_codes(self): self.assertTrue(e.comparer(base(), base(150)))
    def test_prix_double(self): self.assertTrue(e.comparer(base(), base(prix=8.0)))
    def test_hausse_normale(self): self.assertEqual(e.comparer(base(), base(prix=4.1)), [])
    def test_premiere_fois(self): self.assertEqual(e.comparer({}, base()), [])

XLS = b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1"
def ecrit(u, d): open(d, "wb").write(XLS)

class Annee(unittest.TestCase):
    cfg = {"annees": [2026, 2025], "sispea": {"AEP": "u/aep_{an}", "AC": "u/ac_{an}"}}
    def test_annee_vide_repli(self):
        def conv(src, feuille, dest): return 0 if "2026" in src else 500
        self.assertEqual(e.annee_disponible(self.cfg, "/tmp", ecrit, conv), "2025")
    def test_aucune(self):
        self.assertIsNone(e.annee_disponible(self.cfg, "/tmp", ecrit, lambda *a: 0))
    def test_erreur_reseau_repli(self):
        def tel(u, d):
            if "2026" in u: raise OSError("404")
            ecrit(u, d)
        self.assertEqual(e.annee_disponible(self.cfg, "/tmp", tel, lambda *a: 500), "2025")

class Suspects(unittest.TestCase):
    def test_bas_complet_signale(self):
        com = {"06600": "06004~Antibes~1.49~~107~1.12~0.37~d", "61130": "61001~Dame~1.30~s~~1.30", "01000": "01053~Bourg~3.95~~95~2.42~1.53"}
        self.assertEqual(list(e.suspects(com)), ["06004"])


class Candidats(unittest.TestCase):
    def test_premiere_adresse_valide(self):
        import tempfile, os
        def tel(u, d):
            if "bonne" not in u: raise OSError("404")
            open(d, "wb").write(b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1 reste")
        with tempfile.TemporaryDirectory() as t:
            self.assertEqual(e.premier_qui_marche(["https://a/{an}", "https://bonne/{an}"], 2025, os.path.join(t, "x.xls"), tel), "https://bonne/2025")
    def test_page_html_refusee(self):
        import tempfile, os
        def tel(u, d): open(d, "wb").write(b"<html>erreur</html>")
        with tempfile.TemporaryDirectory() as t:
            with self.assertRaises(RuntimeError): e.premier_qui_marche("https://a/{an}", 2025, os.path.join(t, "x.xls"), tel)


class SansPrix(unittest.TestCase):
    def test_commune_sans_prix_ne_casse_pas_comparer(self):
        a = {"01000": "01001~A~~s|01002~B~3.5", "02000": "02001~C~"}
        n = {"01000": "01001~A~~s|01002~B~3.6", "02000": "02001~C~"}
        self.assertEqual(e.prix_valides(a), {"01000": [("01002", 3.5)]})
        self.assertEqual(e.comparer(a, n), [])


class Conversion(unittest.TestCase):
    def test_csv_lisible_par_build_eau(self):
        import tempfile, os, csv
        try: import openpyxl, pandas
        except ImportError: self.skipTest("openpyxl ou pandas absent")
        with tempfile.TemporaryDirectory() as t:
            wb = openpyxl.Workbook(); ws = wb.active; ws.title = "Zones tarifaires"
            ws.append(["Code INSEE de la commune adhérente", "Nom de la commune adhérente", "Population de la commune"]); ws.append(["01053", "Bourg-en-Bresse, ville", 40000])
            x = os.path.join(t, "a.xlsx"); wb.save(x)
            c = os.path.join(t, "a.csv"); self.assertEqual(e.xls_vers_csv(x, "Zones tarifaires", c), 1)
            rows = list(csv.DictReader(open(c, encoding="utf-8", newline="")))
            self.assertEqual(rows[0]["Code INSEE de la commune adhérente"], "01053"); self.assertEqual(rows[0]["Nom de la commune adhérente"], "Bourg-en-Bresse, ville")
