# Comparateur énergie : mise à jour automatique des prix

Ce dossier contient le site (`index.html`), ses données (`elec/data.json` pour l'électricité, `gaz/data.json` pour le gaz, `data.json` pour ce qui est commun : dates, primes, liens, offres combinées) et le programme qui les met à jour avec l'aide d'une IA.

## Comment ça marche

1. Chaque jour du 1er au 10 du mois, puis chaque lundi (ou quand vous le lancez à la main), GitHub exécute `scripts/update_prices.py`.
2. Le programme lit les pages listées dans `sources.json`.
3. Pour chaque offre, l'IA (Gemini, gratuite) renvoie les chiffres **et la phrase exacte où elle les a trouvés**.
4. Le programme refuse un chiffre si la phrase n'est pas dans la page, si le chiffre n'est pas dans la phrase, s'il est hors d'une fourchette plausible, ou s'il s'écarte trop de l'ancienne valeur (alors il est seulement signalé).
5. Les changements acceptés sont mis dans ces fichiers de données avec la date, et GitHub ouvre une **demande de fusion** (pull request) avec un rapport. **Rien n'est publié tant que vous ne l'avez pas acceptée.**
6. Le site lit les trois fichiers de données à chaque visite. S'il ne peut pas le lire, il utilise les données intégrées à `index.html`.

## Mise en route (une seule fois)

1. Créez un dépôt **public** sur GitHub et envoyez-y tout le contenu de ce dossier, y compris le dossier caché `.github`.
2. Créez une clé gratuite sur aistudio.google.com/apikey (compte Google, pas de paiement demandé), puis dans le dépôt : Settings, Secrets and variables, Actions, New repository secret. Nom : `GEMINI_API_KEY`.
3. Dans Settings, Actions, General, Workflow permissions : choisissez « Read and write permissions » et cochez « Allow GitHub Actions to create and approve pull requests ».
4. Pour publier le site : Settings, Pages, « Deploy from a branch », branche `main`, dossier `/ (root)`.
5. Premier essai : onglet Actions, « Mise à jour des prix », Run workflow (la case « recoupement » est décochée par défaut : lancement rapide ; cochez-la pour recouper aussi les prix inchangés sur un second site, plus long, fait automatiquement le lundi). Lisez le rapport dans la demande de fusion qui apparaît.

## Corriger ou ajouter une source

Ouvrez `sources.json` : une adresse par fournisseur dans `tarifs_pages`. Si une page change d'adresse, le rapport l'indique comme « source en échec ».

## Essayer en local, sans rien publier

```
python -m unittest discover -s tests        # tests, sans réseau ni IA
GEMINI_API_KEY=... python scripts/update_prices.py --dry-run
```

## À savoir

- **Sites qui refusent les robots :** Selectra et Kelwatt interdisent la lecture automatique (robots.txt) : le programme les refuse et les signale dans « Sources en échec ». Les sources par défaut sont prix-elec.com, hellowatt.fr et la CRE. Les PDF sont lus grâce à `pypdf`.
- Les tests ont été faits avec des pages et des réponses simulées. Le premier lancement réel peut montrer des adresses à corriger ou des pages que l'IA lit mal : c'est le rôle de la relecture.
- Ne sont pas mis à jour automatiquement : le prix de l'eau, les abonnements à 3 et 9 kVA, et les textes qui citent des chiffres (notes des onglets Gaz et Abonnement).
- **Gratuit, mais avec des limites.** L'offre gratuite de Gemini limite le nombre de requêtes par minute et par jour (chiffres dans aistudio.google.com/rate-limit, ils peuvent changer). Le programme attend entre deux appels et réessaie après une erreur de limite ; s'il est bloqué, relancez le lendemain. Environ 50 appels par mois sont nécessaires, et les pages inchangées sont sautées.
- **Confidentialité :** sur l'offre gratuite, Google peut réutiliser les textes envoyés pour améliorer ses produits. Ici ce sont uniquement des pages publiques, jamais des données de visiteurs.
- **Changer de fournisseur :** dans `sources.json`, `provider` peut valoir `gemini` (gratuit), `mistral` (offre gratuite, clé `MISTRAL_API_KEY`) ou `anthropic` (payant, clé `ANTHROPIC_API_KEY`). Le nom du modèle se règle dans `model`. Adaptez aussi la ligne `env` du fichier `.github/workflows/maj-prix.yml`.
- GitHub Models, autre offre gratuite, est arrêté depuis le 30 juillet 2026.
- Vérifiez les conditions d'utilisation de chaque site lu. Le programme respecte `robots.txt` et se présente sous le nom « ComparateurEnergieBot ».


## Prix de l'eau par commune

Automatique : le workflow « Mise à jour du prix de l'eau » (chaque lundi, ou bouton *Run workflow*) lance `scripts/eau_maj.py`. Il télécharge la base La Poste et les fichiers SISPEA indiqués dans `eau/eau-config.json` (à renseigner : adresses des deux fichiers `tarifs_AEP_{an}.xls` et `tarifs_AC_{an}.xls`), prend la dernière année non vide, reconstruit `communes-cp.json`, refuse le résultat si des codes postaux disparaissent ou si les prix bougent trop, puis, seulement si quelque chose change, ouvre une demande à relire qui vous est assignée (notification GitHub et courriel, étiquette « à-fusionner »).

Procédure manuelle (si besoin) :

Les fichiers `eau/cp/NN.json` (un par début de code postal : communes, avec le prix de l’eau) sont fabriqués par `scripts/build_eau.py` à partir de :
- la base officielle des codes postaux (data.gouv.fr, fichier `019HexaSmal.csv`),
- les fichiers SISPEA « tarifs eau potable » et « tarifs assainissement collectif » (services.eaufrance.fr/pro/telechargement), feuille « Zones tarifaires » exportée en CSV UTF-8 sous les noms `tarifs_AEP_<année>.csv` et `tarifs_AC_<année>.csv`,
- les feuilles « Détail tarifaire » des mêmes fichiers, exportées en `detail_AEP_<année>.csv` et `detail_AC_<année>.csv` (abonnement = part fixe),
- éventuellement `zones_gn.json` (orthographe des communes).

Commande : `python3 scripts/build_eau.py eau-sources communes-cp.json 2025` (fichier unique intermédiaire, que `eau_maj.py` découpe ensuite par département).

## Prix de référence : recoupement obligatoire

Le tarif réglementé de l'électricité et le prix repère du gaz (B0 et B1) sont lus sur plusieurs sites (`sources.json`, section `references`). Une valeur n'est appliquée que si **au moins deux sites** donnent le même chiffre. Un seul site, des sites en désaccord, ou un B0 inférieur ou égal au B1 : rien n'est appliqué et la ligne apparaît dans « À relire ». Le contrôle avec la variation annoncée par le médiateur compare la moyenne annoncée aux variations de B1 et de B0.

## Fréquence

Le prix repère du gaz paraît début de mois et les fournisseurs ajustent leurs offres dans les jours qui suivent : le contrôle tourne donc chaque jour du 1er au 10, puis chaque lundi. Une demande de fusion n'est ouverte que s'il y a un changement ou une ligne à relire ; sinon rien n'est créé. Si une demande est déjà ouverte, elle est mise à jour au lieu d'en créer une nouvelle. Ainsi un chiffre vu sur un seul site un jour est appliqué dès qu'un second site le confirme.

## Prix des offres : second site obligatoire

Chaque offre est lue sur sa page principale (`tarifs_pages`), puis, si le prix a changé, relue sur un second site (`tarifs_pages_2`, par défaut la page tarifs du fournisseur sur fournisseurs-electricite.com). Le changement n'est appliqué que si les deux sites donnent le même kWh (écart de 0,0002 € au plus). Un seul site, ou deux sites en désaccord : la ligne est listée dans « À relire ». Le lundi et lors d'un lancement à la main, les prix inchangés sont aussi recoupés, pour repérer une page source restée périmée. Les adresses de `tarifs_pages_2` n'ont pas toutes été ouvertes : après le premier rapport, corrigez celles qui apparaissent dans « Sources en échec ».

## Sources officielles de la CRE (sans IA)

Le script lit lui-même, avant les sites lus par l'IA :
- le tarif réglementé de l'électricité, via l'API tabulaire de data.gouv.fr (identifiant de la ressource dans `sources.json`, clé `open_data`), avec repli sur le CSV ;
- le prix repère du gaz, via le fichier Excel de la page open data de la CRE (nécessite `openpyxl`, installé par le workflow).

Ces valeurs font foi : elles remplacent celles des autres sites. En cas de lecture impossible, le rapport l'indique dans « Sources en échec » et rien n'est modifié. La ligne en vigueur du tarif réglementé est celle dont la date de fin est vide : on ne se fie pas aux dates de l'API, qui ont été vues avec jour et mois inversés.

### Prix repère du gaz par zone (page de Mint Énergie)

La CRE ne publie pas de prix par zone. La page `informations.mint-energie.com/.../prix-repere-gaz.aspx` (clé `mint_prg` de `sources.json`) republie le prix repère pour les 6 zones. C'est un formulaire : `scripts/mint_prg.py` rejoue ce que fait le navigateur (une requête par zone) et vérifie que la page répond bien à la zone et au mois demandés. Le résultat sert aux offres marquées `"prg": true` dans `data.json` (Mint Biogaz Online, indexée au niveau du prix repère). Le robots.txt du site est respecté. Si la zone 1 s'écarte de plus de 0,0006 €/kWh du prix repère de la CRE, rien n'est appliqué et la ligne apparaît dans « À relire ».

## Prix du gaz par code postal (dossier gaz/prix-cp/)

Quand un fournisseur publie une grille par commune (pour l'instant Alterna gaz), elle est intégrée en entier, **dans un fichier à part par offre** (`gaz/prix-cp/alterna-mon-gaz-naturel-indexe.json`). Rien n'est mélangé entre fournisseurs :
- l'offre concernée (dans `gaz/data.json`) porte un champ `"cpf"` qui désigne son fichier ;
- le fichier rappelle sa clé de fournisseur (`k`), le nom exact de l'offre, la date de la grille et sa source ;
- le site n'utilise un fichier que si sa clé et son offre correspondent à celles de l'offre (sinon il l'ignore) ;
- `scripts/check_data.py` refuse la publication si un fichier est introuvable, ne correspond pas à son offre, contient des codes postaux invalides ou en double, ou des prix hors fourchette.

Sur le site, si l'utilisateur a saisi son code postal, il voit le prix exact de son code postal ; s'il ne figure pas dans la grille, c'est la moyenne du département, puis la moyenne de la grille. Un code postal qui regroupe des communes à prix différents reçoit la moyenne de ces communes. Sans code postal, le site utilise la zone choisie (1 à 6).

Pour ajouter ou mettre à jour une grille : extraire le texte du PDF (`pdftotext -layout`), puis lancer
`python3 scripts/cp_prix.py gaz/prix-cp fournisseur "Nom exact de l'offre" jj/mm/aaaa URL-source grille.txt`
et ajouter le champ `cpf` à l'offre dans `gaz/data.json`.

## Détection automatique des PDF de grilles (rubrique « grilles » de sources.json)

Le nom d'un PDF change souvent (date, version) : on ne garde donc pas son adresse. Chaque entrée de `sources.json > grilles` donne la **page du fournisseur** qui propose le PDF, et des mots qui décrivent le lien :

```
{"k": "alterna", "offre": "Mon gaz naturel indexé", "page": "https://…", "type": "cp-gaz",
 "contient": ["grille"], "un_de": ["gaz naturel"], "exclut": ["biogaz"]}
```

À chaque lancement, le script lit la page, repère le lien PDF dont le **texte** (« Grille tarifaire ») ou le nom de fichier contient ces mots, télécharge ce que le lien désigne ce jour-là et le lit. Garde-fous : `robots.txt` respecté ; aucun ou plusieurs liens possibles = rien n'est deviné, l'entrée apparaît dans « Sources en échec » ; PDF inchangé (empreinte identique) = ignoré ; grille sans date, en HT seulement, avec trop peu de codes postaux ou un prix moyen très différent = non appliquée, listée « À relire ».
- `"type": "cp-gaz"` : grille par code postal, intégrée automatiquement dans `gaz/prix-cp/` et dans l'offre de `data.json` (qui doit déjà porter son champ `cpf`).
- `"type": "info"` : le PDF est seulement détecté ; le rapport signale qu'il a changé, pour une intégration à la main.

Au lieu de `"page"`, une entrée peut donner `"url"` : l'adresse stable du PDF (EDF garde le même nom de fichier chaque mois) ou une adresse qui redirige vers le PDF du moment (Alterna : `/tarifs-gaz-indexe`). C'est la solution la plus simple quand elle existe. Pour le type `"info"`, la première lecture enregistre le PDF comme référence ; ensuite, chaque changement du fichier apparaît dans « À relire » avec son lien.

Les adresses de page de la liste sont à vérifier après le premier rapport (celle d'Alterna est provisoire).

## Liens vers les fournisseurs

Le nom du fournisseur dans les tableaux est un lien (nouvel onglet) vers son site. L'adresse vient de `data.json` (rubrique « liens ») :
- `liens` : une adresse par fournisseur (clé `k`), utilisée pour toutes ses offres ;
- `url` : adresse propre à une offre, à ajouter sur l'offre elle-même pour renvoyer directement vers sa page. Elle l'emporte sur le lien du fournisseur.

Les adresses doivent commencer par `https://`. À chaque mise à jour, `scripts/check_liens.py` vérifie qu'elles répondent et ajoute au rapport la section « Liens fournisseur en échec ». Un fournisseur sans lien s'affiche simplement en texte. Les liens sont sans parrainage ni suivi : le site ne reçoit rien.

Quand les liens PDF d'une page sont intégrés dans des données (JSON) plutôt que dans des balises `<a>` (cas d'Octopus), le script lit aussi les adresses `.pdf` du texte brut de la page, et reconnaît le bon fichier à des mots de son nom (« grille », « base », « hphc »), même si l'identifiant du fichier change chaque mois. Si une page n'affiche ses liens qu'après exécution d'un script dans le navigateur, ni le script ni moi ne les voyons : le rapport le signale (« aucun lien PDF ne correspond ») et on revient à l'envoi manuel.

## Lecture IA des PDF modifiés

Quand le PDF d'une offre suivie (type `info`) change et qu'une clé d'IA est disponible, le script demande à l'IA le prix du kWh qu'il contient (citation obligatoire, chiffre vérifié dans le texte, fourchette plausible) et l'écrit dans « À relire » à côté du prix actuel. Rien n'est appliqué : une grille officielle se saisit à la main.

## Historique des prix (onglet « Marché »)

`scripts/historique.py` est lancé par le workflow des prix, après la mise à jour. Il écrit :
- `elec/historique.json` : le tarif réglementé de vente (Base, 6 kVA), période par période, lu dans les données ouvertes de la CRE (data.gouv.fr). Les dates de ce jeu de données sont écrites de façon incohérente (jour et mois inversés) : le programme reconstruit chaque début de période à partir de la fin de la précédente et refuse d'écrire la série si les périodes ne s'enchaînent pas ;
- `gaz/historique.json` : le prix repère moyen mensuel de la CRE et les grilles B0/B1, lus dans le classeur Excel de la CRE ;
- `elec/historique-offres.json` et `gaz/historique-offres.json` : le prix de chaque offre relevé par le site, ajouté seulement quand il change (l'historique commence à la première exécution).

Aucune valeur n'est estimée. Si une source ne répond pas ou si les contrôles échouent, la série existante est conservée et le rapport indique « Historique … non mis à jour ».

## Historique du prix de l'eau

`scripts/eau_historique.py` (lancé par le workflow de l'eau, avant la mise à jour) télécharge les fichiers `tarifs_AEP_{an}.xls` et `tarifs_AC_{an}.xls` du SISPEA pour chaque année depuis 2009 et écrit dans `eau/historique/` : un fichier par département (`NN.json`, prix de chaque commune année par année), `national.json` (médianes par année) et `annees.json`. Seules les années manquantes et les deux plus récentes sont retéléchargées. Une année dont le fichier est absent, vide ou d'un autre format est ignorée et signalée dans le journal ; aucune valeur n'est estimée. La page affiche la courbe de la commune (onglet Eau) et le prix médian national (onglet Marché).

## Grilles saisies à la main (`data/tarifs_manuels.json`)

Pour un fournisseur dont le site interdit les robots (robots.txt) ou n'a pas de page lisible, on ne force pas la lecture : on saisit sa grille officielle dans `data/tarifs_manuels.json`. Les programmes automatiques ne modifient jamais ce fichier. Au chargement, le site (et `check_data.py`) fusionne ces offres avec celles lues automatiquement : une offre déjà présente (même `k` et même `offer`) est complétée champ par champ, sinon elle est ajoutée. Le fichier contient un exemple (`_exemple`) à copier dans `elec`, `gas` ou `duo`. Renseigner `niv: "officiel"`, `nivd` (date de la grille) et `s` (le PDF en source). Pour un nouveau fournisseur, ajouter aussi son abonnement annuel dans `abo_e`, `abo_g` et `abo_g0`.
