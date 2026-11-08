import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
import facebook_manuel


class TestFacebookManuel(unittest.TestCase):
    def test_brouillons_du_depot(self):
        b = facebook_manuel.brouillons(open(facebook_manuel.FICHIER, encoding="utf-8").read())
        self.assertEqual(sorted(b), ["Parrainage Alpiq", "Parrainage EDF", "Parrainage Gaz de Bordeaux", "Prix de l'eau"])
        self.assertTrue(b["Parrainage EDF"].startswith("🎁 Parrainage EDF"))
        self.assertNotIn("##", b["Prix de l'eau"])

    def test_apercu_sans_publier(self):
        self.assertEqual(facebook_manuel.main(["x", "Parrainage Alpiq"]), 0)
        self.assertEqual(facebook_manuel.main(["x", "Inconnu"]), 2)


if __name__ == "__main__":
    unittest.main()
