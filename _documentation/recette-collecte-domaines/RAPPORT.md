# Recette des domaines prioritaires de Collecte

Recettes réelles du 10 novembre 2026 dans le Projet Assistant
`Newsletter SNUM - Collecte - v5.23.6`, Web activé, avec la même entrée :

```text
DATE_EDITION = 10 novembre 2026
PERIODE = du 3 novembre 2026 au 9 novembre 2026 inclus
```

## Objectif

Réintégrer les quatorze sites à interroger, perdus au fil des versions, et
obtenir de leurs articles dans le paquet V519 :

`economie.gouv.fr`, `numerique.gouv.fr`, `vie-publique.fr`, `cnil.fr`,
`legifrance.gouv.fr`, `presse.economie.gouv.fr`, `acteurspublics.fr`,
`lemonde.fr`, `modernisation.gouv.fr`, `picsel.alize.finances.rie.gouv.fr`,
`itforbusiness.fr`, `next.ink`, `01net.com` et `journaldunet.com`.

## Résultats

| Version | Formulation | Sources | Sites interrogés | Articles des 14 sites | Contrôle V519 |
| --- | --- | --- | --- | --- | --- |
| V1 `e0cf87e` | liste prioritaire dans la méthode | 50 | 1 | 2 / 9 | accepté |
| V2 `bc6dd4b` | quatre recherches groupées | 82 | 12 | 9 / 9 | rejeté : dates hors fenêtre |
| V3 `4b7f1bb` | groupes et contrôle final | 96 | 6 | 5 / 9 | rejeté : fait de plus de 25 mots |
| V4 `de38a1e` | une recherche séparée par site | 117 | 11 | 20 / 20 | accepté |

« Sites interrogés » compte les sites de la liste apparaissant directement dans
les sources consultées ; `economie.gouv.fr` et `numerique.gouv.fr` n’y figurent
que par leurs sous-domaines. Les contrôles V1 à V3 ont été exécutés avec
`scripts/newsletter_html.py build`. Le paquet V4 n’a pas pu être extrait de la
page : ses règles V519 ont été appliquées dans la page par un script qui reprend
celles de `scripts/newsletter_render.py`.

## Diagnostic

Deux conversations ordinaires ont montré que la recherche Web de l’Assistant
atteint `next.ink` et `lemonde.fr` : dix sources du site demandé à chaque fois.
Une troisième, demandant une recherche séparée pour chacun des quatorze sites, a
consulté 106 sources et rapporté des articles pour dix sites. La limite venait
donc de la formulation de Collecte, et non de l’accès au Web. La V4 reprend
cette formulation en étape A du prompt système.

## Décisions

- La liste figure dans le prompt système et dans la méthode, car le modèle lit
  le prompt en priorité.
- Le tri des articles et l’ordre des rubriques sont assurés par l’outil
  `outil-rendu-dsfr.html` et `scripts/newsletter_mail.py` : aucune des quatre
  recettes ne les a respectés.
- Les URL à paramètres sont signalées à l’expéditeur, hors du mail, sans être
  retirées : le contenu éditorial n’est jamais réécrit par l’outil.

## Limites

- Une seule collecte par version : les écarts entre V2 et V3 montrent une forte
  variabilité ; la V4 n’est pas garantie à chaque édition.
- `picsel.alize.finances.rie.gouv.fr` n’a été consulté dans aucune recette :
  l’intranet n’est probablement pas joignable depuis l’Assistant.
- Le Monde, Vie publique, Légifrance et la CNIL ont été consultés en V4 sans
  article retenu.
- Les alertes `watch` produites par Collecte restent approximatives : décomptes
  et rubriques vides ne correspondent pas toujours au paquet.
- Les dates et le contenu des articles retenus n’ont pas été vérifiés en
  ouvrant chaque URL. La relecture humaine reste nécessaire.
- Le Rendu HTML de l’Assistant trie aussi chaque rubrique par date
  décroissante depuis le 11 novembre 2026. Une consigne isolée a d’abord été
  ignorée ; placée dans la phrase qui assemble les rubriques, elle a été
  respectée au second rendu réel du paquet V1. Ce HTML n’a pas été comparé
  octet par octet au canon : la page n’en expose qu’une copie tronquée.
