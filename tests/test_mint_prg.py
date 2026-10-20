import datetime, json, os, re, shutil, sys, tempfile, unittest
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))
import mint_prg as m, update_prices as up
DEPOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.join(DEPOT, "donnees")
PAGE = open(os.path.join(DEPOT, "tests", "fixtures", "mint_prix_repere_gaz.html"), encoding="utf-8").read()
B1 = {1: "0,1456", 2: "0,1463", 3: "0,1470", 4: "0,1477", 5: "0,1484", 6: "0,1491"}

def reponse(form, ok=True):
    z = int(form["DDL_Zone"]); p = PAGE
    p = re.sub(r'(id="LBL_Zone">)[^<]*', r"\g<1>Zone %d" % (z if ok else 1), p)
    return re.sub(r'(id="LBL_PriceKwh_B1_TTC">)[^<]*', r"\g<1>" + B1[z], p)

class T(unittest.TestCase):
    def test_page_reelle_zone_1(self):
        r = m.lire_prix(PAGE, 1, 10, 2026)
        self.assertEqual((r["b1_kwh"], r["b0_kwh"], r["b1_abo"], r["b0_abo"]), (0.1456, 0.1783, 30.07, 12.70))
    def test_champs_caches_et_mauvaise_zone_refusee(self):
        h = m.champs_caches(PAGE); self.assertIn("__VIEWSTATE", h); self.assertIn("__EVENTVALIDATION", h)
        with self.assertRaises(ValueError): m.lire_prix(PAGE, 3, 10, 2026)       # la page répond Zone 1
        with self.assertRaises(ValueError): m.lire_prix(PAGE, 1, 11, 2026)       # la page répond octobre
    def test_six_zones_formulaire_rejoue(self):
        vus = []
        def post(url, form): vus.append(form); return reponse(form)
        z = m.zones(lambda u: PAGE, post, "http://x/p.aspx", 10, 2026)
        self.assertEqual(z["b1"], [0.1456, 0.1463, 0.1470, 0.1477, 0.1484, 0.1491]); self.assertEqual(z["b0"], [0.1783] * 6)
        self.assertTrue(all(f["__EVENTTARGET"] == "LB_Valid" and f["__VIEWSTATE"] and f["DDL_Month"] == "10" for f in vus)); self.assertEqual(len(vus), 6)
    def test_page_qui_ignore_la_zone_demandee(self):
        with self.assertRaises(ValueError): m.zones(lambda u: PAGE, lambda u, f: reponse(f, ok=False), "http://x", 10, 2026)

class Maj(unittest.TestCase):
    def setUp(self):
        self.d = __import__("donnees").charger(ROOT); self.src = json.load(open(os.path.join(ROOT, "sources.json"), encoding="utf-8"))
        self.now = datetime.datetime(2026, 10, 14, 7, 0)
        for r in self.d["gas"]:
            if r.get("prg"): r.pop("zones", None)   # data.json peut déjà porter les zones lues par le workflow : on repart de zéro
    def run_(self, post):
        rep = up.Report(); up.update_mint_zones(self.d, self.src, rep, self.now, get=lambda u: PAGE, post=post); return rep
    def mint(self): return [r for r in self.d["gas"] if r.get("prg")][0]
    def test_applique_prix_par_zone(self):
        rep = self.run_(lambda u, f: reponse(f)); r = self.mint()
        self.assertEqual(r["zones"]["b1"][5], 0.1491); self.assertEqual((r["a"], r["b0"], r["niv"], r["nivd"]), (0.1456, 0.1783, "officiel", "01/10/2026")); self.assertFalse(rep.failed)
    def test_ecart_avec_la_cre_non_applique(self):
        sauve = dict(B1)
        for k in B1: B1[k] = "%.4f" % (float(B1[k].replace(",", ".")) + 0.01)
        B1.update({k: v.replace(".", ",") for k, v in B1.items()})
        try: rep = self.run_(lambda u, f: reponse(f))
        finally: B1.update(sauve)
        self.assertTrue(any("écart trop grand" in x for x in rep.review)); self.assertNotIn("zones", self.mint())
    def test_panne_ne_casse_rien(self):
        def boom(u, f): raise RuntimeError("503")
        rep = self.run_(boom); self.assertTrue(any("Mint" in x for x in rep.failed)); self.assertNotIn("zones", self.mint())

if __name__ == "__main__": unittest.main()
