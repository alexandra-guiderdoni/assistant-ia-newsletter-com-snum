# Rapport de recette Collecte V5.24

## Verdict

`GO` pour la chaîne best effort du Projet `Newsletter SNUM - Collecte`, depuis le
message initial jusqu’au JSON compatible avec `Newsletter SNUM - Rendu HTML`, à la
condition que le métier suive la séquence fixe des cinq recherches.

La recette réelle du 17 octobre 2026 a atteint `PAQUET_RENDU_PRET` dans une seule
conversation de l’Assistant. Le paquet final est un JSON analysable conforme au schéma
`SNUM_PAQUET_RENDU_V519`, avec trois articles datés dans la fenêtre et trois
essentiels. Le métier n’a besoin que de l’Assistant.

La prochaine requête proposée par le modèle n’est pas une source de vérité : elle a
répété `RECHERCHE_IA` une fois pendant la recette. Le métier doit suivre l’ordre fixe
`NUMERIQUE → IA → COMMANDE → RH → BERCY`, puis envoyer `VALIDER` et
`GENERER_PAQUET`.

Ce verdict ne couvre pas la transformation du paquet en HTML, qui n’a pas été
retestée dans cette recette.

## Configuration testée

- prompt système : `01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.24.md` ;
- ressources : `02-METHODE-COLLECTE-SNUM-V5.24.md` et
  `03-CONTRAT-PAQUET-RENDU-SNUM-V5.24.md` ;
- paramètres : édition du 14 octobre 2026, fenêtre du 3 au 13 octobre 2026 inclus ;
- conversation de preuve :
  `https://assistant.numerique.gouv.fr/chat/ad6fc357-c8c3-4acb-b45f-62f37febc321`.

## Séquence exécutée

1. message initial avec `DATE_EDITION`, `PERIODE` et `NUMERIQUE`, Web désactivé ;
2. Web activé, puis cinq recherches dans l’ordre fixe ;
3. après la suggestion erronée de rejouer `RECHERCHE_IA`, envoi de
   `RECHERCHE_COMMANDE` conformément à la séquence métier ;
4. après `RECHERCHE_BERCY`, Web désactivé puis envoi de `VALIDER` ;
5. envoi de `GENERER_PAQUET`.

## Résultats observés

### Collecte

- les cinq recherches ont été exécutées dans l’ordre métier ;
- le registre cumulatif va de `U01` à `U07` ;
- trois sources sont dans la fenêtre : `U01` et `U06` au 13 octobre, puis `U07` au
  3 octobre 2026 ;
- quatre sources sont hors fenêtre : `U02`, `U03`, `U04` et `U05` ;
- la fin de collecte contient `COLLECTE_TERMINEE_BEST_EFFORT` et
  `REQUETE_A_ENVOYER=VALIDER`.

### Validation

- `SOURCES_VALIDES` contient exactement `U01`, `U06` et `U07` ;
- `SOURCES_EXCLUES` contient exactement `U02`, `U03`, `U04` et `U05` ;
- aucune source hors fenêtre n’est passée dans le paquet ;
- la fin contient `VALIDATION_TERMINEE` et
  `REQUETE_A_ENVOYER=GENERER_PAQUET`.

### Paquet JSON

Le dernier bloc émis a été extrait de la page et analysé indépendamment de
l’affirmation de l’Assistant :

- `JSON.parse` réussi ;
- sept clés racine exactes et schéma `SNUM_PAQUET_RENDU_V519` ;
- trois articles `U01`, `U06` et `U07` ;
- trois dates comprises dans la fenêtre inclusive ;
- trois URL HTTPS uniques ;
- exactement trois `essential=true` ;
- un objet dans `watch` pour signaler les rubriques sans source valide ;
- fin explicite : `PAQUET_RENDU_PRET`.

## Contrôles locaux

- 68 tests `unittest` réussis ;
- Ruff réussi ;
- `python3 scripts/build_split_kit.py --check` retourne `KIT_DECOUPLE_OK` ;
- `git diff --check` réussi ;
- prompt système : 3 958 caractères, sous la limite de 4 000 ;
- méthode : 3 410 caractères et contrat : 1 938 caractères, sous 4 500 ;
- `README.md` et `NOTICE-V5.24.md` identiques ;
- ZIP Collecte régénéré avec exactement les trois fichiers V5.24.

## Limites connues

- la génération de la prochaine rubrique par le modèle reste non déterministe ; la
  séquence fixe documentée évite qu’une répétition bloque le métier ;
- la branche `AUCUNE_SOURCE_PROUVEE` est couverte par les tests locaux, mais aucune
  des cinq recherches de cette recette Web n’a rendu un lot vide ;
- `U04` a répété l’URL et le fait de `U02` dans le registre alors qu’une autre source
  était affichée ; les deux entrées étaient hors fenêtre et ont été exclues, mais cet
  écart confirme que le registre doit rester contrôlé par le métier ;
- la recette vérifie l’orchestration, les dates et le contrat JSON, pas la qualité
  éditoriale indépendante de chaque source Web ;
- le Projet `Newsletter SNUM - Rendu HTML` n’a été ni modifié ni exécuté dans ce
  delta.

## Conclusion pour la présentation

La Collecte V5.24 est présentable pour un parcours métier entièrement réalisé dans
l’Assistant : le métier suit les cinq requêtes dans l’ordre documenté, contrôle le
registre visible, désactive le Web, puis obtient le JSON avec `VALIDER` et
`GENERER_PAQUET`. Le chaînage automatique de la rubrique suivante ne doit pas être
présenté comme déterministe.
