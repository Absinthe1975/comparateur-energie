import os, sys, unittest, tempfile, json
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))
import donnees
RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Donnees(unittest.TestCase):
    def test_aller_retour(self):
        d = donnees.charger(RACINE)
        for k in donnees.ELEC + donnees.GAZ + ("primes", "liens", "duo", "updated"): self.assertIn(k, d)
        with tempfile.TemporaryDirectory() as t:
            donnees.enregistrer(t, d); self.assertEqual(donnees.charger(t), d)
            self.assertNotIn("elec", json.load(open(os.path.join(t, "data.json"), encoding="utf-8")))
            self.assertNotIn("gas", json.load(open(os.path.join(t, "elec", "data.json"), encoding="utf-8")))
            self.assertNotIn("elec", json.load(open(os.path.join(t, "gaz", "data.json"), encoding="utf-8")))
