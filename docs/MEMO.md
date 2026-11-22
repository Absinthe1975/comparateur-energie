<!-- Mémo retiré du site le 2 novembre 2026, conservé ici. Ne l'oublie pas : à relire avant chaque session. -->
# Mémo : ce qu'il reste à faire

Mémo du 14 novembre 2026. Il commence par une vue d'ensemble (à lire en premier), puis donne le détail fournisseur par fournisseur. Un sujet est abandonné définitivement : la lecture des factures (vie privée : le site ne demande, ne lit et ne conserve aucune facture ni donnée personnelle).

## Vue d'ensemble

### 1. Ce que je peux faire seul, sans rien de ta part
- Fins de promotions : le site masque tout seul une promotion après sa date de fin ([EDF « 80 ans »](https://particulier.edf.fr/fr/accueil/autres-pages/80ans-80euros.html) 15 nov., [Gaz de Bordeaux](https://ressources.gazdebordeaux.fr/DOCUMENTS/REGLEMENT/Reglement_novafixe_bonus_elec.pdf) 30 nov.). Il n'y a rien d'urgent à faire ; je supprime les lignes périmées de `data.json` dans un nettoyage de temps en temps ([ENGIE](https://particuliers.engie.fr/) retirée le 10 nov.). Les branches mortes du dépôt sont supprimées chaque dimanche par le flux « Nettoyage des anciennes branches ». 31 déc. : [Énergie d'ici](https://www.energiedici.fr/) (offre du bulletin valable jusqu'au 31 déc. 2026, à ressaisir avec la nouvelle grille) ; retirer la prime [OHM](https://www.ohm-energie.com/) / [EDF](https://particulier.edf.fr/) et la fin du parrainage EDF.

### 2. Ce qu'il me faut de toi (documents à m'envoyer)
Par ordre d'utilité. Un fichier enregistré (PDF ou .mhtml, Ctrl+S) suffit à chaque fois.

**À envoyer en priorité**
- **[ENGIE](https://particuliers.engie.fr/) électricité** : fait le 16 nov. : ta capture du simulateur ENGIE (6 kVA, Base, 2 104 kWh par an) donne 0,2403 € le kWh TTC et 186,98 € par an, ce qui confirme le prix du site à 6 kVA. Il reste « À confirmer » (c'est un simulateur, pas une grille publiée ; l'acheminement dépend du profil). Dès 9 kVA : 0,2420 € non confirmé ([Hello Watt](https://www.hellowatt.fr/) donne 0,2389 €). Liens : [simulateur ENGIE (page de souscription, ta capture)](https://particuliers.engie.fr/electricite-gaz.html), [prix Elec Référence 3 ans sur Selectra](https://www.fournisseurs-electricite.com/fournisseurs/engie/tarifs/elec-reference), [prix-elec.com](https://prix-elec.com/fournisseurs/engie/offres).
- **Comparateur officiel du médiateur de l'énergie** : pas de script automatique possible (le robots.txt de son interface, [api-comparateur-offres.energie-info.fr](https://api-comparateur-offres.energie-info.fr/robots.txt), interdit tout : « Disallow: / » ; celui du site, [comparateur-offres.energie-info.fr](https://comparateur-offres.energie-info.fr/), autorise tout, mais les offres viennent de l'interface). Seuls les fichiers que tu enregistres toi-même servent. Très utile pour vérifier les prix en Base. Sur la page reçue le 16 nov., 8 offres concordent avec le site (voir docs/LIENS-RECUS.md). Si tu veux plus de recoupements, refais la recherche en cliquant « Afficher plus de résultats » jusqu'au bout avant de sauvegarder (le fichier ne contient que 15 offres sur 50), puis une page pour le gaz et une pour chaque puissance (9 kVA, HP/HC).
- **Ekwateur, Mint, Alterna** : fermeture des souscriptions constatée sur leurs sites officiels le 20 nov. 2026 (tes captures) : Ekwateur « souscription momentanément indisponible » (pause des nouveaux contrats), Mint « les nouvelles souscriptions sont momentanément fermées » ([page de fermeture](https://souscription.mint-energie.com/Pages/Souscription/fermeture.aspx)), Alterna offres d'électricité « momentanément indisponibles à la souscription » (le gaz reste ouvert). Le site les garde hors classement ; Mint gaz est maintenant retiré aussi. À revérifier de temps en temps pour les rouvrir. Prix Ekwateur : aucune grille lisible chez les comparateurs, rien à envoyer pour l'instant.

**Pour compléter des fournisseurs**
- **[Enercoop](https://www.enercoop.fr/)** : une preuve que les nouvelles souscriptions sont suspendues (sa page d'accueil affiche encore « Je souscris », donc l'offre reste affichée).
- **[Octopus](https://octopusenergy.fr/)** : confirmer que l'offre saisonnière ([OctoSaisons](https://octopusenergy.fr/octosaisons)) suppose bien 55 % de la consommation en hiver et 7 % de jours rouges. Les plages d'heures creuses sont confirmées le 16 nov. par la page officielle d'Octopus ; ces deux parts (55 % et 7 %) sont des hypothèses du site, Octopus ne les publie pas.

**Offres à prix fixe manquantes** (la grille du fournisseur, pas celle de Selectra, une offre à la fois)
- [EDF Zen Fixe](https://particulier.edf.fr/fr/accueil/electricite-gaz/zen-fixe.html) (autres variantes), [Octopus Eco Fixe 2 ans](https://octopusenergy.fr/offre-electricite-tarifs), [Plenitude Plenifix 1 an](https://eniplenitude.fr/), [Gaz de Bordeaux NovaFixe Bonus](https://ressources.gazdebordeaux.fr/DOCUMENTS/REGLEMENT/Reglement_novafixe_bonus_elec.pdf).

**Fiches descriptives pour les filtres**
- Pour plusieurs offres, le type de prix, la durée de blocage et l'énergie verte manquent : elles disparaissent dès qu'on active le filtre correspondant (voir « Limites connues »).


### 3. Ce que tu dois trancher
- **[LLUM](https://www.llum.fr/) avec un Linky** : afficher une moyenne des prix par saison, ou seulement une mention.

### 4. Ce qu'il faut refaire régulièrement
- **Chaque mois (autour du 1er)** : [Dyneff](https://www.dyneff-elec-gaz.fr/) gaz (nouvelle grille mensuelle), [Mint](https://www.mint-energie.com/) gaz (Biogaz Online et Classic), [Octopus](https://octopusenergy.fr/) gaz Fixe, [Gaz de Bordeaux](https://www.gazdebordeaux.fr/) (fiches du mois : NovaFixe et NovaFlex, élec et gaz), [ENGIE](https://particuliers.engie.fr/) Pro Latitude (prix indexé). Le suivi automatique signale les nouveaux PDF dans son rapport ; c'est toi qui m'envoies les fichiers et moi qui saisis.
- **Février et août (changement du tarif réglementé)** : [EDF](https://particulier.edf.fr/) Tarif Bleu (grille 12 à 36 kVA), [Alpiq](https://particuliers.alpiq.fr/) (remise de 0,5 % sur le kWh HT), [Primeo](https://particuliers.primeo-energie.fr/), [Mint](https://www.mint-energie.com/), [Gaz de Bordeaux](https://www.gazdebordeaux.fr/) Novaflex, puis les grilles d'août de chaque fournisseur ([Octopus](https://octopusenergy.fr/), [LLUM](https://www.llum.fr/), [Enercoop](https://www.enercoop.fr/), [La Bellenergie](https://labellenergie.fr/), [GEG](https://www.geg.fr/), [Dyneff](https://www.dyneff-elec-gaz.fr/), [OHM](https://www.ohm-energie.com/)).
- **Quand un fournisseur change sa grille** : surtout [EDF](https://particulier.edf.fr/), [ilek](https://www.ilek.fr/), [GEG](https://www.geg.fr/), [ENGIE](https://particuliers.engie.fr/), [Dyneff](https://www.dyneff-elec-gaz.fr/), [Octopus](https://octopusenergy.fr/) (sites qui bloquent les robots, ou PDF que le programme ne sait pas lire) : tu m'envoies le fichier, je saisis, la PR est relue puis fusionnée automatiquement.
- **À chaque grille saisie** : lien dans docs/LIENS-RECUS.md, puis `python3 scripts/liens.py`.

### 5. Ce qui se fait tout seul
- Nettoyage des branches du dépôt : chaque dimanche (workflow « Nettoyage des anciennes branches »). Il garde main, les branches « sauvegarde… » et celles avec une demande de fusion ouverte ou modifiées depuis moins de 2 jours. Sauvegarde du site avant la refonte : branche `sauvegarde-2026-11-10`.
- Prix du tarif réglementé (CRE) et prix repère du gaz : mise à jour automatique du 1er au 10 de chaque mois, puis chaque lundi.
- Prix par code postal d'[Alterna](https://www.alterna-energie.fr/), historique des prix, vérification des liens fournisseur, eau (chaque lundi : une demande de fusion s'ouvre seulement si des prix changent).
- Relecture automatique des PR (écarts de prix des offres non officielles, offre retirée, source manquante), fusion automatique quand les tests sont au vert, post Facebook à chaque changement de prix officiel. Depuis le 7 nov., les mises à jour de prix du robot se fusionnent seules (plus d'approbation manuelle des tests) ; une PR bloquée porte l'étiquette « ne-pas-fusionner ».

### 6. Ce qui est déjà saisi d'après une grille officielle récente
- Électricité : [EDF](https://particulier.edf.fr/) (Tarif Bleu, Zen), [Octopus](https://octopusenergy.fr/) (Eco fixe, Intelligent), [OHM](https://www.ohm-energie.com/) (octobre), [Mint](https://www.mint-energie.com/), [Dyneff](https://www.dyneff-elec-gaz.fr/), [LLUM](https://www.llum.fr/) (compteur non communicant), [Enercoop](https://www.enercoop.fr/), [GEG](https://www.geg.fr/), [Gaz de Bordeaux](https://www.gazdebordeaux.fr/) (novembre), [Plenitude](https://eniplenitude.fr/), [Alterna](https://www.alterna-energie.fr/), [Alpiq](https://particuliers.alpiq.fr/), [La Bellenergie](https://labellenergie.fr/).
- Gaz : [Dyneff](https://www.dyneff-elec-gaz.fr/) (octobre), [Mint](https://www.mint-energie.com/) (novembre), [Octopus](https://octopusenergy.fr/) (novembre), [Alterna](https://www.alterna-energie.fr/), [GEG](https://www.geg.fr/).
- Électricité [TotalEnergies](https://www.totalenergies.fr/particuliers) « Fixe 2 ans » : ajoutée le 12 nov. (grille officielle du 24 sept. 2026, Base 0,2270 € de 3 à 6 kVA et 0,2252 € dès 7 kVA, heures pleines / creuses 0,2435 / 0,1791 €, page de souscription ouverte le 12 nov. ; [Hello Watt](https://www.hellowatt.fr/) donne les mêmes prix, mis à jour le 6 nov.). Le titre de la page (« -17 % vs TRV ») est périmé : au prix de la grille, l'offre est plus chère que le tarif réglementé.
- Gaz [TotalEnergies](https://www.totalenergies.fr/particuliers) « Fixe 2 ans » : fait le 10 nov. (grille du 24 sept., prix par zone 1 à 6, zone déduite de la commune), reconfirmé le 12 nov. avec la grille et la page de souscription.
- Zones de gaz par code postal : fait. Zones GRDF (7 nov.), puis zones propres aux fournisseurs pour 9 461 communes dont Paris, Lyon, Marseille et Strasbourg (9-10 nov., source secondaire observatoires.net / [Selectra](https://selectra.info/), voir docs/ZONES-GAZ.md). Prix par zone branchés : [ENGIE](https://particuliers.engie.fr/) (groupes A à H), [ilek](https://www.ilek.fr/) (zones A à K), [TotalEnergies](https://www.totalenergies.fr/particuliers) (zones 1 à 6), [GEG](https://www.geg.fr/) (abonnement par zone NTR) ; par zone GRDF : [EDF](https://particulier.edf.fr/), [OHM](https://www.ohm-energie.com/), [Octopus](https://octopusenergy.fr/), [Mint](https://www.mint-energie.com/), [Happ-e](https://www.happ-e.fr/) ; [Alterna](https://www.alterna-energie.fr/) par code postal. [Dyneff](https://www.dyneff-elec-gaz.fr/), [Plenitude](https://eniplenitude.fr/), [Ekwateur](https://ekwateur.fr/) n'ont pas de prix par zone. Rapprochement des communes terminé le 19 nov. : 9 486 communes (contre 9 461), les 17 restantes sont d'anciennes communes fusionnées dans une commune nouvelle déjà couverte (Seynod et Pringy dans Annecy, par exemple), donc sans zone à ajouter.
- [GEG](https://www.geg.fr/) : fiches descriptives de novembre 2026 (Elec Verte, Direct Producteur, Gaz, Biogaz, Gaz Indexée, Tarif Bleu) reçues le 13 nov. : aucune donnée à corriger ; « L'Offre Online » n'existe plus.
- Fait ces derniers jours : nettoyage des demandes de fusion terminé le 22 nov. (275 descriptions nettoyées sur 332 ; plus aucune mention de l'outil d'IA dans les demandes de fusion, les commits ni les contributeurs ; jeton supprimé par toi) ; le script reste dans `outils/nettoyer_pr_local.py` au cas où ; test de bout en bout rendu plus tolérant (attentes sur condition au lieu de durées fixes, marge de 2 px, second essai complet avant de signaler un échec) le 22 nov. ; onglet Pro : choix « Prix affichés » (hors taxes par défaut, ou toutes taxes comprises : accise 0,03085 €/kWh, CTA 15 % de la part fixe du réseau, TVA 20 %, d'après [EDF](https://www.edf.fr/collectivites/decryptages/normes-et-reglementations/evolution-des-taxes-et-contributions-appliquees-sur-l-electricite-au-1er-fevrier-2026) du 1er févr. 2026) pour l'électricité, le gaz reste hors taxes (22 nov.) ; [Primeo](https://particuliers.primeo-energie.fr/) Essentielle Verte (grille officielle du 14 sept. 2026, base et heures pleines / creuses : kWh HT à 95 % du tarif réglementé) et Fixe Sereine (grille officielle du 4 nov. 2026, prix bloqués jusqu'au 31 juil. 2029, sans engagement) saisies le 22 nov. ; robots.txt vus le 22 nov. : aucune interdiction sur les pages de prix ; le parrainage de 15 € est confirmé par le règlement ; l'opération « Hiver Serein » (prime de 10 à 50 € TTC si la consommation baisse d'au moins 10 % entre nov. 2026 et mars 2027, réservée aux clients prévenus par courriel et déjà clients avant le 1er nov. 2025) n'est pas affichée : elle ne concerne pas les nouveaux clients ; [Gaz de Bordeaux](https://www.gazdebordeaux.fr/) : fiches NovaFlex des zones 4 à 6 (Gap, Aurillac, Chamonix) et règlement du Bonus reçus le 22 nov., vérifiés (0,2010 € jusqu'à 4 000 kWh partout ; abonnements inchangés) ; suspensions d'Ekwateur, Mint (gaz compris) et Alterna (électricité) confirmées sur leurs sites officiels le 20 nov. (note du site : « Constaté sur les sites officiels ») ; La Bellenergie « avec Producteur EnR » (option [VertVolt](https://labellenergie.fr/vertvolt-lelectricite-verte-dont-vous-connaissez-le-producteur/), +0,01 € TTC le kWh sur Prudence, Constance et Garance, Base et heures pleines / creuses) saisie le 19 nov. en « À confirmer » : prix calculé, identique à Selectra (0,2085 € à 9 kVA) ; zones de gaz par commune rapprochées le 19 nov. (lecture de la ligne 5 de La Poste + 11 rapprochements à la main, +25 communes, une zone GRDF corrigée : Sarreguemines passe de 3 à 1) ; [TotalEnergies](https://www.totalenergies.fr/particuliers) « Spéciale » (électricité Base et heures pleines / creuses, gaz zones 1 à 6) saisie le 18 nov. en « À confirmer » : la grille officielle du 1er nov. donne le prix avant la remise de 10 % sur le kWh HT (3 ans), le site applique la remise lui-même, taxes de la grille conservées ; remplace l'ancienne ligne « Access » ; « Heures Eco+ » (fiche et grille du 1er nov. reçues) non saisie : 20 jours Éclair à 0,6375 € le kWh (7 h à 15 h et 18 h à 20 h), impossible à chiffrer honnêtement sans profil d'usage ; TotalEnergies « Fixe 3 ans » (électricité Base et heures pleines / creuses, gaz zones 1 à 6, grille officielle du 26 oct. 2026) saisie le 18 nov. et marquée « Vraie offre duo » (une seule offre, une seule fiche, aucune remise duo) ; l'offre « Fixe 2 ans » duo est fermée sur le site de TotalEnergies ; [ENGIE](https://particuliers.engie.fr/) : 200 € TTC offerts sur le Duo Référence 3 ans du 16 nov. au 20 déc. (promotion affichée, non déduite, décision du 18 nov.) ; onglet Élec + Gaz refait le 17 nov. : plus de lignes « duo » saisies à la main (aucune offre duo ne porte de prix ni de remise propre sur les pages officielles lues) ; le tableau additionne la meilleure offre d'électricité et la meilleure offre de gaz de chaque fournisseur, à toutes les puissances, et la case est supprimée tant qu'aucune vraie offre duo n'existe (s'il y en a une, elle s'ajoute dans la liste « duo » de donnees/data.json) ; [Ekwateur](https://ekwateur.fr/), [Mint](https://www.mint-energie.com/) (électricité) et [Alterna](https://www.alterna-energie.fr/) (électricité) sortis du classement car leurs souscriptions sont suspendues (15 nov., source presse, « À confirmer », encadré affiché sous les tableaux) ; ENGIE Elec'Car 1 an (heures pleines / creuses, véhicule électrique, grille d'août 2026) et Elec Happy Week-end 3 ans (grille de novembre 2026, dans le filtre « Prix variable », part du week-end supposée à 31,5 %) saisis le 15 nov. ; la fiche Elec Référence 3 ans reçue est encore celle d'août 2026 : rien de nouveau pour le prix du kWh à trancher ; Urban Solar Energy « Essentielle SMB » (clients sans centrale photovoltaïque, prix fixe, 100 % renouvelable, grille du 1er août 2026) ajoutée le 14 nov. (offres avec centrale et stockage virtuel, et offres professionnelles, non saisies) ; [Énergie d'ici](https://www.energiedici.fr/) « Energie Bleue » (option Base) ajoutée le 14 nov. dans le filtre « Prix variable » (prix par saison et plage horaire, offre valable jusqu'au 31 déc. 2026) avec son parrainage 20 € / 20 € ; l'option heures creuses (MU 4) ajoutée le 16 nov. ; Sobry relevé sans calcul (prix du marché heure par heure) ; mylight150 (Vert France, prix de bienvenue 12 mois, foyers équipés de panneaux solaires) et Symphonics (-50 % heures creuses, Linky niveau 2 et équipement pilotable) ajoutés le 14 nov. d'après leurs grilles officielles (autres offres Symphonics : flexibilité, achat de surplus : pas de grille reçue) ; [La Bellenergie](https://labellenergie.fr/), grille du 1er nov. 2026 saisie (14 nov.) ; mode sombre et clavier du menu vérifiés (11 nov.) ; [OHM](https://www.ohm-energie.com/) « Prix Réservé » en mention hors classement jusqu'au 31 mai 2027 (11 nov.) ; Alterna additionnée en Élec + Gaz avec la mention « deux contrats, une seule facture, aucune remise connue à ce jour » (12 nov.).
- Encore « À confirmer » : [ENGIE](https://particuliers.engie.fr/) (élec), [Ekwateur](https://ekwateur.fr/), [Gaz de Bordeaux](https://www.gazdebordeaux.fr/) gaz (zone de Paris).
- Parrainages : confirmés par une page officielle, sauf [Ekwateur](https://ekwateur.fr/), [Happ-e](https://www.happ-e.fr/) et [ilek](https://www.ilek.fr/) ; [Plenitude](https://eniplenitude.fr/) n'a aucun programme.

## Détail par sujet

## Électricité À faire, au fil de vos envois

### Grilles à saisir ou à confirmer, fournisseur par fournisseur

- [Gaz de Bordeaux](https://www.gazdebordeaux.fr/) : NovaFixe Élec est saisie (fiche officielle de novembre 2026 relevée pour Onnaing, Lille, Paris 1er, Marseille 01 et Moissac, toutes identiques : Base 0,1919 / 0,19042 €, heures pleines / creuses 0,20536 / 0,1528 € ; abonnements inchangés ; les grilles d'octobre étaient identiques dans 6 villes, à vérifier pour novembre dans une autre ville). Novaflex Élec (indexée, 2 % sous le tarif réglementé, 2 ans) est saisie d'après la fiche officielle de novembre 2026 (Base 0,1968 / 0,19526 €, heures pleines / creuses 0,21067 / 0,15646 €, relevée pour Onnaing seulement). La grille du NovaFixe Bonus Élec est identique à celle du NovaFixe Élec. [Gaz de Bordeaux](https://www.gazdebordeaux.fr/) édite ses fiches par commune : NovaFixe novembre est identique dans 5 villes ; Novaflex à vérifier dans une autre ville. Règlement du Bonus Élec lu le 12 nov. 2026 (souscription du 1er oct. au 30 nov. ; remise étalée sur 12 mois pour les mensualisés, sinon déduite de la facture suivant le 11e mois ; perdue en cas de résiliation ou de changement d'offre). Le bonus de 100 € de l'offre Bonus Élec suit son [règlement](https://ressources.gazdebordeaux.fr/DOCUMENTS/REGLEMENT/Reglement_novafixe_bonus_elec.pdf) (souscription jusqu'au 30 novembre 2026) : il s'affiche sous l'offre, hors classement. Ensuite, supprimer sa ligne dans la rubrique « promos » de donnees/data.json.

- [ENGIE](https://particuliers.engie.fr/) : Elec Référence 3 ans à confirmer : prix de novembre 2026 relevés sur [Selectra](https://selectra.info/) (grille du 30 oct. 2026, TTC : base 0,2403 € de 3 à 6 kVA et 0,2420 € dès 9 kVA ; heures pleines 0,2561 €, creuses 0,2023 € ; abonnement 186,98 € par an à 6 kVA), source secondaire. La fiche descriptive officielle d'octobre 2026 est reçue : elle donne fourniture, acheminement et obligations séparément. L'abonnement de 186,98 € à 6 kVA se retrouve exactement (fourniture 45,79 € + acheminement à 4 plages 141,19 €). Contrôle du 2 nov. 2026 avec la fiche (accise 0,0367 € TTC, obligations 0,0184 € à 6 kVA et 0,0201 € dès 9 kVA, acheminement à 4 plages de 0,0144 à 0,0926 €) : la base de Selectra (0,2403 et 0,2420 €) est compatible, et son écart de 0,0017 € entre 6 et 9 kVA correspond exactement aux obligations. En revanche le prix en heures creuses de Selectra (0,2023 €) est inférieur au minimum que permet la fiche (0,2146 €) : il n'est plus affiché. Pour passer l'offre en « Grille officielle », il faut le prix total d'[ENGIE](https://particuliers.engie.fr/) (simulateur ou courrier) ou la formule d'acheminement du client. Promotion de deux mois d'abonnement offerts, jusqu'au 7 novembre 2026 : affichée sous les offres ENGIE, hors classement ; supprimer sa ligne dans « promos » après cette date. Page de promotions ENGIE du 28 octobre 2026 lue : elle confirme cette promotion (souscription du 19 octobre au 7 novembre inclus, Elec, Gaz ou Duo Référence 3 ans, ou Happy Week-End) et décrit la « Promo d'été » (50 % de l'électricité consommée de 13 h à 17 h en cagnotte), notée dans l'onglet Saisons.

- [LLUM](https://www.llum.fr/) : grille officielle d'août 2026 lue. Compteur non communicant : Base 0,19 €/kWh et HP/HC 0,2071 / 0,1540 € (modélisés, officiels). Avec un Linky, [LLUM](https://www.llum.fr/) applique une grille par saison et heures pleines / creuses (Base : 0,22276 € en HP hiver, 0,15064 € en HC été), non modélisée. À décider : modéliser une moyenne, ou afficher une mention.

- [Alpiq](https://particuliers.alpiq.fr/) (Sérénité) : prix indexé (remise de 0,5 % sur le kWh HT du tarif réglementé) : à resaisir à chaque changement du tarif réglementé (février, août), avec la grille PDF d'[Alpiq](https://particuliers.alpiq.fr/).

- [Octopus](https://octopusenergy.fr/) : « Cocon fixe » est le nom du contrat (fiche descriptive de juillet 2026) de l'offre vendue sous le nom « OctoEco Fixe » (« Eco fixe » dans ses grilles) : la page officielle des tarifs relie bien ces trois noms, confirmé le 4 nov. 2026. Eco fixe Base (grille du 12 août 2026) vérifiée : conforme. Gaz Fixe : grille mensuelle de novembre 2026 (applicable au 30 oct.) saisie, à ressaisir chaque mois. Intelligent [Octopus](https://octopusenergy.fr/) Fixe : grille officielle du 1er août 2026 vérifiée (0,1968 € jusqu'à 8 kVA, 0,1953 € au-delà), passée en « Grille officielle ». Pour l'offre saisonnière, le prix moyen suppose 58 % de la consommation en hiver : à confirmer ou corriger. OctoSaisons (ex-OctoTempo, renommée le 21 octobre 2026) : grille officielle du 1er août 2026 reçue (docs/OCTOSAISONS-GRILLE.md) et calculée dans l’onglet Électricité (filtre « Prix variable selon le jour ou l’heure »), avec [EDF](https://particulier.edf.fr/) Tempo et Zen Estival, à partir de vos usages (profil horaire supposé par le site, hors classement général). Les plages d'heures creuses d'OctoSaisons (21 h à 7 h, plus 11 h à 17 h l'été) viennent d'un article de presse et ne figurent pas dans la fiche officielle : à confirmer auprès d'Octopus. Hypothèses des saisons à valider (7 % de jours rouges, 55 % en hiver) ; puis décider d'intégrer ces offres au classement si d'autres fournisseurs adoptent ce principe.

- [Ekwateur](https://ekwateur.fr/) : le prix n'apparaît qu'à la souscription (code postal demandé), sans grille publique. Règle du 15 nov. : se fier aux comparateurs quand au moins deux donnent les mêmes prix (voir « Ce qu'il me faut de toi »).


- [Enercoop](https://www.faq.enercoop.fr/hc/fr/articles/360024967152-Annexes-tarifaires) : grille du 1er août 2026 intégrée (Base et Flexibilité heures creuses). Non modélisées : Nuit & week-end, 2 saisons, jours de pointe (plages horaires et saisons propres à [Enercoop](https://www.enercoop.fr/)). Sa suspension d'accueil, annoncée dans des données sans source datée, n'est pas confirmée par ses pages officielles : à vérifier avant de le retirer.

- [ilek](https://www.ilek.fr/grilles-tarifaires) : ses PDF sont sur un domaine qui interdit les robots : à relire à la main à chaque changement de grille.

- [EDF](https://particulier.edf.fr/) : Zen Estival : grille officielle reçue (15 sept. 2026) et calculée dans l’onglet Électricité (filtre « Prix variable selon le jour ou l’heure ») avec la répartition de consommation publiée par [EDF](https://particulier.edf.fr/) (exemple à 3,6 MWh par an sans chauffage électrique), car les plages d'hiver ne figurent pas dans les documents reçus ; elle n'apparaît pas pour un chauffage électrique. Le site interdit les robots (robots.txt) : ses 12 grilles PDF et ses pages de prix restent saisies à la main à chaque changement. Le tarif réglementé, lui, vient de la CRE.

- [GEG](https://www.geg.fr/) : le script prend le PDF le plus récent de la [page des tarifs](https://www.geg.fr/aide-et-contact/centre-documentation/particulier/tarifs/). « L'Offre Online » n'apparaît plus dans les offres de [GEG](https://www.geg.fr/) (pages et tarifs officiels du 12 nov. 2026) : plus rien à envoyer. Offres actuelles : Elec Verte et Direct Producteur (fixes 3 ans), Gaz et Biogaz (fixes 3 ans), Gaz Indexée (Grenoble seulement), Tarif Bleu (réglementé, Grenoble et communes voisines). Fiches descriptives reçues le 12 nov. : type de prix, 3 ans, énergie verte et biogaz confirmés (déjà saisis) ; GEG écrit que toutes ses offres de marché sont « sans engagement ».

### Heures pleines / creuses

- Le choix « Formule » apparaît dans l'onglet Électricité dès qu'une offre a ses prix. Déjà saisis : [Dyneff](https://www.dyneff-elec-gaz.fr/), [La Bellenergie](https://labellenergie.fr/), [Gaz de Bordeaux](https://www.gazdebordeaux.fr/), [Enercoop](https://www.enercoop.fr/), [ilek](https://www.ilek.fr/), [EDF](https://particulier.edf.fr/) Zen Fixe, [Alpiq](https://particuliers.alpiq.fr/), [Mint](https://www.mint-energie.com/), [GEG](https://www.geg.fr/), [LLUM](https://www.llum.fr/) (compteur non communicant) et [OHM](https://www.ohm-energie.com/) (1, 2 et 3 ans) (Elec Verte et Direct Producteur, grille du 5 oct. 2026, prix des 6 et 9 kVA).

- À saisir dans la rubrique hphc de donnees/manuel/tarifs_manuels.json (champs hp et hc en €/kWh TTC, abo par puissance) : [LLUM](https://www.llum.fr/) ([GEG](https://www.geg.fr/) est fait). Je ne peux pas lire ces PDF d'ici : envoyez les chiffres ou les fichiers.

### Fournisseurs à ajouter ou à compléter (état au 14 novembre 2026)
- [OHM](https://www.ohm-energie.com/) : fiches officielles d'octobre 2026 saisies pour Sérénité 1 an (0,2212 €/kWh Base dès 6 kVA, 0,2001 € à 3-5 kVA non distingué), 2 ans (0,2249 €) et Premi'Ohm 3 ans (0,2287 €), avec heures pleines / creuses. Non modélisée : l'offre Week-end (fiche du 4 sept. 2026 : semaine heures pleines 0,265 € / creuses 0,1737 €, week-end 0,1737 €).
- [OHM](https://www.ohm-energie.com/) « Prix Réservé » (reçu le 6 nov. 2026) : offre à prix fixe 1 an à réserver maintenant, fourniture à partir d'avril-mai 2027, limitée à 20 000 clients. Non intégrée au comparateur (démarrage différé) : voir docs/OHM-PRIX-RESERVE.md. Affichée en mention hors classement depuis le 11 nov. 2026 (grille du 21 oct. 2026).

- Urban Solar Energy : offre « Essentielle SMB » saisie le 14 nov. ; non saisies : offres avec centrale photovoltaïque et stockage virtuel (clients équipés) et offres professionnelles.

- [Énergie d'ici](https://www.energiedici.fr/nos-offres-pour-les-particuliers.html) : Energie Bleue (Base) saisie le 14 nov. ; l'option heures creuses (MU 4) est saisie le 16 nov. ; reste le bulletin PLMO (deux communes des Côtes-d'Armor) et l'offre Riverains de Libaros ; offre du bulletin valable jusqu'au 31 déc. 2026.


- Entreprises locales de distribution (ES Strasbourg, UEM Metz, Gedia, Séolis, Synelva, Électricité de Provence, Enargia) : section régionale à prévoir.

### Limites connues du calcul

- Puissances de 3 à 36 kVA : les offres sans grille complète sont estimées (étoile). Le tarif réglementé de 12 à 36 kVA se ressaisit à la main à chaque changement (février, août) avec la grille [EDF](https://particulier.edf.fr/). Dès qu'un fournisseur donne sa grille, la saisir dans le champ abo de l'offre. Le prix du kWh à 7 et 8 kVA ([Enercoop](https://www.enercoop.fr/)) et à 21 kVA ([Dyneff](https://www.dyneff-elec-gaz.fr/)) n'est pas distingué.

- Abonnement à 3 kVA de [OHM](https://www.ohm-energie.com/) et [Octopus](https://octopusenergy.fr/) : non exact.

- Filtres des offres (panneau latéral ; « Engagement » renommé « Durée du prix » le 13 nov., car aucune offre n'a de frais de résiliation et la durée est celle du prix garanti) : le type de prix est renseigné pour 28 offres sur 37 en électricité et 14 sur 25 en gaz (14 nov. 2026) ; la durée de blocage pour 10 offres en électricité et 5 en gaz ; l'offre verte pour 16 et 10. Une offre dont l'information manque disparaît quand le filtre correspondant est actif (la note sous le panneau indique combien sont masquées). À compléter avec la fiche descriptive de chaque offre (champs typ, eng et vert de data.json). [Selectra](https://selectra.info/) publie un type de prix pour chaque offre, mais c'est une source secondaire : non reprise.

- Autres options des fournisseurs (à faire plus tard) : formules week-end, jours de pointe, voiture électrique.

## Gaz À faire, au fil de vos envois

- [Gaz de Bordeaux](https://www.gazdebordeaux.fr/) : fiches officielles de novembre 2026 reçues pour NovaFixe Gaz (Paris, Marseille, Evian, Bordeaux) et NovaFlex Gaz (9 communes, dont Gap, Aurillac et Chamonix reçues le 22 nov. pour les zones 4, 5 et 6 : plus de 4 000 kWh à 0,1613 · 0,1620 · 0,1627 €) : le prix du kWh varie selon la commune (ex. NovaFixe, plus de 4 000 kWh : Bordeaux 0,1467 · Paris 0,1510 · Marseille 0,1540 · Evian 0,1590 €), voir docs/GDB-GAZ-NOV2026.md. Le site affiche la valeur de Paris en « À confirmer » ; il manque la table commune → zone pour passer en « Grille officielle ».

- [ENGIE](https://particuliers.engie.fr/) : Gaz Référence 3 ans en « Grille officielle du 01/11/2026 », par groupe A à H (docs/ENGIE-GAZ-ZONES.md). Le groupe est déduit de la commune (table [Selectra](https://selectra.info/)) ; sans groupe, le site affiche le groupe B et « À confirmer ». Abonnement 360,79 €/an ; prix TTC du kWh (4 000 à 29 999 kWh) : A 0,14008 · B 0,14108 · C 0,14419 · D 0,14752 · E 0,15114 · F 0,15383 · G et H 0,15604 ; en dessous de 4 000 kWh : 152,46 €/an et 0,16983 €/kWh pour tous.

- [ilek](https://www.ilek.fr/grilles-tarifaires) : ÉnRFixe+ Gaz par zone A à K en « Grille officielle du 01/10/2026 » (prix TTC : 0,1633 à 0,1809 €/kWh en 4 à 335 MWh ; 0,1992 à 0,2090 en 0 à 4 MWh), zone déduite de la commune ; sans zone, zone C et « À confirmer ». À vérifier : la grille dit « disponible du 1er octobre au 1er novembre 2026 », voir si [ilek](https://www.ilek.fr/) en publie une de novembre.

- [Mint Énergie](https://www.mint-energie.com/) : grilles gaz Biogaz Online, Classic et Smart de novembre 2026 saisies. Elles sont mensuelles (indexées sur le prix repère + 5, 10 ou 15 %) : à ressaisir chaque mois avec les PDF du 1er du mois ; la saisie manuelle masque le calcul automatique de Biogaz Online. Électricité : grilles du 20 octobre 2026 saisies (kWh indexé à +10, +15 et +20 % sur le tarif réglementé, abonnement identique au tarif réglementé).

- [TotalEnergies](https://www.totalenergies.fr/particuliers) : gaz « Fixe 2 ans ».

- [Dyneff](https://www.dyneff-elec-gaz.fr/offres/contrat-gaz-vert/) : gaz 15 %, 55 % et 100 % renouvelable déjà intégrés, grilles du 1er octobre 2026 vérifiées (prix et abonnement identiques). Ces grilles sont publiées chaque mois (« fin de l'offre : fin du mois en cours ») : le suivi automatique repère chaque mois le nouveau PDF sur les pages gaz et électricité de [Dyneff](https://www.dyneff-elec-gaz.fr/) et le signale dans le rapport (sans rien appliquer) ; il reste à saisir les nouveaux prix.

- [GEG](https://www.geg.fr/) : non intégrés : Mon Offre Gaz Indexée (Grenoble et communes voisines seulement, prix mensuel), grilles locales Mont Gaz et Nov'Alp. [GEG](https://www.geg.fr/) gaz : le prix du kWh est le même partout, l'abonnement dépend de la zone NTR (0-3, 4-7, 8-10) déduite de la commune.

- Limites du calcul : profil chauffage (B1) pour la comparaison ; les offres dont le seuil varie ([GEG](https://www.geg.fr/), [Plenitude](https://eniplenitude.fr/)) sont à surveiller ; les zones de distribution locales (Bordeaux, Strasbourg, Colmar) ne sont pas modélisées. Prix et abonnements Base et B0 réels pour les offres à grille officielle, estimés (étoile) pour les autres.

- Zone tarifaire : le site déduit maintenant la zone GRDF du code postal (fait le 7 nov., voir docs/ZONES-GAZ.md). Restent les découpages propres à chaque fournisseur, qui n'ont pas de table par commune (tableau ci-dessous, à vérifier sur les grilles officielles). Précision : [ENGIE](https://particuliers.engie.fr/) a 8 groupes A à H (et non 6 zones), ce qui corrige la ligne ENGIE du tableau.

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

- [Gaz de Bordeaux](https://www.gazdebordeaux.fr/) : pages NovaFixe Duo et Bonus Duo reçues le 18 nov. (le bonus de 100 € TTC vaut aussi pour l'électricité seule). Le règlement du Bonus Duo est le même PDF que celui de l'électricité (la page du Bonus Duo y renvoie) : 100 € TTC du 1er oct. au 30 nov. 2026, remise au 11e mois, perdue en cas de résiliation avant. Rien ne manque.

- [Alterna](https://www.alterna-energie.fr/) : ses offres s'additionnent via la case « Ajouter les offres séparées » (mention « deux contrats, une seule facture, aucune remise connue à ce jour », 12 nov.).
- [Gaz de Bordeaux](https://www.gazdebordeaux.fr/) Duo : la page officielle (12 nov.) décrit NovaFixe Biogaz + NovaFixe Élec, prix fixes 3 ans, avec 100 € TTC sur la facture d'électricité la première année pour le Bonus Duo ; aucun prix publié.
- Duos lus sur les pages officielles (1er nov. 2026) : [EDF](https://particulier.edf.fr/fr/accueil/fournisseur-electricite-gaz.html) (page reçue le 17 nov. : 10 offres d'électricité et 2 de gaz, aucune offre duo ni remise combinée, seulement « une seule facture » : les deux lignes [EDF](https://particulier.edf.fr/) de l'onglet Élec + Gaz restent la somme de deux offres, avec cette mention), [ENGIE](https://particuliers.engie.fr/) ([fiche](https://particuliers.engie.fr/content/dam/pdf/fiches-descriptives/fiche-descriptive-duo-reference-3-ans.pdf)), [ilek](https://www.ilek.fr/offre-dual), [Ekwateur](https://ekwateur.fr/fournisseur-elecricite-et-gaz/), [Mint](https://www.mint-energie.com/contrat-electricite/offre-classic-green/), [GEG](https://www.geg.fr/offre-de-marche/) et [Octopus](https://octopusenergy.fr/aide-faq/offres-tarifs/comprendre-nos-offres/souscrire-contrat-gaz) : aucun prix ni remise propre au duo, seulement la somme de deux offres. La remise de 48 € de [Mint](https://www.mint-energie.com/) (2 € par mois et par énergie) vient d'un comparateur et n'est plus comptée. EDF (Zen Fixe + Avantage Gaz, Tarif Bleu + Avantage Gaz Optimisé) : site fermé aux robots, pages à recevoir en fichier.

- Offres duo retirées de l'onglet Élec + Gaz (31 oct. 2026) : [Alterna](https://www.alterna-energie.fr/offre-dual-gaz-electricite) (aucune offre combinée : deux contrats séparés, une seule facture) et [TotalEnergies](https://www.totalenergies.fr/particuliers) Fixe 2 ans Élec + Gaz ([offre fermée](https://www.totalenergies.fr/particuliers/electricite-et-gaz/offres-d-electricite-et-gaz/offre-fixe-2-ans-electricite-et-gaz)). Les offres individuelles restent dans les onglets Électricité et Gaz. [ENGIE](https://particuliers.engie.fr/) Duo référence 3 ans : **200 € TTC offerts du 16 nov. au 20 déc. 2026** (100 € pour une seule énergie, pages reçues le 17 nov. ; promotion affichée, non comptée dans le classement) ; la [fiche officielle](https://particuliers.engie.fr/content/dam/pdf/fiches-descriptives/fiche-descriptive-duo-reference-3-ans.pdf) montre deux grilles séparées, sans remise duo. [EDF](https://particulier.edf.fr/), [Mint](https://www.mint-energie.com/), [Octopus](https://octopusenergy.fr/), [ilek](https://www.ilek.fr/), [Ekwateur](https://ekwateur.fr/), [GEG](https://www.geg.fr/) et [OHM](https://www.ohm-energie.com/) : page officielle à relever.

- Mention « Offre combinée non relevée » pour les fournisseurs sans duo relevé : proposée, non décidée.

- Les offres combinées ne sont relevées que pour 3, 6 et 9 kVA.

## Professionnels (onglet Pro, essai) À faire, au fil de vos envois

- [ENGIE](https://particuliers.engie.fr/) Pro : Référence Pro 1, 2 et 3 ans et Latitude 1 an (prix indexé sur le marché, qui change chaque mois : la valeur saisie est celle d'octobre) d'après les grilles d'octobre 2026, jusqu'à 36 kVA, hors taxes. À refaire quand ENGIE publie ses grilles de novembre. Le calcul n'inclut pas la réduction de 25 % de la première année (3 ans, jusqu'au 31 octobre 2026).

- Autres fournisseurs avec une grille Pro déjà repérée, à lire et saisir : [Enercoop](https://www.faq.enercoop.fr/hc/fr/articles/360024967152-Annexes-tarifaires) (offre « 2 saisons », 4 prix, non modélisée), [Énergie d'ici](https://www.energiedici.fr/nos-offres-pour-les-professionnels.html) (bulletin professionnels reçu le 14 nov., non saisi). Endesa ne propose que des offres professionnelles (à relever).

- [Gaz de Bordeaux](https://www.gazdebordeaux.fr/documents-contractuels) Pro : écarté pour l'instant. Ses CGV Pro (juillet 2026) et ses documents contractuels, lus le 30 oct. 2026, ne contiennent aucune grille : les prix sont établis par cotation envoyée au client. À reprendre si une grille publique apparaît.

- Hors taxes : l'accise, la CTA et la TVA ne sont pas comptées (le taux d'accise dépend de l'activité). À décider : les ajouter avec un choix « Mon activité », ou laisser le prix hors taxes.

- Puissances au-delà de 36 kVA (fiche [ENGIE](https://particuliers.engie.fr/) C4, grilles sur devis) : non traitées.

- Gaz professionnel : [ENGIE](https://particuliers.engie.fr/) Pro saisi (Activert Gaz 1, 2 et 3 ans, Latitude Gaz 1 an, consommation jusqu'à 300 MWh, grilles d'octobre 2026). Le prix dépend de la plage de consommation (P1, P2, P3) et d'un « niveau » de 1 à 6 pour les obligations, que l'utilisateur choisit à la main : à relier au code postal quand on aura la table des communes par niveau (zones GRDF). Le terme de débit normalisé lié au compteur (5,73 €/an par Nm³/h, au-delà de 40 Nm³/h) n'est pas compté. Les autres fournisseurs de gaz professionnel restent à relever.

## Eau À faire

- Chaque lundi : si les prix changent (par exemple quand SISPEA publie l'année 2026), la demande de fusion « eau » est maintenant fusionnée toute seule (depuis le 8 nov.), après les tests et les garde-fous du script. Rien à valider ; les lignes « À vérifier » restent dans le journal de l'exécution si vous voulez les relire.

- Historique : les variations de plus de 40 % en un an sont signalées sous la courbe (par exemple Antibes) ; reste à vérifier ces communes une à une. Les prix par année ne sont pas toujours comparables (couverture variable, 2025 moins complète).

- Communes sans prix : environ 8 700 communes n'ont aucun prix dans SISPEA ; le site le dit et utilise une moyenne indicative (région, ou nationale). À améliorer avec une autre source si elle apparaît.

- Abonnement estimé : pour environ 3 400 communes, médiane du département ; 99 € si le département n'a pas assez de données. Décider d'afficher aussi pour lui la mention « Données non communiquées… ».

- Corse et Provence-Alpes-Côte d'Azur : moyennes peu fiables, la moyenne nationale est utilisée à la place.

- Opérateurs (idée du 10 octobre 2026). Chaque commune a son service, géré par une régie ou par un opérateur (Veolia, Suez, Saur). Deux pistes : les 3 opérateurs les plus présents par région (aucune donnée sourcée trouvée ; sources possibles : rapport de la Fédération professionnelle des entreprises de l'eau, données SISPEA), et l'opérateur de chaque commune dans le tableau des prix (le plus utile, mais à relever commune par commune).

- Consommations par usage : les appareils et l'eau reposent sur des ordres de grandeur sans source précise.

## Parrainages À confirmer

- À confirmer sur le site du fournisseur : [Ekwateur](https://ekwateur.fr/) (montant du parrain absent du règlement), [Happ-e](https://www.happ-e.fr/) (20 € par contrat d'après Hellowatt : à confirmer sur la page de [Happ-e](https://www.happ-e.fr/)), [LLUM](https://www.llum.fr/) et [ilek](https://www.ilek.fr/grilles-tarifaires) (une seule source).

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

- Filtres en panneau latéral à puces, style [Selectra](https://selectra.info/) (fusionné le 11 nov., PR 273), sur Électricité et Gaz : type de prix, énergie verte, engagement, fiabilité (grille officielle), promotion, liste de fournisseurs, compteur « n offres sur N », réinitialisation ; sur mobile, bouton « Filtrer » qui ouvre le panneau. Pas encore sur Élec + Gaz. Non repris de Selectra : option tarifaire (déjà dans « Formule »), note client, Selectra Score.

### Comparaison avec Selectra (12 nov. 2026)
- [Selectra](https://selectra.info/) (page « speciales=1 », enregistrée le 11 nov.) : 21 fournisseurs, 61 offres d'électricité (44 en option Base à Lyon sans les offres spéciales). Nous (14 nov.) : 37 offres d'électricité (22 fournisseurs), plus 4 à prix variable dans le filtre « Prix variable » (OctoSaisons, Tempo, Zen Estival, [Énergie d'ici](https://www.energiedici.fr/)), 25 en gaz. Leur liste n'est lisible dans le fichier enregistré que si la page est chargée en entier (fichier de 10 Mo).
- Fournisseurs de [Selectra](https://selectra.info/) ajoutés depuis le 11 nov. : Symphonics, Urban Solar Energy, mylight150, [Énergie d'ici](https://www.energiedici.fr/) ; Sobry relevé sans calcul (prix du marché heure par heure) ; Jeety Energy, Papernest Énergie et Frank Énergie abandonnés le 15 nov.
- Formules absentes de fournisseurs déjà présents : [EDF](https://particulier.edf.fr/) (Zen Fixe, Zen Estival, Zen Week-End x3, Vert Électrique Week-End), [TotalEnergies](https://www.totalenergies.fr/particuliers) (Heures Eco, Heures Eco+ : fiche reçue le 18 nov., à saisir dans le filtre « Prix variable »), [Octopus](https://octopusenergy.fr/) (Eco Fixe 2 ans, Eco Fixe Plus, Octopus Go, SolarPlus, SolarBoost), [Enercoop](https://www.enercoop.fr/) (3 offres Flexibilité), [Gaz de Bordeaux](https://www.gazdebordeaux.fr/) (NovaFixe Bonus Élec dans la liste de [Selectra](https://selectra.info/)), [Dyneff](https://www.dyneff-elec-gaz.fr/) (Contrat+ Verte), [Happ-e](https://www.happ-e.fr/) (Option Vertelec), [OHM](https://www.ohm-energie.com/) (Week-End), [Plenitude](https://eniplenitude.fr/) (Plenifix 1 an).
- Chez nous mais pas chez eux : [Ekwateur](https://ekwateur.fr/), [Mint](https://www.mint-energie.com/), [Alterna](https://www.alterna-energie.fr/), [Primeo](https://particuliers.primeo-energie.fr/) Essentielle Verte.
- Méthode retenue : pour chaque offre, tu enregistres la page ou la grille du fournisseur (pas celle de [Selectra](https://selectra.info/), source secondaire), je vérifie les prix puis je saisis. Ordre proposé pour les prix fixes : [EDF](https://particulier.edf.fr/) Zen Fixe, [Octopus](https://octopusenergy.fr/) Eco Fixe 2 ans, [Plenitude](https://eniplenitude.fr/) Plenifix 1 an, [Gaz de Bordeaux](https://www.gazdebordeaux.fr/) NovaFixe Bonus. Comparaison de prix possible avec leur réglage 5 360 kWh, 9 kVA, Base.
- [EDF](https://particulier.edf.fr/) Tempo : la grille « Tarif Bleu » applicable au 1er août 2026 (reçue à nouveau le 12 nov.) est identique à nos prix (filtre « Prix variable » de l’onglet Électricité) ; le tarif réglementé ne change qu'en février et août, prochaine révision probable le 1er février 2027.

### Mises à jour automatiques

- Fusion des PR du robot (prix, eau) : le contrôle « tests » de la PR reste « en attente d'approbation » ; les workflows maj-prix et maj-eau l'approuvent maintenant avant de fusionner (10 nov.). Si une PR reste bloquée : approuver le run Tests en attente, puis fusionner.
- Auto-fusion (workflow « Auto-fusion », ajouté le 3 nov. 2026) : toute PR ouverte par Absinthe1975 ou par le robot de mise à jour des prix est fusionnée dès que les tests sont au vert, puis la publication Facebook est lancée. Pour empêcher une fusion : étiquette « ne-pas-fusionner » ou PR en brouillon. Les mises à jour de prix ne sont donc plus relues à la main : surveiller les posts Facebook et le rapport.

- Après chaque fusion : lancer « Run workflow » et lire le rapport (section « Liens fournisseur en échec », lignes [Mint](https://www.mint-energie.com/) et CRE, offres « À relire », premiers repères des PDF suivis). Quand un PDF suivi change, le rapport donne le prix du kWh lu par l'IA (avec citation vérifiée) à côté du nôtre, sans rien appliquer : vous saisissez ensuite la grille à la main.

- Facebook : quatre brouillons (parrainages [EDF](https://particulier.edf.fr/), [Alpiq](https://particuliers.alpiq.fr/), [Gaz de Bordeaux](https://www.gazdebordeaux.fr/), eau) dans docs/FACEBOOK-BROUILLONS.md, à publier avec le workflow « Publication Facebook manuelle » (aperçu par défaut). Chaque fusion qui change un prix officiel publie un post sur la Page (le résultat est écrit dans l'annotation de l'exécution du workflow). À faire : un message pour l'eau (national, sans code postal), et renouveler le jeton de la Page, qui a transité par la conversation (à stocker uniquement dans le secret GitHub).

- Grilles saisies à la main : le fichier donnees/manuel/tarifs_manuels.json est fusionné avec les données automatiques. À y saisir, au fil des envois : les fournisseurs qui interdisent les robots ([EDF](https://particulier.edf.fr/), [ilek](https://www.ilek.fr/)). Mode d'emploi dans docs/LISEZMOI.md.

- Sources bloquées (relevé du 1er nov. 2026, à refaire de temps en temps) : [EDF](https://particulier.edf.fr/) (particuliers et entreprises), [ENGIE](https://particuliers.engie.fr/) particuliers, [ilek](https://www.ilek.fr/), [Selectra](https://selectra.info/) et Kelwatt interdisent la lecture automatique (robots.txt) ; le catalogue des prestations d'Enedis et labellenergie.fr ne s'ouvrent pas depuis l'outil de travail. Pour ces sites, les grilles sont à envoyer en fichier (PDF ou page enregistrée) et à saisir à la main, avec l'étiquette « À confirmer » tant qu'il n'y a pas de grille officielle datée. Pages dont le prix n'est pas lisible par le programme : [Alpiq](https://particuliers.alpiq.fr/) (grille), [GEG](https://www.geg.fr/) et [TotalEnergies](https://www.totalenergies.fr/particuliers) gaz (prix du kWh absent de la page). Fournisseurs relancés sans réponse : à recontacter par le service partenaires ou les réseaux sociaux.

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
