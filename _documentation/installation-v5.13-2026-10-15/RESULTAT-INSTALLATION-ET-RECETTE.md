# Résultat de l’installation et de la recette V5.13

## Résultat

L’installation V5.13 est visible dans le Projet `Newsletter SNUM` de l’Assistant DINUM. Le prompt système et les neuf ressources sont présents.

La recette réelle atteint `COLLECTE_TERMINEE`, `VALIDATION_TERMINEE`, `DONNEES_RENDU_PRETES` et `CANON_HTML_PRET`, mais échoue pendant `RENDU`. Aucun HTML n’est livré.

Verdict : **NO-GO pour la production autonome**.

## Ressources installées

1. `00-PROMPT-PROJET.md` ;
2. `01-ETAT-HISTORIQUE.md` ;
3. `02-METHODE-EDITORIALE.md` ;
4. `05-INDEX-HTML.md` ;
5. `06-COQUE-DEBUT.md` ;
6. `07-PIED-DE-PAGE.md` ;
7. `08-BLOC-ESSENTIEL.md` ;
8. `09-BLOCS-RUBRIQUES.md` ;
9. `10-COQUE-FIN.md`.

Le prompt installé est `PROMPT-SYSTEME-SNUM-V5.13.md` et utilise les jetons `SNUM_CANON_V513_*`.

## Conversation de preuve

[Ouvrir la conversation V5.13](https://assistant.numerique.gouv.fr/chat/2816dcf4-93b9-454e-a94b-c99b26a677c8)

## Résultats par phase

- `COLLECTE` : neuf candidats, couverture annoncée conforme, `COLLECTE_TERMINEE` ;
- `VALIDATION` : deux sources valides et sept exclues, `VALIDATION_TERMINEE` ;
- `DONNEES` : deux fiches complètes, dates sans jour de semaine, `DONNEES_RENDU_PRETES` ;
- `CANON` : paire d’index et onze paires de fragments, `CANON_HTML_PRET` ;
- `RENDU` : `A_COMPLETER | DONNEES_MANQUANTES`, sans HTML ;
- après `continue` : `A_COMPLETER | SOURCE_MANQUANTE`, sans HTML.

## Analyse

Les deux sources attendues figurent intégralement dans `DONNEES_RENDU`. La mention `SOURCE_MANQUANTE` n’est donc pas reliée à une absence observable.

Les deux sources sont cependant marquées `ESSENTIEL : OUI`, alors que la règle exige zéro essentiel sous trois sources. Cette contradiction constitue la cause probable du contrôle bloquant. Elle doit être corrigée avant une nouvelle version.

## Preuve durable

La conversation V5.13 liée plus haut conserve les deux arrêts. Les captures locales ne sont pas publiées, car elles contiennent des éléments d’interface étrangers à la preuve.

## Limites de la preuve

- un seul scénario réel V5.13 exécuté ;
- aucune sortie HTML à comparer au canon Bacoco ;
- aucun audit RGAA complet ;
- aucune publication GitHub Pages ;
- aucun envoi par courriel ;
- `continue` est un diagnostic, pas une étape valide du mode opératoire.
