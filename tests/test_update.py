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
        sj = json.load(open(up.SOURCES, encoding="utf-8")); sj["tarifs_pages_2"] = {"engie": ["https://second.example/engie"]}
        json.dump(sj, open(up.SOURCES, "w", encoding="utf-8"), ensure_ascii=False)
        os.environ["FETCH_DELAY"] = "0"; os.environ.pop("FORCE", None); os.environ.pop("CROSSCHECK", None)
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
    def test_sans_second_site_non_applique(self):
        sj = json.load(open(up.SOURCES, encoding="utf-8")); sj["tarifs_pages_2"] = {}
        json.dump(sj, open(up.SOURCES, "w", encoding="utf-8"), ensure_ascii=False)
        r, _ = self.run_engie(); self.assertEqual(r["a"], 0.2330)
        self.assertIn("à confirmer sur un second", open(up.REPORT, encoding="utf-8").read())
    def test_second_site_contredit_non_applique(self):
        up.fetch_text = lambda url: "Offres ENGIE. Elec Référence 3 ans. Le prix du kWh est de 0,2300 € TTC en option Base. L'abonnement 6 kVA est de 190,00 € par an." if "second" in url else PAGE
        def fake(prompt):
            if "second.example" in prompt:
                return {"fields": {"offre": {"value": 1, "quote": "Elec Référence 3 ans"}, "kwh": {"value": 0.23, "quote": "Le prix du kWh est de 0,2300 € TTC en option Base"}}}
            return GOOD
        up.call_llm = fake
        r, _ = self.run_engie(); self.assertEqual(r["a"], 0.2330)
        self.assertIn("contredit par un second site", open(up.REPORT, encoding="utf-8").read())
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
    def test_page_inchangee_date_du_jour(self):
        self.run_engie()                      # première lecture : empreinte mémorisée
        d = json.load(open(up.DATA, encoding="utf-8"))
        for r in d["elec"]:
            if r["k"] == "engie": r["d"] = "1 janv. 2020"
        d["abo_d"]["engie"] = "1 janv. 2020"; json.dump(d, open(up.DATA, "w", encoding="utf-8"), ensure_ascii=False)
        r, d = self.run_engie()               # page inchangée : la date du jour est posée sans nouvel appel
        self.assertEqual(r["d"], d["updated_label"]); self.assertEqual(d["abo_d"]["engie"], d["updated_label"])
    def test_variation_prix_repere(self):
        import datetime
        d = json.load(open(up.DATA, encoding="utf-8")); src = json.load(open(up.SOURCES, encoding="utf-8"))
        up.fetch_text = lambda url: "Octobre 2026. Le prix repère du gaz augmente de 6,3 % TTC en octobre."
        self.reply = {"fields": {"variation": {"value": 6.3, "quote": "Le prix repère du gaz augmente de 6,3 % TTC en octobre"}}}
        old = d["gas_b1"]["a"]; d["gas_b1"]["a"] = round(old * 1.063, 4)
        rep = up.Report(); up.update_trend(d, src, {}, rep, {}, old, datetime.datetime(2026, 10, 5))
        self.assertTrue(any("cohérent" in x for x in rep.same), rep.same)
        d["gas_b1"]["a"] = round(old * 0.9, 4)       # nous baissons alors que le médiateur annonce une hausse
        rep = up.Report(); up.update_trend(d, src, {}, rep, {}, old, datetime.datetime(2026, 10, 5))
        self.assertTrue(any("écart à vérifier" in x for x in rep.review), rep.review)
    def test_source_en_echec_ne_casse_rien(self):
        up.main(["--only", "elec"]); d = json.load(open(up.DATA, encoding="utf-8")); self.assertEqual(len(d["elec"]), 18)

    # ---- prix de référence : plusieurs sites obligatoires ----
    def _refs(self, pages, b1, b0):
        d = json.load(open(up.DATA, encoding="utf-8")); src = json.load(open(up.SOURCES, encoding="utf-8"))
        src["references"] = {"trv": [], "gas_ref": list(pages)}
        up.fetch_text = lambda url: pages[url]
        def fake(prompt):
            url = prompt.split("\n")[0].replace("Page : ", "")
            q1, q0 = pages[url].split("|")
            return {"fields": {"b1_kwh": {"value": b1[url], "quote": q1}, "b0_kwh": {"value": b0[url], "quote": q0}}}
        up.call_llm = fake
        rep = up.Report(); up.update_refs(d, src, {}, rep, {}); return d, rep
    def test_reference_deux_sites_daccord_appliquee(self):
        pg = {"http://a/x": "Chauffage 0,1500 €/kWh|Cuisson 0,1800 €/kWh", "http://b/x": "Chauffage 0,1500 €/kWh|Cuisson 0,1800 €/kWh"}
        d, rep = self._refs(pg, {u: 0.15 for u in pg}, {u: 0.18 for u in pg})
        self.assertEqual((d["gas_b1"]["a"], d["gas_b0"]["a"], d["gas_ref"]["a"]), (0.15, 0.18, 0.15)); self.assertEqual(len(rep.applied), 2)
    def test_reference_un_seul_site_non_appliquee(self):
        pg = {"http://a/x": "Chauffage 0,1500 €/kWh|Cuisson 0,1800 €/kWh"}
        old = json.load(open(up.DATA, encoding="utf-8"))["gas_b0"]["a"]
        d, rep = self._refs(pg, {u: 0.15 for u in pg}, {u: 0.18 for u in pg})
        self.assertEqual(d["gas_b0"]["a"], old); self.assertTrue(any("second site" in x or "un seul site" in x for x in rep.review + rep.same))
    def test_reference_sites_en_desaccord_non_appliquee(self):
        pg = {"http://a/x": "Chauffage 0,1500 €/kWh|Cuisson 0,1800 €/kWh", "http://b/x": "Chauffage 0,1400 €/kWh|Cuisson 0,1800 €/kWh"}
        b1 = {"http://a/x": 0.15, "http://b/x": 0.14}
        old = json.load(open(up.DATA, encoding="utf-8"))["gas_b1"]["a"]
        d, rep = self._refs(pg, b1, {u: 0.18 for u in pg})
        self.assertEqual(d["gas_b1"]["a"], old); self.assertTrue(any("désaccord" in x for x in rep.review))
    def test_reference_b0_confondu_avec_b1_refuse(self):
        pg = {"http://a/x": "Chauffage 0,1500 €/kWh|Cuisson 0,1500 €/kWh", "http://b/x": "Chauffage 0,1500 €/kWh|Cuisson 0,1500 €/kWh"}
        old = json.load(open(up.DATA, encoding="utf-8"))["gas_b0"]["a"]
        d, rep = self._refs(pg, {u: 0.15 for u in pg}, {u: 0.15 for u in pg})
        self.assertEqual(d["gas_b0"]["a"], old); self.assertTrue(any("incohérentes" in x for x in rep.review))

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
