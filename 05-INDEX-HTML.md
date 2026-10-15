# Index HTML canonique - V5.12 progressive

SNUM_CANON_V512_INDEX_START

## READ_NEXT

Lire intégralement, dans cet ordre et un fichier à la fois :

1. `06-COQUE-DEBUT.md` : `SNUM_SHELL_HEAD_START` à `SNUM_SHELL_HEAD_END` ;
2. `07-PIED-DE-PAGE.md` : `SNUM_FOOTER_START` à `SNUM_FOOTER_END` ;
3. `08-BLOC-ESSENTIEL.md` : les trois paires `SNUM_ESSENTIALS_OPEN`, `SNUM_ESSENTIAL_CARD` et `SNUM_ESSENTIALS_CLOSE` ;
4. `09-BLOCS-RUBRIQUES.md` : les cinq paires `SNUM_RUBRIC_OPEN`, `SNUM_RUBRIC_ARTICLE`, `SNUM_RUBRIC_CLOSE`, `SNUM_WATCH` et `SNUM_EMPTY`.
5. `10-COQUE-FIN.md` : `SNUM_SHELL_CLOSE_START` à `SNUM_SHELL_CLOSE_END`.

La page complète est la concaténation exacte de `06`, du contenu éditorial, de `07`, puis de `10`. Pour `L’essentiel`, concaténer `ESSENTIALS_OPEN`, exactement trois répétitions de `ESSENTIAL_CARD`, puis `ESSENTIALS_CLOSE`. Pour chaque rubrique, concaténer `RUBRIC_OPEN`, une répétition de `RUBRIC_ARTICLE` par source valide de la rubrique, puis `RUBRIC_CLOSE`. Remplacer ensuite les marqueurs.

Rubriques exactes :

- `numerique` : navigation `Numérique`, titre et tag `NUMERIQUE`, enveloppe `<section id="numerique">` ;
- `ia` : navigation `Intelligence artificielle`, titre et tag `INTELLIGENCE ARTIFICIELLE (IA)`, enveloppe `<section id="ia" class="section-muted">` ;
- `commande` : navigation `Commande publique`, titre et tag `COMMANDE PUBLIQUE`, enveloppe `<section id="commande">` ;
- `rh` : navigation `Ressources humaines`, titre et tag `RESSOURCES HUMAINES`, enveloppe `<section id="rh" class="section-muted">` ;
- `bercy` : navigation `Vie de Bercy`, titre et tag `VIE DE BERCY`, enveloppe `<section id="bercy">`.

Avec moins de trois événements, ne produire ni section ni lien `L’essentiel`. À partir de trois événements, insérer exactement trois cartes essentielles et ajouter la navigation `L’essentiel`. Ajouter `À surveiller` seulement si sa section existe. Ne jamais inventer une autre rubrique.

Chaque source valide figure une fois dans sa rubrique. Une carte essentielle est une mise en avant supplémentaire et ne remplace jamais l’article de rubrique.

Pour chaque lien `href="#id"` du menu de rubriques, produire exactement une section `id="id"`. Chaque rubrique produite possède exactement un lien dans ce menu.

Si un jeton manque après une recherche ciblée, répondre `CANON_HTML_INCOMPLET | jeton manquant`. Pendant `RENDU`, un échec doit répondre `A_COMPLETER`, puis `## CONTROLES_EN_ECHEC` et une ligne `CODE | détail`, sans HTML.

SNUM_CANON_V512_INDEX_END
