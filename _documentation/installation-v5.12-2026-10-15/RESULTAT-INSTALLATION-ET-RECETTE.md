# Résultat de l'installation et de la recette V5.12

## Résultat

L'installation V5.12 est visible dans le Projet `Newsletter SNUM` de l'Assistant DINUM : le prompt système et les neuf ressources sont présents. Une recette complète a été exécutée dans une seule conversation.

La chaîne atteint un HTML complet après reprise, mais elle ne satisfait pas encore l'objectif d'une livraison autonome au premier passage. Le verdict métier est `NO-GO` à cause d'une relance manuelle et de jours de semaine faux dans les dates longues.

## Installation observée

Les neuf ressources installées sont :

1. `00-PROMPT-PROJET.md` ;
2. `01-ETAT-HISTORIQUE.md` ;
3. `02-METHODE-EDITORIALE.md` ;
4. `05-INDEX-HTML.md` ;
5. `06-COQUE-DEBUT.md` ;
6. `07-PIED-DE-PAGE.md` ;
7. `08-BLOC-ESSENTIEL.md` ;
8. `09-BLOCS-RUBRIQUES.md` ;
9. `10-COQUE-FIN.md`.

Le prompt système installé mentionne les cinq phases, `DONNEES_RENDU` et les jetons `SNUM_CANON_V512_*`.

## Conversation de preuve

[Ouvrir la conversation V5.12](https://assistant.numerique.gouv.fr/chat/f9064cda-77f1-4dfe-b4e6-2da38e09eb72/)

## Déroulé observé

### COLLECTE

- Web activé ;
- dix requêtes annoncées ;
- cinq rubriques couvertes ;
- au moins cinq domaines ;
- dix candidats ;
- terminaison `COLLECTE_TERMINEE`.

### VALIDATION

- Web désactivé ;
- six sources valides ;
- quatre sources exclues ;
- total cohérent avec les dix candidats ;
- terminaison `VALIDATION_TERMINEE`.

### DONNEES

- six fiches de rendu ;
- trois sources marquées essentielles ;
- terminaison `DONNEES_RENDU_PRETES` ;
- jours de semaine incorrects dans les dates longues.

### CANON

- paire d'index V5.12 présente ;
- onze paires de fragments présentes ;
- terminaison `CANON_HTML_PRET`.

### RENDU

- premier essai resté sans sortie finale ;
- message manuel `continue` ;
- nouvelle réponse `CANON_HTML_PRET` ;
- second envoi du prompt `RENDU` ;
- sortie finale avec `REVUE`, `HTML COMPLET`, `DOSSIER PRIVÉ` et état `PRODUITE - contrôle métier requis`.

## Contrôles du HTML visibles dans l'interface

L'inspection de l'arbre d'accessibilité confirme la présence observable de :

- `<!doctype html>` ;
- un titre pour l'édition du 14 octobre 2026 ;
- DSFR 1.15.2 ;
- `/revue-presse-snum/styles.css?v=20260917` ;
- trois accès rapides ;
- un menu de rubriques ;
- trois cartes essentielles ;
- six articles de source ;
- le pied de page réglementaire ;
- `fr-theme-modal` ;
- les scripts module et nomodule.

Le bouton de copie n'a pas exposé le HTML complet au presse-papiers pendant l'automatisation. La recette ne fournit donc pas de preuve de comparaison octet par octet avec le canon Bacoco.

## Défaut calendaire vérifié

Les dates ISO sélectionnées sont dans la fenêtre, mais les dates longues ne respectent pas le calendrier. Les valeurs correctes sont notamment :

- mercredi 14 octobre 2026 ;
- lundi 12 octobre 2026 ;
- mercredi 7 octobre 2026 ;
- lundi 5 octobre 2026 ;
- dimanche 11 octobre 2026 ;
- mardi 13 octobre 2026.

Cette anomalie suffit à interdire la livraison métier de la sortie générée.

## Contrôles locaux après recette

- construction du kit : `KIT_PROGRESSIF_OK` ;
- tests : 23 réussis ;
- prompt système : 3 969 caractères ;
- prompt du README identique au fichier source ;
- `git diff --check` sans erreur ;
- ZIP V5.12 : SHA-256 `97880a8c29431cb29f908d5d41d5f982443540d32b2320fadf9c9cc357e17e7e`.

## Conduite à tenir

Ne pas utiliser cette édition comme livrable final. Conserver la conversation comme preuve. La prochaine version doit recevoir ou vérifier les dates longues de façon déterministe et réussir `RENDU` sans message de reprise.

## Limites de la preuve

- aucune publication GitHub Pages ;
- aucun envoi par courriel ;
- aucun audit RGAA complet ;
- aucune comparaison octet par octet du HTML final ;
- un seul scénario réel exécuté.
