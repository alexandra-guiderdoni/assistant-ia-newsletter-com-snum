# Veille SNUM V4 : note de corrections après contre-revue V3

Date : 11 novembre 2026. **Statut : expérimental uniquement.** Cette note est une vérification de corrections locales, **pas une nouvelle contre-revue EGM indépendante**. Aucune vraie clé Albert, aucun contenu interne ni aucune publication n'ont été utilisés.

## Verdict par point

| Point | Action V4 | Preuve | Reste à faire |
| --- | --- | --- | --- |
| F01 | Refus de redirections Albert V3 conservé | Tests du gestionnaire et rapport de la revue V3 | Valider TLS et réseau ministériel |
| F02 | Contradiction JSON-LD et date d'annexe rejetées | Tests de sources simulées | Comparer avec pages réelles, contradictions complexes |
| F03 | Contrôle des titres de blocage et métadonnées; faux positif sur sujet CAPTCHA évité | Tests de challenge, de paywall et de vrai article | Lisibilité complète/CSS/JS à qualifier humainement |
| F04 | Erreurs sitemap distinguées d'un résultat vide | Test 13 sitemaps en timeout et état `partial` | Définir la couverture acceptable sur chaque site |
| F05 | URL écartées par plafonds et sitemaps tracées dans le rapport local | Examen du code + tests existants | Mesurer les pertes et le rappel en continu |
| F06 | `watch` visible, inchangé | Tests V3 + code V4 conservé | Recette clavier/lecteur d'écran |
| F07 | Schéma V519 conservé, 14 sources identiques | Suite Python + SHA-256 sources identique V3 | Revalider dans le convertisseur distribué sur poste |
| F08 | Validation des faits uniquement structurelle | Avertissements inchangés; design explicité | Relecture humaine des faits, instructions malveillantes et droits |
| F09 | Deadline avant chaque nouvelle requête, état/plan précisés | Test horloge simulée; tests HTTP locaux | Durée maximale stricte non garantie; recettes réseau et métier |
| S01 | Messages d'échec persistance/effacement corrigés | Tests stockage en erreur | Vérifier comportements réels navigateur et politiques |
| S02 | JavaScript externe et `script-src 'self'` | Serveur HTTP + CSP, sans inline; tests HTTP | Vérifier CSP/XSS dans navigateur autorisé |
| S03 | Comparaison avant écriture + notification `storage` | Deux contextes JS simulés | Test vrai navigateur multi-onglets; éviter les courses concurrentes résiduelles |

## Épreuves réellement exécutées

- `python3 -m unittest discover -s tests -v` : **28 tests réussis** (config, admissibilité, découverte, budgets, contrat, serveur HTTP loopback).
- `node --test tests/test_storage.cjs` : **9 tests réussis** (opt-in, restauration, effacement, révocation par autre onglet, échecs de stockage).
- HTTP loopback : réponse CSP sans `unsafe-inline` pour JavaScript; script `/app.js` servi; Host externe refusé 403, Origin externe refusée 403, mauvaise Content-Type refusée 415.
- Tentative Chromium : `ERR_BLOCKED_BY_ADMINISTRATOR` sur l'origine loopback de test ; aucune recette visuelle/multionglet en navigateur réel n'est donc revendiquée.

## Périmètre immuable

- `veille_snum/sources.json` conservé octet pour octet, SHA-256 `292ea241e892829b75e1b0f71af4f9396bd48ddb56a0bb3739579f6eafdd76c9`.
- 13 sites publics + 1 source interne désactivée, cinq rubriques identiques.
- JSON SNUM V519; aucune modification du dépôt builder-mail-dsfr ni des rendus HTML/DSFR.
- Aucun Tavily, SearXNG, GDELT ou backend distant.

## Risques ouverts avant pilote

1. **Clé Albert** : la persistance en localStorage reste en clair et soumise à la politique du poste; des écritures simultanées très rapprochées entre onglets ne sont pas une transaction atomique. Par défaut la case reste décochée.
2. **Qualité de collecte** : HTML dynamique, paywalls non déclarés et fausses métadonnées ne sont pas détectés universellement. La couverture réelle des 13 sources publiques n'est pas mesurée.
3. **Budget** : échéance contrôlée avant lancement des requêtes, mais les délais de systèmes externes restent susceptibles de dépasser la borne souple.
4. **Recette** : navigateur réel, clavier, VoiceOver/NVDA, macOS, réseau ministériel, gestion de proxy, modèle/quota Albert, droits de diffusion, faits et import interactif restent à qualifier.

**Décision : aucune vraie clé Albert sur poste ministériel et aucun usage institutionnel autorisé par ces seules corrections.** Le verdict EGM V3 n'est pas levé. Demander une nouvelle contre-revue indépendante sur la V4 et réaliser la recette sur poste autorisé.
