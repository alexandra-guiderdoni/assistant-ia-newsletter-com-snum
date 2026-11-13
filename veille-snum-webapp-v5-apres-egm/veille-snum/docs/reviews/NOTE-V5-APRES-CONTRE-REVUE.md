# Veille SNUM V5 : réponse aux contre-exemples de la revue EGM V4

Date : 11 novembre 2026. **Statut : EXPÉRIMENTAL UNIQUEMENT.** Cette note décrit le travail réalisé sur une copie de la V4 fournie, et non un changement du dépôt GitHub ou une nouvelle revue indépendante EGM.

## Références

- Rapport utilisateur : `CONTRE-REVUE-EGM-VEILLE-SNUM-V4.md` et ZIP de preuves.
- Version de départ : archive V4 dont le rapport fournit l'empreinte SHA-256 `5e8cb59d76e4172ce1c256290c1df7af9a6a4b3ca8fd6d68adb5de889b2b68bc`.
- Contrat de production : `SNUM_PAQUET_RENDU_V519` (Collecte V5.23), inchangé.
- Le builder-mail-dsfr n'a pas été modifié.

## Corrections vérifiées sur fixtures

| Constat de la revue V4 | Correction locale V5 | Résultat |
| --- | --- | --- |
| F02 identifiants JSON-LD imbriqués, listes | Récolte de toutes les valeurs d'identité dans les structures pertinentes, exclusion des contradictions | Contradictoires rejetés, fragment de la même page admis |
| F03 challenge en alerte et citation éditoriale | Capture des zones UI visibles indépendamment du corps, pas de détection de challenge par substring dans les paragraphes | Alerte refusée, citation conservée |
| F03 paywall `WebPage` | Restriction du nœud `WebPage` désignant la page active, indépendamment du nœud éditorial | Paywall principal rejeté, recommandation secondaire non bloquante |
| F04 sitemap interdit via robots | Motif, URL, compteur et statut partiel | Pas de `ready` sans réserve sur ce cas |
| F05 enfant sitemap en échec | Exceptions gérées enfant par enfant, poursuite du suivant dans le budget, inventaire des sitemaps non visités | Deuxième enfant réellement tenté dans la simulation |
| F09 redirection après échéance | Deadline transmise à `RestrictedRedirect`, vérifiée avant réémission, timeout restant recalculé | Un seul dispatch avec 302 après l'échéance simulée |
| F09 budget masqué par erreur robots | `BudgetExceeded` propagée | Statut `skipped_budget`, pas d'erreur robots fictive |
| R01 provenance manquante | Dates et heure UTC, version et SHA-256 du collecteur dans le rapport ; fichier nommé d'après le rapport figé | Rapport exploitable même sans Albert |
| S01/S03 persistance race | Web Locks V5 pour toutes les mutations, epoch anti-opérations périmées, suppression implicite conditionnelle, nouvelle clé V5 | 16 tests Node verts en contexte simulé |

## Choix de sécurité pour le secret

**Le serveur interdit désormais la persistance par défaut.** Pour la démonstration locale avec clés fictives, `SNUM_ALLOW_LOCALSTORAGE=1` permet une case à cocher d'opt-in. Même alors, la persistance requiert `navigator.locks` ; sans cette API, aucune nouvelle entrée n'est enregistrée. Le code tente de supprimer les entrées V4/V5 lorsque la politique serveur l'interdit.

L'option conserve néanmoins des secrets **en clair**, lisibles par les scripts de même origine et lors d'une éventuelle reprise du port par un autre service local. Les Web Locks ne coordonnent pas les anciennes pages V4 ni les programmes non coopérants. Fermer les anciennes pages ; si l'effacement échoue, supprimer les données du site via les réglages du navigateur. Le bouton n'annule ni une requête Albert déjà envoyée, ni une clé configurée dans l'environnement Python, ni le jeton chez le fournisseur.

Cette option n'est **pas homologuée** pour un poste ministériel. Une décision de sécurité doit préciser si elle doit être entièrement interdite en usage institutionnel ou remplacée par un mécanisme agréé. Aucune clé authentique n'a été utilisée pour tester la V5.

## Résultats reproductibles

- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v` : **40 tests Python réussis**.
- `node --test tests/test_storage.cjs` : **16 tests JavaScript réussis**, avec faux stockages, onglets et verrous Web Locks simulés.
- Contrat consommateur : **16 conversions réussies** avec le code du convertisseur distribué fourni dans le dossier de preuves EGM, pour 0, 1, 2, 3, 4, 5, 7 et 42 articles en JSON brut ou enveloppé. Le vrai parseur, adapter, modèle et rendu ont été exécutés dans Node. Ce n'est pas une recette interactive.
- SHA-256 de `sources.json` **inchangé** : `292ea241e892829b75e1b0f71af4f9396bd48ddb56a0bb3739579f6eafdd76c9` ; 14 sources dont une interne désactivée.
- `node --check veille_snum/app.js` et compilation Python : sans erreur.
- Un essai Chromium headless a été **bloqué par l'environnement** : `ERR_BLOCKED_BY_ADMINISTRATOR` à l'ouverture du serveur sur loopback. Aucun résultat de navigateur natif n'est revendiqué.

## Limites et prochain point de décision

La validation est locale et hors Internet. Restent **non vérifiés** : collecte des treize sources publiques réelles, droits de réutilisation de la presse, modèle/clé/quota Albert, TLS/proxy du réseau cible, concurrence native multi-onglets et politique CSP effective, lancement macOS, navigation clavier, zoom/reflow, VoiceOver/NVDA et examen humain source-fait avant diffusion.

Avant tout pilote, faire une recette contrôlée sur poste autorisé, fixer les seuils métier de rappel/précision, puis comparer quatre semaines de publications de référence indépendantes. N'introduire ni Tavily, ni SearXNG, ni GDELT tant que les pertes de découverte ne sont pas mesurées.

**Aucune approbation de pilote ou de diffusion institutionnelle n'est implicite dans les tests verts.**
