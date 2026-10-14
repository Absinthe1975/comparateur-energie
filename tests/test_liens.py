import json, os, sys, unittest, urllib.error
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))
import check_liens as c

class R:
    def __init__(self, s): self.status = s
    def __enter__(self): return self
    def __exit__(self, *a): pass

class Liens(unittest.TestCase):
    def test_etats(self):
        self.assertIsNone(c.etat("https://x.fr", lambda r, timeout: R(200)))
        def e(code):
            def f(r, timeout): raise urllib.error.HTTPError("https://x.fr", code, "x", {}, None)
            return f
        self.assertIsNone(c.etat("https://x.fr", e(403)))        # refuse les robots : pas compté comme cassé
        self.assertEqual(c.etat("https://x.fr", e(404)), "code 404")
        def panne(r, timeout): raise OSError("réseau")
        self.assertIn("réseau", c.etat("https://x.fr", panne))
    def test_liste(self):
        d = {"liens": {"edf": "https://a.fr/"}, "elec": [{"name": "X", "offer": "O", "url": "https://b.fr/o"}], "gas": [{"name": "Y", "offer": "P"}]}
        self.assertEqual(set(c.liens(d)), {"https://a.fr/", "https://b.fr/o"})
    def test_data_json_liens_https(self):
        d = json.load(open(os.path.join(c.RACINE, "data.json"), encoding="utf-8"))
        self.assertTrue(d["liens"] and all(u.startswith("https://") for u in d["liens"].values()))
if __name__ == "__main__": unittest.main()
