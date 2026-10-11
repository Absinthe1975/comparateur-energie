"""Tests du script de mise à jour, sans réseau ni IA : on simule les pages et les réponses.
Lancer : python -m unittest discover -s tests"""
import json, os, shutil, sys, tempfile, unittest
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))
import update_prices as up

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGE = "Offres ENGIE. Elec Référence 3 ans. Le prix du kWh est de 0,2400 € TTC en option Base. L'abonnement 6 kVA est de 190,00 € par an."
GOOD = {"fields": {"offre": {"value": 1, "quote": "Elec Référence 3 ans"},
                   "kwh": {"value": 0.24, "quote": "Le prix du kWh est de 0,2400 € TTC en option Base"},
                   "abo": {"value": 190.0, "quote": "L'abonnement 6 kVA est de 190,00 € par an"},
                   "kwh9": {"value": None, "quote": None}}}

class T(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        for f in ("data.json", "sources.json"): shutil.copy(os.path.join(ROOT, f), self.tmp)
        up.DATA, up.SOURCES = os.path.join(self.tmp, "data.json"), os.path.join(self.tmp, "sources.json")
        up.STATE, up.REPORT = os.path.join(self.tmp, "state", "hashes.json"), os.path.join(self.tmp, "report.md")
        os.environ["FETCH_DELAY"] = "0"; os.environ.pop("FORCE", None)
        up.fetch_text = lambda url: PAGE if "engie" in url else (_ for _ in ()).throw(RuntimeError("404"))
        self.calls = 0
        self.reply = GOOD
        def fake(prompt):
            self.calls += 1; return self.reply
        up.call_llm = fake
    def run_engie(self):
        up.main(["--only", "elec"])
        d = json.load(open(up.DATA, encoding="utf-8"))
        return next(r for r in d["elec"] if r["k"] == "engie"), d
    def test_valeur_correcte_appliquee(self):
        r, d = self.run_engie()
        self.assertEqual(r["a"], 0.24); self.assertEqual(d["abo_e"]["engie"], 190.0)
        self.assertEqual(r["d"], d["updated_label"])
    def test_phrase_inventee_refusee(self):
        self.reply = json.loads(json.dumps(GOOD)); self.reply["fields"]["kwh"]["quote"] = "Le kWh coûte 0,2400 € chez nous"
        r, _ = self.run_engie(); self.assertEqual(r["a"], 0.2330)
    def test_chiffre_absent_de_la_phrase_refuse(self):
        self.reply = json.loads(json.dumps(GOOD)); self.reply["fields"]["kwh"]["value"] = 0.2500
        r, _ = self.run_engie(); self.assertEqual(r["a"], 0.2330)
    def test_hors_fourchette_refuse(self):
        self.reply = json.loads(json.dumps(GOOD)); self.reply["fields"]["kwh"]["value"] = 2.4
        r, _ = self.run_engie(); self.assertEqual(r["a"], 0.2330)
    def test_gros_ecart_non_applique(self):
        global PAGE
        old = PAGE; PAGE = PAGE.replace("0,2400", "0,3200"); self.reply = json.loads(json.dumps(GOOD))
        self.reply["fields"]["kwh"] = {"value": 0.32, "quote": "Le prix du kWh est de 0,3200 € TTC en option Base"}
        up.fetch_text = lambda url: PAGE if "engie" in url else (_ for _ in ()).throw(RuntimeError("404"))
        r, _ = self.run_engie(); PAGE = old
        self.assertEqual(r["a"], 0.2330); self.assertIn("non appliqué", open(up.REPORT, encoding="utf-8").read())
    def test_page_inchangee_pas_dappel(self):
        self.run_engie(); n = self.calls
        self.run_engie(); self.assertEqual(self.calls, n)
    def test_offre_absente(self):
        self.reply = json.loads(json.dumps(GOOD)); self.reply["fields"]["offre"]["quote"] = "Offre Fantôme"
        r, _ = self.run_engie(); self.assertEqual(r["a"], 0.2330)
    def test_accents_differents_acceptes(self):
        d = json.load(open(up.DATA, encoding="utf-8"))
        for r in d["elec"]:
            if r["k"] == "engie": r["offer"] = "Électricité Référence"
        json.dump(d, open(up.DATA, "w", encoding="utf-8"), ensure_ascii=False)
        up.fetch_text = lambda url: ("Offres ENGIE. Electricite Reference 3 ans. Le prix du kWh est de 0,2400 € TTC en option Base. L'abonnement 6 kVA est de 190,00 € par an." if "engie" in url else (_ for _ in ()).throw(RuntimeError("404")))
        self.reply = json.loads(json.dumps(GOOD)); self.reply["fields"]["offre"]["quote"] = "Electricite Reference 3 ans"
        r, _ = self.run_engie(); self.assertEqual(r["a"], 0.24)
    def test_offre_a_verifier_a_la_main_ignoree(self):
        up.main(["--only", "gaz"]); rap = open(up.REPORT, encoding="utf-8").read()
        self.assertIn("à vérifier à la main", rap)
    def test_source_en_echec_ne_casse_rien(self):
        up.main(["--only", "elec"]); d = json.load(open(up.DATA, encoding="utf-8")); self.assertEqual(len(d["elec"]), 18)

class Http(unittest.TestCase):
    def setUp(self):
        import importlib; importlib.reload(up)   # remet les vraies fonctions (les autres tests les remplacent)
    def test_gemini_reponse_lue_et_429_reessaye(self):
        os.environ.update(GEMINI_API_KEY="x", PROVIDER="gemini", LLM_DELAY="0", RETRY_WAIT="0")
        import urllib.error, io
        calls = {"n": 0}
        class R:
            def __init__(s, b): s.b = b
            def read(s): return s.b
            def __enter__(s): return s
            def __exit__(s, *a): pass
        def fake_open(req, timeout=0):
            calls["n"] += 1
            assert "generativelanguage.googleapis.com" in req.full_url and req.headers.get("X-goog-api-key") == "x"
            if calls["n"] == 1: raise urllib.error.HTTPError(req.full_url, 429, "limite", {}, io.BytesIO(b"{}"))
            return R(json.dumps({"candidates": [{"content": {"parts": [{"text": "{\"fields\": {\"a\": {\"value\": 1, \"quote\": \"x\"}}}"}]}}]}).encode())
        orig = up.urllib.request.urlopen; up.urllib.request.urlopen = fake_open
        try: out = up.call_llm("test")
        finally: up.urllib.request.urlopen = orig
        self.assertEqual(out["fields"]["a"]["value"], 1); self.assertEqual(calls["n"], 2)

class Pdf(unittest.TestCase):
    def test_pdf_lu(self):
        import importlib; importlib.reload(up)
        objs = [b"<</Type/Catalog/Pages 2 0 R>>", b"<</Type/Pages/Kids[3 0 R]/Count 1>>",
                b"<</Type/Page/Parent 2 0 R/MediaBox[0 0 300 100]/Contents 4 0 R/Resources<</Font<</F1 5 0 R>>>>>>",
                None, b"<</Type/Font/Subtype/Type1/BaseFont/Helvetica>>"]
        stream = b"BT /F1 12 Tf 10 50 Td (Prime 15 euros) Tj ET"
        objs[3] = b"<</Length " + str(len(stream)).encode() + b">>\nstream\n" + stream + b"\nendstream"
        pdf, offs = b"%PDF-1.4\n", []
        for i, o in enumerate(objs, 1):
            offs.append(len(pdf)); pdf += str(i).encode() + b" 0 obj\n" + o + b"\nendobj\n"
        xr = len(pdf)
        pdf += b"xref\n0 6\n0000000000 65535 f \n" + b"".join(("%010d 00000 n \n" % o).encode() for o in offs)
        pdf += b"trailer<</Size 6/Root 1 0 R>>\nstartxref\n" + str(xr).encode() + b"\n%%EOF"
        self.assertIn("Prime 15 euros", up.pdf_to_text(pdf))

    def test_echecs_regroupes(self):
        rep = up.Report(); cache = {}
        up.fetch_text = lambda u: (_ for _ in ()).throw(RuntimeError("interdit"))
        os.environ["FETCH_DELAY"] = "0"
        up.pagetext("http://x/a", cache, {}, rep, "elec · A"); up.pagetext("http://x/a", cache, {}, rep, "gaz · A")
        md = rep.md("1 janv.")
        self.assertEqual(md.count("http://x/a"), 1); self.assertIn("gaz · A", md)

if __name__ == "__main__":
    unittest.main()
