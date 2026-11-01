import os, sys, unittest
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))
import facebook as fb

def off(prix, niv="officiel"): return {"k": "x", "name": "EDF", "offer": "Zen", "a": prix, "niv": niv}

class T(unittest.TestCase):
    def test_offres_officielles_seulement(self):
        a = {"elec": [off(0.2), {**off(0.3, "confirmer"), "offer": "B"}]}
        b = {"elec": [off(0.21), {**off(0.4, "confirmer"), "offer": "B"}]}
        self.assertEqual(fb.ch_offres(a, b, "elec"), ["• EDF, Zen : 0,2000 → 0,2100 €/kWh"])
    def test_nouvelle_offre_ignoree(self):
        self.assertEqual(fb.ch_offres({"elec": []}, {"elec": [off(0.2)]}, "elec"), [])
    def test_duo(self):
        d = lambda e, g: {"duo": [{"k": "e", "name": "ENGIE", "offer": "Duo", "ea": e, "ga": g, "niv": "officiel"}]}
        r = fb.ch_duo(d(0.2, 0.1), d(0.21, 0.1))
        self.assertEqual(len(r), 1); self.assertIn("électricité 0,2000 → 0,2100", r[0]); self.assertNotIn("gaz", r[0])
    def test_primes_ok_seulement(self):
        mk = lambda pn, st: {"primes": {"a": {"name": "A", "p": f"{pn} €", "f": "10 €", "pn": pn, "fn": 10, "st": st}}}
        self.assertEqual(len(fb.ch_primes(mk(20, "ok"), mk(30, "ok"))), 1)
        self.assertEqual(fb.ch_primes(mk(20, "check"), mk(30, "check")), [])
        self.assertEqual(fb.ch_primes(mk(20, "ok"), mk(20, "ok")), [])
    def test_abo(self):
        ea, eb = {"abo_e": {"edf": 190.0}}, {"abo_e": {"edf": 195.5}, "primes": {"edf": {"name": "EDF"}}}
        r = fb.ch_abo(ea, eb, {"abo_g": {}, "abo_g0": {}}, {"abo_g": {}, "abo_g0": {}})
        self.assertEqual(r, ["• EDF, abonnement électricité 6 kVA : 190,00 → 195,50 € par an"])
    def test_plafond_lignes(self):
        self.assertEqual(fb.MAX_LIGNES, 8)
if __name__ == "__main__": unittest.main()
