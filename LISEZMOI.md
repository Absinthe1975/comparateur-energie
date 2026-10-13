# Comparateur énergie : mise à jour automatique des prix

Ce dossier contient le site (`index.html`), ses données (`data.json`) et le programme qui les met à jour une fois par mois avec l'aide d'une IA.

## Comment ça marche

1. Chaque jour du 1er au 10 du mois, puis chaque lundi (ou quand vous le lancez à la main), GitHub exécute `scripts/update_prices.py`.
2. Le programme lit les pages listées dans `sources.json`.
3. Pour chaque offre, l'IA (Gemini, gratuite) renvoie les chiffres **et la phrase exacte où elle les a trouvés**.
4. Le programme refuse un chiffre si la phrase n'est pas dans la page, si le chiffre n'est pas dans la phrase, s'il est hors d'une fourchette plausible, ou s'il s'écarte trop de l'ancienne valeur (alors il est seulement signalé).
5. Les changements acceptés sont mis dans `data.json` avec la date, et GitHub ouvre une **demande de fusion** (pull request) avec un rapport. **Rien n'est publié tant que vous ne l'avez pas acceptée.**
6. Le site lit `data.json` à chaque visite. S'il ne peut pas le lire, il utilise les données intégrées à `index.html`.

## Mise en route (une seule fois)

1. Créez un dépôt **public** sur GitHub et envoyez-y tout le contenu de ce dossier, y compris le dossier caché `.github`.
2. Créez une clé gratuite sur aistudio.google.com/apikey (compte Google, pas de paiement demandé), puis dans le dépôt : Settings, Secrets and variables, Actions, New repository secret. Nom : `GEMINI_API_KEY`.
3. Dans Settings, Actions, General, Workflow permissions : choisissez « Read and write permissions » et cochez « Allow GitHub Actions to create and approve pull requests ».
4. Pour publier le site : Settings, Pages, « Deploy from a branch », branche `main`, dossier `/ (root)`.
5. Premier essai : onglet Actions, « Mise à jour des prix », Run workflow. Lisez le rapport dans la demande de fusion qui apparaît.

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


## Prix de l'eau par commune (une fois par an)

Le fichier `communes-cp.json` (communes par code postal, avec le prix de l'eau) est fabriqué par `scripts/build_eau.py` à partir de :
- la base officielle des codes postaux (data.gouv.fr, fichier `019HexaSmal.csv`),
- les fichiers SISPEA « tarifs eau potable » et « tarifs assainissement collectif » (services.eaufrance.fr/pro/telechargement), feuille « Zones tarifaires » exportée en CSV UTF-8 sous les noms `tarifs_AEP_<année>.csv` et `tarifs_AC_<année>.csv`,
- les feuilles « Détail tarifaire » des mêmes fichiers, exportées en `detail_AEP_<année>.csv` et `detail_AC_<année>.csv` (abonnement = part fixe),
- éventuellement `zones_gn.json` (orthographe des communes).

Commande : `python3 scripts/build_eau.py eau-sources communes-cp.json 2025`

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
