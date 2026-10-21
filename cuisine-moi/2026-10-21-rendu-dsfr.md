Assistant Newsletter SNUM - rendu DSFR : notes cuisine-moi
=========================================================

Date : 21 octobre 2026 | Objectif : ajouter une sortie de courriel DSFR au paquet de Collecte existant.

## Résumé / décisions clés

- Dépôt cible : `assistant-ia-newsletter-com-snum`.
- Préserver la dernière Collecte et le Projet `Newsletter SNUM - Rendu HTML`.
- Ajouter `Newsletter SNUM - rendu DSFR`, avec le même paquet `SNUM_PAQUET_RENDU_V519` en entrée.
- Référence visuelle : `../builder-mail-dsfr/newsletter-snum-2026-10-14.html`, avec les flèches devant les titres.
- Conserver les dates et présenter les articles hors fenêtre comme les autres, conformément à la correction de l’utilisateur.
- Installer et tester le nouveau Projet dans l’Assistant avec le navigateur, puis itérer sur les écarts observés.
- Après trois essais non fidèles, l’utilisateur accepte un outil autonome : coller le même paquet, prévisualiser et télécharger le mail avec le logo base64 exact. Le Projet Assistant expérimental reste non validé.
- Le métier conserve son parcours : coller le paquet et récupérer le HTML ; aucun terminal métier ajouté.
- État Git avant écriture : arbre propre, branche `main`, divergence avec la branche suivie `0/0` après `git fetch`.

## Journal questions-réponses

### Q1 — Transport et reproduction du logo

- Question : choix du traitement du logo avant stabilisation du gabarit destiné à l’Assistant.
- Capture : l’utilisateur demande explicitement un rendu autonome avec le logo en base64. La chaîne dépasse 12 000 caractères ; sa reproduction sera contrôlée en recette. Le navigateur ne prouve pas sa transportabilité dans Outlook.
- Drapeaux : aucun choix de logo en attente ; recette de reproduction nécessaire.

### Q2 — Suite après trois essais non fidèles

- Constat : les trois variantes essayées dans l’Assistant ont altéré le logo. Les deux dernières sorties contiennent une image de 904 octets au lieu des 9 024 attendus.
- Question posée : accepter un outil autonome recevant le même JSON pour produire le mail avec le logo base64 exact, ou conserver l’objectif d’un rendu uniquement dans l’Assistant.
- Réponse : « oui ». L’utilisateur accepte le fichier autonome proposé pour produire le mail exact à partir du même JSON. La Collecte et le Rendu HTML restent inchangés.

## Drapeaux ouverts

- Logo conservé en base64 : HTML autonome, sans image distante, à la demande explicite de l’utilisateur.
- Capacité réelle du nouveau Projet à reproduire le gabarit sur plusieurs paquets → trois essais non fidèles ; livraison du Projet non validée.
- Transport et rendu dans un véritable message Outlook → non exercés à ce stade.
- La préparation du téléchargement de l’outil est exercée avec une simulation du DOM. L’utilisateur a confirmé l’aperçu sur son poste ; le téléchargement effectif, la réouverture et le poste de la collègue restent à vérifier.

## Sources consultées

- `AGENTS.md`, `README.md`, `NOTICE-V5.23.md`, prompts et contrat actifs.
- `_source/05-BLOCS-HTML-CANONIQUES.md` et scripts de génération, rendu et validation.
- `RAPPORT-V5.23.md` et comptes rendus d’installation V5.17 et de stabilisation V5.23.

## Prochaine étape

Le fichier `outil-rendu-dsfr.html` remplace le candidat Assistant pour ce parcours métier. Ses scripts produisent un HTML identique au canon sur dix variantes, dont les paquets vides, le paquet fourni, 60 articles et des contenus contenant du balisage. Aucun contenu n’est confié à un modèle pour le rendu.

Les 53 tests, Ruff et les trois contrôles de génération réussissent. La relecture indépendante a confirmé la correction du défaut de lien révoqué. L’utilisateur confirme l’aperçu après chargement par URL Blob ; le téléchargement natif et le transport dans Outlook restent à contrôler. Le détail des preuves figure dans `../_documentation/recette-mail-dsfr/RAPPORT.md`.

Pour préparer la démonstration, l’utilisateur a confirmé le ménage des projets. Dix anciennes versions SNUM ont été supprimées. Collecte v5.23.6, Rendu HTML v5.23.6 et rendu DSFR sont conservés ; leurs instructions et ressources restent préservées. Les deux autres projets sans lien avec la newsletter sont conservés.
