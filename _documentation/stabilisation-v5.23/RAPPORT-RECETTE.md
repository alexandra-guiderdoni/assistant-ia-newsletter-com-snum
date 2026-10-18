# Rapport de recette de stabilisation V5.23

Date : 18 octobre 2026

## Verdict courant

`GOAL_BLOQUE_SERVICE_RECHERCHE_WEB`

Le candidat n’est pas livrable. La bifurcation v5.23.5 remplace les trois grammaires
aliasées par des lignes littérales tout en conservant la normalisation B03, avec 74
tests locaux verts. Une seconde recette réelle a validé les lots NUMERIQUE et IA,
chacun avec une source datée, le registre, `VALIDATION_METIER_REQUISE` et la commande
suivante. P04 est donc prouvé sur deux lots sur cinq. Le lot COMMANDE a ensuite répondu
trois fois `RESULTATS_RECHERCHE=` vide et `RECHERCHE_NON_PROUVEE`, alors que son panneau
affichait dix sources. Les deux relances reprenaient exactement la même requête. La
chaîne a été arrêtée sans modifier la requête, injecter une source ni transmettre un
paquet au Rendu HTML. Le même blocage ayant persisté pendant trois tours de suivi, la
recette exige désormais un changement observable du service Web avant reprise.

La recette v5.23.4 reste la dernière preuve complète : B03 était vert sur le contenu
JSON, mais P04 et B01 omettaient les marqueurs demandés et B02 dupliquait le JSON avec
des marqueurs `START=SNUM_...` et `END=SNUM_...`.

Un commit de checkpoint et le push de la branche de stabilisation sont autorisés pour
préserver le travail. Aucun tag de livraison, fusion dans `main` ni déclaration de
conformité ne doit précéder une nouvelle recette exacte hors service dégradé.

## Preuves locales

- Baseline : commit `db532b21630df17d31e56f06e2fc73e82312c6e0`, tag local
  `v5.23-baseline`.
- Candidat courant : prompt Collecte de 3 953 caractères.
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
| 9 | V5.23.5 ; dix sources visibles, mais deux réponses `RECHERCHE_NON_PROUVEE` au premier lot. | <https://assistant.numerique.gouv.fr/chat/18bf6904-b4bc-43c1-a25a-f99140b25b60> |
| 10 | V5.23.5 ; NUMERIQUE et IA conformes, puis trois contradictions successives sur COMMANDE. | <https://assistant.numerique.gouv.fr/chat/69a2c48b-873f-4766-b20e-23f4d11505de> |

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
- V5.23.5 : P04 vert sur NUMERIQUE et IA ; non évalué sur les trois autres lots. B01 à
  B04 restent non évaluables, car les essais 9 et 10 se sont arrêtés avant Bercy.
- Les autres comportements P01 à P08 : couverts localement, à confirmer par la recette
  exacte.

## Prochaine action autorisée

1. Ne pas modifier le candidat : le panneau de sources contredit la réponse du modèle.
2. Reprendre le goal seulement après un changement observable du service Web, puis
   rejouer v5.23.5 dans une conversation vierge.
3. Ne tester le Rendu HTML que si B01, B02, B03 et P04 sont simultanément verts.

## Limites

- Les projets de production `Newsletter SNUM - Collecte` et
  `Newsletter SNUM - Rendu HTML` n’ont pas été modifiés pendant cette recette.
- Le candidat n’est pas publiable tant que les étapes B01 à B04 ne disposent pas de
  preuves réelles vertes dans un parcours conforme.
