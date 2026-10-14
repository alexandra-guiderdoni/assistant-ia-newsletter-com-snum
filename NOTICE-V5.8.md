# Configurer l’Assistant DINUM pour la revue SNUM V5.8

Ce guide permet à une personne métier de créer son Projet dans l’Assistant DINUM et d’obtenir la revue, le HTML complet ou un arrêt explicite directement dans le chat. Aucun script, terminal, dépôt GitHub ou outil local n’est nécessaire sur son poste.

## Résultat attendu

La réponse finale apparaît dans une seule conversation, dans cet ordre :

1. `REVUE` ;
2. `HTML COMPLET` ;
3. `DOSSIER PRIVÉ`.

Le chat est le canal de livraison. La V5.8 ne publie pas sur GitHub Pages et n’envoie pas de courriel.

Le modèle peut encore s’écarter du gabarit malgré son auto-contrôle. Si le HTML canonique n’est pas établi, la sortie sûre est :

```text
A_COMPLETER — HTML canonique non établi
```

Cette sortie constitue un arrêt contrôlé, pas une newsletter publiable.

## Choisir le bon paquet source

Utiliser `kit-dinum-snum-v5-8-assistant-only-6-fichiers.zip`.

Le paquet `kit-dinum-snum-v5-8-production-5-fichiers.zip` reste une archive V5.8, mais il ne contient pas `05-BLOCS-HTML-CANONIQUES.md`. Il ne suffit donc pas, seul, pour le parcours Assistant-only.

Préparer également le fichier `PROMPT-SYSTEME-SNUM-V5.8.md`, situé à côté du ZIP dans le code source.

## Étape 1 — Extraire le paquet

Décompresser le ZIP dans un dossier de travail. Le dossier doit contenir exactement ces six fichiers :

1. `00-PROMPT-PROJET.md` ;
2. `01-ETAT-HISTORIQUE.md` ;
3. `02-METHODE-EDITORIALE.md` ;
4. `03-GABARIT-HTML.md` ;
5. `04-RELAIS-HUMAIN.md` ;
6. `05-BLOCS-HTML-CANONIQUES.md`.

Ne pas téléverser le ZIP lui-même. Ne pas ajouter `_documentation/prompt-loic.md` : il archive un ancien prompt de planification et ne remplace pas le prompt système V5.8.

## Étape 2 — Créer un Projet

1. Ouvrir <https://assistant.numerique.gouv.fr/>.
2. Ouvrir le panneau de gauche.
3. Choisir **Nouveau projet**.
4. Donner un nom explicite, par exemple `Newsletter SNUM - Production V5.8`.

Créer un Projet neuf évite de mélanger la V5.8 avec d’anciennes instructions ou pièces jointes.

![Projet et conversation dans l’Assistant](./_documentation/validation-v5.8-2026-10-14/captures/02-projet-et-conversation.png)

## Étape 3 — Ajouter le prompt système

1. Ouvrir `PROMPT-SYSTEME-SNUM-V5.8.md` depuis le code source.
2. Copier tout son contenu, de la première à la dernière ligne.
3. Le coller dans **Instructions (expérimental)**.
4. Ne pas le résumer, le reformuler ni retirer les blocs HTML, les marqueurs ou la règle d’arrêt.

Le premier contrôle consiste à retrouver dans le champ les expressions suivantes :

- `05-BLOCS-HTML-CANONIQUES.md` ;
- `RÈGLE-DE-COPIE` ;
- `A_COMPLETER — HTML canonique non établi` ;
- `## REVUE`, `## HTML COMPLET` et `## DOSSIER PRIVÉ`.

## Étape 4 — Téléverser les six fichiers

1. Dans la zone **Fichiers**, choisir **Ajouter des fichiers**.
2. Sélectionner ensemble les six fichiers Markdown extraits.
3. Vérifier leurs six noms dans le formulaire.
4. Choisir **Créer un projet**.
5. Attendre la disparition du message indiquant que les fichiers sont en cours d’indexation.

Ne pas envoyer de demande tant que l’interface annonce que les fichiers seront ignorés : la conversation partirait sans sa base de connaissances.

## Étape 5 — Ouvrir une conversation liée au Projet

Utiliser **Nouvelle conversation** depuis le Projet créé. Dans le panneau de gauche, la conversation doit apparaître sous le nom du Projet.

Une conversation générale créée hors du Projet ne garantit pas l’accès aux six fichiers.

![Conversation neuve](./_documentation/validation-v5.8-2026-10-14/captures/01-conversation-neuve.png)

## Étape 6 — Préparer les trois dates

Avant l’envoi, déterminer :

- la date de l’édition ;
- le début inclus de la collecte ;
- la fin incluse de la collecte.

Ne jamais laisser les variables entre accolades dans la demande. Si la fenêtre n’est pas connue, la faire confirmer par le responsable éditorial avant la génération.

## Étape 7 — Activer la recherche Web

Dans le menu des actions de la zone de saisie, activer **Rechercher sur le web** lorsqu’elle est proposée. Le démarrage effectif se reconnaît au message `Recherche…`.

Si le Web n’est pas disponible, ne pas prétendre qu’une collecte réelle a été faite. La conversation peut seulement traiter des sources intégrales fournies et correctement datées.

## Étape 8 — Envoyer la demande

Remplacer les trois dates dans ce modèle, puis l’envoyer en un seul message :

```text
Prépare à partir de zéro la revue SNUM du {{DATE_EDITION_LONGUE}}, pour les informations publiées du {{DATE_DEBUT}} au {{DATE_FIN}} inclus, heure de Paris. Lance la recherche Web et réalise toute la production selon le Projet. Livre la revue, un unique bloc HTML complet strictement fidèle aux blocs canoniques et le dossier privé directement dans ce chat. Ne reprends aucun ancien brouillon. Ne publie rien et n’envoie rien.
```

Exemple renseigné :

```text
Prépare à partir de zéro la revue SNUM du 14 octobre 2026, pour les informations publiées du 3 octobre 2026 au 13 octobre 2026 inclus, heure de Paris. Lance la recherche Web et réalise toute la production selon le Projet. Livre la revue, un unique bloc HTML complet strictement fidèle aux blocs canoniques et le dossier privé directement dans ce chat. Ne reprends aucun ancien brouillon. Ne publie rien et n’envoie rien.
```

## Étape 9 — Attendre la livraison complète

Ne pas interrompre la conversation pendant `Lecture des instructions du projet…` ou `Recherche…`. La livraison est terminée lorsque le bouton **Stop** disparaît et que la zone de saisie redevient disponible.

![Réponse finalisée dans le chat](./_documentation/validation-v5.8-2026-10-14/captures/03-reponse-finalisee.png)

## Étape 10 — Contrôler avant utilisation

La vérification métier minimale porte sur la réponse exacte du chat :

- les trois titres sont présents dans le bon ordre ;
- chaque source retenue est datée dans la fenêtre et intégralement accessible ;
- aucun marqueur `@@` ne subsiste ;
- à partir de trois événements, « L’essentiel » contient exactement trois cartes ;
- seules les rubriques `numerique`, `ia`, `commande`, `rh` et `bercy` sont utilisées ;
- chaque rubrique affichée figure aussi dans la navigation ;
- un seul `h1`, trois accès rapides et les deux scripts DSFR 1.15.2 sont présents ;
- le modal `fr-theme-modal` se trouve après le footer ;
- aucune affirmation de contrôle n’est contredite par le texte ou le HTML.

Si un seul de ces points reste incertain, conserver l’état `A_COMPLETER` et demander un contrôle extérieur. L’auto-évaluation du modèle n’est pas une preuve de conformité.

## Incidents courants

### Les fichiers sont annoncés comme ignorés

Attendre la fin de l’indexation. Si le message persiste, ouvrir une nouvelle conversation depuis le Projet après indexation.

### L’Assistant demande encore la fenêtre

Répondre avec les deux bornes incluses. Ne pas lui demander de les inventer depuis un ancien brouillon.

### Le HTML contient des marqueurs ou des rubriques inventées

Ne pas le corriger manuellement dans le chat et ne pas le publier. La réponse acceptable est l’arrêt `A_COMPLETER — HTML canonique non établi`.

### La réponse ne contient pas de HTML

Lire `DOSSIER PRIVÉ`. Si le modèle explique qu’il ne peut pas établir le HTML canonique, le garde-fou a fonctionné. Ce résultat doit être repris ou contrôlé, pas présenté comme une édition prête.

## Recette autonome du 14 octobre 2026

Un Projet neuf a été créé avec le prompt source exact et les six fichiers. La demande portait sur l’édition du 14 octobre et la fenêtre du 3 au 13 octobre 2026 inclus. L’envoi a attendu la fin de l’indexation et la recherche Web s’est exécutée.

[Ouvrir la conversation de recette](https://assistant.numerique.gouv.fr/chat/33dab78f-39a8-4140-b364-10c9023b8e20/)

L’Assistant n’a retenu aucun événement. Il a déclaré dans `DOSSIER PRIVÉ` que le bloc `COQUE` n’avait pas été retrouvé et que le HTML était une reconstruction partielle. Il a pourtant affiché 5 454 caractères de HTML au lieu de l’arrêt obligatoire.

Le contrôle du bloc livré constate notamment :

- dépendances `cdn.gouv.fr` non canoniques à la place de `cdn.jsdelivr.net` ;
- absence du composant `fr-skiplinks` ;
- absence de `<main id="main">` ;
- absence du script module `dsfr.module.min.js` ;
- présence du script nomodule et du modal de thème ;
- aucun marqueur `@@` restant.

Verdict : le canal de livraison dans le chat fonctionne, mais cette recette est `NO-GO` pour une acceptation autonome. Le statut `A_COMPLETER` est cohérent ; le HTML affiché ne doit pas être utilisé.

## Tentative de prompt monobloc

Une tentative complémentaire a placé directement les blocs HTML canoniques dans le prompt système. Elle ne peut pas être livrée : le champ **Instructions (expérimental)** de l’Assistant DINUM accepte au maximum 4 000 caractères, alors que le prompt obtenu en compte 14 466.

Après collage, l’interface a conservé exactement 4 000 caractères et a tronqué le texte avant `<!doctype html>`. Même la seule coque canonique compactée compte 5 464 caractères. Le Projet invalide a été fermé sans être créé et aucune conversation n’a été lancée avec ce contexte incomplet.

La V5.8 reste donc fondée sur le prompt court et les six fichiers de connaissance. Cette limite n’annule pas le garde-fou `A_COMPLETER`, mais confirme que l’identité autonome du HTML avec Bacoco n’est pas garantie par le prompt système seul.

Le protocole et les mesures sont consignés dans [le résultat de la recette monobloc](./_documentation/validation-v5.8-monobloc-2026-10-14/RESULTAT-RECETTE-MONOBLOC.md).

## Références et preuves

- [Prompt système V5.8](./PROMPT-SYSTEME-SNUM-V5.8.md)
- [Blocs HTML canoniques](./05-BLOCS-HTML-CANONIQUES.md)
- [Guide de validation Assistant-only](./_documentation/validation-v5.8-assistant-only-2026-10-14/GUIDE-VALIDATION-ASSISTANT-DINUM-V5.8-ASSISTANT-ONLY.md)
- [Rendu Bacoco de référence](./_documentation/validation-v5.8-assistant-only-2026-10-14/captures/02-reference-bacoco.png)

Le résultat d’une recette prouve seulement le cas exécuté. Il ne garantit pas que toutes les futures générations reproduiront littéralement le gabarit Bacoco.
