# Installer et tester le kit SNUM V5.4

1. Décompresser `kit-dinum-snum-v5-4-production-5-fichiers.zip`.
2. Dans le Projet DINUM, remplacer les cinq anciens fichiers par les cinq Markdown du ZIP. Les laisser à la racine.
3. Copier tout le contenu de `PROMPT-SYSTEME-SNUM-V5.4.md` dans le champ « Instructions (expérimental) ». Le kit ne dépend pas uniquement de ce champ : `00-PROMPT-PROJET.md` contient aussi les règles de démarrage.
4. Ouvrir une nouvelle conversation dans ce même Projet, avec la recherche Web activée.
5. Envoyer uniquement la commande suivante :

> Commence par ouvrir `00-PROMPT-PROJET.md`, puis prépare la nouvelle revue SNUM selon le Projet, avec les informations publiées depuis la dernière collecte réussie. Livre la revue, son HTML complet autonome dans le gabarit de Loïc et le dossier privé. Ne publie rien et n’envoie rien.

DINUM doit effectuer la collecte avant de conclure `A_COMPLETER`. Avec au moins un événement admissible, il rend la revue et son HTML. Avec un ou deux événements, le HTML ne contient pas de section L’essentiel. Avec zéro événement après collecte réelle, il rend un seul lot `A_COMPLETER`, sans HTML. La coque se récupère par les huit titres `COQUE-01` à `COQUE-08`, jamais en un seul passage. Ne jamais fournir le corps ou la capture d’un article `PAYANT_OU_LOGIN`.

## Après publication et envoi réellement confirmés

Envoyer cette commande avec les preuves obtenues :

> Voici les preuves réelles de publication et d’envoi de l’édition [date] : [preuves]. Produis `02-HISTORIQUE.md` complet actualisé, prêt à remplacer l’ancien fichier. Ne publie rien et n’envoie rien.

Ne pas importer le ZIP, le prompt système, cette notice, le rapport ni `test.html` comme fichiers de connaissance. Les cinq fichiers à importer sont `00-PROMPT-PROJET.md`, `01-MODELE-EDITORIAL.md`, `02-HISTORIQUE.md`, `03-PUBLICATION-DIFFUSION.md` et `04-INTEGRATION-HTML.md`.
