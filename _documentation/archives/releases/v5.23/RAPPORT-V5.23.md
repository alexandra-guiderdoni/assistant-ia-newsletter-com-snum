# Rapport de recette Collecte V5.23

## Verdict

`GO` pour la chaîne best effort du Projet `Newsletter SNUM - Collecte`, depuis le
message initial jusqu’au JSON compatible avec `Newsletter SNUM - Rendu HTML`.

La recette réelle du 17 octobre 2026 a enchaîné les cinq recherches guidées, la
validation des dates et `GENERER_PAQUET` dans une même conversation de l’Assistant.
Le paquet final est un JSON analysable conforme au schéma
`SNUM_PAQUET_RENDU_V519`, avec trois articles datés dans la fenêtre et trois
essentiels. Aucun terminal ni outil externe n’est nécessaire au métier.

Ce verdict ne couvre pas la transformation du paquet en HTML, qui n’a pas été
retestée dans cette recette.

## Configuration testée

- prompt système : `01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.23.md` ;
- ressources : `02-METHODE-COLLECTE-SNUM-V5.23.md` et
  `03-CONTRAT-PAQUET-RENDU-SNUM-V5.23.md` ;
- paramètres : édition du 14 octobre 2026, fenêtre du 3 au 13 octobre 2026 inclus ;
- conversation de preuve :
  `https://assistant.numerique.gouv.fr/chat/46dcbba0-69b8-4467-9e0e-4c8ced8f9036`.

## Séquence exécutée

1. message initial avec `DATE_EDITION`, `PERIODE` et `NUMERIQUE` ;
2. cinq lignes `REQUETE_A_ENVOYER`, validées une à une par le métier ;
3. `VALIDER` ;
4. `GENERER_PAQUET`.

## Résultats observés

### Collecte

- cinq recherches exécutées dans l’ordre : `NUMERIQUE`, `IA`, `COMMANDE`, `RH`,
  `BERCY` ;
- registre cumulatif stable de `U01` à `U05` ;
- trois sources dans la fenêtre : `U01` au 13 octobre, `U04` au 6 octobre et `U05`
  au 3 octobre 2026 ;
- deux sources hors fenêtre conservées dans le registre puis exclues ;
- fin explicite : `COLLECTE_TERMINEE_BEST_EFFORT`, puis
  `REQUETE_A_ENVOYER=VALIDER`.

### Validation

- `SOURCES_VALIDES` contient exactement `U01`, `U04` et `U05` ;
- `SOURCES_EXCLUES` contient exactement `U02` et `U03` ;
- aucune source hors fenêtre n’est passée dans le paquet ;
- fin explicite : `VALIDATION_TERMINEE`, puis
  `REQUETE_A_ENVOYER=GENERER_PAQUET`.

### Paquet JSON

Le contrôle indépendant du dernier bloc émis a réussi sur tous les points suivants :

- marqueurs `SNUM_PAQUET_RENDU_V519_START` et
  `SNUM_PAQUET_RENDU_V519_END` présents ;
- `JSON.parse` réussi ;
- sept clés racine exactes et schéma `SNUM_PAQUET_RENDU_V519` ;
- trois articles, douze champs exacts par article et dates dans la fenêtre ;
- rubriques autorisées `numerique`, `rh` et `bercy` ;
- `snum_interest` textuel, trois à cinq mots-clés par article et exactement trois
  `essential=true` ;
- `watch` est un tableau d’objets `title` et `summary` ;
- fin explicite : `PAQUET_RENDU_PRET`.

## Contrôles locaux

- 65 tests `unittest` réussis ;
- Ruff réussi ;
- `python3 scripts/build_split_kit.py --check` retourne `KIT_DECOUPLE_OK` ;
- `git diff --check` réussi ;
- prompt système : 3 987 caractères, sous la limite de 4 000 ;
- méthode : 3 104 caractères et contrat : 1 938 caractères, sous 4 500 ;
- `README.md` et `NOTICE-V5.23.md` identiques ;
- ZIP Collecte régénéré avec exactement les trois fichiers V5.23.

## Limites et conduite métier

- la recherche Web reste non déterministe : si aucune source n’est visible,
  l’Assistant répond `A_COMPLETER | RECHERCHE_NON_PROUVEE` et le métier relance la
  même requête ;
- le passage à la requête suivante vaut validation métier de la source et de sa date ;
- moins de cinq sources valides ne bloque plus le paquet : l’insuffisance est tracée
  dans `watch` ;
- la recette vérifie l’orchestration et le contrat JSON, pas la qualité éditoriale
  indépendante de chaque source ;
- le Projet `Newsletter SNUM - Rendu HTML` n’a pas été exécuté dans ce delta.

## Conclusion pour la présentation

La Collecte V5.23 est présentable lundi pour le parcours métier convenu : le métier
reste entièrement dans l’Assistant, valide chaque recherche en copiant la commande
suivante, puis obtient un JSON directement transmissible au Projet Rendu HTML.
