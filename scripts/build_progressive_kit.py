#!/usr/bin/env python3
"""Génère le paquet V5.16 progressif depuis le canon HTML unique."""

import argparse
import sys
from io import BytesIO
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

from newsletter_render import canonical_blocks

PROJECT = Path(__file__).resolve().parents[1]
SOURCE = PROJECT / "05-BLOCS-HTML-CANONIQUES.md"
ARCHIVE = PROJECT / "kit-dinum-snum-v5-16-progressif-9-fichiers.zip"
UPLOAD_FILES = (
    "00-PROMPT-PROJET.md",
    "01-ETAT-HISTORIQUE.md",
    "02-METHODE-EDITORIALE.md",
    "05-INDEX-HTML.md",
    "06-COQUE-DEBUT.md",
    "07-PIED-DE-PAGE.md",
    "08-BLOC-ESSENTIEL.md",
    "09-BLOCS-RUBRIQUES.md",
    "10-COQUE-FIN.md",
)


def document(title, start, end, body):
    return f"""# {title}

{start}

Copier uniquement le bloc HTML suivant, sans les jetons de contrôle.

```html
{body}
```

{end}
"""


def split_repeatable(block, start_marker, end_marker):
    """Découpe un bloc en enveloppe ouvrante, élément répétable et fermeture."""
    before, marker, after = block.partition(start_marker)
    if not marker:
        raise ValueError(f"début de bloc répétable introuvable : {start_marker}")
    item_body, marker, after_item = after.partition(end_marker)
    if not marker:
        raise ValueError(f"fin de bloc répétable introuvable : {end_marker}")
    return (
        before.rstrip("\n"),
        start_marker + item_body + end_marker,
        after_item.lstrip("\n"),
    )


def expected_files():
    blocks = canonical_blocks(SOURCE.read_text(encoding="utf-8"))
    footer_marker = '  <footer id="footer"'
    start, separator, after_footer = blocks["page"].partition(footer_marker)
    if not separator:
        raise ValueError("point de découpe de la coque introuvable")
    footer_and_tail = separator + after_footer
    dialog_marker = '  <dialog id="fr-theme-modal"'
    footer, separator, after_dialog = footer_and_tail.partition(dialog_marker)
    if not separator or start + footer + separator + after_dialog != blocks["page"]:
        raise ValueError("point de découpe de la modale introuvable")
    tail = separator + after_dialog
    essential_open, essential_card, essential_close = split_repeatable(
        blocks["essential"],
        '    <div class="fr-col-12 fr-col-md-4">',
        "</article></div>",
    )
    rubric_open, rubric_article, rubric_close = split_repeatable(
        blocks["rubric"],
        '    <article class="fr-col-12">',
        "    </article>",
    )
    index = """# Index HTML canonique - V5.16 progressive

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
"""
    return {
        "05-INDEX-HTML.md": index,
        "06-COQUE-DEBUT.md": document(
            "Coque HTML canonique - début",
            "SNUM_SHELL_HEAD_START",
            "SNUM_SHELL_HEAD_END",
            start.rstrip("\n"),
        ),
        "07-PIED-DE-PAGE.md": document(
            "Pied de page HTML canonique",
            "SNUM_FOOTER_START",
            "SNUM_FOOTER_END",
            footer.rstrip("\n"),
        ),
        "08-BLOC-ESSENTIEL.md": "\n".join(
            (
                document(
                    "Bloc HTML canonique - ouverture de L’essentiel",
                    "SNUM_ESSENTIALS_OPEN_START",
                    "SNUM_ESSENTIALS_OPEN_END",
                    essential_open,
                ),
                document(
                    "Bloc HTML canonique - carte essentielle",
                    "SNUM_ESSENTIAL_CARD_START",
                    "SNUM_ESSENTIAL_CARD_END",
                    essential_card,
                ),
                document(
                    "Bloc HTML canonique - fermeture de L’essentiel",
                    "SNUM_ESSENTIALS_CLOSE_START",
                    "SNUM_ESSENTIALS_CLOSE_END",
                    essential_close,
                ),
            )
        ),
        "09-BLOCS-RUBRIQUES.md": "\n".join(
            (
                document(
                    "Bloc HTML canonique - ouverture de rubrique",
                    "SNUM_RUBRIC_OPEN_START",
                    "SNUM_RUBRIC_OPEN_END",
                    rubric_open,
                ),
                document(
                    "Bloc HTML canonique - article de rubrique",
                    "SNUM_RUBRIC_ARTICLE_START",
                    "SNUM_RUBRIC_ARTICLE_END",
                    rubric_article,
                ),
                document(
                    "Bloc HTML canonique - fermeture de rubrique",
                    "SNUM_RUBRIC_CLOSE_START",
                    "SNUM_RUBRIC_CLOSE_END",
                    rubric_close,
                ),
                document(
                    "Bloc HTML canonique - à surveiller",
                    "SNUM_WATCH_START",
                    "SNUM_WATCH_END",
                    blocks["watch"],
                ),
                document(
                    "Bloc HTML canonique - collecte vide",
                    "SNUM_EMPTY_START",
                    "SNUM_EMPTY_END",
                    blocks["empty"],
                ),
            )
        ),
        "10-COQUE-FIN.md": document(
            "Coque HTML canonique - fin",
            "SNUM_SHELL_CLOSE_START",
            "SNUM_SHELL_CLOSE_END",
            tail,
        ),
    }


def archive_bytes(source_files, generated):
    buffer = BytesIO()
    with ZipFile(buffer, "w", ZIP_DEFLATED) as archive:
        for name in UPLOAD_FILES:
            data = generated.get(name, source_files.get(name)).encode("utf-8")
            info = ZipInfo(name, (2026, 10, 15, 0, 0, 0))
            info.compress_type = ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, data)
    return buffer.getvalue()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    check = parser.parse_args().check
    generated = expected_files()
    source_files = {
        name: (PROJECT / name).read_text(encoding="utf-8")
        for name in UPLOAD_FILES
        if name not in generated
    }
    expected_archive = archive_bytes(source_files, generated)
    drift = [
        name
        for name, content in generated.items()
        if not (PROJECT / name).exists()
        or (PROJECT / name).read_text(encoding="utf-8") != content
    ]
    if not ARCHIVE.exists() or ARCHIVE.read_bytes() != expected_archive:
        drift.append(ARCHIVE.name)
    if check:
        if drift:
            print("KIT_PROGRESSIF_DRIFT: " + ", ".join(drift), file=sys.stderr)
            return 1
        print("KIT_PROGRESSIF_OK")
        return 0
    for name, content in generated.items():
        (PROJECT / name).write_text(content, encoding="utf-8")
    ARCHIVE.write_bytes(expected_archive)
    print("KIT_PROGRESSIF_GENERE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
