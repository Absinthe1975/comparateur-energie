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

class Annee(unittest.TestCase):
    cfg = {"annees": [2026, 2025], "sispea": {"AEP": "u/aep_{an}", "AC": "u/ac_{an}"}}
    def test_annee_vide_repli(self):
        def conv(src, feuille, dest): return 0 if "2026" in src else 500
        self.assertEqual(e.annee_disponible(self.cfg, "/tmp", lambda u, d: None, conv), "2025")
    def test_aucune(self):
        self.assertIsNone(e.annee_disponible(self.cfg, "/tmp", lambda u, d: None, lambda *a: 0))
    def test_erreur_reseau_repli(self):
        def tel(u, d):
            if "2026" in u: raise OSError("404")
        self.assertEqual(e.annee_disponible(self.cfg, "/tmp", tel, lambda *a: 500), "2025")
