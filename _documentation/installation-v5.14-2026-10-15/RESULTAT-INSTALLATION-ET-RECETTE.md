# Résultat de l’installation et de la recette V5.14

## Résultat

L’installation V5.14 est visible dans le Projet `Newsletter SNUM` de l’Assistant DINUM. Le prompt système et les neuf ressources sont présents.

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

Le prompt installé est `PROMPT-SYSTEME-SNUM-V5.14.md` et utilise les jetons `SNUM_CANON_V514_*`.

## Conversation de preuve

[Ouvrir la conversation V5.14](https://assistant.numerique.gouv.fr/chat/f841d9c3-a65b-4ebf-84bd-d8a4d2993c8f)

## Résultats par phase

- `COLLECTE` : onze candidats, dix requêtes, cinq rubriques, au moins cinq domaines, `COLLECTE_TERMINEE` ;
- `VALIDATION` : cinq sources valides et six exclues, total égal à onze, `VALIDATION_TERMINEE` ;
- `DONNEES` : cinq fiches complètes, exactement trois essentiels, dates sans jour de semaine, `DONNEES_RENDU_PRETES` ;
- `CANON` : réponse `CANON_HTML_PRET`, mais cinq entrées ne correspondent pas aux paires `START/END` du canon ;
- `RENDU` : `A_COMPLETER` avec huit lignes `DONNEES_MANQUANTES`, sans HTML ;
- aucun message `continue` envoyé.

## Analyse

La V5.14 corrige bien la contradiction sur les essentiels et remplace les diagnostics génériques par des diagnostics nominatifs.

Le test révèle deux blocages distincts :

1. `CANON_HTML_PRET` est déclaré malgré cinq noms de fragments inexacts ;
2. les URL perdent leur schéma `https://`, puis échouent au contrôle d’URL exacte.

Les éléments d’édition signalés comme manquants existent dans les fragments locaux. Leur absence au rendu confirme que le canon n’a pas été chargé ou conservé fidèlement.

## Preuve durable

La conversation V5.14 liée plus haut conserve l’arrêt et ses contrôles nominatifs. Les captures locales ne sont pas publiées, car elles contiennent des éléments d’interface étrangers à la preuve.

## Limites de la preuve

- un seul scénario réel V5.14 exécuté ;
- aucune sortie HTML à comparer au canon Bacoco ;
- aucun audit RGAA complet ;
- aucune publication GitHub Pages ;
- aucun envoi par courriel ;
- aucun commit ni push pendant cette recette.
