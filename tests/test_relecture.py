import os
import sys
import unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
import relecture


class TestRelecture(unittest.TestCase):
    def test_variation(self):
        self.assertAlmostEqual(relecture.variation(0.2, 0.25), 0.25)
        self.assertIsNone(relecture.variation(None, 0.2))
        self.assertIsNone(relecture.variation(0, 0.2))

    def test_offres(self):
        d = {"elec": [{"k": "x", "offer": "y", "a": 1}], "autre": 3}
        self.assertEqual(list(relecture.offres(d, "f")), [("f:elec", "x", "y")])

    def test_identique_rien_a_signaler(self):
        self.assertEqual(relecture.comparer("HEAD", "HEAD"), [])

    def test_officiel_source_valide_meme_gros_ecart(self):
        o = {"niv": "officiel", "nivd": "01/08/2026", "s": ["x", "https://a.fr/g.pdf"]}
        self.assertTrue(relecture.officielle_sourcee(o))
        self.assertFalse(relecture.officielle_sourcee(dict(o, nivd=None)))
        self.assertFalse(relecture.officielle_sourcee(dict(o, niv="confirmer")))


if __name__ == "__main__":
    unittest.main()
