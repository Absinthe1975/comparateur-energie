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
class Donnees_integrees(unittest.TestCase):
    H = ('<script id="__NEXT_DATA__">{"a":"https:\\/\\/a.storyblok.com\\/f\\/1\\/x\\/f9e6\\/grille-tarifaire-eco-fixe-aout-26-base.pdf",'
         '"b":"https:\\u002F\\u002Fa.storyblok.com\\u002Ff\\u002F1\\u002Fx\\u002Fd505\\u002Fgrille-tarifaire-ecofixe-aout-26-hphc.pdf"}</script>'
         '<a href="https://a.storyblok.com/f/1/x/f0fd/fiche-descriptive-cocon.pdf">Fiche descriptive de l\'offre</a>')
    def test_liens_dans_le_json_de_la_page(self):
        l = grilles_pdf.liens_pdf(self.H, "https://octopusenergy.fr/offre-electricite-tarifs")
        self.assertEqual(len(l), 3)
        u, why = grilles_pdf.choisir(l, {"contient": ["grille", "base"], "exclut": ["hphc"]}); self.assertIsNone(why); self.assertIn("f9e6", u)
        u, why = grilles_pdf.choisir(l, {"contient": ["grille", "hphc"]}); self.assertIn("d505", u)
    def test_identifiant_change_chaque_mois(self):
        h2 = self.H.replace("f9e6", "aaaa").replace("aout-26", "sept-26")
        u, _ = grilles_pdf.choisir(grilles_pdf.liens_pdf(h2, "https://x.fr/"), {"contient": ["grille", "base"], "exclut": ["hphc"]}); self.assertIn("aaaa", u)

class Octopus_noms_reels(unittest.TestCase):
    NOMS = ["grille-tarifaire-eco-fixe-aout-26-base.pdf", "grille-tarifaire-ecofixe-aout-26-hphc.pdf", "grille-tarifaire-ecofixe_aout26.pdf",
            "fiche-descriptive-de-l-offre-d-electricite-cocon-juillet-26.pdf", "grille-tarifaire-octotempo_aout26.pdf",
            "fiche-descriptive-de-l-offre-electricite-octotempo-aout-26.pdf", "grille-tarifaire-gaz_fixe_oct26_b.pdf", "fiche-descriptive-de-l-offre-de-gaz-gaz-fixe-octobre-2026.pdf"]
    def test_chaque_regle_designe_un_seul_fichier(self):
        liens = [("https://a.storyblok.com/f/151412/x/%d/%s" % (i, n), "") for i, n in enumerate(self.NOMS)]
        regles = [e for e in json.load(open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "sources.json"), encoding="utf-8"))["grilles"] if e["k"] == "octo"]
        self.assertEqual(len(regles), 3)
        for e, attendu in zip(regles, ["eco-fixe-aout-26-base", "ecofixe-aout-26-hphc", "gaz_fixe_oct26"]):
            u, why = grilles_pdf.choisir(liens, e); self.assertIsNone(why, e); self.assertIn(attendu, u)

class Geg_noms_reels(unittest.TestCase):
    NOMS = ["Grille-tarifaire-Mes_Offres_Elec_fixes_3_ans-PART1026.pdf", "Grille-tarifaire-Offres-Gaz-Prix-fixes-3-ans-21092026.pdf",
            "Grille-tarifaire-Mon_Offre_Gaz_Index_e-PART1026_1.pdf", "Grille-tarifaire-Mes_Offres_Tarifs_R_glement_es_Bleues-PART08.26.pdf",
            "Fiche%20descriptive%20-%20Mon%20Offre%20Gaz%20-%20fixe%203%20ans.pdf", "fiche%20descriptive%20offre%20de%20fourniture%20d%E2%80%99%C3%A9lectricit%C3%A9%20verte%20GEG%20-%20Mon%20Offre%20Elec%20Verte%20-%20fixe%203%20ans.pdf"]
    def test_regles_geg(self):
        liens = [("https://www.geg.fr/Medias/tarifs/" + n, "") for n in self.NOMS]
        regles = [e for e in json.load(open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "sources.json"), encoding="utf-8"))["grilles"] if e["k"] == "geg"]
        self.assertEqual(len(regles), 2)
        for e, attendu in zip(regles, ["Mes_Offres_Elec_fixes_3_ans", "Offres-Gaz-Prix-fixes-3-ans"]):
            u, why = grilles_pdf.choisir(liens, e)
            self.assertIsNone(why, (e, why)); self.assertIn(attendu, u)

class Urls_directes(unittest.TestCase):
    def lancer(self, entree, reponses, data, state, txt=TXT, racine="."):
        rep = update_prices.Report()
        grilles_pdf.update_grilles(data, {"grilles": [entree]}, state, rep, None, get=lambda u: reponses[u], racine=racine, to_text=lambda raw: txt)
        return rep
    def test_info_reference_puis_changement(self):
        e = {"k": "edf", "offre": "Zen Fixe", "url": "https://edf.fr/g.pdf", "type": "info"}; st = {}
        r1 = self.lancer(e, {"https://edf.fr/g.pdf": b"%PDF-1.4 a"}, {"gas": []}, st); self.assertEqual((len(r1.same), len(r1.review)), (1, 0))
        r2 = self.lancer(e, {"https://edf.fr/g.pdf": b"%PDF-1.4 a"}, {"gas": []}, st); self.assertEqual((len(r2.same), len(r2.review)), (1, 0))
        r3 = self.lancer(e, {"https://edf.fr/g.pdf": b"%PDF-1.4 b"}, {"gas": []}, st); self.assertEqual((len(r3.same), len(r3.review)), (0, 1)); self.assertIn("edf.fr/g.pdf", r3.review[0])
    def test_url_qui_est_une_page(self):
        e = {"k": "alterna", "offre": "Mon gaz naturel indexé", "url": "https://x.fr/tarifs", "type": "info", "contient": ["grille"], "un_de": ["gaz naturel"], "exclut": ["biogaz"]}
        rep = self.lancer(e, {"https://x.fr/tarifs": PAGE.encode(), "https://x.fr/docs/DOC_Grille_Tarifaire_Mon_gaz_naturel_011026_index_e_HT_TTC__1_.pdf": b"%PDF-1.4 z"}, {"gas": []}, {})
        self.assertEqual((len(rep.same), len(rep.failed)), (1, 0))
    def test_url_ni_pdf_ni_page_utile(self):
        e = {"k": "alterna", "offre": "X", "url": "https://x.fr/t", "type": "info"}
        rep = self.lancer(e, {"https://x.fr/t": b"<html>rien</html>"}, {"gas": []}, {}); self.assertEqual(len(rep.failed), 1)
    def test_cp_gaz_par_url_directe(self):
        with tempfile.TemporaryDirectory() as t:
            os.makedirs(os.path.join(t, "prix-cp")); d = {"gas": [{"k": "alterna", "offer": "Mon gaz naturel indexé", "a": 0.1, "cpf": "prix-cp/alterna-test.json", "niv": "confirmer"}]}
            e = dict(E1, url="https://x.fr/tarifs-gaz-indexe"); e.pop("page")
            rep = self.lancer(e, {"https://x.fr/tarifs-gaz-indexe": b"%PDF-1.4 t"}, d, {}, racine=t); self.assertEqual(len(rep.applied), 1, rep.failed + rep.review)
            f = json.load(open(os.path.join(t, "prix-cp/alterna-test.json"), encoding="utf-8")); self.assertEqual(f["source"], "https://x.fr/tarifs-gaz-indexe")
if __name__ == "__main__": unittest.main()


class Proposition_ia(unittest.TestCase):
    E = {"k": "llum", "offre": "Base", "url": "https://x.fr/g.pdf", "type": "info"}
    def lancer(self, kwh, quote, state):
        rep = update_prices.Report()
        data = {"elec": [{"k": "llum", "offer": "Base", "a": 0.19}], "gas": []}
        def ia(label, url, text, needle, fields, st, rp, extra="", nocache=False):
            return {"kwh": {"value": kwh, "quote": quote}}, None
        pdf = [b"%PDF-1.4 un", b"%PDF-1.4 deux"][state.pop("n", 0)]
        grilles_pdf.update_grilles(data, {"grilles": [self.E]}, state, rep, None, get=lambda u: pdf, to_text=lambda raw: "Base : prix du kWh 0,2010 € TTC", ask_fn=ia)
        return rep, data
    def test_pdf_modifie_propose_sans_appliquer(self):
        st = {}; self.lancer(0.19, "prix du kWh 0,19 €", st)           # première vue : référence
        st["n"] = 1
        rep, data = self.lancer(0.2010, "Base : prix du kWh 0,2010 € TTC", st)
        self.assertEqual(len(rep.review), 1); self.assertIn("0.201", rep.review[0]); self.assertEqual(data["elec"][0]["a"], 0.19)
    def test_citation_fausse_refusee(self):
        st = {}; self.lancer(0.19, "x", st); st["n"] = 1
        rep, data = self.lancer(0.2010, "phrase inventée 0,2010", st)
        self.assertIn("n'a pas pu lire", rep.review[0]); self.assertEqual(data["elec"][0]["a"], 0.19)
