# Zones tarifaires du gaz déduites du code postal

Le site déduit la zone gaz (1 à 6, zones historiques de GRDF) du code postal saisi à l'accueil.

- **Données** : `donnees/gaz/zones/NN.json` (un fichier par début de code postal, chargé seulement pour le visiteur). `i` : codes INSEE des communes par zone ; `c` : codes postaux dont toutes les communes ont la même zone.
- **Si le code postal couvre plusieurs communes de zones différentes** : la commune choisie dans la liste de l'accueil donne la zone (code INSEE). Le message sous le menu de zone le dit.
- **Si le code postal est absent** (commune non desservie par GRDF, réseau local comme Bordeaux ou Strasbourg) : le menu de zone reste manuel.
- **Offres concernées** : celles qui ont des prix par zone historique dans `donnees/` (Octopus, Mint, OHM, EDF, Happ-e). Alterna garde ses prix par code postal. ENGIE, TotalEnergies et ilek ont leurs propres découpages (non modélisés : leurs tables de zones sont à obtenir). Gaz de Bordeaux NovaFixe ne suit pas les zones historiques ; NovaFlex les suit (zones 1, 2, 3 vérifiées : 0,1591 / 0,1598 / 0,1605 €/kWh, zones 4 à 6 non relevées).
- **Source** : liste des communes par zone d'observatoires.net (source secondaire, relevée le 6 nov. 2026 avec `outils/telecharger_zones_gaz.py`, 94 pages de départements), croisée avec la base officielle des codes postaux de La Poste (fichier 019HexaSmal). Contrôle : Lille, Marseille, Onnaing zone 1 ; Paris zone 2 ; Évian-les-Bains, Moissac zone 3 (conforme aux prix Gaz de Bordeaux NovaFlex).
- **Mise à jour** : `python3 scripts/zones_gaz.py zones_gaz.zip 019HexaSmal.csv` régénère tous les fichiers. 69 communes (nouvelles communes, noms différents) ne sont pas rapprochées. À refaire de temps en temps (les zones changent rarement).

## Zones propres à chaque fournisseur (en cours)
Chaque page de commune d'observatoires.net (source secondaire, Selectra) contient un tableau « zones tarifaires gaz par fournisseur » :
ilek (A à K), TotalEnergies (1 à 6), ENGIE 6 zones, Alterna, ENGIE 8 zones (A à H), GEG (NTR). Exemple Ambronay : ilek I, TotalEnergies 5, ENGIE 6, Alterna 6, ENGIE 8 zones D, GEG NTR 8-10.
- Téléchargement (côté utilisateur) : `python3 telecharger_zones_gaz.py --communes` → `zones_gaz_communes.zip` (tableaux seuls).
- Zip trop gros : `python3 outils/reduire_communes.py` (côté utilisateur) crée `zones_gaz_communes.csv` (petit) ; le script de construction accepte le .csv à la place du zip.
- Construction : `python3 scripts/zones_gaz.py zones_gaz.zip 019HexaSmal.csv zones_gaz_communes.zip` → `donnees/gaz/zones-fournisseurs/NN.json` (format : `t` lignes « ilek|total|engie8|alterna|geg », `i` INSEE → ligne, `c` code postal → ligne si sans ambiguïté).
- À faire ensuite : brancher ces zones sur les prix (ENGIE par groupe A à H : grille dans docs/ENGIE-GAZ-ZONES.md ; ilek, TotalEnergies : il faudra les grilles par zone).

### Premier lot de données (8 nov. 2026)
4 562 communes lues (pages du plan du site), 4 524 rattachées à un code INSEE, dans `donnees/gaz/zones-fournisseurs/`.
Contrôle : la colonne « ENGIE 6 zones » est identique à la zone GRDF des pages de départements pour 4 560 communes sur 4 562
(les deux exceptions : Druelle et Saint-Maurice-sur-Dargoire). TotalEnergies et Alterna s'écartent souvent de GRDF (environ 70 % des communes), ce qui confirme qu'ils ont leur propre découpage.
Exemple Onnaing : GRDF 1, ENGIE groupe B, ilek C, TotalEnergies 2, Alterna 2. (Lesfurets annonce « zone 2 » pour Onnaing : probablement le découpage TotalEnergies/Alterna, pas celui de GRDF.)

### ENGIE gaz : branché sur le site (9 nov. 2026)
Le groupe ENGIE (A à H) de la commune choisit la ligne de prix (`zg` dans `tarifs_manuels.json`, grille officielle de novembre 2026). Sans groupe connu, le site affiche le groupe B (le plus fréquent après A) avec « À confirmer ». Les zones ilek, TotalEnergies, Alterna et GEG sont chargées (`state.sz`) mais pas encore utilisées : il faut leurs grilles par zone.

### ilek et GEG : branchés sur le site (9 nov. 2026)
- **ilek ÉnRFixe+ Gaz** : 11 zones A à K (`zg`, `zsys: "ilek"`), prix TTC de la grille officielle (0-4 MWh et 4-335 MWh ; abonnement 18,17 et 36,53 €/mois TTC). La grille dit « disponible du 1er octobre au 1er novembre 2026 » : à vérifier si ilek publie une grille de novembre. Zone inconnue : zone C (la plus fréquente), « À confirmer ».
- **GEG Mon Offre Gaz / Biogaz fixe 3 ans** : le prix du kWh est identique partout ; seul l'abonnement dépend de la zone NTR (0-3, 4-7, 8-10) : `zabo` (B1 : 41,62 / 48,88 / 54,33 €/mois TTC ; B0 : 10,47 / 10,99 / 11,38). Zone inconnue : NTR 0-3 (valeur d'avant).
- **Pas de grille par zone dans les documents reçus** : TotalEnergies, Dyneff (un seul prix standard, « zones identiques aux anciens tarifs réglementés »), Plenitude (aucune zone), Ekwateur (national).
- **Déjà par zone GRDF** : EDF, OHM, Octopus, Mint, Happ-e (grilles 6 zones) ; Alterna par code postal.
