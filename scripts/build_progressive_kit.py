#!/usr/bin/env python3
"""Génère le paquet V5.8 progressif depuis le canon HTML unique."""

import argparse
import sys
from io import BytesIO
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

from newsletter_render import canonical_blocks


PROJECT = Path(__file__).resolve().parents[1]
SOURCE = PROJECT / "05-BLOCS-HTML-CANONIQUES.md"
ARCHIVE = PROJECT / "kit-dinum-snum-v5-8-progressif-8-fichiers.zip"
UPLOAD_FILES = (
    "00-PROMPT-PROJET.md",
    "01-ETAT-HISTORIQUE.md",
    "02-METHODE-EDITORIALE.md",
    "05-INDEX-HTML.md",
    "06-COQUE-DEBUT.md",
    "07-COQUE-FIN.md",
    "08-BLOC-ESSENTIEL.md",
    "09-BLOCS-RUBRIQUES.md",
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


def expected_files():
    blocks = canonical_blocks(SOURCE.read_text(encoding="utf-8"))
    footer = '  <footer id="footer"'
    start, separator, end = blocks["page"].partition(footer)
    if not separator or start + separator + end != blocks["page"]:
        raise ValueError("point de découpe de la coque introuvable")
    index = """# Index HTML canonique - V5.8 progressive

SNUM_CANON_V58_INDEX_START

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

À partir de trois événements, insérer exactement trois cartes essentielles et ajouter la navigation `L’essentiel`. Ajouter `À surveiller` seulement si sa section existe. Ne jamais inventer une autre rubrique.

Si un jeton de fin manque après une nouvelle recherche ciblée, arrêter avec `A_COMPLETER — HTML canonique non établi` sans produire de code HTML.

SNUM_CANON_V58_INDEX_END
"""
    return {
        "05-INDEX-HTML.md": index,
        "06-COQUE-DEBUT.md": document(
            "Coque HTML canonique - début",
            "SNUM_SHELL_HEAD_START",
            "SNUM_SHELL_HEAD_END",
            start.rstrip("\n"),
        ),
        "07-COQUE-FIN.md": document(
            "Coque HTML canonique - fin",
            "SNUM_SHELL_TAIL_START",
            "SNUM_SHELL_TAIL_END",
            separator + end,
        ),
        "08-BLOC-ESSENTIEL.md": document(
            "Bloc HTML canonique - essentiel",
            "SNUM_ESSENTIAL_START",
            "SNUM_ESSENTIAL_END",
            blocks["essential"],
        ),
        "09-BLOCS-RUBRIQUES.md": "\n".join(
            (
                document(
                    "Bloc HTML canonique - rubrique",
                    "SNUM_RUBRIC_START",
                    "SNUM_RUBRIC_END",
                    blocks["rubric"],
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
    }


def archive_bytes(source_files, generated):
    buffer = BytesIO()
    with ZipFile(buffer, "w", ZIP_DEFLATED) as archive:
        for name in UPLOAD_FILES:
            data = generated.get(name, source_files.get(name)).encode("utf-8")
            info = ZipInfo(name, (2026, 10, 14, 0, 0, 0))
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
