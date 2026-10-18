# Rapport de recette de stabilisation V5.23

Date : 18 octobre 2026

## Verdict courant

`RECETTE_ASSISTANT_V5234_ECHEC_B01_B02_P04`

Le candidat n’est pas livrable. Les tests locaux sont verts, mais la recette réelle
v5.23.4 échoue. Les cinq recherches ont avancé avec des sources visibles et `VALIDER`
a produit une ligne de contrôle par entrée. Le contenu JSON respecte désormais B03 :
identifiants continus, quatre URL uniques, dates dans la fenêtre, trois essentiels,
textes courts et `watch` composé d’objets. En revanche, P04 et B01 omettent les
marqueurs demandés. B02 régresse : un premier JSON en bloc de code précède un second
JSON, et les marqueurs deviennent `START=SNUM_...` et `END=SNUM_...`. La chaîne a donc
été arrêtée avant le Rendu HTML, sans correction manuelle du paquet.

Un commit de checkpoint et le push de la branche de stabilisation sont autorisés pour
préserver le travail. Aucun tag de livraison, fusion dans `main` ni déclaration de
conformité ne doit précéder une nouvelle recette exacte hors service dégradé.

## Preuves locales

- Baseline : commit `db532b21630df17d31e56f06e2fc73e82312c6e0`, tag local
  `v5.23-baseline`.
- Candidat courant : prompt Collecte de 3 993 caractères.
- `python3 -m unittest discover -s tests -v` : 74 tests réussis sur 74 après
  synchronisation des dérivés.
- Ruff, contrôle des kits et `git diff --check` : réussis.
- Ces contrôles prouvent les invariants textuels et les validateurs locaux, pas le
  comportement du modèle hébergé par l’Assistant.

## Audit de la recette V5.23 historique

Conversation :
<https://assistant.numerique.gouv.fr/chat/46dcbba0-69b8-4467-9e0e-4c8ced8f9036>

Le transcript confirme :

- chaque recherche métier envoyait la ligne complète avec
  `REQUETE_A_ENVOYER=` ;
- les cinq recherches ont avancé dans l’ordre, y compris après deux résultats hors
  fenêtre ;
- la réponse Bercy contenait directement `COLLECTE_TERMINEE_BEST_EFFORT` puis
  `REQUETE_A_ENVOYER=VALIDER`.

Il contredit toutefois le verdict strict de l’ancien rapport : quatre messages
`GENERER_PAQUET` ont été nécessaires. Les trois premières réponses avaient
successivement un mauvais schéma, des champs incomplets, puis des rubriques, types et
identifiants non conformes. Seule la quatrième réponse s’approche du contrat, mais ses
identifiants restent `U01`, `U04`, `U05`. Cette conversation ne prouve donc pas B02 ni
B03 sans correction manuelle.

## Retests non recevables comme verdict

| Essai | Écart de protocole ou d’environnement | Conversation |
|---|---|---|
| 1 | Cinq commandes envoyées sans le préfixe `REQUETE_A_ENVOYER=`. | <https://assistant.numerique.gouv.fr/chat/f03d253f-51b7-4776-966f-0be42e20b94b> |
| 2 | Même omission du préfixe ; variante ensuite abandonnée. | <https://assistant.numerique.gouv.fr/chat/2d2dba94-592a-43ce-8737-ef3b5beca005> |
| 3 | Même omission du préfixe ; variante ensuite abandonnée. | <https://assistant.numerique.gouv.fr/chat/9d200b4d-9069-4f9d-ad15-7d1b875d1385> |
| 4 | Expérience de prompt réduit, hors candidat restauré. | <https://assistant.numerique.gouv.fr/chat/d2751252-b9d3-44ae-945a-fb33573926e6> |
| 5 | Protocole exact, mais réponse initiale pendant `Trafic élevé - service dégradé`. | <https://assistant.numerique.gouv.fr/chat/21697f13-21c2-4afa-9da2-ad07dbf414ff> |
| 6 | Protocole exact et chaîne atteinte ; paquet dupliqué, `watch` chaîne et fait trop long. | <https://assistant.numerique.gouv.fr/chat/0220d074-dbcc-4b98-9f74-e80758b5659f> |
| 7 | Service normal ; B01 et B02 verts, P04 et B03 rouges selon l’audit détaillé ci-dessus. | <https://assistant.numerique.gouv.fr/chat/e23e5670-3167-4a9b-8c71-947ff27cd3c7> |
| 8 | V5.23.4, service normal ; B03 vert, mais P04, B01 et B02 rouges. | <https://assistant.numerique.gouv.fr/chat/b9213270-ec0a-4621-82d5-f15e9250d6f6> |

## État des critères

- B01, transition Bercy vers validation : rouge sur le candidat v5.23.4 ; la commande
  `VALIDER` est présente, mais `COLLECTE_TERMINEE_BEST_EFFORT` manque.
- B02, JSON unique marqué : rouge sur le candidat v5.23.4 ; deux JSON, un bloc de code
  et deux marqueurs altérés.
- B03, paquet normalisé sans correction : vert sur le contenu JSON de l’essai 8, mais
  ce contenu reste inutilisable tant que B02 est rouge.
- B04, date longue dans le HTML : vert seulement en préflight local, non exercé avec un
  paquet réel du candidat.
- P04 : rouge sur les cinq recherches de l’essai 8 ;
  `VALIDATION_METIER_REQUISE` est toujours omis.
- Les autres comportements P01 à P08 : couverts localement, à confirmer par la recette
  exacte.

## Prochaine action autorisée

1. Arrêter les micro-variantes du même prompt : trois recettes successives ont déplacé
   les échecs sans produire un parcours entièrement vert.
2. Reprendre mot pour mot la grammaire B02 qui avait réussi dans l’essai 7, conserver
   la normalisation B03 de l’essai 8 et rendre P04/B01 par des lignes littérales, sans
   alias `START` ou `END`.
3. Produire un unique candidat de bifurcation, le tester localement, puis rejouer une
   seule recette Collecte complète.
4. Ne tester le Rendu HTML que si B01, B02, B03 et P04 sont simultanément verts.

## Limites

- Les projets de production `Newsletter SNUM - Collecte` et
  `Newsletter SNUM - Rendu HTML` n’ont pas été modifiés pendant cette recette.
- Le candidat n’est pas publiable tant que les étapes B01 à B04 ne disposent pas de
  preuves réelles vertes dans un parcours conforme.
