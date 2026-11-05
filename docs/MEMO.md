<!-- Mémo retiré du site le 2 novembre 2026, conservé ici. Ne l'oublie pas : à relire avant chaque session. -->
# Mémo : ce qu'il reste à faire

Mémo mis à jour le 2 novembre 2026, classé par énergie : électricité, gaz, offres combinées, eau, parrainages, puis le site lui-même. Seul ce qui reste à faire y figure. Un sujet est abandonné pour le moment : la lecture des factures (trop de formats). L'onglet « Pro » est relancé en essai, avec ENGIE Pro pour commencer.

## Électricité À faire, au fil de vos envois

### Grilles à saisir ou à confirmer, fournisseur par fournisseur

- [Gaz de Bordeaux](https://www.gazdebordeaux.fr/) : NovaFixe Élec est saisie (fiche officielle de novembre 2026 relevée pour Onnaing : Base 0,1919 / 0,19042 €, heures pleines / creuses 0,20536 / 0,1528 € ; abonnements inchangés ; les grilles d'octobre étaient identiques dans 6 villes, à vérifier pour novembre dans une autre ville). Novaflex Élec (indexée, 2 % sous le tarif réglementé, 2 ans) est saisie d'après la fiche officielle de novembre 2026 (Base 0,1968 / 0,19526 €, heures pleines / creuses 0,21067 / 0,15646 €, Onnaing). La grille du NovaFixe Bonus Élec est identique à celle du NovaFixe Élec. Gaz de Bordeaux édite ses fiches par commune : vérifier avec une fiche d'une autre ville que novembre est bien identique partout. Le bonus de 100 € de l'offre Bonus Élec suit son [règlement](https://ressources.gazdebordeaux.fr/DOCUMENTS/REGLEMENT/Reglement_novafixe_bonus_elec.pdf) (souscription jusqu'au 30 novembre 2026) : il s'affiche sous l'offre, hors classement. Ensuite, supprimer sa ligne dans la rubrique « promos » de donnees/data.json.

- [ENGIE](https://particuliers.engie.fr/) : Elec Référence 3 ans à confirmer : prix de novembre 2026 relevés sur Selectra (grille du 30 oct. 2026, TTC : base 0,2403 € de 3 à 6 kVA et 0,2420 € dès 9 kVA ; heures pleines 0,2561 €, creuses 0,2023 € ; abonnement 186,98 € par an à 6 kVA), source secondaire. La fiche descriptive officielle d'octobre 2026 est reçue : elle donne fourniture, acheminement et obligations séparément. L'abonnement de 186,98 € à 6 kVA se retrouve exactement (fourniture 45,79 € + acheminement à 4 plages 141,19 €). Contrôle du 2 nov. 2026 avec la fiche (accise 0,0367 € TTC, obligations 0,0184 € à 6 kVA et 0,0201 € dès 9 kVA, acheminement à 4 plages de 0,0144 à 0,0926 €) : la base de Selectra (0,2403 et 0,2420 €) est compatible, et son écart de 0,0017 € entre 6 et 9 kVA correspond exactement aux obligations. En revanche le prix en heures creuses de Selectra (0,2023 €) est inférieur au minimum que permet la fiche (0,2146 €) : il n'est plus affiché. Pour passer l'offre en « Grille officielle », il faut le prix total d'ENGIE (simulateur ou courrier) ou la formule d'acheminement du client. Promotion de deux mois d'abonnement offerts, jusqu'au 7 novembre 2026 : affichée sous les offres ENGIE, hors classement ; supprimer sa ligne dans « promos » après cette date. Page de promotions ENGIE du 28 octobre 2026 lue : elle confirme cette promotion (souscription du 19 octobre au 7 novembre inclus, Elec, Gaz ou Duo Référence 3 ans, ou Happy Week-End) et décrit la « Promo d'été » (50 % de l'électricité consommée de 13 h à 17 h en cagnotte), notée dans l'onglet Saisons.

- [LLUM](https://www.llum.fr/) : grille officielle d'août 2026 lue. Compteur non communicant : Base 0,19 €/kWh et HP/HC 0,2071 / 0,1540 € (modélisés, officiels). Avec un Linky, LLUM applique une grille par saison et heures pleines / creuses (Base : 0,22276 € en HP hiver, 0,15064 € en HC été), non modélisée. À décider : modéliser une moyenne, ou afficher une mention.

- [Alpiq](https://particuliers.alpiq.fr/) (Sérénité) : prix indexé (remise de 0,5 % sur le kWh HT du tarif réglementé) : à resaisir à chaque changement du tarif réglementé (février, août), avec la grille PDF d'Alpiq.

- [Octopus](https://octopusenergy.fr/) : « Cocon fixe » est le nom du contrat (fiche descriptive de juillet 2026) de l'offre vendue sous le nom « OctoEco Fixe » (« Eco fixe » dans ses grilles) : la page officielle des tarifs relie bien ces trois noms, confirmé le 4 nov. 2026. Eco fixe Base (grille du 12 août 2026) vérifiée : conforme. Gaz Fixe : grille mensuelle de novembre 2026 (applicable au 30 oct.) saisie, à ressaisir chaque mois. Intelligent Octopus Fixe : grille officielle du 1er août 2026 vérifiée (0,1968 € jusqu'à 8 kVA, 0,1953 € au-delà), passée en « Grille officielle ». Pour l'offre saisonnière, le prix moyen suppose 58 % de la consommation en hiver : à confirmer ou corriger. OctoSaisons (ex-OctoTempo, renommée le 21 octobre 2026) : grille officielle du 1er août 2026 reçue (docs/OCTOSAISONS-GRILLE.md) et calculée dans l'onglet Saisons, avec EDF Tempo et Zen Estival, à partir de vos usages (profil horaire supposé par le site, hors classement général). Les plages d'heures creuses d'OctoSaisons (21 h à 7 h, plus 11 h à 17 h l'été) viennent d'un article de presse et ne figurent pas dans la fiche officielle : à confirmer auprès d'Octopus. Hypothèses des saisons à valider (7 % de jours rouges, 55 % en hiver) ; puis décider d'intégrer ces offres au classement si d'autres fournisseurs adoptent ce principe.

- [Ekwateur](https://ekwateur.fr/) : le prix n'apparaît qu'à la souscription (code postal demandé), sans grille publique. Il faut un PDF de grille, ou renoncer à « Grille officielle » pour cet acteur.

- [Primeo](https://particuliers.primeo-energie.fr/) (Essentielle Verte) : le prix est une formule (kWh HT à 95 % du tarif réglementé, abonnement identique). Notre 0,1919 €/kWh en 6 kVA est cohérent mais calculé par nous. À décider : l'afficher comme « calculé selon la formule officielle (tarif réglementé −5 %) » et le recalculer à chaque mise à jour du tarif réglementé, ou le laisser « À confirmer ».

- [Enercoop](https://www.faq.enercoop.fr/hc/fr/articles/360024967152-Annexes-tarifaires) : grille du 1er août 2026 intégrée (Base et Flexibilité heures creuses). Non modélisées : Nuit & week-end, 2 saisons, jours de pointe (plages horaires et saisons propres à Enercoop). Sa suspension d'accueil, annoncée dans des données sans source datée, n'est pas confirmée par ses pages officielles : à vérifier avant de le retirer.

- [ilek](https://www.ilek.fr/grilles-tarifaires) : ses PDF sont sur un domaine qui interdit les robots : à relire à la main à chaque changement de grille.

- [EDF](https://particulier.edf.fr/) : Zen Estival : grille officielle reçue (15 sept. 2026) et calculée dans l'onglet Saisons avec la répartition de consommation publiée par EDF (exemple à 3,6 MWh par an sans chauffage électrique), car les plages d'hiver ne figurent pas dans les documents reçus ; elle n'apparaît pas pour un chauffage électrique. Le site interdit les robots (robots.txt) : ses 12 grilles PDF et ses pages de prix restent saisies à la main à chaque changement. Le tarif réglementé, lui, vient de la CRE.

- [GEG](https://www.geg.fr/) : le script prend le PDF le plus récent de la [page des tarifs](https://www.geg.fr/aide-et-contact/centre-documentation/particulier/tarifs/). Non intégré : « L'Offre Online » (indexée sur le tarif réglementé −5 %, grille du 1er février 2026 sans doute dépassée : envoyer la grille récente).

### Heures pleines / creuses

- Le choix « Formule » apparaît dans l'onglet Électricité dès qu'une offre a ses prix. Déjà saisis : Dyneff, La Bellenergie, Gaz de Bordeaux, Enercoop, ilek, EDF Zen Fixe, Alpiq, Mint et GEG (Elec Verte et Direct Producteur, grille du 5 oct. 2026, prix des 6 et 9 kVA).

- À saisir dans la rubrique hphc de donnees/manuel/tarifs_manuels.json (champs hp et hc en €/kWh TTC, abo par puissance) : LLUM (GEG est fait). Je ne peux pas lire ces PDF d'ici : envoyez les chiffres ou les fichiers.

### Fournisseurs à ajouter (liste du 24 octobre 2026, à confirmer sur leurs sites)

- [Urban Solar Energy](https://www.urbansolarenergy.fr/mentions-legales/) (prix fixe, autoconsommation) : pas de grille publique, tarifs par simulation. Documents : [CGV ≤ 36 kVA](https://www.urbansolarenergy.fr/wp-content/uploads/2026/07/CGV-inferieures-ou-egales-a-36kVA_01_06_2026.pdf), [conditions générales de septembre 2026](https://www.urbansolarenergy.fr/wp-content/uploads/2026/09/GC-01.09.2026.pdf).

- [Énergie d'ici](https://www.energiedici.fr/nos-offres-pour-les-particuliers.html) (électricité locale, hydroélectricité) : envoyer la fiche descriptive et le bulletin d'adhésion (voir docs/LIENS-RECUS.md).

- [Jeety Energy](https://jeety.energy/) (ex-Élecocité) : aucune grille publique ; tarifs à relever par simulation sur leur site.

- Entreprises locales de distribution (ES Strasbourg, UEM Metz, Gedia, Séolis, Synelva, Électricité de Provence, Enargia) : section régionale à prévoir.

### Limites connues du calcul

- Puissances de 3 à 36 kVA : les offres sans grille complète sont estimées (étoile). Le tarif réglementé de 12 à 36 kVA se ressaisit à la main à chaque changement (février, août) avec la grille EDF. Dès qu'un fournisseur donne sa grille, la saisir dans le champ abo de l'offre. Le prix du kWh à 7 et 8 kVA (Enercoop) et à 21 kVA (Dyneff) n'est pas distingué.

- Abonnement à 3 kVA de [OHM](https://www.ohm-energie.com/) et [Octopus](https://octopusenergy.fr/) : non exact.

- Filtres des offres : prix fixe ou indexé, engagement et offre verte ne sont renseignés que pour environ la moitié des offres (15 sur 29 en électricité, 9 sur 22 en gaz le 30 octobre 2026). À compléter avec la fiche descriptive de chaque offre (champs typ, eng et vert de data.json).

- Autres options des fournisseurs (à faire plus tard) : formules week-end, jours de pointe, voiture électrique.

## Gaz À faire, au fil de vos envois

- [Gaz de Bordeaux](https://www.gazdebordeaux.fr/) : relevés du simulateur officiel pour Lille (59000, trois niveaux de consommation) dans docs/GDB-GAZ-RELEVES.md : NovaFixe Biogaz 0,1336 €/kWh (accise comprise) en B1 et 0,1753 en B0, contre 0,1346 aujourd'hui sur le site. Pour savoir si ces prix valent partout, relever une consommation moyenne dans deux ou trois autres codes postaux de zones différentes (par exemple Bordeaux 33000, Paris 75001, Marseille 13001) sur la [page gaz](https://www.gazdebordeaux.fr/nos-offres-d-energie/gaz-naturel#telechargement-grille-tarifaire-gaz).

- [ENGIE](https://particuliers.engie.fr/) : Gaz Référence 3 ans à confirmer. Les deux prix vus (0,1414 et 0,1373 €/kWh) sont deux zones de la même grille. Selectra (1er oct. 2026, TTC, 4 001 à 29 999 kWh/an, abonnement 360,79 €/an) donne 8 zones : A 0,13728 · B 0,1383 · C 0,1414 · D 0,14474 · E 0,14835 · F 0,15104 · G 0,15324 · H 0,15326 €/kWh. Nous affichons la zone C. La fiche officielle d'août 2026 recoupe Selectra (à moins de 0,001 €/kWh) : il manque seulement la table code postal → groupe A à H (ENGIE ne la donne que par formulaire).

- [ilek](https://www.ilek.fr/grilles-tarifaires) : relier la zone gaz (A à K, de 0,1633 à 0,1809 €/kWh en T2) au code postal avec [ilek.fr/zone-tarifaire-gaz-vert](https://www.ilek.fr/zone-tarifaire-gaz-vert) ; nous affichons la zone B (0,1652 €/kWh).

- [Mint Énergie](https://www.mint-energie.com/) : grilles gaz Biogaz Online, Classic et Smart de novembre 2026 saisies. Elles sont mensuelles (indexées sur le prix repère + 5, 10 ou 15 %) : à ressaisir chaque mois avec les PDF du 1er du mois ; la saisie manuelle masque le calcul automatique de Biogaz Online. Électricité : grilles du 20 octobre 2026 saisies (kWh indexé à +10, +15 et +20 % sur le tarif réglementé, abonnement identique au tarif réglementé).

- [TotalEnergies](https://www.totalenergies.fr/particuliers) : gaz « Fixe 2 ans ».

- [Dyneff](https://www.dyneff-elec-gaz.fr/offres/contrat-gaz-vert/) : gaz 15 %, 55 % et 100 % renouvelable déjà intégrés, grilles du 1er octobre 2026 vérifiées (prix et abonnement identiques). Ces grilles sont publiées chaque mois (« fin de l'offre : fin du mois en cours ») : le suivi automatique repère chaque mois le nouveau PDF sur les pages gaz et électricité de Dyneff et le signale dans le rapport (sans rien appliquer) ; il reste à saisir les nouveaux prix.

- [GEG](https://www.geg.fr/) : non intégrés : Mon Offre Gaz Indexée (Grenoble et communes voisines seulement, prix mensuel), grilles locales Mont Gaz et Nov'Alp. GEG gaz au réseau NTR 0-3 seulement.

- Limites du calcul : profil chauffage (B1) pour la comparaison ; les offres dont le seuil varie ([GEG](https://www.geg.fr/), [Plenitude](https://eniplenitude.fr/)) sont à surveiller ; les zones de distribution locales (Bordeaux, Strasbourg, Colmar) ne sont pas modélisées. Prix et abonnements Base et B0 réels pour les offres à grille officielle, estimés (étoile) pour les autres.

- Zone tarifaire par commune : aucune liste trouvée, donc aucun écart n'est appliqué. Avec le code postal, une table « code postal → zone » suffirait, mais chaque fournisseur découpe les zones à sa façon (tableau ci-dessous, à vérifier sur les grilles officielles).

 | Fournisseur | Système de zones | Particularités | 

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

- Chaque lundi : si une demande de fusion « eau » s'ouvre (prix changés, par exemple quand SISPEA publie l'année 2026), elle vous est assignée : relire les lignes « À vérifier » du journal, puis fusionner.

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

### Mises à jour automatiques

- Auto-fusion (workflow « Auto-fusion », ajouté le 3 nov. 2026) : toute PR ouverte par Absinthe1975 ou par le robot de mise à jour des prix est fusionnée dès que les tests sont au vert, puis la publication Facebook est lancée. Pour empêcher une fusion : étiquette « ne-pas-fusionner » ou PR en brouillon. Les mises à jour de prix ne sont donc plus relues à la main : surveiller les posts Facebook et le rapport.

- Après chaque fusion : lancer « Run workflow » et lire le rapport (section « Liens fournisseur en échec », lignes [Mint](https://www.mint-energie.com/) et CRE, offres « À relire », premiers repères des PDF suivis). Quand un PDF suivi change, le rapport donne le prix du kWh lu par l'IA (avec citation vérifiée) à côté du nôtre, sans rien appliquer : vous saisissez ensuite la grille à la main.

- Facebook : chaque fusion qui change un prix officiel publie un post sur la Page (le résultat est écrit dans l'annotation de l'exécution du workflow). À faire : un message pour l'eau (national, sans code postal), et renouveler le jeton de la Page, qui a transité par la conversation (à stocker uniquement dans le secret GitHub).

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

- **Relecture automatique** : avant chaque fusion automatique, `scripts/relecture.py` compare les données (prix non officiels > 15 % (un prix officiel sourcé est toujours accepté), offre retirée, « officielle » sans source…). Si elle signale quelque chose, la PR reçoit un commentaire et l'étiquette `ne-pas-fusionner`. À corriger : Alterna gaz (2 offres officielles sans lien de source).
