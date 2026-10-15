# Index HTML canonique - V5.9 progressive

SNUM_CANON_V59_INDEX_START

## READ_NEXT

Lire intégralement, dans cet ordre et un fichier à la fois :

1. `06-COQUE-DEBUT.md` : `SNUM_SHELL_HEAD_START` à `SNUM_SHELL_HEAD_END` ;
2. `07-COQUE-FIN.md` : `SNUM_SHELL_TAIL_START` à `SNUM_SHELL_TAIL_END` ;
3. `08-BLOC-ESSENTIEL.md` : `SNUM_ESSENTIAL_START` à `SNUM_ESSENTIAL_END` ;
4. `09-BLOCS-RUBRIQUES.md` : les trois paires `SNUM_RUBRIC`, `SNUM_WATCH` et `SNUM_EMPTY`.

La coque complète est la concaténation exacte des blocs HTML `06`, puis `07`. Remplacer ensuite ses marqueurs. Dupliquer uniquement la carte de `08` et l’élément `article` du bloc `RUBRIQUE` de `09`.

Rubriques exactes :

- `numerique` : navigation `Numérique`, titre et tag `NUMERIQUE`, enveloppe `<section id="numerique">` ;
- `ia` : navigation `Intelligence artificielle`, titre et tag `INTELLIGENCE ARTIFICIELLE (IA)`, enveloppe `<section id="ia" class="section-muted">` ;
- `commande` : navigation `Commande publique`, titre et tag `COMMANDE PUBLIQUE`, enveloppe `<section id="commande">` ;
- `rh` : navigation `Ressources humaines`, titre et tag `RESSOURCES HUMAINES`, enveloppe `<section id="rh" class="section-muted">` ;
- `bercy` : navigation `Vie de Bercy`, titre et tag `VIE DE BERCY`, enveloppe `<section id="bercy">`.

Avec moins de trois événements, ne produire ni section ni lien `L’essentiel`. À partir de trois événements, insérer exactement trois cartes essentielles et ajouter la navigation `L’essentiel`. Ajouter `À surveiller` seulement si sa section existe. Ne jamais inventer une autre rubrique.

Chaque source valide figure une fois dans sa rubrique. Une carte essentielle est une mise en avant supplémentaire et ne remplace jamais l’article de rubrique.

Pour chaque lien `href="#id"` du menu de rubriques, produire exactement une section `id="id"`. Chaque rubrique produite possède exactement un lien dans ce menu.

Si un jeton de fin manque après une nouvelle recherche ciblée, arrêter avec `A_COMPLETER — HTML canonique non établi` sans produire de code HTML.

SNUM_CANON_V59_INDEX_END
