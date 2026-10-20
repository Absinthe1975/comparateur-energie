import json, os, sys, tempfile, unittest
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))
import eau_classement as ec

class Classement(unittest.TestCase):
    def dossier(self, t, contenu):
        os.makedirs(os.path.join(t, "cp"))
        for nom, d in contenu.items(): json.dump(d, open(os.path.join(t, "cp", nom), "w", encoding="utf-8"))
        return os.path.join(t, "cp")
    def test_filtre_et_ordre(self):
        with tempfile.TemporaryDirectory() as t:
            cp = self.dossier(t, {"01.json": {
                "01000": "01001~A~4.00~~100~2~2~d|01002~B~3.50~~100~2~1.5~d|01003~C~1.50~~100~1~0.5~d|01004~D~3.00~ap~100~3~~d",
                "01001": "01002~B~3.50~~100~2~1.5~d|01005~E~3.60~~100~2~1.6~d|01006~F~5.00~~100~2~3~d|01007~G~4.50~~100~2~2.5~d"}})
            r = ec.classement(cp, {"01": "ARA"})
            self.assertEqual([c[0] for c in r["ARA"]], ["01002", "01005", "01001"])   # C trop bas, D incomplet, B une seule fois
    def test_regions_depuis_html(self):
        html = 'x\nvar DEPT_RAW = "01|Ain|ARA;03|Allier|ARA;"\n  + "2A|Corse-du-Sud|COR;";\nvar CITY_RAW = "a"'
        self.assertEqual(ec.regions_depuis_html(html), {"01": "ARA", "03": "ARA", "2A": "COR"})
    def test_fichier_du_depot(self):
        d = json.load(open(os.path.join(ec.DEPOT, "donnees", "eau", "classement.json"), encoding="utf-8"))
        self.assertEqual(len(d["regions"]), 13); self.assertTrue(all(len(v) == 3 for v in d["regions"].values()))
