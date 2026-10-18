# Rapport de recette Newsletter SNUM V5.23

## Verdict

`GO TECHNIQUE BEST EFFORT` pour le parcours réel en deux conversations :
`Collecte avec Web → JSON V519 → Rendu HTML`.

Le chaînage ne demande plus de chat Web intermédiaire, de requête à recopier ni de
commande de reprise. La recette a aussi validé le cas sans article : le JSON reste
transmissible et Rendu produit un HTML d’alerte au lieu de répondre `A_COMPLETER`.

Ce verdict ne signifie pas que la recherche garantit des articles. Le Web de
l’Assistant reste non déterministe et le contrôle éditorial métier demeure requis.

## Configuration testée

- date de recette : 18 octobre 2026 ;
- branche : `stabilisation/v5.23` ;
- période : du 11 octobre 2026 au 17 octobre 2026 inclus ;
- date d’édition : 18 octobre 2026 ;
- Projet Collecte : `Newsletter SNUM - Collecte - v5.23.6` ;
- Projet Rendu : `Newsletter SNUM - Rendu HTML - v5.23.6` ;
- Web activé dans Collecte et désactivé dans Rendu.

## Parcours réel exécuté

1. Envoi de `DATE_EDITION` et `PERIODE` dans une conversation Collecte neuve.
2. Recherche Web composite lancée automatiquement dans la même conversation.
3. Production directe d’un paquet V519 encadré par ses deux marqueurs.
4. Copie du paquet dans une conversation Rendu neuve.
5. Production directe d’un unique bloc HTML et des contrôles finaux.

## Preuves observées

### Collecte

La conversation Collecte a consulté 51 sources et a répondu directement avec :

- `schema_version=SNUM_PAQUET_RENDU_V519` ;
- `edition_date=2026-10-18` ;
- `window_start=2026-10-11` et `window_end=2026-10-17` ;
- `articles=[]` ;
- trois alertes `watch` expliquant l’absence d’article, les rubriques vides et le
  nombre insuffisant de sources ;
- `SNUM_PAQUET_RENDU_V519_END`, puis `PAQUET_RENDU_PRET`.

Aucune requête à recopier, commande `CONTINUER` ou normalisation manuelle n’a été
nécessaire.

Conversation :
<https://assistant.numerique.gouv.fr/chat/21b02de2-74c0-4a1f-b0df-8adbc14a8015>

### Rendu HTML

Le premier passage du paquet vide avait échoué avec `DONNEES_MANQUANTES` et
`ESSENTIELS_INCORRECTS`. La cause était double : le prompt ne déclarait pas assez
explicitement le paquet vide valide et le validateur local numérotait à la fois le
bloc vide et `À surveiller` en section 01.

Deux sorties intermédiaires ont ensuite produit le HTML mais omis le lien interne
vers `#surveiller`. Une substitution exacte de `@@NAVIGATION@@` a été ajoutée avant
le troisième et dernier essai.

Après correction, une conversation Rendu neuve a produit :

- `## HTML COMPLET` en première ligne ;
- un seul bloc de code de `<!doctype html>` à `</html>` ;
- un seul `h1` et aucun marqueur `@@` ;
- `Collecte à compléter` en section 01 ;
- `À surveiller` en section 02 avec les trois alertes du paquet ;
- le lien `À surveiller` vers `#surveiller`, suivi du lien `Archives` ;
- la modale après le footer et DSFR 1.15.2 ;
- `État : HTML_CANONIQUE_PRODUIT - contrôle métier requis`.

Conversation :
<https://assistant.numerique.gouv.fr/chat/7fc5a0bc-1099-4891-92e1-1d78ff490854>

## Limites

- Une première exécution du même créneau avait trouvé des articles mais produit des
  formats de dates non conformes. Le contrat de dates a été renforcé avant la recette
  finale.
- La recette finale n’a retenu aucun article malgré 51 sources consultées. Elle
  prouve le chaînage best effort, pas la complétude éditoriale de la collecte.
- La sélection des sources et leur qualité restent à vérifier par le métier.
- Le cas vide a nécessité une valeur de navigation explicite ; une consigne
  sémantique seule a été ignorée deux fois par le modèle.
- Les contrôles locaux déterministes couvrent la structure ; ils ne remplacent pas
  le comportement réel de l’Assistant.

## Contrôles locaux

- 39 tests `unittest` réussis ;
- Ruff réussi ;
- `python3 scripts/build_split_kit.py --check` retourne `KIT_DECOUPLE_OK` ;
- `git diff --check` réussi ;
- prompt Collecte : 3 562 caractères ;
- prompt Rendu : 3 962 caractères ;
- six ressources téléversables sous 4 500 caractères ;
- contenus des deux ZIP identiques aux fichiers actifs.

## Décision

Le parcours à conserver comporte exactement deux conversations. Le mode sans
article est une sortie nominale dégradée, visible dans le JSON et dans le HTML. Une
indisponibilité technique du Web ou un paquet réellement invalide restent des motifs
d’arrêt avec `A_COMPLETER`.
