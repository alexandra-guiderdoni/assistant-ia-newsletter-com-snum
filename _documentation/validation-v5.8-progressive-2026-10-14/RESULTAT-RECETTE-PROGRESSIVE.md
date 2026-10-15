# Résultat de la recette V5.8 progressive du 14 octobre 2026

## Objet

Cette recette vérifie si l’Assistant DINUM peut produire dans le chat un HTML fidèle au canon Bacoco malgré la limite de 4 000 caractères du champ **Instructions (expérimental)**.

Aucune publication GitHub Pages et aucun envoi de courriel n’ont été réalisés.

## Dispositif testé

Un Projet neuf, `Newsletter SNUM - V5.8 progressive - Recette 2`, a été créé avec :

- le prompt système V5.8 progressif ;
- huit fichiers Markdown ;
- une fenêtre de collecte du 3 au 13 octobre 2026 inclus ;
- une date d’édition au 14 octobre 2026.

Le prompt système a été accepté sans troncature. Les huit noms de fichiers ont été visibles avant la création du Projet et l’envoi a attendu la fin de l’indexation.

## Architecture de divulgation progressive

`05-INDEX-HTML.md` fournit un ordre `READ_NEXT` et les jetons à rechercher. La coque est séparée entre `06-COQUE-DEBUT.md` et `07-COQUE-FIN.md`. Les éléments duplicables sont isolés dans `08-BLOC-ESSENTIEL.md` et `09-BLOCS-RUBRIQUES.md`.

Chaque ressource destinée à la récupération reste sous 4 000 caractères. Les fichiers sont générés depuis `05-BLOCS-HTML-CANONIQUES.md` ; ils ne créent pas une seconde source éditable.

## Résultats observés

### 1. Récupération du canon

Deux conversations ont répondu `CANON_HTML_PRET` et listé les six paires :

- `SNUM_SHELL_HEAD_START / SNUM_SHELL_HEAD_END` ;
- `SNUM_SHELL_TAIL_START / SNUM_SHELL_TAIL_END` ;
- `SNUM_ESSENTIAL_START / SNUM_ESSENTIAL_END` ;
- `SNUM_RUBRIC_START / SNUM_RUBRIC_END` ;
- `SNUM_WATCH_START / SNUM_WATCH_END` ;
- `SNUM_EMPTY_START / SNUM_EMPTY_END`.

Verdict partiel : la divulgation progressive résout la recherche des blocs malgré la limite du prompt.

### 2. Production immédiatement après le canon

Une production en deux phases a livré les trois titres, un bloc HTML complet et un dossier privé. Le HTML reprenait la coque, le footer, le modal et les scripts attendus.

Les écarts restants portaient sur le contenu :

- publications hors fenêtre retenues ;
- dates d’événement confondues avec les dates de publication ;
- titres de rubrique en casse non canonique ;
- liens de navigation pour des sections absentes.

Conversation : <https://assistant.numerique.gouv.fr/chat/88b774da-c07b-4b78-a5bb-22739def300f>

### 3. Durcissement de la règle de date

Le prompt a été renforcé avec la date de publication de la page comme seule date d’admissibilité, les libellés exacts de rubrique et la navigation conditionnelle.

Le premier passage a néanmoins classé le 6 octobre hors d’une fenêtre allant du 3 au 13 octobre. Une phase d’audit avec l’inégalité ISO a corrigé cette contradiction, sans produire une revue visible complète.

Conversation : <https://assistant.numerique.gouv.fr/chat/066f718b-db2f-432c-a576-ec96104ebb57>

### 4. Séparation des responsabilités

La recette a ensuite séparé les tâches :

1. collecte Web sans revue ni HTML ;
2. validation des dates et doublons sans Web ;
3. chargement du canon sans Web ;
4. rendu sans Web.

La collecte a produit cinq candidats. La validation a conservé trois sources datées du 6 octobre, écarté un titre incohérent entre 2025 et 2026 et supprimé un doublon.

Un premier rendu a malgré tout reconstruit un HTML étranger au canon : titre, feuilles CSS, structure des cartes, archives, footer et modal différaient.

Le canon a été rechargé immédiatement avant une nouvelle tentative. Cette fois, le garde-fou a refusé l’assemblage et renvoyé :

```text
A_COMPLETER — HTML canonique non établi
```

Conversation : <https://assistant.numerique.gouv.fr/chat/4dddefda-e5da-4736-b4ca-9464e8b5c9dd>

## Diagnostic

La limite des 4 000 caractères n’est plus le blocage principal. Trois comportements distincts sont observés :

1. l’index et les jetons permettent de retrouver les fragments ;
2. les dates deviennent plus fiables quand collecte et validation sont séparées ;
3. la copie littérale de plusieurs fragments dans une longue réponse reste non déterministe.

Le troisième point ne peut pas être garanti par du texte supplémentaire dans le prompt. L’Assistant peut déclarer les jetons présents puis reconstruire un autre HTML, ou détecter une divergence et s’arrêter.

## Décision de livraison

Le kit progressif est livré avec le protocole en quatre messages et l’arrêt fermé. Il ne doit pas être présenté comme une génération HTML autonome garantie.

Le résultat acceptable sans validateur externe est :

- soit un HTML contrôlé extérieurement ;
- soit `A_COMPLETER — HTML canonique non établi` sans code HTML.

Le résultat interdit est un HTML reconstruit accompagné d’une affirmation de conformité non prouvée.

## Contrôles locaux

Les contrôles finaux doivent être relancés après toute modification :

```text
python3 scripts/build_progressive_kit.py --check
python3 -m unittest tests/test_progressive_kit.py tests/test_newsletter_html.py
git diff --check
```

Le contrôle automatique couvre les tailles, la recomposition des fragments, le contenu du ZIP, la validation du gabarit et les titres canoniques de rubrique. Il ne couvre pas la fidélité future d’une génération non déterministe de l’Assistant.

## PDG self-check, not independent review

- source canonique unique conservée ;
- fragments générés, pas édités en parallèle ;
- protocole séparé en phases nommées ;
- arrêt et limites visibles ;
- aucun outil local demandé au métier ;
- aucun changement du dépôt Bacoco ;
- aucune publication ni diffusion pendant la recette.
