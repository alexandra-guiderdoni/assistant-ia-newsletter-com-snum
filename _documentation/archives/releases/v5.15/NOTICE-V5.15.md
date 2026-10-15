<!-- PDG-BINARY-ASSET-JUSTIFICATION: le ZIP fournit les neuf ressources téléversables sans terminal ; ses sources restent les fichiers Markdown et le générateur versionnés. -->

# Configurer l’Assistant DINUM pour la revue SNUM V5.15

La V5.15 corrige les deux blocages observés en V5.14 : perte du schéma `https://` dans les URL et faux positif `CANON_HTML_PRET` malgré des paires de fragments inexactes.

## Livrables

Télécharger :

1. `kit-dinum-snum-v5-15-progressif-9-fichiers.zip` ;
2. `PROMPT-SYSTEME-SNUM-V5.15.md`.

Après extraction, téléverser exactement :

1. `00-PROMPT-PROJET.md` ;
2. `01-ETAT-HISTORIQUE.md` ;
3. `02-METHODE-EDITORIALE.md` ;
4. `05-INDEX-HTML.md` ;
5. `06-COQUE-DEBUT.md` ;
6. `07-PIED-DE-PAGE.md` ;
7. `08-BLOC-ESSENTIEL.md` ;
8. `09-BLOCS-RUBRIQUES.md` ;
9. `10-COQUE-FIN.md`.

Ne pas téléverser le ZIP, la notice, le README ni le prompt système comme ressource.

## Installation

1. Ouvrir le Projet `Newsletter SNUM`.
2. Remplacer les instructions par le contenu complet de `PROMPT-SYSTEME-SNUM-V5.15.md`.
3. Remplacer les neuf ressources V5.14 par les neuf ressources V5.15.
4. Attendre la fin de l’indexation.
5. Enregistrer le Projet.
6. Créer une conversation vierge depuis ce Projet.

Les cinq phases restent dans cette conversation.

## Contrats corrigés

### URL

Chaque candidat doit conserver une URL canonique absolue commençant par `https://`. Une URL sans schéma est invalide et ne peut pas atteindre `DONNEES_RENDU_PRETES`.

### CANON

Rechercher `SNUM_CANON_V515_INDEX_START` et `SNUM_CANON_V515_INDEX_END`, suivre `READ_NEXT`, puis comparer les onze lignes de `PAIRES_EXACTES`.

`CANON_HTML_PRET` est autorisé seulement si les onze lignes sont recopiées littéralement. Toute omission, fusion, autre paire ou mention « auto-fermant » impose `CANON_HTML_INCOMPLET | paire incorrecte`.

N’affiche aucun bloc HTML pendant cette phase.

### DONNEES

Les dates longues restent en majuscules sans jour de semaine. Sinon, arrêter avec `DONNEES_RENDU_INCOMPLETES | DATE_CALENDRIER_INCOHERENTE`.

### RENDU

Pendant `RENDU`, recharge les fragments. Les marqueurs @@ des fragments sont des entrées normales. Construis un brouillon HTML complet non affiché, remplace les marqueurs, corrige, puis contrôle seulement ce brouillon final.

Un arrêt `A_COMPLETER` ne contient aucun HTML et ne doit jamais être suivi de `continue` dans une recette autonome.

## Condition de réussite

La recette réussit seulement si le premier `RENDU`, sans correction intermédiaire, livre dans l’ordre :

1. `## REVUE` ;
2. `## HTML COMPLET` avec un bloc de `<!doctype html>` à `</html>` ;
3. `## DOSSIER PRIVÉ` ;
4. `État : PRODUITE - contrôle métier requis`.

## État de la recette

La recette réelle V5.15 a été exécutée dans une conversation vierge le 15 octobre 2026.

- `COLLECTE`, `VALIDATION`, `DONNEES` et `CANON` réussissent ;
- les URL restent absolues avec `https://` ;
- les onze paires `START/END` sont restituées exactement ;
- le premier `RENDU` répond `A_COMPLETER`, puis `CANON_MANQUANT`, sans HTML.

Verdict : `NO-GO` pour la production autonome. N’envoyez pas `continue`. Consultez `RAPPORT-V5.15.md` et la conversation de preuve avant toute nouvelle évolution.
