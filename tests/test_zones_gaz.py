import io
import json
import os
import sys
import unittest
import zipfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
import zones_gaz

RACINE = os.path.join(os.path.dirname(__file__), "..")


def page(dep, communes):
    liens = "".join('<a href="/zone-gaz/%s/%s"\n data-k="%s" x-show="1"><span>%s</span><span>Zone\xa0%d</span></a>' % (dep, s, s, n, z) for s, n, z in communes)
    return "<html>%s<a href=\"/zone-gaz/metz\">Zone tarifaire gaz à Metz</a></html>" % liens


def tableau(zones):
    lignes = "".join('<tr><td data-label="Fournisseur" class="x"> <a href="#"><img alt="x"> <span>%s</span></a> </td>'
                     '<td data-label="Zone tarifaire" class="y">Zone %s</td></tr>' % (n, z) for n, z in zones)
    return '<!-- u --><table><caption>Zones tarifaires gaz \xe0 X par fournisseur</caption><tbody>%s</tbody></table>' % lignes


AMBRONAY = [("Grille par d\xe9faut (GRDF/Engie)", "6"), ("Ilek", "I"), ("TotalEnergies", "5"), ("Engie", "6"),
            ("Alterna", "6"), ("Engie 8 zones", "D"), ("GEG Fixe", "NTR 8-10"), ("NTR", "8")]


class TestZonesFournisseurs(unittest.TestCase):
    def test_lecture_et_construction(self):
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w") as z:
            z.writestr("zone-gaz__ain__ambronay.html", tableau(AMBRONAY))
            z.writestr("zone-gaz__ain__arbent.html", tableau([("Ilek", "A"), ("Engie 8 zones", "B")]))
            z.writestr("zone-gaz__ain__vide.html", "<!-- pas de tableau -->")
        com = zones_gaz.lire_communes(zipfile.ZipFile(buf))
        self.assertEqual(com[("ain", "ambronay")], {"grdf": "6", "ilek": "I", "total": "5", "engie6": "6", "alterna": "6",
                                                    "engie8": "D", "geg": "NTR 8-10", "ntr": "8"})
        self.assertNotIn(("ain", "vide"), com)
        ids = {("ain", "ambronay"): "01007", ("ain", "arbent"): "01017"}
        cp = {"01007": {"01500"}, "01017": {"01100"}}
        out = zones_gaz.construire_fournisseurs(ids, com, cp)["01"]
        self.assertEqual(out["t"][out["i"]["01007"]], "I|5|D|6|NTR 8-10")
        self.assertEqual(out["t"][out["i"]["01017"]], "A||B||")
        self.assertEqual(out["t"][out["c"]["01500"]], "I|5|D|6|NTR 8-10")


class TestZonesGaz(unittest.TestCase):
    def test_pages_et_rapprochement(self):
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w") as z:
            z.writestr("zone-gaz__nord.html", page("nord", [("lille", "Lille", 1), ("onnaing", "Onnaing", 1)]))
            z.writestr("zone-gaz__ain.html", page("ain", [("pont-d-ain", "Pont-d&#039;Ain", 3), ("arbent", "Arbent", 4)]))
            z.writestr("_accueil.html", "rien")
        pages = zones_gaz.lire_pages(zipfile.ZipFile(buf))
        self.assertEqual(len(pages), 4)  # le lien de navigation sans data-k est ignoré
        poste = [("59350", "LILLE", "59000", "LILLE"), ("59447", "ONNAING", "59264", "ONNAING"),
                 ("01289", "PONT D AIN", "01160", "PONT D AIN"), ("01017", "ARBENT", "01100", "ARBENT"),
                 ("01018", "AUTRE", "01100", "AUTRE")]
        res, manque, cp = zones_gaz.rapprocher(pages, poste)
        self.assertEqual(res, {"59350": 1, "59447": 1, "01289": 3, "01017": 4})
        self.assertEqual(manque, [])
        out = zones_gaz.construire(res, cp)
        self.assertEqual(out["59"]["c"]["1"], "59000 59264")
        self.assertIn("01100", out["01"]["c"]["4"].split())  # une commune sans zone connue (non desservie) ne rend pas le code postal ambigu
        self.assertEqual(out["01"]["i"]["3"], "01289")

    def test_alias_paris(self):
        res = {str(75100 + i): 2 for i in range(1, 21)}
        cp = {k: {"750%02d" % (int(k) - 75100)} for k in res}
        out = zones_gaz.construire(res, cp)
        self.assertIn("75056", out["75"]["i"]["2"].split())

    def test_fichiers_publies(self):
        def zone(pre, insee):
            j = json.load(open(os.path.join(RACINE, "donnees", "gaz", "zones", pre + ".json")))
            for z, s in j["i"].items():
                if insee in s.split():
                    return int(z)
        self.assertEqual(zone("59", "59350"), 1)   # Lille
        self.assertEqual(zone("75", "75056"), 2)   # Paris
        self.assertEqual(zone("74", "74119"), 3)   # Évian-les-Bains
        j = json.load(open(os.path.join(RACINE, "donnees", "gaz", "zones", "82.json")))
        self.assertIn("82200", j["c"]["3"].split())  # Moissac


if __name__ == "__main__":
    unittest.main()
