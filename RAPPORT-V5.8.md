# Rapport de contrôle du kit SNUM V5.8

## Résultat

Le kit V5.8 corrige la stratégie de recherche Web, le filtre d’admissibilité, le prompt de lancement à variables et le gabarit HTML. La fidélité locale du gabarit est établie contre `bacoco/revue-presse-snum` au SHA `dc3c87f4f4e7305de0cd9c71da25171252402a83`.

La réussite de DINUM n’est pas déduite de ces contrôles locaux. Elle dépend de la recette finale exécutée dans le Projet `newsletter_BGS` après remplacement des fichiers corrigés.

## Changements

- Prompt système ramené sous 1 200 caractères et recentré sur les règles éliminatoires.
- Prompt de lancement paramétré par `{{DATE_EDITION_LONGUE}}`, `{{DATE_DEBUT}}` et `{{DATE_FIN}}`.
- Requêtes Web courtes, domaines canoniques et poursuite après un échec technique.
- Exclusion sans exception des dates hors fenêtre, accès partiels, payants ou avec compte.
- Exclusions interdites dans la revue et le HTML.
- Titres de sortie simples, sans gras ni séparateurs décoratifs.
- Coque, cartes, articles, pied de page, modal et CSS alignés sur le dépôt de référence.

## Recettes DINUM rejetées

### Recette 1

La recherche Web a produit une revue non vide, mais la sortie a retenu des contenus hors fenêtre et un article reconnu payant. Elle a aussi dépassé les limites de mots et indiqué un jour de semaine erroné. Verdict : rejetée.

### Recette 2

La recherche Web a retenu deux articles datés dans la fenêtre et a exclu l’article payant. Cependant, un candidat de novembre 2025 est resté dans la revue avec la mention « exclu », certains champs dépassaient les limites et la coque HTML ne correspondait pas au gabarit. Le HTML contenait notamment un attribut de header mal formé et omettait le modal de thème. Verdict : rejetée.

Les titres `REVUE`, `HTML COMPLET` et `DOSSIER PRIVÉ` n’étaient plus entourés de gras dans cette deuxième sortie.

## Contrôles locaux exécutés

- SHA du dépôt de référence obtenu par clonage en lecture seule : `dc3c87f4f4e7305de0cd9c71da25171252402a83`.
- Coque paramétrée comparée au `index.html` de référence après substitution des seules zones variables : identité normalisée confirmée.
- Structure d’une carte « L’essentiel » et d’un article de rubrique comparée à la source : identité confirmée.
- Bloc `CSS-DE-RÉFÉRENCE` comparé à `styles.css` : identité octet par octet confirmée hors saut final.
- Document synthétique rempli avec le contenu de référence soumis localement à Nu : aucune erreur.
- ZIP contrôlé : cinq Markdown à la racine et contenus identiques aux fichiers sources.
- Prompt système : 1 193 caractères hors saut final.

Nu contrôle la validité HTML, pas la conformité RGAA. La comparaison locale du modèle ne valide pas automatiquement un futur HTML généré par DINUM.

## Limites

- Aucun audit RGAA complet n’a été exécuté.
- Aucune newsletter n’a été publiée et aucun courriel n’a été envoyé.
- Un HTML ouvert directement comme fichier local ne charge pas nécessairement `/revue-presse-snum/styles.css?v=20260917` ; ce comportement ne constitue pas une différence avec le gabarit publié.
