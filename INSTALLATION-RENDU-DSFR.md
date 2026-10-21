# Installer Newsletter SNUM - rendu DSFR

Ce paquet contient le fichier autonome pour produire le mail, ainsi que le
candidat Assistant expérimental. La Collecte reste celle du Projet habituel.
Le parcours à utiliser pour conserver exactement le logo est **JSON → outil
autonome → mail HTML**. L’Assistant DSFR ne garantit pas la fidélité du logo.

## Installer l’outil autonome

1. Extraire entièrement `Newsletter SNUM - rendu DSFR.zip`.
2. Copier [outil-rendu-dsfr.html](outil-rendu-dsfr.html) dans un dossier du poste.
3. L’ouvrir par double-clic avec le navigateur autorisé, JavaScript activé.
4. Coller le JSON réel de Collecte, puis cliquer sur **Prévisualiser le mail**.
5. Relire l’aperçu et les commentaires de collecte affichés à part.
6. Cliquer sur **Télécharger le mail (.html)** et conserver le fichier obtenu.

Seul le fichier HTML est nécessaire à l’exécution. Il peut être renommé ou
déplacé ; aucune installation de Python, Node, serveur, extension ou bibliothèque
n’est requise. Il fonctionne hors connexion et ne conserve pas le paquet après
fermeture ou rechargement. Garder le JSON et le mail dans les dossiers autorisés.

La [notice détaillée](NOTICE-RENDU-DSFR-V1.0.md) et le
[mode opératoire](MODE-OPERATOIRE.md) sont inclus dans ce ZIP.

## Réinstaller aussi le Projet Assistant expérimental

Cette option reproduit le troisième Projet de démonstration ; elle ne remplace
pas l’outil autonome. Ses trois essais antérieurs ont altéré le logo. La
correction des consignes sur `watch` n’a pas fait l’objet d’une nouvelle recette
de génération par le modèle.

1. Créer un Projet nommé `Newsletter SNUM - rendu DSFR`.
2. Ouvrir **Paramètres du projet** et copier tout le texte de
   [prompt système du rendu DSFR, fichier 30](30-PROMPT-SYSTEME-RENDU-DSFR-V1.0.md)
   dans **Instructions (expérimental)**.
3. Ajouter exactement ces neuf ressources :

```text
31-MAIL-DSFR-COQUE-01-V1.0.md
31-MAIL-DSFR-COQUE-02-V1.0.md
31-MAIL-DSFR-COQUE-03-V1.0.md
31-MAIL-DSFR-LOGO-01-V1.0.md
31-MAIL-DSFR-LOGO-02-V1.0.md
31-MAIL-DSFR-LOGO-03-V1.0.md
32-MAIL-DSFR-ARTICLE-V1.0.md
33-MAIL-DSFR-RUBRIC-V1.0.md
34-MAIL-DSFR-WATCH-V1.0.md
```

4. Attendre leur indexation et enregistrer. Désactiver la recherche Web dans la
   conversation du Projet.
5. Pour un essai explicitement décidé, coller le même paquet que dans l’outil.
   Attendre `## HTML COMPLET` et un seul bloc HTML. Les commentaires de Collecte
   doivent apparaître après `CONTROLES`, hors du bloc HTML.

Si le Projet existe, conserver ses ressources conformes ; mettre à jour seulement
les instructions à partir du fichier `30`. Ne pas utiliser sa sortie comme
preuve que le PNG original est intact. En cas de doute, reprendre le même JSON
dans l’outil autonome, sans modifier le contenu éditorial.

## Vérifier le poste et Outlook avant diffusion

Suivre la recette manuelle du [mode opératoire](MODE-OPERATOIRE.md) : fichier seul,
hors connexion, aperçu, téléchargement et réouverture, puis essai dans
l’environnement Outlook autorisé. Aucun envoi automatique n’est effectué.
Ces vérifications réelles restent nécessaires ; un aperçu navigateur ne prouve
pas la conservation du logo dans Outlook administration.
