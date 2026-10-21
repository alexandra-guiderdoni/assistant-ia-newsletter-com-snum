# Installer Newsletter SNUM - Rendu HTML

Ce paquet fournit le gabarit HTML habituel pour le Web. Il consomme le JSON
produit par Collecte ; il ne recherche aucune actualité et ne change aucun texte.
Il nécessite un compte Assistant DINUM autorisé, sans terminal métier.

## Préparer

1. Extraire entièrement `Newsletter SNUM - Rendu HTML.zip`.
2. Lire cette notice puis le [mode opératoire](MODE-OPERATOIRE.md).
3. Ouvrir l’Assistant DINUM avec son compte habituel.

Ne pas téléverser le ZIP, les notices, le mode opératoire ou le prompt comme
pièces jointes. Seules les quatre ressources numérotées `21` à `24` sont jointes.

## Installer

1. Créer un Projet nommé `Newsletter SNUM - Rendu HTML - v5.23.6`.
2. Ouvrir **Paramètres du projet**.
3. Copier tout le texte de
   [prompt système du Rendu HTML, fichier 20](20-PROMPT-SYSTEME-RENDU-HTML-SNUM-V5.19.md)
   dans **Instructions (expérimental)**.
4. Ajouter séparément, dans cet ordre :
   - [21-CANON-HTML-COQUE-A-V5.19.md](21-CANON-HTML-COQUE-A-V5.19.md) ;
   - [22-CANON-HTML-COQUE-B-V5.19.md](22-CANON-HTML-COQUE-B-V5.19.md) ;
   - [23-CANON-HTML-ESSENTIEL-RUBRIQUE-V5.19.md](23-CANON-HTML-ESSENTIEL-RUBRIQUE-V5.19.md) ;
   - [24-CANON-HTML-SURVEILLER-VIDE-V5.19.md](24-CANON-HTML-SURVEILLER-VIDE-V5.19.md).
5. Attendre la fin de leur indexation, puis enregistrer.
6. Ouvrir une nouvelle conversation du Projet et désactiver la recherche Web.

Si le Projet possède déjà ces instructions et ces quatre ressources, le
conserver. Pour essayer une installation différente, créer un Projet distinct
sans supprimer l’existant. Les fichiers restent en V5.19 : c’est la version
consommant le contrat JSON V519 de la Collecte actuelle.

## Premier usage

Coller le paquet réel de Collecte, de `SNUM_PAQUET_RENDU_V519_START` à
`SNUM_PAQUET_RENDU_V519_END` inclus, sans nouvelle consigne.

La réponse doit commencer par `## HTML COMPLET`, puis présenter un seul bloc
HTML complet et une section `## CONTROLES`. Relire le résultat avant toute
publication. Le HTML de ce Projet contient des ressources Web DSFR ; il ne
constitue pas le mail autonome destiné à Outlook.

Si `articles=[]`, le gabarit affiche « Collecte à compléter » et les alertes
`watch` éventuelles. Ce comportement historique est conservé. Pour le gabarit
mail DSFR, les alertes restent en dehors du mail.

## Limites

Un résultat `A_COMPLETER`, un préambule avant le HTML ou des marqueurs `@@`
restants imposent un arrêt. Suivre le [mode opératoire](MODE-OPERATOIRE.md).
La recette historique réussie portait sur un paquet vide ; chaque édition doit
être relue. Ce ZIP ne publie rien et n’envoie aucun courriel.
