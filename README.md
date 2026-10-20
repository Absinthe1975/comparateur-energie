# comparateur-energie

Comparateur d'électricité, de gaz et d'eau, sans but lucratif, publié sur GitHub Pages.

## Organisation des dossiers

| Dossier | Contenu |
|---|---|
| `index.html` | Le site (une seule page), à la racine pour GitHub Pages |
| `donnees/` | Toutes les données du site |
| `donnees/data.json`, `sources.json` | Données communes (primes, liens, offres combinées) et liste des sources lues |
| `donnees/elec/`, `donnees/gaz/` | Offres, tarif réglementé et historiques de l'électricité et du gaz ; `gaz/prix-cp/` : prix du gaz par code postal |
| `donnees/eau/` | Prix de l'eau par code postal (`cp/`) et historique (`historique/`) |
| `donnees/manuel/` | `tarifs_manuels.json` : grilles saisies à la main, jamais modifiées par les programmes |
| `donnees/etat/` | Mémoire des programmes (empreintes des pages déjà lues) |
| `scripts/` | Programmes de mise à jour et de contrôle |
| `tests/` | Tests automatiques |
| `docs/` | `LISEZMOI.md` (mode d'emploi détaillé) et `LIENS-RECUS.md` (tous les liens utiles) |
| `.github/workflows/` | Mises à jour automatiques (prix chaque jour 1 à 10 et le lundi, eau chaque lundi) |
