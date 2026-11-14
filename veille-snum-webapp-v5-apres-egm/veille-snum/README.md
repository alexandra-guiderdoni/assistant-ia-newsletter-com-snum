# Prototype de webapp Veille SNUM V5 : expérimental

Application locale Python + navigateur permettant de lancer une première recherche Web sur 14 sources fixes (13 publiques et 1 interne volontairement désactivée), d'obtenir un rapport et, avec Albert API configurée, de produire un paquet JSON `SNUM_PAQUET_RENDU_V519` destiné au convertisseur SNUM existant du builder-mail-dsfr.

**Ceci n'est pas encore une recette de couverture des 14 sites, ni une application pouvant fonctionner hors ligne pour effectuer la collecte.** La contre-revue EGM V4 conclut « EXPÉRIMENTAL UNIQUEMENT » ; la V5 corrige les cas adverses reproduits hors réseau, mais ne constitue pas une autorisation d'utiliser une vraie clé ministérielle. Les sitemaps, HTML et dates restent à tester sur chaque site.

## Version 6 : couverture réelle des 14 sources (11 novembre 2026)

Mesurée par une collecte réelle sans Albert, du 4 au 11 novembre 2026 : 49 candidats issus de 9 sites, aucune erreur technique, contre 10 candidats issus de 3 sites en V5.

- Pages d’accueil jusqu’à 2,5 Mo (Le Monde) et plans de site jusqu’à 3 Mo.
- 15 pages visitées par site au lieu de 6, les plus récentes d’abord, d’après la date du plan de site ou de l’adresse ; cette date oriente seulement la visite et ne prouve jamais la publication.
- Date visible acceptée en dernier recours : une seule mention « Publié le », ou une date placée juste sous le titre principal. Les métadonnées restent prioritaires.
- Lien court WordPress (`/?p=123`) reconnu comme identité de l’article (Presse Bercy) ; titre `h1` retenu quand `og:title` n’est que le nom du site.
- Budget Albert distinct de 240 secondes, ouvert après la découverte.
- Sites protégés contre les robots signalés `blocked` : economie.gouv.fr et Légifrance (HTTP 403), vie-publique.fr (vérification JavaScript et cookies), Le Monde (page « Client Challenge »). Aucun contournement n’est tenté ; ces sites restent couverts par la Collecte de l’Assistant.
- Le lanceur macOS utilise le port 8766 : sur un poste où une autre application a enregistré un service worker sur `127.0.0.1:8765`, cette adresse affiche l’autre application.

- Albert : deux appels simultanés (quatre provoquaient 30 refus sur 43), attente du délai demandé sur un refus 429 ou 503, délai de 30 secondes par appel, seconde tentative après un délai dépassé ou une réponse rejetée, avec le motif du rejet. Les erreurs indiquent le code HTTP, sans donnée sensible. Consigne précisant le périmètre du SNUM, les exclusions (commerce, marchés financiers, emploi privé, produits grand public hors IA) et le classement en ia des annonces de modèles et d’outils d’IA.
- Alertes : « Sources non couvertes » ne cite plus les sources lues mais plafonnées ; sources protégées et source interne ont leur propre alerte.
- Résumés en français imposés par la consigne ; un résumé majoritairement en anglais est rejeté (`LANGUE_NON_FRANCAISE`) et redemandé une fois avec ce motif.
- Articles retenus regroupés sous leur thématique (Numérique, Intelligence artificielle, Commande publique, Ressources humaines, Bercy), avec leur nombre.
- Sélection éditoriale : seuls les deux premiers articles de chaque thématique, les plus récents, sont cochés par défaut ; s’il en reste d’autres, le paquet est à mettre à jour avant le téléchargement. Chaque article retenu peut être coché, décoché ou reclassé ; un article écarté comme hors thématique peut être ajouté, Albert rédigeant alors son résumé dans la thématique choisie (texte gardé côté serveur, jamais renvoyé par le navigateur). « Mettre à jour le paquet » reconstruit le JSON côté serveur (`/api/packet`) : numérotation, tri, essentiels, alertes, contrôle des 14 domaines et des règles V519. Le téléchargement reste bloqué tant que la sélection modifiée n’est pas revalidée.
- Repêchage étendu aux candidats non résumés faute de temps et aux échecs Albert, avec leur motif. Le résultat et la sélection sont conservés dans l’onglet (`sessionStorage`, effacé à sa fermeture, sans clé ni listes d’URL non visitées) et restaurés après un rechargement de la page.
- Budget Albert porté à 360 secondes ; un génitif anglais (« Anthropic's ») suffit à rejeter un résumé non français.
- Interface sur les composants officiels DSFR 1.15.4 (`fr-header` neutre sans bloc marque, `fr-skiplinks`, `fr-input-group`, `fr-checkbox-group`, `fr-select`, `fr-btn`, `fr-accordion`, `fr-alert`, `fr-footer`), embarqués dans `veille_snum/dsfr/` pour un fonctionnement hors ligne : 87 fichiers copiés du paquet officiel par `outils/embarquer_dsfr.py`, version et empreintes dans `MANIFEST.json`. Politique de sécurité ouverte aux seules polices et icônes locales.
- RGAA 11.1 : chaque case et chaque menu créé par le script a une étiquette visible liée par `for`/`id` (« Garder », « Thématique »), complétée du titre de l’article en texte réservé aux lecteurs d’écran ; le focus revient sur le champ modifié. Description de page (`meta description`) ajoutée.
- Grille DSFR : colonne de lecture centrée (`fr-grid-row--center`, `fr-col-lg-10`), dates sur trois colonnes et champs Albert sur deux à partir de 768 px, statistiques en liste-grille (chiffre en `fr-h4` puis libellé, deux colonnes sur mobile, trois sur bureau), case et thématique de chaque article sur une même ligne alignée par le bas, articles espacés de 24 px (`fr-mb-3w`). Un test refuse toute classe `fr-*` absente du DSFR embarqué (`fr-col-auto` et `fr-background-alt--grey` n’existent pas en 1.15.4).
- Formulaires : mention « Sauf mention contraire, tous les champs sont obligatoires », champs Albert marqués « (facultatif) », validation différée des dates (contraintes posées au premier envoi, état `fr-input-group--error`, message `fr-message--error` relié par `aria-describedby`, `aria-invalid`, focus sur le premier champ en erreur, contrôle de l’ordre et des 61 jours) ; invite « Sélectionner une thématique » et état d’erreur pour le repêchage.
- Suivi de l’avancement : `/api/progress` et message mis à jour pendant la collecte (« Recherche sur les sites : 5/13 », « Résumés Albert : 12/43 »).

Tests : 130 Python et 19 Node réussis hors réseau. Recette avec une vraie clé Albert le 11 novembre 2026, avant parallélisme : 23 articles conformes au V519, 11 candidats non résumés faute de temps.

## Sans Python : la page GitHub Pages

https://alexandra-guiderdoni.github.io/assistant-ia-newsletter-com-snum/ offre le même usage sans serveur local : la collecte et Albert passent par GitHub Actions (tâches « Publier le paquet Veille SNUM » et « Repêcher un candidat Veille SNUM »), la sélection et l'export JSON V519 se font dans le navigateur. Lancer une collecte, une rédaction de résumés ou un repêchage depuis la page demande le jeton GitHub partagé par l'équipe : procédure, permissions, sécurité et dépannage dans [docs/jeton-github.md](docs/jeton-github.md), liée depuis la page.

La collecte se fait en deux temps :

1. « Lancer la collecte » (mode `titres`) explore les treize sites publics sans Albert, puis publie les titres trouvés : trois à quatre minutes (estimation, ce mode n'a pas encore été mesuré en réel). La page se vide dès que GitHub accepte la demande ; la collecte précédente, si elle avait été résumée, reste dans les archives.
2. La personne coche les titres à garder (un par un, ou « Tout garder » pour une source), impose une thématique ou laisse « Albert choisit », puis « Rédiger les résumés » (mode `resumes`). Albert ne résume que ces titres, deux à la fois : une à deux minutes pour dix articles, puis environ deux minutes de publication. Albert s'arrête après six minutes : au-delà d'une trentaine d'articles, les derniers peuvent rester sans résumé. Le paquet V519 est alors archivé puis publié : si l'archivage échoue, rien n'est publié et la page l'annonce. Un paquet sans article est publié sans être archivé.
3. Sélection fine habituelle : garder, écarter, changer de thématique, repêcher un candidat écarté, puis copier le JSON dans l'atelier de courriels.

Les titres non gardés, jugés hors thématique, non résumés faute de temps ou en échec rejoignent l'accordéon « Candidats écartés », avec leur motif ; chacun reste repêchable. La case « Collecte complète en une fois » garde l'ancien déroulement (mode `collecte`, cinq à neuf minutes selon le nombre d'articles : mesuré sur quatre collectes du 13 novembre 2026). Le mode `page seule`, lancé depuis GitHub, republie la page avec les fichiers en ligne, sans Albert ni archive.

Ce que la page vérifie pour vous :

- le fichier `etat-collecte.json` porte le numéro de l'exécution qui l'a publié. Après un lancement, la page attend que le site serve bien ce numéro avant d'afficher le résultat : GitHub Pages garde ses fichiers dix minutes en cache et peut servir un court moment l'ancienne version ;
- une collecte déjà en cours (autre personne, autre onglet, page rechargée) est signalée à l'ouverture et avant tout nouvel envoi ;
- si le suivi se perd (jeton expiré, réseau), la tâche continue sur GitHub : recharger la page quelques minutes plus tard, sans relancer ;
- le second temps refuse des titres déjà résumés ou remplacés : la page se recharge et l'explique. Ce refus s'appuie sur le rapport en ligne et, pour ne pas dépendre du cache du site, sur l'index des archives lu par git (champ `titres_started_at` de chaque archive).

Chaque collecte résumée est archivée sur la branche publique `donnees-veille` (`collectes/<édition>_<run>/` : paquet, candidats écartés, rapport ; index `collectes/index.json`), avec les résultats de repêchage (`repechages/`). Des titres jamais résumés ne sont pas archivés. La page [archives.html](https://alexandra-guiderdoni.github.io/assistant-ia-newsletter-com-snum/archives.html) liste les archives et rouvre une ancienne collecte dans la page de sélection, sans jeton ; une archive peut mettre jusqu'à cinq minutes à y apparaître (cache de raw.githubusercontent.com).

Tests de la page : `node --test tests/test_pages_*.cjs`. Parcours de bout en bout dans Chromium, GitHub simulé et vrai code serveur : [tests/navigateur/](tests/navigateur/README.md). Rapports de l'audit du 14 novembre 2026 et points laissés ouverts : [docs/reviews/2026-11-14-audit-shipguard/](docs/reviews/2026-11-14-audit-shipguard/README.md).

## Démarrer

Python 3.10+ ; bibliothèque standard uniquement. Aucune installation de package nécessaire. Sur macOS, double-cliquer `Lancer Veille SNUM.command` (sous réserve des règles de sécurité du poste) ; la fenêtre Terminal reste ouverte pendant l’utilisation. En cas de blocage macOS, suivre les procédures autorisées sans contourner la politique du poste.

```bash
# Depuis le dossier contenant veille_snum/
python3 -m veille_snum.web
# puis ouvrir http://127.0.0.1:8765/
```

Le formulaire fonctionne sans Albert et permet d'inspecter les sources et les candidats, puis de télécharger le rapport de collecte. Pour générer le JSON lors d’un lancement par double-clic, ouvrir « Connexion à Albert API » et saisir temporairement le jeton ; le modèle `openweight-large` est prérempli et reste remplaçable. Le jeton n’est jamais inclus dans les rapports. Par défaut, il n’est pas enregistré et le champ est vidé après la collecte. La case à cocher de conservation localStorage est **désactivée par défaut par le serveur**, qui tente aussi d'effacer les anciennes entrées du stockage sous cette politique. Pour une démonstration personnelle avec une clé factice uniquement, lancer `SNUM_ALLOW_LOCALSTORAGE=1 python3 -m veille_snum.web`. L'enregistrement demeure explicite, en clair, et exige un navigateur prenant en charge la Web Locks API. Ne pas activer sur un poste institutionnel sans validation de sa politique de sécurité. **L'export V519 nécessite une clé Albert**, fournie dans l’interface ou par variable d’environnement ; sans elle, le bouton de téléchargement reste désactivé. Le modèle est choisi dans cet ordre : champ de l’interface, puis `ALBERT_MODEL`, puis `openweight-large`.

```bash
export ALBERT_API_KEY='votre-jeton-personnel'
export ALBERT_MODEL='identifiant-retourné-par-GET-/v1/models'  # facultatif, remplace openweight-large
python3 -m veille_snum.web
```

Ne jamais copier la clé dans un fichier HTML, commit GitHub, log ou copie d'écran. Le service se limite à `127.0.0.1`; son endpoint n'est pas fait pour Internet. Albert reçoit les extraits publics des articles retenus, pas le contenu de la source interne.

## Utilisation

1. Saisir date d'édition et période (bornes incluses).
2. Cliquer sur « Lancer la collecte » ; consulter l'état de chaque source et les exclusions.
3. Si Albert est configuré, relire les fiches et télécharger le JSON V519.
4. Ouvrir `builder-mail-dsfr/app/distribution/snum.html`, coller le paquet puis exporter la composition vers le builder.

Les contenus payants et les publications sans date de publication certaine sont exclus. Une source indisponible et une source sans candidat doivent être distinguées. La page ne transmet ni ne publie de newsletter.

## Tests

```bash
python3 -m unittest discover -s tests -v
node --test tests/test_storage.cjs
```

`docs/designs/veille-snum.md` : proposition et invariants ; `docs/reviews/veille-snum-egm-pre-review.md` : critique préparatoire, pas revue indépendante.

## Publication dans les dépôts existants

Le prototype est livré dans un ZIP à intégrer à la racine de `assistant-ia-newsletter-com-snum` sur une **branche dédiée**. Les dossiers `veille_snum/`, `docs/designs/`, `docs/reviews/` et le fichier `tests/test_veille_snum.py` sont nouveaux : aucun outil de rendu ni prompt historique n'est remplacé. Refaire les tests du dépôt d'origine avant toute fusion. Ce dossier ne contient aucun jeton Albert et n'ouvre aucun tunnel réseau.

Une contre-revue indépendante est préparée dans `docs/reviews/PROMPT-CONTRE-REVUE-EGM.md`.

## Clé Albert et stockage local optionnel

La case « Mémoriser la clé et le modèle » est **désactivée** tant que `SNUM_ALLOW_LOCALSTORAGE=1` n'est pas explicitement fourni au serveur. Dans ce mode d'expérimentation, elle reste décochée par défaut ; la Web Locks API sérialise lecture/comparaison/écriture/suppression entre onglets V5 de même origine. Sans Web Locks, l'option reste inutilisable. Les valeurs sont conservées en clair sous `veille-snum:albert:v2` dans le stockage associé à `http://127.0.0.1:8765`. Le nouveau code tente de retirer l'ancienne entrée V4 (`veille-snum:albert:v1`) lorsqu'il en découvre une et que la persistance est autorisée. Fermer tous les onglets V4 : leurs écritures ne respectent pas le nouveau verrou. Le bouton « Effacer » supprime l'entrée V5 et l'ancienne V4 dans la mesure où le stockage le permet. Décocher la case supprime la persistance tout en conservant les valeurs du formulaire pour l'appel courant.

**Limite de sécurité :** le localStorage n'est pas chiffré par l'application. Les Web Locks coordonnent seulement les onglets coopérants de même origine : ils ne protègent pas contre une application locale malveillante reprenant le même port, une ancienne V4 ouverte, un navigateur compromis, une extension ou un utilisateur du profil. Les scripts exécutés sur la même origine et toute personne pouvant accéder au profil du navigateur peuvent potentiellement lire le jeton. `localhost:8765` et `127.0.0.1:8765` ont des stockages séparés. Ne pas l'utiliser sur un poste partagé ou institutionnel sans validation de la politique de sécurité ; préférer un gestionnaire de secrets autorisé ou le Trousseau macOS. La clé n'est jamais incluse dans les rapports ni les exports, mais elle est transmise au serveur Python local pour appeler Albert.

## Corrections V5 à partir des preuves de la contre-revue V4

- **F02** : inspection exhaustive des identifiants JSON-LD `url`, `@id` et `mainEntityOfPage`, y compris objets et listes. Les contradictions empêchent l'admission.
- **F03** : détection des challenges visibles dans les alertes de la page, sans transformer une citation du message dans un article en blocage ; restriction `isAccessibleForFree:false` vérifiée sur le nœud `WebPage` principal.
- **F04/F05** : robots refusant un sitemap = source partielle ; traitement indépendant des sitemaps enfants, inventaire de leurs échecs et des éléments non visités.
- **F09** : échéance portée jusque dans le gestionnaire des redirections HTTP de collecte ; timeout recalculé ; `BudgetExceeded` n'est plus transformée en erreur de robots.
- **R01** : `edition_date`, `window_start`, `window_end`, heure UTC et empreinte/version du collecteur dans le **rapport uniquement**, y compris sans Albert. Nom du rapport issu du résultat, pas des champs éventuellement modifiés.
- **S01/S03** : champs effacés même si la suppression persistante échoue, avertissement exact ; mémorisation **off par défaut côté serveur**, option V5 uniquement avec Web Locks et opt-in explicite, sans repli non atomique. Nouvelle clé de stockage distincte de V4.
- **Interopérabilité** : aucune modification des 14 sources, des cinq rubriques, de V519 ou du builder. 16 chemins de conversion contrôlés avec le convertisseur distribué fourni dans les preuves EGM.

**Tests exécutés hors réseau :** 40 Python, 16 Node, 16 conversions V519 (0/1/2/3/4/5/7/42 articles, JSON brut/enveloppé). Tentative Chromium native : refus d'accès à loopback (`ERR_BLOCKED_BY_ADMINISTRATOR`) ; ce n'est pas un défaut applicatif démontré.

**Statut : EXPÉRIMENTAL UNIQUEMENT.** Les tests navigateur réel, macOS, VoiceOver/NVDA, accès Albert/TLS/proxy et la comparaison du rappel sur quatre semaines restent ouverts. Ne pas utiliser de vraie clé ou de contenu institutionnel dans cette version sans décision de sécurité et recette autorisée.

## Historique : modifications V4 après contre-revue EGM

- Dates JSON-LD contradictoires et dates provenant d'annexes rejetées (F02).
- Détection de blocage dans des titres visibles et exclusion conservatrice des paywalls déclarés (F03).
- Erreurs de sitemap signalées dans les compteurs, état partiel et alerte V519 (F04).
- Listes des URL non visitées et des entrées de sitemaps coupées dans le rapport, hors du paquet V519 (F05).
- Deadline vérifiée avant toute requête HTTP de collecte ; délai global toujours souple (F09).
- JavaScript distinct, CSP sans scripts inline, et erreur d’effacement du stockage honnêtement signalée (S01/S02).
- Détection d’effacement/modification du secret dans un autre onglet par `storage` et vérification du stockage juste avant écriture (S03). Ne garantit pas une atomicité parfaite des écritures concurrentes.
- Un formulaire dont les dates sont inversées désactive les exports précédents.

**Contrôles historiques V4** : 28 tests Python et 9 tests JavaScript réussis, sans réseau externe. Le test HTTP passe sur loopback pour Host/Origin, contenus et CSP. Une tentative de navigation Chromium vers loopback a été bloquée par l’environnement (`ERR_BLOCKED_BY_ADMINISTRATOR`) ; la recette navigateur réelle, VoiceOver/NVDA, macOS, la collecte des 13 sites et Albert restent à faire sur poste autorisé. La V4 ne doit pas être déclarée prête au pilote sur cette seule base.

**Sécurité localStorage** : la clé reste lisible par les scripts de même origine. Le bouton « Effacer » supprime uniquement l’entrée de cette origine, pas une éventuelle clé définie côté Python, et ne révoque pas le jeton Albert. Valider la politique de sécurité du poste avant toute persistance ; par défaut ne pas activer cette option.

Rapport : `docs/reviews/NOTE-V4-APRES-CONTRE-REVUE.md`.

Voir aussi `docs/reviews/NOTE-V5-APRES-CONTRE-REVUE.md` et `docs/reviews/PROMPT-CONTRE-REVUE-V5.md`.
