import os, sys, tempfile, shutil, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
import liens

class LiensRecus(unittest.TestCase):
    def test_ecriture_idempotente_et_partie_manuelle_conservee(self):
        racine = os.path.join(os.path.dirname(__file__), "..")
        with tempfile.TemporaryDirectory() as t:
            for f in ("data.json", "sources.json"): shutil.copy(os.path.join(racine, f), t)
            for d in ("elec", "gaz", "eau"): shutil.copytree(os.path.join(racine, d), os.path.join(t, d), ignore=shutil.ignore_patterns("cp", "historique", "prix-cp"))
            open(os.path.join(t, "LIENS-RECUS.md"), "w", encoding="utf-8").write("# Titre\nlien manuel https://exemple.fr/a\n")
            liens.ecrire(t); a = open(os.path.join(t, "LIENS-RECUS.md"), encoding="utf-8").read()
            liens.ecrire(t); b = open(os.path.join(t, "LIENS-RECUS.md"), encoding="utf-8").read()
            self.assertEqual(a, b); self.assertIn("lien manuel https://exemple.fr/a", b); self.assertEqual(b.count(liens.DEB), 1)
            self.assertIn("ilek", b.lower())
