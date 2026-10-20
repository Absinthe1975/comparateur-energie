import os, sys, unittest, tempfile, json
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))
import donnees
RACINE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "donnees")

class Donnees(unittest.TestCase):
    def test_aller_retour(self):
        d = donnees.charger(RACINE)
        for k in donnees.ELEC + donnees.GAZ + ("primes", "liens", "duo", "updated"): self.assertIn(k, d)
        with tempfile.TemporaryDirectory() as t:
            donnees.enregistrer(t, d); self.assertEqual(donnees.charger(t), d)
            self.assertNotIn("elec", json.load(open(os.path.join(t, "data.json"), encoding="utf-8")))
            self.assertNotIn("gas", json.load(open(os.path.join(t, "elec", "data.json"), encoding="utf-8")))
            self.assertNotIn("elec", json.load(open(os.path.join(t, "gaz", "data.json"), encoding="utf-8")))


class Manuels(unittest.TestCase):
    D = {"elec": [{"k": "a", "offer": "X", "a": 0.2, "b": 0.2, "niv": "confirmer"}], "gas": [], "duo": [], "abo_e": {"a": 190.0}, "abo_g": {}, "abo_g0": {}}
    def test_complete_une_offre_et_en_ajoute_une(self):
        m = {"elec": [{"k": "a", "offer": "X", "a": 0.19, "niv": "officiel"}, {"k": "b", "offer": "Y", "a": 0.21, "b": 0.21}], "abo_e": {"_note": 1, "b": 200.0}}
        out = donnees.fusionner_manuels(self.D, m)
        self.assertEqual(out["elec"][0]["a"], 0.19); self.assertEqual(out["elec"][0]["b"], 0.2); self.assertEqual(out["elec"][0]["niv"], "officiel")
        self.assertEqual(len(out["elec"]), 2); self.assertEqual(out["abo_e"], {"a": 190.0, "b": 200.0})
        self.assertEqual(self.D["elec"][0]["a"], 0.2)   # l'original n'est pas modifié
    def test_fichier_vide_ne_change_rien(self):
        self.assertEqual(donnees.fusionner_manuels(self.D, {"elec": [], "_exemple": {}}), self.D)
    def test_fichier_du_depot(self):
        import json, os
        racine = os.path.join(os.path.dirname(__file__), "..", "donnees")
        self.assertIsInstance(json.load(open(os.path.join(racine, "manuel", "tarifs_manuels.json"), encoding="utf-8"))["elec"], list)
