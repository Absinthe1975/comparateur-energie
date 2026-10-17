import datetime, json, os, shutil, sys, tempfile, unittest
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))
import eau_historique as h
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EN_TETE = "Code INSEE de la commune adhérente,Nom de la commune adhérente,Population de la commune,Zone tarifaire 1,Tarif zone tarifaire 1,Identifiant SISPEA de l'entité de gestion à laquelle la commune adhère\n"

def csv_annee(prix, n=3200):
    """n communes (INSEE 01000…) au prix donné ; la 1re commune a un prix différent."""
    lignes = [EN_TETE]
    for i in range(n):
        ins = "%02d%03d" % (1 + i // 900, i % 900); lignes.append('%s,Commune %d,500,Indicateur tarif,"%s",123\n' % (ins, i, str(prix + (0.5 if i == 0 else 0)).replace(".", ",")))
    return "".join(lignes)

class T(unittest.TestCase):
    def lancer(self, t, annees_ok, jour=datetime.date(2026, 10, 17)):
        os.makedirs(os.path.join(t, "eau"), exist_ok=True); shutil.copy(os.path.join(ROOT, "eau", "eau-config.json"), os.path.join(t, "eau"))
        def tel(url, dest):
            an = int(url.split("_")[-1][:4])
            if an not in annees_ok: raise OSError("404")
            open(dest, "wb").write(b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1")
        def conv(src, feuille, dest):
            an = int(os.path.basename(src).split("_")[1][:4]); txt = csv_annee(2.0 + (an - 2020) * 0.1 if "AEP" in src else 1.0)
            open(dest, "w", encoding="utf-8").write(txt); return len(txt.splitlines()) - 1
        return h.main(t, tel, conv, jour)

    def test_series_par_commune_et_national(self):
        with tempfile.TemporaryDirectory() as t:
            self.assertEqual(self.lancer(t, {2023, 2024, 2025}), 0)
            d = h.lire(os.path.join(t, "eau", "historique"))
            self.assertEqual(sorted(d["01001"]), [2023, 2024, 2025]); self.assertEqual(d["01001"][2025], (2.5, 1.0))
            nat = json.load(open(os.path.join(t, "eau", "historique", "national.json"), encoding="utf-8"))
            self.assertEqual(sorted(nat), ["2023", "2024", "2025"]); self.assertEqual(nat["2025"]["ep"], 2.5)
    def test_annee_absente_ignoree_et_rien_de_nouveau(self):
        with tempfile.TemporaryDirectory() as t:
            self.assertEqual(self.lancer(t, set()), 1)
            self.assertFalse(os.path.exists(os.path.join(t, "eau", "historique")))
    def test_annees_anciennes_conservees(self):
        with tempfile.TemporaryDirectory() as t:
            self.lancer(t, {2022, 2025})
            self.lancer(t, {2025})   # 2022 n'est plus servi : on garde ce qu'on a
            self.assertIn(2022, h.lire(os.path.join(t, "eau", "historique"))["01001"])
if __name__ == "__main__": unittest.main()
