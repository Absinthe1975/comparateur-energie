<!-- Mémo retiré du site le 2 novembre 2026, conservé ici. Ne l'oublie pas : à relire avant chaque session. -->
# Mémo : ce qu'il reste à faire

Mémo du 13 novembre 2026. Il commence par une vue d'ensemble (à lire en premier), puis donne le détail fournisseur par fournisseur. Un sujet est abandonné définitivement : la lecture des factures (vie privée : le site ne demande, ne lit et ne conserve aucune facture ni donnée personnelle).

## Vue d'ensemble

### 1. Ce que je peux faire seul, sans rien de ta part
- Fins de promotions : le site masque tout seul une promotion après sa date de fin (EDF « 80 ans » 15 nov., Gaz de Bordeaux 30 nov.). Il n'y a rien d'urgent à faire ; je supprime les lignes périmées de `data.json` dans un nettoyage de temps en temps (ENGIE retirée le 10 nov.). Les branches mortes du dépôt sont supprimées chaque dimanche par le flux « Nettoyage des anciennes branches ». 31 déc. : Énergie d'ici (offre du bulletin valable jusqu'au 31 déc. 2026, à ressaisir avec la nouvelle grille) ; retirer la prime OHM / EDF et la fin du parrainage EDF.
- Rendre le test de bout en bout plus tolérant.
- Rapprocher à la main les 41 petites communes sans zone fournisseur (communes nouvelles ou renommées).

### 2. Ce qu'il me faut de toi (documents à m'envoyer)
- **Gaz de Bordeaux gaz** : fiches NovaFlex des zones 4 à 6 et table commune → zone.
- **ENGIE électricité** : la fiche descriptive de **novembre 2026** est reçue le 12 nov. (fourniture 0,17110 €/kWh TTC et 45,79 €/an, obligations 0,01834 € à 6 kVA et 0,02005 € dès 9 kVA ; acheminement : sans différenciation 0,05988 € le kWh et 149,39 €/an à 6 kVA, ou 4 plages de 0,0144 à 0,0926 € et 141,19 €/an). Le site garde 0,2403 et 186,98 €/an (Selectra, 4 plages, « À confirmer ») : l'abonnement est confirmé, pas le prix du kWh, qui dépend de la formule d'acheminement du client. Pour la décision, voir « Ce que tu dois trancher ». Ancienne note : la fiche reçue était la grille d'**août 2026** (fourniture + acheminement + obligations séparés ; en base 6 kVA : 0,14384 + 0,05988 + 0,01804 = 0,2218 €/kWh TTC, abonnement 195,18 €/an), alors que le site affiche 0,2403 (2 nov., source secondaire, « À confirmer »). Décision à prendre : afficher la grille d'août calculée (« Grille officielle du 08/2026 ») ou attendre la grille de novembre.
- **Ekwateur** : un PDF de grille (le prix n'apparaît qu'à la souscription).
- **Enercoop** : preuve de la suspension des nouvelles souscriptions (la page d'accueil affiche toujours « Je souscris », donc il reste affiché).
- **Gaz de Bordeaux** : conditions du NovaFixe Duo et règlement du Novafixe Bonus Duo (le règlement du Bonus Élec est reçu et lu le 12 nov. ; la page Duo ne publie aucun prix) ; une fiche Novaflex Élec d'une autre ville. **EDF** : pages des offres duo.
- **Octopus** : hypothèses d'OctoSaisons (55 % de la consommation en hiver, 7 % de jours rouges) à valider ; durées d'heures creuses confirmées le 12 nov. par la page officielle (16 h l'été, 10 h l'hiver, 22 jours rouges de novembre à mars, jamais le week-end), mais les plages exactes (21 h à 7 h, plus 11 h à 17 h l'été) ne viennent encore que de Selectra. La grille du 30 oct. 2026 reçue donne les mêmes prix qu'en août.
- **Fournisseurs à ajouter** : fiches de Urban Solar Energy, Jeety Energy (la grille reçue est celle de l'outre-mer : il faut la grille de métropole) ; Papernest Énergie gaz (page sans grille) ; et, d'après la liste de Selectra du 11 nov., La Bellenergie (autres offres).
- **Offres à prix fixe manquantes (une à la fois, grille du fournisseur et non celle de Selectra)** : EDF Zen Fixe (autres variantes), TotalEnergies Fixe 3 ans (TotalEnergies Fixe 2 ans électricité est faite), Octopus Eco Fixe 2 ans, Plenitude Plenifix 1 an, Gaz de Bordeaux NovaFixe Bonus.
- **Fiches descriptives pour les filtres** : type de prix, durée de blocage et énergie verte manquent pour plusieurs offres (voir « Limites connues »), donc elles disparaissent dès qu'on active le filtre correspondant.


### 3. Ce que tu dois trancher
- **LLUM avec un Linky** : afficher une moyenne des prix par saison, ou seulement une mention.
- **Primeo** : afficher le prix calculé (tarif réglementé −5 %) comme « calculé selon la formule officielle », ou le laisser « À confirmer ».
- **ENGIE électricité, prix du kWh** : (a) garder 0,2403 « À confirmer » (Selectra) ; (b) afficher la grille officielle de novembre calculée avec l'acheminement sans différenciation (6 kVA : 0,2493 € le kWh, 195,18 €/an), en « Grille officielle du 11/2026 » mais plus cher que Selectra ; (c) attendre le prix total d'ENGIE (simulateur). Ma préférence : (c) en gardant (a) d'ici là.
- **Pro** : ajouter les taxes avec un choix « Mon activité », ou rester hors taxes.

### 4. Ce qu'il faut refaire régulièrement
- **Chaque mois (autour du 1er)** : Dyneff gaz (nouvelle grille mensuelle), Mint gaz (Biogaz Online et Classic), Octopus gaz Fixe, Gaz de Bordeaux (fiches du mois : NovaFixe et NovaFlex, élec et gaz), ENGIE Pro Latitude (prix indexé). Le suivi automatique signale les nouveaux PDF dans son rapport ; c'est toi qui m'envoies les fichiers et moi qui saisis.
- **Février et août (changement du tarif réglementé)** : EDF Tarif Bleu (grille 12 à 36 kVA), Alpiq (remise de 0,5 % sur le kWh HT), Primeo, Mint, Gaz de Bordeaux Novaflex, puis les grilles d'août de chaque fournisseur (Octopus, LLUM, Enercoop, La Bellenergie, GEG, Dyneff, OHM).
- **Quand un fournisseur change sa grille** : surtout EDF, ilek, GEG, ENGIE, Dyneff, Octopus (sites qui bloquent les robots, ou PDF que le programme ne sait pas lire) : tu m'envoies le fichier, je saisis, la PR est relue puis fusionnée automatiquement.
- **À chaque grille saisie** : lien dans docs/LIENS-RECUS.md, puis `python3 scripts/liens.py`.

### 5. Ce qui se fait tout seul
- Nettoyage des branches du dépôt : chaque dimanche (workflow « Nettoyage des anciennes branches »). Il garde main, les branches « sauvegarde… » et celles avec une demande de fusion ouverte ou modifiées depuis moins de 2 jours. Sauvegarde du site avant la refonte : branche `sauvegarde-2026-11-10`.
- Prix du tarif réglementé (CRE) et prix repère du gaz : mise à jour automatique du 1er au 10 de chaque mois, puis chaque lundi.
- Prix par code postal d'Alterna, historique des prix, vérification des liens fournisseur, eau (chaque lundi : une demande de fusion s'ouvre seulement si des prix changent).
- Relecture automatique des PR (écarts de prix des offres non officielles, offre retirée, source manquante), fusion automatique quand les tests sont au vert, post Facebook à chaque changement de prix officiel. Depuis le 7 nov., les mises à jour de prix du robot se fusionnent seules (plus d'approbation manuelle des tests) ; une PR bloquée porte l'étiquette « ne-pas-fusionner ».

### 6. Ce qui est déjà saisi d'après une grille officielle récente
- Électricité : EDF (Tarif Bleu, Zen), Octopus (Eco fixe, Intelligent), OHM (octobre), Mint, Dyneff, LLUM (compteur non communicant), Enercoop, GEG, Gaz de Bordeaux (novembre), Plenitude, Alterna, Alpiq, La Bellenergie.
- Gaz : Dyneff (octobre), Mint (novembre), Octopus (novembre), Alterna, GEG.
- Électricité TotalEnergies « Fixe 2 ans » : ajoutée le 12 nov. (grille officielle du 24 sept. 2026, Base 0,2270 € de 3 à 6 kVA et 0,2252 € dès 7 kVA, heures pleines / creuses 0,2435 / 0,1791 €, page de souscription ouverte le 12 nov. ; Hello Watt donne les mêmes prix, mis à jour le 6 nov.). Le titre de la page (« -17 % vs TRV ») est périmé : au prix de la grille, l'offre est plus chère que le tarif réglementé.
- Gaz TotalEnergies « Fixe 2 ans » : fait le 10 nov. (grille du 24 sept., prix par zone 1 à 6, zone déduite de la commune), reconfirmé le 12 nov. avec la grille et la page de souscription.
- Zones de gaz par code postal : fait. Zones GRDF (7 nov.), puis zones propres aux fournisseurs pour 9 461 communes dont Paris, Lyon, Marseille et Strasbourg (9-10 nov., source secondaire observatoires.net / Selectra, voir docs/ZONES-GAZ.md). Prix par zone branchés : ENGIE (groupes A à H), ilek (zones A à K), TotalEnergies (zones 1 à 6), GEG (abonnement par zone NTR) ; par zone GRDF : EDF, OHM, Octopus, Mint, Happ-e ; Alterna par code postal. Dyneff, Plenitude, Ekwateur n'ont pas de prix par zone. Reste à faire seul : 41 petites communes non rapprochées (zone GRDF utilisée).
- GEG : fiches descriptives de novembre 2026 (Elec Verte, Direct Producteur, Gaz, Biogaz, Gaz Indexée, Tarif Bleu) reçues le 13 nov. : aucune donnée à corriger ; « L'Offre Online » n'existe plus.
- Fait ces derniers jours : Énergie d'ici « Energie Bleue » (option Base) ajoutée le 14 nov. dans le filtre « Prix variable » (prix par saison et plage horaire, offre valable jusqu'au 31 déc. 2026) avec son parrainage 20 € / 20 € ; reste l'option heures creuses (MU 4) à modéliser ; Papernest Énergie électricité saisie (14 nov., grille du 22 sept. 2026 ; tarif nettement plus cher que le tarif réglementé) ; Sobry et Frank Énergie relevés sans calcul (prix du marché heure par heure) ; mylight150 (Vert France, prix de bienvenue 12 mois, foyers équipés de panneaux solaires) et Symphonics (-50 % heures creuses, Linky niveau 2 et équipement pilotable) ajoutés le 14 nov. d'après leurs grilles officielles (autres offres Symphonics : flexibilité, achat de surplus : pas de grille reçue) ; La Bellenergie, grille du 1er nov. 2026 saisie (14 nov.) ; mode sombre et clavier du menu vérifiés (11 nov.) ; OHM « Prix Réservé » en mention hors classement jusqu'au 31 mai 2027 (11 nov.) ; Alterna additionnée en Élec + Gaz avec la mention « deux contrats, une seule facture, aucune remise connue à ce jour » (12 nov.).
- Encore « À confirmer » : ENGIE (élec), Ekwateur, Primeo (calculé), Gaz de Bordeaux gaz (zone de Paris).
- Parrainages : confirmés par une page officielle, sauf Ekwateur, Happ-e et ilek ; Plenitude n'a aucun programme.

## Détail par sujet

## Électricité À faire, au fil de vos envois

### Grilles à saisir ou à confirmer, fournisseur par fournisseur

- [Gaz de Bordeaux](https://www.gazdebordeaux.fr/) : NovaFixe Élec est saisie (fiche officielle de novembre 2026 relevée pour Onnaing, Lille, Paris 1er, Marseille 01 et Moissac, toutes identiques : Base 0,1919 / 0,19042 €, heures pleines / creuses 0,20536 / 0,1528 € ; abonnements inchangés ; les grilles d'octobre étaient identiques dans 6 villes, à vérifier pour novembre dans une autre ville). Novaflex Élec (indexée, 2 % sous le tarif réglementé, 2 ans) est saisie d'après la fiche officielle de novembre 2026 (Base 0,1968 / 0,19526 €, heures pleines / creuses 0,21067 / 0,15646 €, relevée pour Onnaing seulement). La grille du NovaFixe Bonus Élec est identique à celle du NovaFixe Élec. Gaz de Bordeaux édite ses fiches par commune : NovaFixe novembre est identique dans 5 villes ; Novaflex à vérifier dans une autre ville. Règlement du Bonus Élec lu le 12 nov. 2026 (souscription du 1er oct. au 30 nov. ; remise étalée sur 12 mois pour les mensualisés, sinon déduite de la facture suivant le 11e mois ; perdue en cas de résiliation ou de changement d'offre). Le bonus de 100 € de l'offre Bonus Élec suit son [règlement](https://ressources.gazdebordeaux.fr/DOCUMENTS/REGLEMENT/Reglement_novafixe_bonus_elec.pdf) (souscription jusqu'au 30 novembre 2026) : il s'affiche sous l'offre, hors classement. Ensuite, supprimer sa ligne dans la rubrique « promos » de donnees/data.json.

- [ENGIE](https://particuliers.engie.fr/) : Elec Référence 3 ans à confirmer : prix de novembre 2026 relevés sur Selectra (grille du 30 oct. 2026, TTC : base 0,2403 € de 3 à 6 kVA et 0,2420 € dès 9 kVA ; heures pleines 0,2561 €, creuses 0,2023 € ; abonnement 186,98 € par an à 6 kVA), source secondaire. La fiche descriptive officielle d'octobre 2026 est reçue : elle donne fourniture, acheminement et obligations séparément. L'abonnement de 186,98 € à 6 kVA se retrouve exactement (fourniture 45,79 € + acheminement à 4 plages 141,19 €). Contrôle du 2 nov. 2026 avec la fiche (accise 0,0367 € TTC, obligations 0,0184 € à 6 kVA et 0,0201 € dès 9 kVA, acheminement à 4 plages de 0,0144 à 0,0926 €) : la base de Selectra (0,2403 et 0,2420 €) est compatible, et son écart de 0,0017 € entre 6 et 9 kVA correspond exactement aux obligations. En revanche le prix en heures creuses de Selectra (0,2023 €) est inférieur au minimum que permet la fiche (0,2146 €) : il n'est plus affiché. Pour passer l'offre en « Grille officielle », il faut le prix total d'ENGIE (simulateur ou courrier) ou la formule d'acheminement du client. Promotion de deux mois d'abonnement offerts, jusqu'au 7 novembre 2026 : affichée sous les offres ENGIE, hors classement ; supprimer sa ligne dans « promos » après cette date. Page de promotions ENGIE du 28 octobre 2026 lue : elle confirme cette promotion (souscription du 19 octobre au 7 novembre inclus, Elec, Gaz ou Duo Référence 3 ans, ou Happy Week-End) et décrit la « Promo d'été » (50 % de l'électricité consommée de 13 h à 17 h en cagnotte), notée dans l'onglet Saisons.

- [LLUM](https://www.llum.fr/) : grille officielle d'août 2026 lue. Compteur non communicant : Base 0,19 €/kWh et HP/HC 0,2071 / 0,1540 € (modélisés, officiels). Avec un Linky, LLUM applique une grille par saison et heures pleines / creuses (Base : 0,22276 € en HP hiver, 0,15064 € en HC été), non modélisée. À décider : modéliser une moyenne, ou afficher une mention.

- [Alpiq](https://particuliers.alpiq.fr/) (Sérénité) : prix indexé (remise de 0,5 % sur le kWh HT du tarif réglementé) : à resaisir à chaque changement du tarif réglementé (février, août), avec la grille PDF d'Alpiq.

- [Octopus](https://octopusenergy.fr/) : « Cocon fixe » est le nom du contrat (fiche descriptive de juillet 2026) de l'offre vendue sous le nom « OctoEco Fixe » (« Eco fixe » dans ses grilles) : la page officielle des tarifs relie bien ces trois noms, confirmé le 4 nov. 2026. Eco fixe Base (grille du 12 août 2026) vérifiée : conforme. Gaz Fixe : grille mensuelle de novembre 2026 (applicable au 30 oct.) saisie, à ressaisir chaque mois. Intelligent Octopus Fixe : grille officielle du 1er août 2026 vérifiée (0,1968 € jusqu'à 8 kVA, 0,1953 € au-delà), passée en « Grille officielle ». Pour l'offre saisonnière, le prix moyen suppose 58 % de la consommation en hiver : à confirmer ou corriger. OctoSaisons (ex-OctoTempo, renommée le 21 octobre 2026) : grille officielle du 1er août 2026 reçue (docs/OCTOSAISONS-GRILLE.md) et calculée dans l’onglet Électricité (filtre « Prix variable selon le jour ou l’heure »), avec EDF Tempo et Zen Estival, à partir de vos usages (profil horaire supposé par le site, hors classement général). Les plages d'heures creuses d'OctoSaisons (21 h à 7 h, plus 11 h à 17 h l'été) viennent d'un article de presse et ne figurent pas dans la fiche officielle : à confirmer auprès d'Octopus. Hypothèses des saisons à valider (7 % de jours rouges, 55 % en hiver) ; puis décider d'intégrer ces offres au classement si d'autres fournisseurs adoptent ce principe.

- [Ekwateur](https://ekwateur.fr/) : le prix n'apparaît qu'à la souscription (code postal demandé), sans grille publique. Il faut un PDF de grille, ou renoncer à « Grille officielle » pour cet acteur.

- [Primeo](https://particuliers.primeo-energie.fr/) (Essentielle Verte) : le prix est une formule (kWh HT à 95 % du tarif réglementé, abonnement identique). Notre 0,1919 €/kWh en 6 kVA est cohérent mais calculé par nous. À décider : l'afficher comme « calculé selon la formule officielle (tarif réglementé −5 %) » et le recalculer à chaque mise à jour du tarif réglementé, ou le laisser « À confirmer ».

- [Enercoop](https://www.faq.enercoop.fr/hc/fr/articles/360024967152-Annexes-tarifaires) : grille du 1er août 2026 intégrée (Base et Flexibilité heures creuses). Non modélisées : Nuit & week-end, 2 saisons, jours de pointe (plages horaires et saisons propres à Enercoop). Sa suspension d'accueil, annoncée dans des données sans source datée, n'est pas confirmée par ses pages officielles : à vérifier avant de le retirer.

- [ilek](https://www.ilek.fr/grilles-tarifaires) : ses PDF sont sur un domaine qui interdit les robots : à relire à la main à chaque changement de grille.

- [EDF](https://particulier.edf.fr/) : Zen Estival : grille officielle reçue (15 sept. 2026) et calculée dans l’onglet Électricité (filtre « Prix variable selon le jour ou l’heure ») avec la répartition de consommation publiée par EDF (exemple à 3,6 MWh par an sans chauffage électrique), car les plages d'hiver ne figurent pas dans les documents reçus ; elle n'apparaît pas pour un chauffage électrique. Le site interdit les robots (robots.txt) : ses 12 grilles PDF et ses pages de prix restent saisies à la main à chaque changement. Le tarif réglementé, lui, vient de la CRE.

- [GEG](https://www.geg.fr/) : le script prend le PDF le plus récent de la [page des tarifs](https://www.geg.fr/aide-et-contact/centre-documentation/particulier/tarifs/). « L'Offre Online » n'apparaît plus dans les offres de GEG (pages et tarifs officiels du 12 nov. 2026) : plus rien à envoyer. Offres actuelles : Elec Verte et Direct Producteur (fixes 3 ans), Gaz et Biogaz (fixes 3 ans), Gaz Indexée (Grenoble seulement), Tarif Bleu (réglementé, Grenoble et communes voisines). Fiches descriptives reçues le 12 nov. : type de prix, 3 ans, énergie verte et biogaz confirmés (déjà saisis) ; GEG écrit que toutes ses offres de marché sont « sans engagement ».

### Heures pleines / creuses

- Le choix « Formule » apparaît dans l'onglet Électricité dès qu'une offre a ses prix. Déjà saisis : Dyneff, La Bellenergie, Gaz de Bordeaux, Enercoop, ilek, EDF Zen Fixe, Alpiq, Mint, GEG, LLUM (compteur non communicant) et OHM (1, 2 et 3 ans) (Elec Verte et Direct Producteur, grille du 5 oct. 2026, prix des 6 et 9 kVA).

- À saisir dans la rubrique hphc de donnees/manuel/tarifs_manuels.json (champs hp et hc en €/kWh TTC, abo par puissance) : LLUM (GEG est fait). Je ne peux pas lire ces PDF d'ici : envoyez les chiffres ou les fichiers.

### Fournisseurs à ajouter (liste du 24 octobre 2026, à confirmer sur leurs sites)
- [OHM](https://www.ohm-energie.com/) : fiches officielles d'octobre 2026 saisies pour Sérénité 1 an (0,2212 €/kWh Base dès 6 kVA, 0,2001 € à 3-5 kVA non distingué), 2 ans (0,2249 €) et Premi'Ohm 3 ans (0,2287 €), avec heures pleines / creuses. Non modélisée : l'offre Week-end (fiche du 4 sept. 2026 : semaine heures pleines 0,265 € / creuses 0,1737 €, week-end 0,1737 €).
- [OHM](https://www.ohm-energie.com/) « Prix Réservé » (reçu le 6 nov. 2026) : offre à prix fixe 1 an à réserver maintenant, fourniture à partir d'avril-mai 2027, limitée à 20 000 clients. Non intégrée au comparateur (démarrage différé) : voir docs/OHM-PRIX-RESERVE.md. Affichée en mention hors classement depuis le 11 nov. 2026 (grille du 21 oct. 2026).

- [Urban Solar Energy](https://www.urbansolarenergy.fr/mentions-legales/) (prix fixe, autoconsommation) : pas de grille publique, tarifs par simulation. Documents : [CGV ≤ 36 kVA](https://www.urbansolarenergy.fr/wp-content/uploads/2026/07/CGV-inferieures-ou-egales-a-36kVA_01_06_2026.pdf), [conditions générales de septembre 2026](https://www.urbansolarenergy.fr/wp-content/uploads/2026/09/GC-01.09.2026.pdf).

- [Énergie d'ici](https://www.energiedici.fr/nos-offres-pour-les-particuliers.html) (électricité locale, hydroélectricité) : envoyer la fiche descriptive et le bulletin d'adhésion (voir docs/LIENS-RECUS.md).

- [Jeety Energy](https://jeety.energy/) (ex-Élecocité) : aucune grille publique ; tarifs à relever par simulation sur leur site.

- Entreprises locales de distribution (ES Strasbourg, UEM Metz, Gedia, Séolis, Synelva, Électricité de Provence, Enargia) : section régionale à prévoir.

### Limites connues du calcul

- Puissances de 3 à 36 kVA : les offres sans grille complète sont estimées (étoile). Le tarif réglementé de 12 à 36 kVA se ressaisit à la main à chaque changement (février, août) avec la grille EDF. Dès qu'un fournisseur donne sa grille, la saisir dans le champ abo de l'offre. Le prix du kWh à 7 et 8 kVA (Enercoop) et à 21 kVA (Dyneff) n'est pas distingué.

- Abonnement à 3 kVA de [OHM](https://www.ohm-energie.com/) et [Octopus](https://octopusenergy.fr/) : non exact.

- Filtres des offres (panneau latéral ; « Engagement » renommé « Durée du prix » le 13 nov., car aucune offre n'a de frais de résiliation et la durée est celle du prix garanti) : le type de prix est renseigné pour 24 offres sur 33 en électricité et 14 sur 25 en gaz (12 nov. 2026) ; la durée de blocage pour environ 8 offres en électricité et 5 en gaz ; l'offre verte pour 13 et 10. Une offre dont l'information manque disparaît quand le filtre correspondant est actif (la note sous le panneau indique combien sont masquées). À compléter avec la fiche descriptive de chaque offre (champs typ, eng et vert de data.json). Selectra publie un type de prix pour chaque offre, mais c'est une source secondaire : non reprise.

- Autres options des fournisseurs (à faire plus tard) : formules week-end, jours de pointe, voiture électrique.

## Gaz À faire, au fil de vos envois

- [Gaz de Bordeaux](https://www.gazdebordeaux.fr/) : fiches officielles de novembre 2026 reçues pour NovaFixe Gaz (Paris, Marseille, Evian, Bordeaux) et NovaFlex Gaz (6 communes) : le prix du kWh varie selon la commune (ex. NovaFixe, plus de 4 000 kWh : Bordeaux 0,1467 · Paris 0,1510 · Marseille 0,1540 · Evian 0,1590 €), voir docs/GDB-GAZ-NOV2026.md. Le site affiche la valeur de Paris en « À confirmer » ; il manque la table commune → zone pour passer en « Grille officielle ».

- [ENGIE](https://particuliers.engie.fr/) : Gaz Référence 3 ans en « Grille officielle du 01/11/2026 », par groupe A à H (docs/ENGIE-GAZ-ZONES.md). Le groupe est déduit de la commune (table Selectra) ; sans groupe, le site affiche le groupe B et « À confirmer ». Abonnement 360,79 €/an ; prix TTC du kWh (4 000 à 29 999 kWh) : A 0,14008 · B 0,14108 · C 0,14419 · D 0,14752 · E 0,15114 · F 0,15383 · G et H 0,15604 ; en dessous de 4 000 kWh : 152,46 €/an et 0,16983 €/kWh pour tous.

- [ilek](https://www.ilek.fr/grilles-tarifaires) : ÉnRFixe+ Gaz par zone A à K en « Grille officielle du 01/10/2026 » (prix TTC : 0,1633 à 0,1809 €/kWh en 4 à 335 MWh ; 0,1992 à 0,2090 en 0 à 4 MWh), zone déduite de la commune ; sans zone, zone C et « À confirmer ». À vérifier : la grille dit « disponible du 1er octobre au 1er novembre 2026 », voir si ilek en publie une de novembre.

- [Mint Énergie](https://www.mint-energie.com/) : grilles gaz Biogaz Online, Classic et Smart de novembre 2026 saisies. Elles sont mensuelles (indexées sur le prix repère + 5, 10 ou 15 %) : à ressaisir chaque mois avec les PDF du 1er du mois ; la saisie manuelle masque le calcul automatique de Biogaz Online. Électricité : grilles du 20 octobre 2026 saisies (kWh indexé à +10, +15 et +20 % sur le tarif réglementé, abonnement identique au tarif réglementé).

- [TotalEnergies](https://www.totalenergies.fr/particuliers) : gaz « Fixe 2 ans ».

- [Dyneff](https://www.dyneff-elec-gaz.fr/offres/contrat-gaz-vert/) : gaz 15 %, 55 % et 100 % renouvelable déjà intégrés, grilles du 1er octobre 2026 vérifiées (prix et abonnement identiques). Ces grilles sont publiées chaque mois (« fin de l'offre : fin du mois en cours ») : le suivi automatique repère chaque mois le nouveau PDF sur les pages gaz et électricité de Dyneff et le signale dans le rapport (sans rien appliquer) ; il reste à saisir les nouveaux prix.

- [GEG](https://www.geg.fr/) : non intégrés : Mon Offre Gaz Indexée (Grenoble et communes voisines seulement, prix mensuel), grilles locales Mont Gaz et Nov'Alp. GEG gaz : le prix du kWh est le même partout, l'abonnement dépend de la zone NTR (0-3, 4-7, 8-10) déduite de la commune.

- Limites du calcul : profil chauffage (B1) pour la comparaison ; les offres dont le seuil varie ([GEG](https://www.geg.fr/), [Plenitude](https://eniplenitude.fr/)) sont à surveiller ; les zones de distribution locales (Bordeaux, Strasbourg, Colmar) ne sont pas modélisées. Prix et abonnements Base et B0 réels pour les offres à grille officielle, estimés (étoile) pour les autres.

- Zone tarifaire : le site déduit maintenant la zone GRDF du code postal (fait le 7 nov., voir docs/ZONES-GAZ.md). Restent les découpages propres à chaque fournisseur, qui n'ont pas de table par commune (tableau ci-dessous, à vérifier sur les grilles officielles). Précision : ENGIE a 8 groupes A à H (et non 6 zones), ce qui corrige la ligne ENGIE du tableau.

| Fournisseur | Système de zones | Particularités |
|---|---|---|
| GRDF (référence) | 6 zones (1 à 6) | Système officiel de référence, base de toutes les autres grilles. |
| ENGIE | 6 zones (1 à 6) | Aligné sur GRDF historiquement, héritage du tarif réglementé. |
| TotalEnergies | 6 zones (modifié) | Reprend le système GRDF avec quelques reclassifications de communes. |
| Alterna | 6 zones (modifié) | Reprend GRDF avec des ajustements ponctuels selon les coûts d'approvisionnement. |
| ilek | 11 zones (A à K) | Système propre, plus fin, pour refléter les coûts d'achat du biogaz local. |
| Ekwateur | Aucune zone | Tarif national unique. |


 Source : [fournisseurs-electricite.com](https://www.fournisseurs-electricite.com/contrat-gaz/abonnement/zone-tarifaire) (second comparateur, octobre 2026), consultée le 29 oct. 2026. Source secondaire : les classifications de communes peuvent changer chaque année.

- Hausse du gaz de novembre : volontairement non affichée.

- Historique avant 2024 : piste [histo_TRV.pdf](https://www.gazdebordeaux.fr/sites/default/files/2024-12/histo_TRV.pdf) (anciens tarifs réglementés du gaz jusqu'en avril 2023) ; dates difficiles à relier aux valeurs, à comparer avec la CRE avant tout usage.

## Élec + Gaz (offres combinées) À faire

- Gaz de Bordeaux : conditions du NovaFixe Duo à obtenir. Le règlement du [Novafixe Bonus Duo](https://www.gazdebordeaux.fr/documents-contractuels) (100 € aussi) n'est pas reçu.

- Alterna : ses offres s'additionnent via la case « Ajouter les offres séparées » (mention « deux contrats, une seule facture, aucune remise connue à ce jour », 12 nov.).
- Gaz de Bordeaux Duo : la page officielle (12 nov.) décrit NovaFixe Biogaz + NovaFixe Élec, prix fixes 3 ans, avec 100 € TTC sur la facture d'électricité la première année pour le Bonus Duo ; aucun prix publié.
- Duos lus sur les pages officielles (1er nov. 2026) : ENGIE ([fiche](https://particuliers.engie.fr/content/dam/pdf/fiches-descriptives/fiche-descriptive-duo-reference-3-ans.pdf)), [ilek](https://www.ilek.fr/offre-dual), [Ekwateur](https://ekwateur.fr/fournisseur-elecricite-et-gaz/), [Mint](https://www.mint-energie.com/contrat-electricite/offre-classic-green/), [GEG](https://www.geg.fr/offre-de-marche/) et [Octopus](https://octopusenergy.fr/aide-faq/offres-tarifs/comprendre-nos-offres/souscrire-contrat-gaz) : aucun prix ni remise propre au duo, seulement la somme de deux offres. La remise de 48 € de Mint (2 € par mois et par énergie) vient d'un comparateur et n'est plus comptée. EDF (Zen Fixe + Avantage Gaz, Tarif Bleu + Avantage Gaz Optimisé) : site fermé aux robots, pages à recevoir en fichier.

- Offres duo retirées de l'onglet Élec + Gaz (31 oct. 2026) : [Alterna](https://www.alterna-energie.fr/offre-dual-gaz-electricite) (aucune offre combinée : deux contrats séparés, une seule facture) et TotalEnergies Fixe 2 ans Élec + Gaz ([offre fermée](https://www.totalenergies.fr/particuliers/electricite-et-gaz/offres-d-electricite-et-gaz/offre-fixe-2-ans-electricite-et-gaz)). Les offres individuelles restent dans les onglets Électricité et Gaz. ENGIE Duo référence 3 ans : la [fiche officielle](https://particuliers.engie.fr/content/dam/pdf/fiches-descriptives/fiche-descriptive-duo-reference-3-ans.pdf) montre deux grilles séparées, sans remise duo. EDF, Mint, Octopus, ilek, Ekwateur, GEG et OHM : page officielle à relever.

- Mention « Offre combinée non relevée » pour les fournisseurs sans duo relevé : proposée, non décidée.

- Les offres combinées ne sont relevées que pour 3, 6 et 9 kVA.

## Professionnels (onglet Pro, essai) À faire, au fil de vos envois

- ENGIE Pro : Référence Pro 1, 2 et 3 ans et Latitude 1 an (prix indexé sur le marché, qui change chaque mois : la valeur saisie est celle d'octobre) d'après les grilles d'octobre 2026, jusqu'à 36 kVA, hors taxes. À refaire quand ENGIE publie ses grilles de novembre. Le calcul n'inclut pas la réduction de 25 % de la première année (3 ans, jusqu'au 31 octobre 2026).

- Autres fournisseurs avec une grille Pro déjà repérée, à lire et saisir : [Enercoop](https://www.faq.enercoop.fr/hc/fr/articles/360024967152-Annexes-tarifaires) (offre « 2 saisons », 4 prix, non modélisée), [Énergie d'ici](https://www.energiedici.fr/nos-offres-pour-les-professionnels.html). Endesa ne propose que des offres professionnelles (à relever).

- [Gaz de Bordeaux](https://www.gazdebordeaux.fr/documents-contractuels) Pro : écarté pour l'instant. Ses CGV Pro (juillet 2026) et ses documents contractuels, lus le 30 oct. 2026, ne contiennent aucune grille : les prix sont établis par cotation envoyée au client. À reprendre si une grille publique apparaît.

- Hors taxes : l'accise, la CTA et la TVA ne sont pas comptées (le taux d'accise dépend de l'activité). À décider : les ajouter avec un choix « Mon activité », ou laisser le prix hors taxes.

- Puissances au-delà de 36 kVA (fiche ENGIE C4, grilles sur devis) : non traitées.

- Gaz professionnel : ENGIE Pro saisi (Activert Gaz 1, 2 et 3 ans, Latitude Gaz 1 an, consommation jusqu'à 300 MWh, grilles d'octobre 2026). Le prix dépend de la plage de consommation (P1, P2, P3) et d'un « niveau » de 1 à 6 pour les obligations, que l'utilisateur choisit à la main : à relier au code postal quand on aura la table des communes par niveau (zones GRDF). Le terme de débit normalisé lié au compteur (5,73 €/an par Nm³/h, au-delà de 40 Nm³/h) n'est pas compté. Les autres fournisseurs de gaz professionnel restent à relever.

## Eau À faire

- Chaque lundi : si les prix changent (par exemple quand SISPEA publie l'année 2026), la demande de fusion « eau » est maintenant fusionnée toute seule (depuis le 8 nov.), après les tests et les garde-fous du script. Rien à valider ; les lignes « À vérifier » restent dans le journal de l'exécution si vous voulez les relire.

- Historique : les variations de plus de 40 % en un an sont signalées sous la courbe (par exemple Antibes) ; reste à vérifier ces communes une à une. Les prix par année ne sont pas toujours comparables (couverture variable, 2025 moins complète).

- Communes sans prix : environ 8 700 communes n'ont aucun prix dans SISPEA ; le site le dit et utilise une moyenne indicative (région, ou nationale). À améliorer avec une autre source si elle apparaît.

- Abonnement estimé : pour environ 3 400 communes, médiane du département ; 99 € si le département n'a pas assez de données. Décider d'afficher aussi pour lui la mention « Données non communiquées… ».

- Corse et Provence-Alpes-Côte d'Azur : moyennes peu fiables, la moyenne nationale est utilisée à la place.

- Opérateurs (idée du 10 octobre 2026). Chaque commune a son service, géré par une régie ou par un opérateur (Veolia, Suez, Saur). Deux pistes : les 3 opérateurs les plus présents par région (aucune donnée sourcée trouvée ; sources possibles : rapport de la Fédération professionnelle des entreprises de l'eau, données SISPEA), et l'opérateur de chaque commune dans le tableau des prix (le plus utile, mais à relever commune par commune).

- Consommations par usage : les appareils et l'eau reposent sur des ordres de grandeur sans source précise.

## Parrainages À confirmer

- À confirmer sur le site du fournisseur : [Ekwateur](https://ekwateur.fr/) (montant du parrain absent du règlement), [Happ-e](https://www.happ-e.fr/) (20 € par contrat d'après Hellowatt : à confirmer sur la page de Happ-e), [LLUM](https://www.llum.fr/) et [ilek](https://www.ilek.fr/grilles-tarifaires) (une seule source).

- Tous les parrainages affichés sont confirmés par une page ou un règlement officiel ([EDF](https://particulier.edf.fr/) 20 € / 40 € jusqu'au 31 déc. 2026, [Alpiq](https://particuliers.alpiq.fr/parrainages) 15 € / 15 €, [Gaz de Bordeaux](https://www.gazdebordeaux.fr/) 20 € / 20 € sans date de fin : confirmés le 3 nov. 2026).

- Confirmés par une page ou un règlement officiel : [Octopus](https://octopusenergy.fr/) (grille du 1er août 2026), [Primeo](https://particuliers.primeo-energie.fr/), [ENGIE](https://particuliers.engie.fr/) (20 €, plus 5 € avec l'option verte) et [TotalEnergies](https://www.totalenergies.fr/particuliers) (20 €). Ces montants sont saisis à la main, car le script ne lit pas ces pages.

- Primes ponctuelles (20, 50, 60 €) : non comptées dans le classement. Parrainages en kWh ou en cartes cadeaux : non automatisés.

## Le site À faire

### Navigation et accueil (refonte du 10-11 nov. 2026)

- En-tête centré sur 3 lignes : interrupteur Particulier / Professionnel, nom du site, rubriques. Rubriques principales (particulier) : Accueil, Mon logement, Électricité, Gaz, Élec + Gaz, Eau, puis un menu « Plus » (Parrainages, Abonnement, Marché, Méthode, Sources, Statistiques, Mentions légales). Mode professionnel : Accueil, Offres pro (essai) et « Plus ».
- Accueil : code postal d'abord, promotions repliées sur une ligne (conditions au clic), « Comment ça marche » en 3 cases, notes sur les prix repliées.
- Tableaux électricité, gaz et duo : le repère (tarif réglementé ou prix repère CRE) est toujours en première ligne ; le bouton « Total par an » inverse l'ordre (▲ moins cher d'abord, ▼ l'inverse).
- Aperçu privé d'une maquette avant fusion : page publiée par Claude dans l'espace Claude (données de 5 départements seulement : 13, 33, 59, 69, 75). Une branche en PR marquée `ne-pas-fusionner` n'est pas fusionnée par l'auto-fusion.
- Offres à prix variable (OctoSaisons, Tempo, Zen Estival) : onglet Saisons supprimé le 13 nov. (PR 283), elles s'affichent dans l'onglet Électricité avec le filtre « Prix variable selon le jour ou l'heure » ; grilles et autres offres dans la section dépliante sous le tableau.
- Filtres en panneau : pas encore sur l'onglet Élec + Gaz ; à décider.
- Idée non faite : aperçu permanent dans un dossier /apercu/ du site GitHub (avec noindex).

- Filtres en panneau latéral à puces, style Selectra (fusionné le 11 nov., PR 273), sur Électricité et Gaz : type de prix, énergie verte, engagement, fiabilité (grille officielle), promotion, liste de fournisseurs, compteur « n offres sur N », réinitialisation ; sur mobile, bouton « Filtrer » qui ouvre le panneau. Pas encore sur Élec + Gaz. Non repris de Selectra : option tarifaire (déjà dans « Formule »), note client, Selectra Score.

### Comparaison avec Selectra (12 nov. 2026)
- Selectra (page « speciales=1 », enregistrée le 11 nov.) : 21 fournisseurs, 61 offres d'électricité (44 en option Base à Lyon sans les offres spéciales). Nous : 33 offres d'électricité (18 fournisseurs), 25 en gaz. Leur liste n'est lisible dans le fichier enregistré que si la page est chargée en entier (fichier de 10 Mo).
- Fournisseurs absents chez nous : Frank Énergie, Papernest Énergie, Sobry, Symphonics, Urban Solar Energy, La Bellenergie (6 offres), mylight150.
- Formules absentes de fournisseurs déjà présents : EDF (Zen Fixe, Zen Estival, Zen Week-End x3, Vert Électrique Week-End), TotalEnergies (Fixe 3 ans, Heures Eco, Heures Eco+, Spéciale), Octopus (Eco Fixe 2 ans, Eco Fixe Plus, Octopus Go, SolarPlus, SolarBoost), Enercoop (3 offres Flexibilité), ENGIE (Happy Week-end, Elec'Car 1 an), Gaz de Bordeaux (NovaFixe Bonus Élec dans la liste de Selectra), Dyneff (Contrat+ Verte), Happ-e (Option Vertelec), OHM (Week-End), Plenitude (Plenifix 1 an).
- Chez nous mais pas chez eux : Ekwateur, Mint, Alterna, Primeo Essentielle Verte.
- Méthode retenue : pour chaque offre, tu enregistres la page ou la grille du fournisseur (pas celle de Selectra, source secondaire), je vérifie les prix puis je saisis. Ordre proposé pour les prix fixes : EDF Zen Fixe, TotalEnergies Fixe 3 ans, Octopus Eco Fixe 2 ans, Plenitude Plenifix 1 an, Gaz de Bordeaux NovaFixe Bonus. Comparaison de prix possible avec leur réglage 5 360 kWh, 9 kVA, Base.
- EDF Tempo : la grille « Tarif Bleu » applicable au 1er août 2026 (reçue à nouveau le 12 nov.) est identique à nos prix (filtre « Prix variable » de l’onglet Électricité) ; le tarif réglementé ne change qu'en février et août, prochaine révision probable le 1er février 2027.

### Mises à jour automatiques

- Fusion des PR du robot (prix, eau) : le contrôle « tests » de la PR reste « en attente d'approbation » ; les workflows maj-prix et maj-eau l'approuvent maintenant avant de fusionner (10 nov.). Si une PR reste bloquée : approuver le run Tests en attente, puis fusionner.
- Auto-fusion (workflow « Auto-fusion », ajouté le 3 nov. 2026) : toute PR ouverte par Absinthe1975 ou par le robot de mise à jour des prix est fusionnée dès que les tests sont au vert, puis la publication Facebook est lancée. Pour empêcher une fusion : étiquette « ne-pas-fusionner » ou PR en brouillon. Les mises à jour de prix ne sont donc plus relues à la main : surveiller les posts Facebook et le rapport.

- Après chaque fusion : lancer « Run workflow » et lire le rapport (section « Liens fournisseur en échec », lignes [Mint](https://www.mint-energie.com/) et CRE, offres « À relire », premiers repères des PDF suivis). Quand un PDF suivi change, le rapport donne le prix du kWh lu par l'IA (avec citation vérifiée) à côté du nôtre, sans rien appliquer : vous saisissez ensuite la grille à la main.

- Facebook : quatre brouillons (parrainages EDF, Alpiq, Gaz de Bordeaux, eau) dans docs/FACEBOOK-BROUILLONS.md, à publier avec le workflow « Publication Facebook manuelle » (aperçu par défaut). Chaque fusion qui change un prix officiel publie un post sur la Page (le résultat est écrit dans l'annotation de l'exécution du workflow). À faire : un message pour l'eau (national, sans code postal), et renouveler le jeton de la Page, qui a transité par la conversation (à stocker uniquement dans le secret GitHub).

- Grilles saisies à la main : le fichier donnees/manuel/tarifs_manuels.json est fusionné avec les données automatiques. À y saisir, au fil des envois : les fournisseurs qui interdisent les robots (EDF, ilek). Mode d'emploi dans docs/LISEZMOI.md.

- Sources bloquées (relevé du 1er nov. 2026, à refaire de temps en temps) : EDF (particuliers et entreprises), ENGIE particuliers, ilek, Selectra et Kelwatt interdisent la lecture automatique (robots.txt) ; le catalogue des prestations d'Enedis et labellenergie.fr ne s'ouvrent pas depuis l'outil de travail. Pour ces sites, les grilles sont à envoyer en fichier (PDF ou page enregistrée) et à saisir à la main, avec l'étiquette « À confirmer » tant qu'il n'y a pas de grille officielle datée. Pages dont le prix n'est pas lisible par le programme : Alpiq (grille), GEG et TotalEnergies gaz (prix du kWh absent de la page). Fournisseurs relancés sans réponse : à recontacter par le service partenaires ou les réseaux sociaux.

- Conditions d'utilisation : le script respecte robots.txt et signale son nom, mais cela ne remplace pas la lecture des conditions de chaque site (à faire par vous).

### Mesure d'audience

- Lire la rubrique « Privacy policy » de [GoatCounter](https://www.goatcounter.com/) et vérifier qu'elle correspond aux Mentions légales (adresse IP non conservée, absence de cookie). Google Analytics (identifiant G-FKWB5WZJW6) est en suspens, retiré du site : son ancien code est dans l'historique (PR n° 99).

### Avant la mise en ligne

- Mentions légales : l'identité et le contact sont renseignés, l'adresse postale n'est pas publiée. Pour rester sans adresse publique, vérifier que votre identité figure sur votre compte GitHub (l'hébergeur) ; faire relire le texte par un juriste ou selon les guides de la CNIL ; le décrire à nouveau quand la mise à jour automatique des prix existera. L'adresse e-mail est visible de tous : elle peut recevoir du courrier indésirable, une adresse dédiée est possible.

- Site sans but lucratif : si des liens de parrainage rémunérés ou de la publicité sont ajoutés un jour, revoir les Mentions légales (rémunération, identité de l'éditeur, confidentialité).

- Hébergement GitHub Pages (choisi) : le dépôt doit être public avec le compte gratuit. Les conditions de GitHub excluent Pages pour une activité commerciale : sans but lucratif, ce n'est pas un obstacle, mais à relire si le site change de nature. Plus tard, un nom de domaine à soi.

### Rendre le comparateur plus juste

- Afficher la durée de blocage des prix fixes (le filtre fixe / indexé existe déjà).

- Historique des prix (onglet « Marché ») : remonter plus loin pour les offres des fournisseurs demande des archives de grilles (PDF datés) à fournir.

- Simuler la facture sur 12 mois plutôt qu'un total annuel à prix constant.

- Inclure les frais ponctuels (mise en service, déplacement) dans le total de la première année.

- Mode « DPE » en plus du mode réaliste, avec des valeurs conventionnelles sourcées, une fois le texte officiel de la méthode 3CL relevé.

- Graphique du détail des taxes : la barre actuelle sépare seulement consommation et abonnement. Taux relevés sur le BOFiP au 26 octobre 2026 : accise électricité 30,85 €/MWh (ménages, depuis le 1er février 2026), accise gaz naturel 10,73 €/MWh avant majoration. Il reste à vérifier la CTA et la TVA par poste, puis à décomposer chaque offre ; sans cela le graphique serait faux.

- Prix par code postal : un code postal regroupant des communes à prix différents reçoit la moyenne de ces communes (233 cas chez [Alterna](https://www.alterna-energie.fr/)).

### Accessibilité

- Test avec un vrai lecteur d'écran (NVDA, VoiceOver) : seul un humain avec ce logiciel peut le faire. Déjà vérifié automatiquement : ordre des titres, tableaux avec en-têtes, onglets, repères de page, libellés des champs, contrastes.

- **Relecture automatique** : avant chaque fusion automatique, `scripts/relecture.py` compare les données (prix non officiels > 15 % (un prix officiel sourcé est toujours accepté), offre retirée, « officielle » sans source…). Si elle signale quelque chose, la PR reçoit un commentaire et l'étiquette `ne-pas-fusionner`.
