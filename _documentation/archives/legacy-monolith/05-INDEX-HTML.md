# Index HTML canonique - V5.16 progressive

SNUM_CANON_V516_INDEX_START

## READ_NEXT

Lire dans cet ordre :

1. `06-COQUE-DEBUT.md` ;
2. `07-PIED-DE-PAGE.md` ;
3. `08-BLOC-ESSENTIEL.md` ;
4. `09-BLOCS-RUBRIQUES.md` ;
5. `10-COQUE-FIN.md`.

## PAIRES_EXACTES

- `SNUM_SHELL_HEAD_START / SNUM_SHELL_HEAD_END` ;
- `SNUM_FOOTER_START / SNUM_FOOTER_END` ;
- `SNUM_SHELL_CLOSE_START / SNUM_SHELL_CLOSE_END` ;
- `SNUM_ESSENTIALS_OPEN_START / SNUM_ESSENTIALS_OPEN_END` ;
- `SNUM_ESSENTIAL_CARD_START / SNUM_ESSENTIAL_CARD_END` ;
- `SNUM_ESSENTIALS_CLOSE_START / SNUM_ESSENTIALS_CLOSE_END` ;
- `SNUM_RUBRIC_OPEN_START / SNUM_RUBRIC_OPEN_END` ;
- `SNUM_RUBRIC_ARTICLE_START / SNUM_RUBRIC_ARTICLE_END` ;
- `SNUM_RUBRIC_CLOSE_START / SNUM_RUBRIC_CLOSE_END` ;
- `SNUM_WATCH_START / SNUM_WATCH_END` ;
- `SNUM_EMPTY_START / SNUM_EMPTY_END`.

Recopier ces onze lignes sans fusion ni auto-fermant, sinon `CANON_HTML_INCOMPLET | paire incorrecte`.

Concaténation exacte : `06`, contenu éditorial, `07`, puis `10`. Instancier les blocs essentiels uniquement si au moins trois sources sont valides : concaténer alors `ESSENTIALS_OPEN`, exactement trois répétitions de `ESSENTIAL_CARD`, puis `ESSENTIALS_CLOSE`. Sinon, remplacer `@@ESSENTIELS@@` par une chaîne vide. Pour chaque rubrique, concaténer `RUBRIC_OPEN`, une répétition de `RUBRIC_ARTICLE` par source valide de la rubrique, puis `RUBRIC_CLOSE`. Remplacer ensuite les marqueurs.

Rubriques exactes :

- `numerique` : navigation `Numérique`, titre et tag `NUMERIQUE`, enveloppe `<section id="numerique">` ;
- `ia` : navigation `Intelligence artificielle`, titre et tag `INTELLIGENCE ARTIFICIELLE (IA)`, enveloppe `<section id="ia" class="section-muted">` ;
- `commande` : navigation `Commande publique`, titre et tag `COMMANDE PUBLIQUE`, enveloppe `<section id="commande">` ;
- `rh` : navigation `Ressources humaines`, titre et tag `RESSOURCES HUMAINES`, enveloppe `<section id="rh" class="section-muted">` ;
- `bercy` : navigation `Vie de Bercy`, titre et tag `VIE DE BERCY`, enveloppe `<section id="bercy">`.

Avec moins de trois événements, ne produire ni section ni lien `L’essentiel`. À partir de trois événements, insérer exactement trois cartes essentielles et ajouter la navigation `L’essentiel`. Ajouter `À surveiller` seulement si sa section existe. Ne jamais inventer une autre rubrique.

Chaque source valide figure une fois dans sa rubrique. Une carte essentielle est une mise en avant supplémentaire et ne remplace jamais l’article de rubrique.

Pour chaque lien `href="#id"` du menu de rubriques, produire exactement une section `id="id"`. Chaque rubrique produite possède exactement un lien dans ce menu.

Si une paire manque ou diffère pendant `CANON_RENDU`, répondre `A_COMPLETER`, puis `## CONTROLES_EN_ECHEC` et `CANON_MANQUANT | <paire>`, sans HTML. Dans ce même tour, assembler, corriger, contrôler et livrer le HTML ; ne jamais demander un second message de rendu.

SNUM_CANON_V516_INDEX_END
