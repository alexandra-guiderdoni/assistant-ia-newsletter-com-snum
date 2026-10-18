# Rapport de recette de stabilisation V5.23

Date : 18 octobre 2026

## Verdict courant

`RECETTE_LOCALE_VERTE_ASSISTANT_A_REJOUER`

Le candidat n’est pas livrable. Les tests locaux sont verts. Le dernier parcours réel
exact a correctement enchaîné les cinq recherches, Bercy, `VALIDER` et
`GENERER_PAQUET`. Sa réponse finale a toutefois enfreint B02 et B03 : un brouillon JSON
précédait le marqueur de début, le JSON était dupliqué, `watch` était une chaîne et un
fait dépassait 25 mots. Le prompt et le contrat locaux ont été resserrés après cette
observation, mais cette correction n’a pas encore été rejouée dans l’Assistant.

Un commit de checkpoint et le push de la branche de stabilisation sont autorisés pour
préserver le travail. Aucun tag de livraison, fusion dans `main` ni déclaration de
conformité ne doit précéder une nouvelle recette exacte hors service dégradé.

## Preuves locales

- Baseline : commit `db532b21630df17d31e56f06e2fc73e82312c6e0`, tag local
  `v5.23-baseline`.
- Candidat de checkpoint : prompt Collecte de 3 997 caractères.
- `python3 -m unittest discover -s tests -v` : 73 tests réussis sur 73.
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

## État des critères

- B01, transition Bercy vers validation : démontrée lors de l’essai 6, à confirmer sur
  le checkpoint final.
- B02, JSON unique marqué : contredite lors de l’essai 6, corrigée localement, à rejouer.
- B03, paquet normalisé sans correction : contredite lors de l’essai 6, corrigée
  localement, à rejouer.
- B04, date longue dans le HTML : vert seulement en préflight local, non exercé avec un
  paquet réel du candidat.
- P01 à P08 : couverts localement, à confirmer par la recette exacte.

## Prochaine action autorisée

1. Attendre la disparition de la bannière de service dégradé.
2. Créer une conversation vierge dans le projet de stabilisation.
3. Envoyer les cinq lignes complètes `REQUETE_A_ENVOYER=...` avec le Web.
4. Désactiver le Web, puis envoyer `VALIDER` et une seule fois `GENERER_PAQUET`.
5. Contrôler indépendamment le JSON, puis le transmettre au projet Rendu HTML de
   stabilisation sans correction.

## Limites

- Les projets de production `Newsletter SNUM - Collecte` et
  `Newsletter SNUM - Rendu HTML` n’ont pas été modifiés pendant cette recette.
- Le candidat n’est pas publiable tant que les étapes B01 à B04 ne disposent pas de
  preuves réelles vertes dans un parcours conforme.
