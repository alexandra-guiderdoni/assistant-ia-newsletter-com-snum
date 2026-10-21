# Installer Newsletter SNUM - Collecte

Ce paquet fournit les fichiers du Projet qui recherche les actualités et produit le JSON
commun aux deux gabarits. Il nécessite un compte Assistant DINUM autorisé et
l’accès à sa recherche Web. Aucun terminal ni logiciel à installer.

## Préparer

1. Extraire entièrement `Newsletter SNUM - Collecte.zip`.
2. Conserver le dossier extrait : il contient cette notice, le
   [mode opératoire](MODE-OPERATOIRE.md), la notice historique et les trois
   fichiers numérotés ci-dessous.
3. Ouvrir l’Assistant DINUM avec son compte habituel.

Ne pas téléverser le ZIP, les notices, le mode opératoire ou le prompt comme
pièces jointes. Le prompt se copie dans les instructions du Projet.

## Installer

1. Créer un Projet nommé `Newsletter SNUM - Collecte - v5.23.6`.
2. Ouvrir **Paramètres du projet**.
3. Ouvrir le [prompt système de Collecte, fichier 01](01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.23.md)
   comme texte et copier tout son contenu dans **Instructions (expérimental)**.
4. Ajouter exactement ces deux ressources :
   - [méthode de Collecte, fichier 02](02-METHODE-COLLECTE-SNUM-V5.23.md) ;
   - [03-CONTRAT-PAQUET-RENDU-SNUM-V5.23.md](03-CONTRAT-PAQUET-RENDU-SNUM-V5.23.md).
5. Attendre la fin de leur indexation, puis enregistrer.
6. Dans une nouvelle conversation du Projet, activer la recherche Web.

Si le Projet existe déjà avec ces instructions et ces deux ressources, le
conserver. En cas de doute, créer un Projet distinct pour l’installation ; ne
pas supprimer les autres Projets ou leurs conversations.

## Premier usage

Envoyer seulement, en remplaçant les dates à chaque édition :

```text
DATE_EDITION = 14 octobre 2026
PERIODE = du 3 octobre 2026 au 13 octobre 2026 inclus
```

La première ligne attendue est `SNUM_PAQUET_RENDU_V519_START`. La réponse doit
contenir un seul JSON, puis `SNUM_PAQUET_RENDU_V519_END` et `PAQUET_RENDU_PRET`.
Une collecte sans article peut produire un paquet valide avec des alertes.

Si la réponse commence par `A_COMPLETER`, ne pas la transmettre à un rendu.
Suivre le dépannage du [mode opératoire](MODE-OPERATOIRE.md).

## Limites

Les sources et les dates doivent être relues. Le succès historique observé porte
sur une collecte sans article retenu ; il ne garantit pas chaque future
recherche. La version des fichiers V5.23 et le nom du Projet v5.23.6 sont
volontairement conservés. Ce ZIP ne produit aucun mail à lui seul.
