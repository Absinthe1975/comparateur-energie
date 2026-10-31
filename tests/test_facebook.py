import os, sys, unittest
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))
import facebook as fb

class T(unittest.TestCase):
    def test_message_vide(self): self.assertIsNone(fb.message([]))
    def test_message(self):
        m = fb.message([("EDF", "Tarif Bleu", 0.2, 0.21)])
        self.assertIn("EDF, Tarif Bleu : 0,2000 → 0,2100", m); self.assertIn(fb.SITE, m)
    def test_officielles_ignore_confirmer(self):
        d = {"elec": [{"k": "a", "offer": "x", "niv": "confirmer"}, {"k": "b", "offer": "y", "niv": "officiel"}]}
        self.assertEqual(list(fb.officielles(d, "elec")), [("b", "y")])
if __name__ == "__main__": unittest.main()
