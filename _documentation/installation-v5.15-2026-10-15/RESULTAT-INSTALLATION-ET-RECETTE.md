# Résultat de l’installation et de la recette V5.15

## Résultat

L’installation V5.15 est visible dans le Projet `Newsletter SNUM` de l’Assistant DINUM. Le prompt système et les neuf ressources sont présents.

La recette réelle atteint `COLLECTE_TERMINEE`, `VALIDATION_TERMINEE`, `DONNEES_RENDU_PRETES` et `CANON_HTML_PRET`. Le premier `RENDU` échoue avec `A_COMPLETER` et `CANON_MANQUANT`. Aucun HTML n’est livré.

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

Le prompt installé est `PROMPT-SYSTEME-SNUM-V5.15.md` et utilise les jetons `SNUM_CANON_V515_*`.

## Conversation de preuve

[Ouvrir la conversation V5.15](https://assistant.numerique.gouv.fr/chat/712d3864-0310-488d-9256-9c44a054b4bc)

## Résultats par phase

- `COLLECTE` : dix candidats, dix requêtes, cinq rubriques, cinq domaines, URL absolues et `COLLECTE_TERMINEE` ;
- `VALIDATION` : cinq sources valides et cinq exclues, total égal à dix, `VALIDATION_TERMINEE` ;
- `DONNEES` : cinq fiches complètes, URL absolues, exactement trois essentiels, dates sans jour de semaine, `DONNEES_RENDU_PRETES` ;
- `CANON` : `CANON_HTML_PRET`, paire d’index V5.15 et onze paires `START/END` exactes ;
- `RENDU` : `A_COMPLETER`, puis `CANON_MANQUANT`, sans HTML ;
- aucun message `continue` envoyé.

## Analyse

La V5.15 corrige les deux défauts explicitement visés : perte du schéma `https://` et faux positif sur les noms des paires canoniques.

Le test révèle un blocage distinct. Le tour `RENDU` ne parvient pas à rétablir le canon qu’il doit recharger, malgré la preuve correcte fournie au tour `CANON`. Le mécanisme interne exact n’est pas observable depuis la conversation.

Le diagnostic `CANON_MANQUANT` est en outre moins précis que le format `CODE | détail` demandé. Cette imprécision doit être corrigée avec le mécanisme de chargement dans la prochaine version.

## Preuves visuelles

Des captures ont été prises pendant la recette navigateur pour `DONNEES_RENDU_PRETES`, les paires `CANON` et l’arrêt `A_COMPLETER`. Elles restent visibles dans la trace de session. La conversation liée ci-dessus constitue la preuve durable de cette recette ; aucune image locale n’a été créée.

## Limites de la preuve

- un seul scénario réel V5.15 exécuté ;
- aucune sortie HTML à comparer au canon Bacoco ;
- aucun audit RGAA complet ;
- aucune publication GitHub Pages ;
- aucun envoi par courriel ;
- aucun commit ni push pendant cette recette.
