# Zones tarifaires du gaz déduites du code postal

Le site déduit la zone gaz (1 à 6, zones historiques de GRDF) du code postal saisi à l'accueil.

- **Données** : `donnees/gaz/zones/NN.json` (un fichier par début de code postal, chargé seulement pour le visiteur). `i` : codes INSEE des communes par zone ; `c` : codes postaux dont toutes les communes ont la même zone.
- **Si le code postal couvre plusieurs communes de zones différentes** : la commune choisie dans la liste de l'accueil donne la zone (code INSEE). Le message sous le menu de zone le dit.
- **Si le code postal est absent** (commune non desservie par GRDF, réseau local comme Bordeaux ou Strasbourg) : le menu de zone reste manuel.
- **Offres concernées** : celles qui ont des prix par zone historique dans `donnees/` (Octopus, Mint, OHM, EDF, Happ-e). Alterna garde ses prix par code postal. ENGIE, TotalEnergies et ilek ont leurs propres découpages (non modélisés : leurs tables de zones sont à obtenir). Gaz de Bordeaux NovaFixe ne suit pas les zones historiques ; NovaFlex les suit (zones 1, 2, 3 vérifiées : 0,1591 / 0,1598 / 0,1605 €/kWh, zones 4 à 6 non relevées).
- **Source** : liste des communes par zone d'observatoires.net (source secondaire, relevée le 6 nov. 2026 avec `outils/telecharger_zones_gaz.py`, 94 pages de départements), croisée avec la base officielle des codes postaux de La Poste (fichier 019HexaSmal). Contrôle : Lille, Marseille, Onnaing zone 1 ; Paris zone 2 ; Évian-les-Bains, Moissac zone 3 (conforme aux prix Gaz de Bordeaux NovaFlex).
- **Mise à jour** : `python3 scripts/zones_gaz.py zones_gaz.zip 019HexaSmal.csv` régénère tous les fichiers. 69 communes (nouvelles communes, noms différents) ne sont pas rapprochées. À refaire de temps en temps (les zones changent rarement).
