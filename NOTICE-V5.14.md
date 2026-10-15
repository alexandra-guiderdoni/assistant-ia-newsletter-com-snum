<!-- PDG-BINARY-ASSET-JUSTIFICATION: le ZIP fournit les neuf ressources téléversables sans terminal ; ses sources restent les fichiers Markdown et le générateur versionnés. -->

# Configurer l’Assistant DINUM pour la revue SNUM V5.14

La V5.14 corrige l’arrêt observé en V5.13 lorsque seulement deux sources étaient valides. Elle rend la règle des essentiels non contradictoire et exige un diagnostic nominatif pour toute donnée ou source manquante.

## Livrables

Télécharger :

1. `kit-dinum-snum-v5-14-progressif-9-fichiers.zip` ;
2. `PROMPT-SYSTEME-SNUM-V5.14.md`.

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
2. Remplacer les instructions par le contenu complet de `PROMPT-SYSTEME-SNUM-V5.14.md`.
3. Remplacer les neuf ressources V5.13 par les neuf ressources V5.14.
4. Attendre la fin de l’indexation.
5. Enregistrer le Projet.
6. Créer une conversation vierge depuis ce Projet.

Les cinq phases suivantes restent dans cette conversation.

## Contrats corrigés

### DONNEES

La date longue reste en majuscules sans jour de semaine. Tout jour de semaine impose `DONNEES_RENDU_INCOMPLETES | DATE_CALENDRIER_INCOHERENTE`.

Si moins de trois sources sont valides, attribue ESSENTIEL=NON à chaque source. À partir de trois sources, exactement trois fiches valent `ESSENTIEL=OUI` et les autres valent `ESSENTIEL=NON`.

`DONNEES_RENDU_PRETES` est autorisé seulement si chaque source possède tous ses champs et si la règle des essentiels est satisfaite.

### CANON

Rechercher `SNUM_CANON_V514_INDEX_START` et `SNUM_CANON_V514_INDEX_END`, suivre `READ_NEXT` et charger les onze fragments. N’affiche aucun bloc HTML.

`CANON_HTML_PRET` doit citer la paire d’index et les onze paires de fragments.

### RENDU

Recharge les fragments au début du tour sans les afficher. Utilise seulement `DONNEES_RENDU`.

Instancie les blocs essentiels uniquement si au moins trois sources sont valides. Sous trois sources, `@@ESSENTIELS@@` devient vide et aucun lien `L’essentiel` n’est produit.

Les marqueurs @@ des fragments sont des entrées normales avant remplacement. Construis un brouillon HTML complet non affiché, remplace tous les marqueurs, corrige, puis contrôle seulement ce brouillon final.

Une erreur doit être précise :

- `SOURCE_MANQUANTE | <identifiant> | <champ>` ;
- `DONNEES_MANQUANTES | <identifiant ou EDITION> | <champ>`.

Un arrêt `A_COMPLETER` ne contient aucun HTML.

## Condition de réussite

La recette est réussie seulement si le premier `RENDU`, sans `continue` ni correction, livre dans l’ordre :

1. `## REVUE` ;
2. `## HTML COMPLET` avec un bloc de `<!doctype html>` à `</html>` ;
3. `## DOSSIER PRIVÉ` ;
4. `État : PRODUITE - contrôle métier requis`.

La checklist du README reste obligatoire avant de copier le HTML.

## État de la recette

La recette réelle V5.14 a été exécutée dans une conversation vierge le 15 octobre 2026.

Elle atteint `COLLECTE_TERMINEE`, `VALIDATION_TERMINEE`, `DONNEES_RENDU_PRETES` et `CANON_HTML_PRET`. `DONNEES` respecte exactement la règle des trois essentiels.

Le premier `RENDU` répond toutefois `A_COMPLETER` avec huit diagnostics nominatifs : trois éléments d’édition et la vérification exacte des cinq URL. Aucun HTML n’est affiché et aucun message `continue` n’est envoyé.

Verdict : **NO-GO pour la production autonome**.

Consulter le [rapport V5.14](./RAPPORT-V5.14.md) et la [conversation de preuve](https://assistant.numerique.gouv.fr/chat/f841d9c3-a65b-4ebf-84bd-d8a4d2993c8f).
