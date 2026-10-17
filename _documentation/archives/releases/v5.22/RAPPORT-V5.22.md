# Rapport de recette Newsletter SNUM V5.22

Date de recette : 16 octobre 2026.

## Verdict

**NO-GO.** La configuration V5.22 est correctement installée et les contrôles locaux
sont verts, mais la recette réelle s’arrête au premier lot `NUMERIQUE`. Avec le Web
activé, l’Assistant répond uniquement `PROCHAINE_COMMANDE=IA` : aucune source, aucune
citation et aucune preuve des deux recherches prescrites n’apparaît.

La chaîne `COLLECTE → VALIDER → GENERER_PAQUET → RENDU` n’a donc pas été poursuivie
au-delà de ce premier échec terminal.

## Périmètre vérifié

- édition : 14 octobre 2026 ;
- période inclusive : du 3 octobre 2026 au 13 octobre 2026 ;
- projet modifié : `Newsletter SNUM - Collecte` ;
- projet préservé : `Newsletter SNUM - Rendu HTML` ;
- prompt Collecte persistant : V5.22, 3 606 caractères dans le formulaire, soit la
  source de 3 607 caractères avec son saut de ligne terminal ;
- seules ressources Collecte visibles après réouverture des paramètres :
  `02-METHODE-COLLECTE-SNUM-V5.22.md` et
  `03-CONTRAT-PAQUET-RENDU-SNUM-V5.22.md`.

## Preuves locales

- `python3 -m unittest discover -s tests -v` : 53 tests réussis ;
- `ruff check --no-cache scripts tests` : aucun écart ;
- `python3 scripts/build_split_kit.py --check` : `KIT_DECOUPLE_OK` ;
- `git diff --check` : aucun écart ;
- README et NOTICE : sommes SHA-256 identiques ;
- ZIP Collecte régénéré depuis les trois fichiers V5.22.

Les tests couvrent notamment les cinq lots Web sans état intermédiaire, la consolidation
unique au tour `RECOMPTER`, le comptage des seules URL uniques avec date exacte dans la
fenêtre inclusive, l’arrêt sous cinq candidats, les contrôles de validation et l’analyse
du JSON exact avant `PAQUET_RENDU_PRET`.

## Preuve Assistant

Conversation terminale :
`https://assistant.numerique.gouv.fr/chat/7f83ff7c-e983-454e-960d-45e69377703c`

Message envoyé avec le bouton `Rechercher sur le web` activé :

```text
DATE_EDITION = 14 octobre 2026
PERIODE = du 3 octobre 2026 au 13 octobre 2026 inclus
NUMERIQUE
```

Réponse complète observée :

```text
PROCHAINE_COMMANDE=IA
```

La réponse est terminée et l’interface affiche les actions de copie et d’évaluation,
mais aucun bouton de sources ni aucune citation. Le marqueur seul ne prouve donc pas
l’exécution des deux recherches Web exigées. Envoyer `IA` aurait masqué cet échec.

## Non vérifié

Les lots `IA`, `COMMANDE`, `RH` et `BERCY`, puis `RECOMPTER`, `VALIDER`,
`GENERER_PAQUET` et `RENDU`, ne sont pas vérifiés sur V5.22. Le critère d’arrêt imposait
de ne pas franchir le premier échec terminal.

## Cause établie et limite

La V5.22 a bien supprimé l’état cumulatif qui échouait en V5.21, mais elle autorise
encore une transition fondée sur une simple sortie textuelle. Dans l’exécution observée,
le modèle a produit le marqueur attendu sans preuve d’appel Web. Le prompt seul ne
garantit donc pas l’orchestration de l’outil Web sur cette surface.

Ce rapport établit le comportement observé ; il ne permet pas de distinguer une décision
du modèle d’une limite propre à l’intégration Web de l’Assistant.
