# Proposition technique : webapp de collecte SNUM

État : prototype **V5 expérimental**, non validé sur poste ou en production. Date : 11 novembre 2026.

## Problème et expérience cible

L'Assistant DINUM produit aujourd'hui un paquet `SNUM_PAQUET_RENDU_V519`. Le métier souhaite choisir les dates d'une édition dans une webapp de type builder-mail-dsfr, exécuter une recherche ciblée sur **14 sources fixes** et télécharger ce même paquet sans abonnement à une API de recherche. Le convertisseur SNUM présent dans `builder-mail-dsfr/app/distribution/snum.html` reste inchangé.

## Non négociable

- Préserver les cinq rubriques `numerique`, `ia`, `commande`, `rh`, `bercy`.
- Dates de publication exactement comprises dans les bornes incluses ; jamais une date de mise à jour ou de sitemap comme preuve.
- URL HTTPS canoniques et uniques, identifiants `U01...UN`, ordre date décroissante puis rubrique puis URL.
- Trois essentiels exactement si au moins trois articles ; sinon zéro.
- `fact` ≤ 25 mots ; `takeaway` et `snum_interest` ≤ 15 mots ; 3 à 5 mots-clés.
- Rubriques vides et moins de cinq articles signalés par `watch`; paquet vide admissible après recherche exécutée.
- Exporter seulement un paquet conforme au schéma et aux règles de Collecte V5.23.
- Ne pas exposer la clé Albert ou le contenu d'une source interne ; ne pas modifier les rendus existants.

## Décision de portée

1. Webapp statique servie par un **petit serveur local Python** sur `127.0.0.1`, sans serveur extérieur ni compte supplémentaire. Elle n'est pas un fichier HTML entièrement autonome pour la collecte, en raison des règles CORS des sites tiers et du secret Albert.
2. Découverte initiale par pages d'accueil et sitemaps, extraction HTML et métadonnées sur les seuls domaines autorisés. Résultats non prouvés = exclus ; les erreurs restent visibles dans le journal.
3. Albert API (`/v1/chat/completions`, `json_object`) classe et rédige chaque source admissible. Le modèle et la clé sont fournis par variables d’environnement ou saisis temporairement dans la webapp locale. Par défaut, la clé n’est pas persistée et le champ est vidé après la collecte ; la mémorisation en clair dans localStorage est **désactivée côté serveur par défaut** et ne peut être activée pour une démonstration qu'avec `SNUM_ALLOW_LOCALSTORAGE=1`, consentement explicite et Web Locks API. Le code V5 sérialise les écritures/suppressions entre onglets coopérants sous la même origine, sans garantir la sécurité des anciennes versions ou la persistance sur un poste compromis. L'usage sur poste ministériel n'est pas autorisé par cette spécification.
4. Validation Python finale indépendante du modèle ; aucun remplissage fictif.
5. Pas de RSS, pas de Tavily, pas de SearXNG ni GDELT au MVP. Ces secours ne seront ajoutés qu'après mesure de l'absence de couverture.
6. Source interne : emplacement logique conservé, mais **collecte désactivée** dans le prototype public ; activation future uniquement via composant privé sur réseau autorisé et validation de sécurité.
7. Contenu de presse : le pilote doit respecter les conditions d'utilisation et ne traite que du contenu librement accessible ; aucun contournement de paywall ou CAPTCHA. Une revue des droits de réutilisation est requise avant diffusion institutionnelle.

## Interfaces

- `GET /api/info` : configuration non secrète, 14 sources, statut Albert et booléen `secret_persistence_enabled` (désactivé par défaut), jamais de clé.
- `POST /api/collect` : `{ "edition_date":"YYYY-MM-DD", "window_start":"YYYY-MM-DD", "window_end":"YYYY-MM-DD", "albert_api_key":"<facultatif>", "albert_model":"<facultatif>" }` ; renvoie `sources` (statuts), `candidates`, `excluded`, `packet` ou `null`, et `status`.
- Le navigateur permet prévisualisation, vérification des exclusions et téléchargement local du paquet seulement si `packet` est présent.
- En cas d'absence de clé Albert, la découverte et son rapport fonctionnent, mais le JSON éditorial n'est pas inventé.

## Risques et contrôles

- **Couverture** : un sitemap n'est pas exhaustif et un `HTTP 200` ne prouve pas la lecture ; chaque source a un état (collectée / erreur / non traitée / sans candidat). Comparer sur quatre semaines avec une sélection de référence.
- **Dates** : seules des métadonnées explicitement liées à une publication sont admissibles ; `lastmod`, date d'événement ou `dateModified` sont exclues. Les identités JSON-LD contradictoires en objets/listes et les dates d’annexes masquées sont rejetées. Une preuve de date fournie par le site n’est pas une garantie absolue de justesse.
- **Accessibilité** : test manuel clavier, VoiceOver et NVDA sur l'application réellement servie ; séquences de progression et erreurs dans des régions `role=status/alert`.
- **Quota Albert** : identifier le modèle via configuration et vérifier `/v1/me/info` hors pilote ; aucun prix ou quota garanti.
- **Sécurité** : domaines en liste blanche, HTTPS, interdiction des redirections Albert, liaison localhost, CSP `script-src 'self'` sans script inline, secrets en variables d’environnement ou saisis temporairement. Persistance localStorage désactivée par défaut ; Web Locks et opt-in explicites en expérimentation seulement. Revue spécifique avant tout usage ministériel.
- **Échecs** : le service doit rendre les exclusions et les sources inaccessibles sans prétendre que zéro article signifie zéro publication.

## Tests d'acceptation (MVP)

1. Exactement 14 entrées fixes ; la source interne est marquée non traitée, jamais envoyée à Albert.
2. Page avec date de mise à jour seulement rejetée ; date de publication exacte dans la fenêtre acceptée.
3. Redirection inter-domaine rejetée ; URL hors domaine rejetée.
4. Albert retourne un objet non conforme : article rejeté, sans fait inventé.
5. Paquet conforme au schéma V519 (champs, limites, tri, `essential`, `watch`).
6. Sans configuration Albert : aucune publication présentée comme prête à exporter.
7. Test manuel d'import du paquet généré dans `builder-mail-dsfr/app/distribution/snum.html`.
8. Tests d'accessibilité réels et recette métier avant diffusion.

## Décision après mesures

Ajouter un secours de recherche seulement lorsqu'un échantillon de référence établit un manque de couverture. Préférer un ciblage par domaine et thème aux requêtes globales. Ne pas annoncer la couverture complète sans preuve.

## Compatibilité

Le paquet V519 est le seul artefact d'interopérabilité ; l'export `dsfr-mail/document` est déjà assuré par le convertisseur dans le dépôt builder. Aucun changement du format du builder ni des prompts historiques n'est prévu.

## Provenance

- `assistant-ia-newsletter-com-snum/01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.23.md`
- `assistant-ia-newsletter-com-snum/03-CONTRAT-PAQUET-RENDU-SNUM-V5.23.md`
- `builder-mail-dsfr/app/snum/adapter.js` et `app/snum/page.js`
- `google/elephant-goldfish-model/docs/designs/architecture.md` ; `skills/egm-brainstorm/SKILL.md` ; `agents/zoom_out.md`.

## Plan V4 : décisions et garde-fous (proposition, pas autorisation de pilote)

| Phase | Fichiers | État de validation | Condition de sortie |
| --- | --- | --- | --- |
| 1. Admissibilité | `veille_snum/core.py`, `tests/test_v4_regressions.py` | Dates contradictoires et annexes rejetées en simulation ; vraie lecture non recettée | Parcours nominal + contradictoire sur pages réelles et test de concordance métier |
| 2. Découverte et budgets | `core.py`, tests Python | Erreurs sitemap affichées comme partiel, deadline vérifiée avant chaque requête ; budget global reste souple | Rapport quantifié de pertes et mesure de rappel |
| 3. Secrets et interface | `app.js`, `index.html`, `web.py`, tests Node/HTTP | Politique serveur opt-in désactivée par défaut ; verrou Web Locks inter-onglets ; pas de persistance sans coordination | Recette native à deux onglets, décision sécurité ministérielle et politique proxy |
| 4. Compatibilité et qualité | `tests/`, builder existant inchangé | Format V519 structurel vérifié ; pas de nouvelle recette builder V4 | Import interactif, rendu, revue de faits, droit de réutilisation |
| 5. Décision | rapport de recette | Expérimental uniquement | Critères métier fixés puis quatre semaines de comparaison, sécurité et accessibilité validées |

### Signification des états

- `checked` : recherche tentée sans erreur technique détectée sur les voies exécutées, **pas une preuve d’exhaustivité**. Un sitemap absent en 404 ne constitue pas en soi une panne.
- `partial` : voie de découverte en erreur, budget local/global, panne d’article ou sitemap tronqué ; les candidats sûrs restent utilisables et une alerte `watch` indique la réserve.
- `error` : absence d’accès exploitable ; `blocked` : accès interdit par robots ou obstacles constatés ; `skipped_budget` : source non tentée faute de temps ; `skipped_internal` : source interne désactivée.
- Rapport `ready` : paquet produit à partir de voies explorées sans erreur technique identifiée (sous réserve de l’examen humain). `partial` : paquet produit avec une réserve ; `needs_albert` : paquet absent faute de configuration ; `unavailable` : exploration insuffisante ; `incomplete` : analyse Albert insuffisante pour exporter.

La durée de 180 secondes est un **budget souple** : il est contrôlé avant de lancer chaque requête de collecte et le timeout de connexion est réduit au temps restant, mais DNS, fermeture des sockets et tâches non interruptibles ne garantissent pas une durée maximale globale absolue. Aucun service de recherche complémentaire n’est inclus.

### Contrat de preuve

Les synthèses sont uniquement **validées structurellement**, sans certification automatique des faits. Les résultats nécessitent une relecture source/fiche et une décision humaine avant diffusion. Les données des 14 sources restent inchangées (13 publiques + 1 interne inactive). Le JSON V519 et les rendus historiques restent inchangés.

## Complément V5 : fermeture des objections de la contre-revue V4 (hors recette)

| Constat | Fichier et règle | Assertion exigée | Résultat local |
| --- | --- | --- | --- |
| F02-R1 | `core.py`, `_ids` | Toute identité JSON-LD imbriquée ou en liste divergente bloque la date ; fragment identique admis | Fixture Python verte |
| F03-R1/R2/R3 | `core.py`, `Page`/`contains_challenge` | Alerte de challenge refusée ; paywall WebPage principal refusé ; citation dans article admise | Fixtures Python vertes |
| F04-R1 | `core.py`, `discover_source` | Refus robots du sitemap => état partiel et URL tracée | Fixture Python verte |
| F05-R1 | `core.py`, `discover_source` | Une panne d'enfant sitemap n'empêche pas l'examen de l'enfant suivant autorisé | Fixture Python verte |
| F09-R1/R2 | `core.py`, `HttpClient`/`RestrictedRedirect`/`robots_allowed` | Aucune réémission après échéance ; budget conservé comme budget | Test urllib et fixtures verts |
| R01 | `core.py`, `collect` et `app.js` | Rapport sans Albert daté, versionné et nommé sur ses paramètres figés | Python + inspection JS |
| S03 | `app.js`, Web Locks | Opérations V5 sérialisées ; mémoire off sans verrou/politique ; conflits non réécrits | Node simulé, non certifié navigateur |

**Frontières non démontrées :** véritables pages sources, conditions de réutilisation, exactitude sémantique d'Albert, compatibilité sécurité du réseau institutionnel, scénario natif multi-onglets/CSP et accessibilité lecteur d'écran. Ces limites empêchent toute transition automatique vers un pilote qualifié.
