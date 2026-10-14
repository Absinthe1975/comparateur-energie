import json, os, sys, tempfile, unittest, copy
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))
import grilles_pdf, update_prices
FX = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures")
PAGE = open(os.path.join(FX, "alterna_page.html"), encoding="utf-8").read()
TXT = open(os.path.join(FX, "alterna_cp_gaz.txt"), encoding="utf-8").read()
E1 = {"k": "alterna", "offre": "Mon gaz naturel indexé", "page": "https://www.alterna-energie.fr/gaz", "type": "cp-gaz", "contient": ["grille"], "un_de": ["gaz naturel"], "exclut": ["biogaz"]}

class Detection(unittest.TestCase):
    def setUp(self): self.l = grilles_pdf.liens_pdf(PAGE, "https://www.alterna-energie.fr/gaz")
    def test_liens_relatifs(self):
        self.assertEqual(len(self.l), 4); self.assertTrue(all(u.startswith("https://www.alterna-energie.fr/docs/") for u, _ in self.l))
    def test_gaz_naturel(self):
        u, why = grilles_pdf.choisir(self.l, E1); self.assertIsNone(why); self.assertIn("Mon_gaz_naturel_011026", u)
    def test_biogaz_via_nom_de_fichier(self):
        u, _ = grilles_pdf.choisir(self.l, {"contient": ["grille"], "un_de": ["biogaz"]}); self.assertIn("biogaz", u)
    def test_nom_change_mais_lien_retrouve(self):
        l2 = grilles_pdf.liens_pdf(PAGE.replace("011026", "011126"), "https://x.fr/"); u, _ = grilles_pdf.choisir(l2, E1); self.assertIn("011126", u)
    def test_ambigu_ou_absent(self):
        u, why = grilles_pdf.choisir(self.l, {"contient": ["grille"]}); self.assertIsNone(u); self.assertIn("plusieurs", why)
        u, why = grilles_pdf.choisir(self.l, {"contient": ["introuvable"]}); self.assertIsNone(u); self.assertIn("aucun", why)
    def test_date(self): self.assertEqual(grilles_pdf.lire_date(TXT), "01/10/2026")

class Mise_a_jour(unittest.TestCase):
    def lancer(self, racine, data, state, txt=TXT):
        rep = update_prices.Report()
        def get(u): return PAGE.encode() if u.endswith("/gaz") else b"%PDF-1.4 test"
        grilles_pdf.update_grilles(data, {"grilles": [E1]}, state, rep, None, get=get, racine=racine, to_text=lambda raw: txt)
        return rep
    def data(self): return {"gas": [{"k": "alterna", "offer": "Mon gaz naturel indexé", "a": 0.1, "cpf": "prix-cp/alterna-test.json", "niv": "confirmer"}]}
    def test_applique_et_ne_refait_pas(self):
        with tempfile.TemporaryDirectory() as t:
            os.makedirs(os.path.join(t, "prix-cp")); d, st = self.data(), {}
            rep = self.lancer(t, d, st); self.assertEqual(len(rep.applied), 1, rep.failed + rep.review)
            f = json.load(open(os.path.join(t, "prix-cp/alterna-test.json"), encoding="utf-8"))
            self.assertEqual((f["k"], f["offre"], f["date"]), ("alterna", "Mon gaz naturel indexé", "01/10/2026"))
            self.assertEqual((d["gas"][0]["niv"], d["gas"][0]["nivd"]), ("officiel", "01/10/2026")); self.assertGreater(d["gas"][0]["a"], 0.12)
            rep2 = self.lancer(t, d, st); self.assertEqual((len(rep2.applied), len(rep2.same)), (0, 1))
    def test_refuse_si_trop_peu_de_codes(self):
        with tempfile.TemporaryDirectory() as t:
            os.makedirs(os.path.join(t, "prix-cp")); d, st = self.data(), {}
            self.lancer(t, d, st); st.clear()
            rep = self.lancer(t, d, st, txt="\n".join([l for l in TXT.splitlines() if " 14,50 " in l][:20] + ["Tarifs TTC - applicables au 01/10/2026"]))
            self.assertEqual((len(rep.applied), len(rep.review)), (0, 1))
    def test_sans_date_non_applique(self):
        with tempfile.TemporaryDirectory() as t:
            os.makedirs(os.path.join(t, "prix-cp")); rep = self.lancer(t, self.data(), {}, txt=TXT.replace("applicables au 01/10/2026", ""))
            self.assertEqual((len(rep.applied), len(rep.review)), (0, 1))
if __name__ == "__main__": unittest.main()
