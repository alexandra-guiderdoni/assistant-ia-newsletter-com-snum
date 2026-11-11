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

Si le Projet existe déjà, remplacer tout le texte des instructions par le
fichier 01, puis ajouter le fichier 02 et choisir **Remplacer le fichier
existant**. En cas de doute, créer un Projet distinct pour l’installation ; ne
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

La Collecte interroge d’abord séparément quatorze sites, listés dans le fichier
01, puis complète par des recherches générales. La recette du 10 novembre 2026
a rapporté vingt articles de ces sites ; une autre édition peut en couvrir
moins. L’intranet `picsel.alize.finances.rie.gouv.fr` n’a jamais été consulté :
l’Assistant ne l’atteint probablement pas.

Les sources, les dates et les alertes doivent être relues. La version des
fichiers V5.23 et le nom du Projet v5.23.6 sont volontairement conservés. Ce
ZIP ne produit aucun mail à lui seul.
