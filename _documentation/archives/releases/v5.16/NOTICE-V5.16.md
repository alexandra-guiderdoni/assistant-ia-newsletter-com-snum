<!-- PDG-BINARY-ASSET-JUSTIFICATION: le ZIP fournit les neuf ressources téléversables sans terminal ; ses sources restent les fichiers Markdown et le générateur versionnés. -->

# Configurer l’Assistant DINUM pour la revue SNUM V5.16

La V5.16 vise à éliminer la dépendance entre deux tours observée en V5.15. Le chargement du canon, l’assemblage, les contrôles et la livraison ont lieu dans un seul message `CANON_RENDU`.

> **Verdict réel : NO-GO pour la production autonome.** Le premier `CANON_RENDU` de la recette s’arrête avec `A_COMPLETER` et deux diagnostics `CANON_MANQUANT` visant les marqueurs d’index V5.16. Aucun HTML n’est livré.

## Livrables

Télécharger :

1. `kit-dinum-snum-v5-16-progressif-9-fichiers.zip` ;
2. `PROMPT-SYSTEME-SNUM-V5.16.md`.

Après extraction, téléverser exactement les neuf fichiers Markdown du ZIP. Ne pas téléverser le ZIP, la notice, le README ni le prompt système comme ressource.

## Installation

1. Ouvrir le Projet `Newsletter SNUM`.
2. Remplacer les instructions par `PROMPT-SYSTEME-SNUM-V5.16.md`.
3. Remplacer les neuf ressources V5.15 par les neuf ressources V5.16.
4. Attendre la fin de l’indexation.
5. Enregistrer le Projet.
6. Créer une conversation vierge depuis ce Projet.

Les quatre phases restent dans cette conversation : `COLLECTE`, `VALIDATION`, `DONNEES`, puis `CANON_RENDU`.

## Données

`DONNEES` conserve les URL absolues et prépare toutes les fiches avant le canon. Chaque date longue reste en majuscules sans jour de semaine ; sinon l’Assistant répond `DONNEES_RENDU_INCOMPLETES | DATE_CALENDRIER_INCOHERENTE`. La phase se termine par `DONNEES_RENDU_PRETES` seulement si tous les champs sont présents.

## Contrat corrigé

`CANON_RENDU` recherche `SNUM_CANON_V516_INDEX_START` et `SNUM_CANON_V516_INDEX_END`, charge les cinq fragments et vérifie les onze paires exactes dans le même tour. Les marqueurs @@ des fragments sont des entrées normales. L’Assistant assemble un brouillon HTML complet non affiché, remplace les marqueurs, puis contrôle seulement ce brouillon final.

La phase ne doit afficher ni l’index, ni les paires, ni les fragments avant le résultat. Une paire absente ou différente impose `A_COMPLETER`, `## CONTROLES_EN_ECHEC`, puis `CANON_MANQUANT | <paire>`, sans HTML.

Un arrêt `A_COMPLETER` ne doit jamais être suivi de `continue` dans une recette autonome.

## Condition de réussite

Le premier `CANON_RENDU`, sans correction intermédiaire, doit livrer dans l’ordre :

1. `## REVUE` ;
2. `## HTML COMPLET` avec un bloc de `<!doctype html>` à `</html>` ;
3. `## DOSSIER PRIVÉ` ;
4. `État : PRODUITE - contrôle métier requis`.

## État de la recette

La recette réelle V5.16 a été exécutée dans une conversation vierge le 15 octobre 2026. `COLLECTE`, `VALIDATION` et `DONNEES` réussissent. Le premier `CANON_RENDU` ne retrouve pas les marqueurs `SNUM_CANON_V516_INDEX_START` et `SNUM_CANON_V516_INDEX_END`, puis s’arrête sans HTML.

[Ouvrir la conversation de preuve V5.16](https://assistant.numerique.gouv.fr/chat/4767347f-c1cd-442d-a3e7-f7f55628311f)
