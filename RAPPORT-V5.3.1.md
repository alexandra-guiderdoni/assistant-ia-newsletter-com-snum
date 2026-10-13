# Compte rendu du kit SNUM V5.3.1

## Résultat

Le kit contient cinq fichiers de connaissance et un prompt système séparé de 1 151 caractères Unicode hors saut final, soit 1 152 avec celui-ci et 1 202 octets en UTF-8. Le gabarit HTML est vide, conserve la structure de Loïc et embarque le CSS de référence pour rester correctement présenté lorsqu’il est ouvert localement.

Cette validation établit la cohérence du kit et du gabarit. Deux sorties réelles V5.3 ont été observées : elles démontrent l’arrêt `A_COMPLETER`, mais ni une collecte autonome correcte ni la génération du HTML. La V5.3.1 reste à tester dans DINUM.

## Changements principaux

- Passage de V5.3 à V5.3.1 dans les cinq documents actifs.
- Ouverture obligatoire des URL officielles exactes, liens ELI, articles ou PDF publics avant de conclure qu’un texte est inaccessible.
- Interdiction explicite de demander le corps ou la capture d’un article `PAYANT_OU_LOGIN`.
- Livraison d’une revue courte et de son HTML dès un événement admissible ; avec un ou deux événements, suppression complète de L’essentiel et état `A_COMPLETER`.
- Arrêt sans revue ni HTML uniquement lorsqu’aucun événement n’est admissible.
- Retrait du lien éditorial figé concernant le budget 2027.
- Retrait de la copie complète et vieillissante des archives ; seul un fragment d’insertion vide reste fourni.
- Remplacement des cinq modèles d’article répétés par un fragment ARTICLE duplicable sans plafond de sujets.
- Séparation explicite entre sélection éditoriale et assemblage HTML.
- Conservation du lien public vers `styles.css` et ajout du même CSS dans la page pour la prévisualisation locale.
- Interdiction vérifiable des emplacements non remplacés, des rubriques vides et des rubriques inventées par commodité.
- Ajout d’une recette objective portant sur la sortie exacte, sans présenter l’autoévaluation du modèle comme un contrôle externe.
- Parcours utilisateur réduit à un remplacement de cinq fichiers, un prompt et une commande de production.

## Capacités établies par les sources publiques

Révisions examinées : fork `bacoco/conversations` à `febfb6f6b6f1fd904b2f82aed2971957d7a29ef4`, dépôt amont `suitenumerique/conversations` à `b1daaa9e4c381bdc881741858a930ea1e4349aec`, site de Loïc à `dc3c87f4f4e7305de0cd9c71da25171252402a83`.

Faits établis :

- La valeur par défaut de `PROJECT_FILES_MAX_COUNT` est 10 et le contrôle est réalisé à l’import. Le réglage est configurable.
- Le 13 octobre 2026, l’API publique de l’instance a annoncé 15 fichiers de Projet, 10 Mo par fichier et l’acceptation de Markdown et HTML, sans CSS autonome. Cette observation actuelle ne réécrit pas l’observation antérieure de l’utilisatrice ni la valeur par défaut du code.
- Les fichiers du Projet sont indexés de façon asynchrone. Le modèle dispose d’une recherche de passages et, dans un Projet, d’un outil de synthèse des fichiers. Une liste de fichiers ou une synthèse ne prouve pas que chaque passage a été relu exactement.
- Les instructions du Projet sont injectées dans le contexte. Le code du fork limite actuellement leur champ à 4 000 caractères ; la cible prudente du kit reste inférieure à 1 200 caractères à cause de la troncature déjà observée dans l’instance.
- La recherche Web est activable par conversation et son implémentation dépend du modèle configuré. Le moteur Staan présent dans le fork fournit des extraits et des morceaux supplémentaires ; le moteur Brave peut extraire une page ou renvoyer des morceaux RAG. Le code n’établit pas lequel est affecté au modèle utilisé dans la session.
- La seule génération de fichier dédiée trouvée est celle des présentations PowerPoint. Aucune génération générique de fichier HTML, écriture GitHub, messagerie ou planification de Projet n’a été trouvée dans les surfaces examinées.
- Aucune convention de chargement automatique d’`AGENTS.md` n’a été trouvée. Le prompt renvoie donc explicitement aux cinq documents.

Sources primaires :

- [Limite et indexation des fichiers de Projet](https://github.com/bacoco/conversations/blob/febfb6f6b6f1fd904b2f82aed2971957d7a29ef4/docs/project-file-indexing.md)
- [Contrôle d’import des pièces](https://github.com/bacoco/conversations/blob/febfb6f6b6f1fd904b2f82aed2971957d7a29ef4/src/backend/chat/views/attachments.py)
- [Instructions du Projet et limite de 4 000 caractères](https://github.com/bacoco/conversations/blob/febfb6f6b6f1fd904b2f82aed2971957d7a29ef4/src/backend/chat/serializers.py)
- [Composition du contexte, outils documentaires et recherche Web](https://github.com/bacoco/conversations/blob/febfb6f6b6f1fd904b2f82aed2971957d7a29ef4/src/backend/chat/clients/pydantic_ai.py)
- [Recherche Staan par extraits](https://github.com/bacoco/conversations/blob/febfb6f6b6f1fd904b2f82aed2971957d7a29ef4/src/backend/chat/tools/web_search_staan.py)
- [Recherche Brave et extraction de pages](https://github.com/bacoco/conversations/blob/febfb6f6b6f1fd904b2f82aed2971957d7a29ef4/src/backend/chat/tools/web_search_brave.py)
- [Configuration publique de l’instance](https://assistant.numerique.gouv.fr/api/v1.0/config/)
- [HTML de référence de Loïc](https://github.com/bacoco/revue-presse-snum/blob/dc3c87f4f4e7305de0cd9c71da25171252402a83/index.html)
- [CSS de référence de Loïc](https://github.com/bacoco/revue-presse-snum/blob/dc3c87f4f4e7305de0cd9c71da25171252402a83/styles.css)

## Cause de la mauvaise présentation observée

`test.html` charge le CSS personnalisé par un chemin absolu du site. Ouvert seul depuis le disque, ce chemin ne résout pas `styles.css` : le DSFR reste chargé depuis son CDN, mais l’organisation visuelle propre à Loïc disparaît. Le même fichier retrouve sa grille et sa hiérarchie lorsqu’il est servi avec le CSS au bon chemin.

La V5.3.1 conserve le chemin requis pour GitHub Pages et embarque une copie figée du CSS. Le gabarit peut donc être prévisualisé localement sans pièce CSS séparée.

## Retours de l’essai réel V5.3

La première sortie a correctement respecté la fenêtre et refusé d’inventer une lecture intégrale, mais elle a demandé les copies de trois articles payants. La seconde a documenté les requêtes, puis a déclaré inaccessibles deux textes Légifrance publiquement disponibles et s’est arrêtée sans HTML. Le décret n° 2026-928 était publié sous `JORFTEXT000054953345`, différent de l’identifiant interrogé ; le décret n° 2026-944 était disponible par son URL ELI avec ses cinq articles.

Ces résultats identifient deux causes : la conclusion d’inaccessibilité tirée d’une URL ou d’une extraction défaillante, puis la règle V5.3 imposant au moins trois événements avant toute livraison. Ils ne permettent pas d’évaluer la mise en page HTML, puisqu’aucun HTML V5.3 n’a été généré.

## Contrôles réellement exécutés

- Validation Nu de la coque standard et de sa variante sans le lien ni la section L’essentiel : aucune erreur.
- Comparaison du CSS intégré avec `styles.css` au SHA fixé : contenu identique après retrait de l’indentation du bloc HTML.
- Structure de la coque standard : un `h1`, exactement trois cartes essentielles, trois accès rapides et leurs cibles, un identifiant `navigation`, un footer complet, un script module et un script `nomodule` DSFR 1.15.2. La variante courte retire entièrement le lien et la section L’essentiel.
- Contenu vide : aucune actualité, date d’édition, URL d’article ni entrée d’archives figée.
- Marquage : trois `p.fr-tag`, aucun `span.fr-tag` dans la coque.
- Navigateur Chrome local sur la coque standard, dont le HTML et le CSS restent inchangés : CSS intégré appliqué ; trois colonnes à 1 440 px, une colonne à 360 px, aucun débordement horizontal à 200 %.
- Contrôle des accents exécuté après chaque écriture Markdown.
- Prompt système mesuré à 1 151 caractères Unicode hors saut final, soit 1 152 avec celui-ci et 1 202 octets en UTF-8.
- Archive contrôlée : cinq entrées Markdown à la racine, aucune autre pièce. Empreinte SHA-256 : `6e9ed0fb31814f7f10cae4bdba5e00281f7c31ea3ccc46820461369cd7226722`.

Ces contrôles portent sur la coque V5.3.1. Ils ne valident ni les faits, ni les longueurs, ni les liens, ni l’accessibilité complète d’une future édition remplie. Nu n’est pas un audit RGAA.

## Limites et inconnues

- Le moteur Web et ses réglages réellement associés au modèle de la session ne sont pas accessibles sans authentification ; le dépôt montre des possibilités, pas le déploiement effectif.
- Une recherche pouvant ne livrer que des extraits, l’autonomie éditoriale complète n’est pas garantie. Le parcours de repli demande les textes publics complets dans une seule pièce temporaire.
- La capacité de rendre un véritable fichier HTML téléchargeable n’est pas démontrée. Le kit accepte donc un unique bloc HTML complet copiable.
- La variante courte sans L’essentiel passe Nu, mais n’a pas encore été produite ni contrôlée visuellement dans DINUM avec un contenu réel.
- Aucune planification automatique n’est prévue : les deux lancements hebdomadaires restent manuels.
- La publication, la vérification GitHub Pages et l’envoi restent humains et séparés.
- Un essai réel V5.3.1 reste nécessaire. Son verdict doit porter sur la collecte, la production complète et le HTML rendu, pas sur la récitation des consignes.

## PDG self-check, pas une revue indépendante

Les sources capables d’invalider les affirmations ont été ouvertes à des SHA fixes. Le chevauchement avec la V5.2 a été classé « étendre » : les règles éditoriales et opérationnelles sont conservées, seul le mécanisme HTML est simplifié. Le mauvais chemin testé est l’ouverture locale sans CSS externe ; le garde-fou ajouté est le CSS figé intégré. Les raccourcis interdits restent : revue préremplie, validation transférée d’un autre HTML, lecture intégrale inventée, publication ou envoi prétendus, ordonnanceur supposé. La preuve de non-régression est limitée au gabarit et aux contrôles listés ci-dessus.
