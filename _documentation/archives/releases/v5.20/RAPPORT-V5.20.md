# Rapport de recette Collecte V5.20

## Verdict

`GO` pour l’orchestration du Projet `Newsletter SNUM - Collecte`.

La recette réelle a produit successivement `COLLECTE_TERMINEE`,
`VALIDATION_TERMINEE` et `PAQUET_RENDU_PRET` dans une même conversation. Le paquet
est un JSON analysable conforme au schéma `SNUM_PAQUET_RENDU_V519`, avec cinq articles,
cinq URL uniques et trois essentiels.

Ce verdict concerne uniquement la Collecte V5.20. Le Projet Rendu HTML V5.19 reste
`NO-GO` selon `RAPPORT-V5.19.md` : son identité octet par octet avec le canon Bacoco
n’est pas démontrée.

## Configuration testée

- prompt système : `01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.20.md` ;
- ressources : `02-METHODE-COLLECTE-SNUM-V5.20.md` et
  `03-CONTRAT-PAQUET-RENDU-SNUM-V5.20.md` ;
- conversation neuve du Projet Collecte ;
- Web actif uniquement pendant `COLLECTE`, puis désactivé avant `VALIDER` ;
- conversation de preuve :
  `https://assistant.numerique.gouv.fr/chat/56c27143-7762-4255-aa40-70c8871e4fe5`.

## Séquence exécutée

Message initial avec le Web :

```text
DATE_EDITION = 14 octobre 2026
PERIODE = du 3 octobre 2026 au 13 octobre 2026 inclus
```

Premier message sans le Web :

```text
VALIDER
```

Second message sans le Web :

```text
GENERER_PAQUET
```

## Résultats observés

### Collecte

- extraction correcte de `2026-10-14`, `2026-10-03` et `2026-10-13` ;
- dix requêtes Web affichées ;
- quinze candidats affichés ;
- fin de tour : `COLLECTE_TERMINEE` puis
  `ETAPE_SUIVANTE | Envoyez VALIDER`.

### Validation

- Web désactivé avant le message `VALIDER` ;
- contrôle explicite des deux bornes pour chaque candidat ;
- cinq sources conservées et dix sources exclues ;
- aucune URL dupliquée parmi les sources conservées ;
- fin de tour : `VALIDATION_TERMINEE` puis
  `ETAPE_SUIVANTE | Envoyez GENERER_PAQUET`.

### Paquet

- `JSON.parse` réussi sur le contenu entre les marqueurs ;
- schéma : `SNUM_PAQUET_RENDU_V519` ;
- cinq articles et cinq URL uniques ;
- trois articles marqués `essential` ;
- fin de tour : `SNUM_PAQUET_RENDU_V519_END` puis
  `PAQUET_RENDU_PRET`.

## Contrôles locaux

- 27 tests `unittest` réussis ;
- Ruff réussi ;
- `python3 scripts/build_split_kit.py --check` retourne `KIT_DECOUPLE_OK` ;
- `git diff --check` réussi ;
- prompt système : 3 069 caractères, sous la limite de 4 000 ;
- méthode : 3 060 caractères et contrat : 1 938 caractères, sous 4 500 ;
- `README.md` et `NOTICE-V5.20.md` identiques ;
- ZIP Collecte régénéré avec exactement les trois fichiers V5.20.

## Limites de la preuve

- la recette prouve l’orchestration et la structure du paquet, pas un audit éditorial
  indépendant de chaque fait ni de chaque date de publication ;
- le contenu doit conserver le contrôle métier prévu avant diffusion ;
- le Projet Rendu HTML n’a pas été modifié ni retesté dans ce delta ;
- aucun commit, push, tag, HTML, publication GitHub Pages ni courriel n’a été réalisé.
