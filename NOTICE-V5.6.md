# Installer et utiliser le kit SNUM V5.6

## Installation unique

1. Décompresser `kit-dinum-snum-v5-6-production-5-fichiers.zip`.
2. Dans le Projet DINUM, remplacer tous les anciens fichiers de connaissance par les cinq Markdown du ZIP.
3. Coller tout le contenu de `PROMPT-SYSTEME-SNUM-V5.6.md` dans « Instructions (expérimental) ».
4. Ouvrir une nouvelle conversation dans ce Projet et activer « Rechercher sur le web ».

Le ZIP seul s’importe après décompression. Le prompt système, cette notice, le générateur, le gabarit et le rapport ne sont pas des fichiers de connaissance.

## Commande pour reprendre le brouillon connu

Envoyer uniquement :

> Reprends le brouillon `2026-10-13-brouillon-01` et sa fenêtre déjà fixée du 2 au 12 octobre 2026 inclus. Prépare la revue SNUM selon le Projet. Livre uniquement le JSON V5.6 demandé. Ne publie rien et n’envoie rien.

DINUM doit rendre un seul bloc JSON. Il rédige et sélectionne le contenu ; il ne fabrique plus le HTML.

## Produire les livrables

1. Copier toute la réponse JSON de DINUM.
2. Ouvrir Terminal et lancer exactement :

```bash
cd /Users/alex/Claude/projets-actifs/assistant-ia-newsletter-com-snum
./generer-revue.command
```

Le dossier `livrable-AAAA-MM-JJ` contient la revue Markdown, le HTML, le dossier privé et le JSON source. Si DINUM remet un fichier JSON téléchargé, lancer à la place :

```bash
./generer-revue.command /chemin/vers/le-fichier.json
```

Une erreur commence par `ERREUR` et nomme le champ à faire corriger. Ne retoucher ni le JSON ni le HTML à la main : demander à DINUM de corriger seulement l’erreur indiquée.

## Commande réutilisable

Après établissement d’une première borne de collecte réussie :

> Prépare la nouvelle revue SNUM selon le Projet, avec les informations publiées depuis la dernière collecte réussie. Livre uniquement le JSON V5.6 demandé. Ne publie rien et n’envoie rien.

## Mise à jour après preuves réelles

> Voici les preuves réelles de publication et d’envoi de l’édition [date] : [preuves]. Produis `01-ETAT-HISTORIQUE.md` complet actualisé, prêt à remplacer l’ancien fichier. Ne publie rien et n’envoie rien.
