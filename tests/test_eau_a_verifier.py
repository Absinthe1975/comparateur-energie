import os, sys, unittest, tempfile, json
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))
import eau_a_verifier

class Basses(unittest.TestCase):
    def test_filtre(self):
        with tempfile.TemporaryDirectory() as t:
            json.dump({"01000": "01053~A~1.50~~31~0.8~0.7|01344~B~3.10~~95~1.5~1.6|01999~C~1.20~x~30~0.6~0.6", "01001": "01053~A~1.50~~31~0.8~0.7"}, open(os.path.join(t, "01.json"), "w"))
            r = eau_a_verifier.communes_basses(t)
            self.assertEqual([x[2] for x in r], ["01053"])
