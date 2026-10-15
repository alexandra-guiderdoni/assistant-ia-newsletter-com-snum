# Installation et recette V5.17

## Résultat

La chaîne en deux Projets fonctionne dans l’Assistant DINUM.

- Projet Collecte : collecte réelle, validation exhaustive et paquet JSON réussi.
- Projet Rendu HTML : HTML complet livré au premier message d’une conversation neuve.
- Rendu autonome : feuille Bacoco chargée depuis son URL publique absolue.
- Comparaison : mêmes styles calculés que Bacoco au viewport 1 440 × 900 pixels.
- Comparaison du DOM : `DOM_DIFF_COUNT=0` face au canon alimenté par le même paquet.
- Résultat final : `HTML_CANONIQUE_PRODUIT - contrôle métier requis`.

## Configuration testée

### Newsletter SNUM - Collecte

- Prompt : `PROMPT-SYSTEME-COLLECTE-SNUM-V5.17.md`.
- Ressource : aucune.
- Web : activé pour `COLLECTE`, désactivé pour `VALIDATION` et `PAQUET`.

### Newsletter SNUM - Rendu HTML

- Prompt : `PROMPT-SYSTEME-RENDU-HTML-SNUM-V5.17.md`.
- Web : désactivé.
- Ressources utilisées :
  - `CANON-HTML-01-COQUE-A-V5.17.md` ;
  - `CANON-HTML-02-COQUE-B-V5.17.md` ;
  - `CANON-HTML-03-ESSENTIEL-RUBRIQUE-V5.17.md` ;
  - `CANON-HTML-04-SURVEILLER-VIDE-V5.17.md`.

La première ressource contient l’URL absolue de la feuille Bacoco. Le HTML copié
depuis le chat conserve ainsi son rendu lorsqu’il est ouvert hors de GitHub Pages.

## Données de la démonstration

- Édition : 14 octobre 2026.
- Fenêtre inclusive : 3 au 13 octobre 2026.
- Candidats : 10.
- Sources valides : 4.
- Sources exclues : 6.
- Articles du paquet : 4.
- Essentiels : 3.

## Séquence exécutée

1. Envoyer `PHASE COLLECTE` avec le Web.
2. Vérifier `COLLECTE_TERMINEE` et compter 10 candidats.
3. Désactiver le Web.
4. Envoyer `PHASE VALIDATION` dans la même conversation.
5. Vérifier `VALIDATION_TERMINEE` et l’égalité `4 + 6 = 10`.
6. Envoyer `PHASE PAQUET` dans la même conversation.
7. Vérifier que le JSON est parseable et que la réponse se termine par
   `PAQUET_RENDU_PRET`.
8. Copier le bloc entre les deux marqueurs V5.17.
9. Ouvrir une conversation neuve dans le Projet Rendu HTML.
10. Envoyer `PHASE RENDRE_EDITION` avec le paquet.
11. Vérifier le HTML complet et l’état final.
12. Vérifier que la feuille personnalisée commence par
    `https://bacoco.github.io/revue-presse-snum/styles.css`.
13. Comparer le DOM au canon construit avec le même paquet et exiger
    `DOM_DIFF_COUNT=0`.

## Incident de recette

Le premier essai RENDU utilisait un seul fichier canonique et a échoué avec
`CANON_MANQUANT`. La ressource a été remplacée dans le kit par quatre blocs courts.
La conversation neuve suivante a réussi au premier message.

Un second défaut a ensuite été détecté par contrôle visuel : le chemin relatif de
`styles.css` ne fonctionnait que sur GitHub Pages. Après passage à l’URL absolue, une
nouvelle conversation RENDU a livré un HTML autonome. Son espacement de tête, sa grille,
ses colonnes et la taille de son titre correspondent aux valeurs calculées sur Bacoco.

Une comparaison déterministe a ensuite détecté 12 écarts d’assemblage : le lien
`L’essentiel`, 4 titres de rubrique et 7 séparateurs de mots-clés. Le prompt Rendu a
été précisé, puis une conversation neuve a produit un DOM sans différence avec le
canon. Un faux rejet de longueur a également été supprimé : le Projet Rendu ne
recompte plus les textes déjà validés par le Projet Collecte.

## Périmètre non exécuté

- aucune publication GitHub Pages ;
- aucun envoi de courriel ;
- aucune suppression de projet ou de conversation ;
- aucun audit RGAA manuel complet.
