# Résultat de l’installation et de la recette V5.16

## Résultat

L’installation V5.16 est visible dans le Projet `Newsletter SNUM` de l’Assistant DINUM. Le prompt système et les neuf ressources sont présents.

La recette réelle atteint `COLLECTE_TERMINEE`, `VALIDATION_TERMINEE` et `DONNEES_RENDU_PRETES`. Le premier `CANON_RENDU` échoue avec `A_COMPLETER` et deux diagnostics `CANON_MANQUANT`. Aucun HTML n’est livré.

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

Le prompt installé est `PROMPT-SYSTEME-SNUM-V5.16.md` et utilise les jetons `SNUM_CANON_V516_*`.

## Conversation de preuve

[Ouvrir la conversation V5.16](https://assistant.numerique.gouv.fr/chat/4767347f-c1cd-442d-a3e7-f7f55628311f)

## Résultats par phase

- `COLLECTE` : dix candidats, dix requêtes et cinq rubriques, puis `COLLECTE_TERMINEE` ;
- `VALIDATION` : trois sources valides et sept exclues, total égal à dix, puis `VALIDATION_TERMINEE` ;
- `DONNEES` : trois fiches complètes, exactement trois essentiels, dates sans jour de semaine, puis `DONNEES_RENDU_PRETES` ;
- `CANON_RENDU` : `A_COMPLETER`, puis absence des deux marqueurs d’index V5.16, sans HTML ;
- aucun message `continue` envoyé.

## Analyse

La fusion demandée est bien exécutée dans un seul message. Elle élimine le passage d’un état `CANON_HTML_PRET` à un nouveau tour `RENDU`, mais la récupération initiale de l’index n’est pas établie dans cette recette.

Les fichiers sont visibles dans les paramètres du Projet. La trace ne permet pas de distinguer un délai d’indexation d’un échec de recherche ou de classement des ressources.

## Limites de la preuve

- un seul scénario réel V5.16 exécuté ;
- aucune sortie HTML à comparer au canon Bacoco ;
- aucun audit RGAA complet ;
- aucune publication GitHub Pages ;
- aucun envoi par courriel.
