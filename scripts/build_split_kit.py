#!/usr/bin/env python3
"""Construit le kit V5.17 des deux Projets Assistant DINUM."""

import argparse
import sys
from io import BytesIO
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

from newsletter_render import canonical_blocks

PROJECT = Path(__file__).resolve().parents[1]
SOURCE = PROJECT / "05-BLOCS-HTML-CANONIQUES.md"
ARCHIVE = PROJECT / "kit-dinum-snum-v5-17-deux-projets-6-fichiers.zip"
RESOURCE_SPECS = (
    ("CANON-HTML-01-COQUE-A-V5.17.md", "SNUM_CANON_V517_COQUE_A"),
    ("CANON-HTML-02-COQUE-B-V5.17.md", "SNUM_CANON_V517_COQUE_B"),
    (
        "CANON-HTML-03-ESSENTIEL-RUBRIQUE-V5.17.md",
        "SNUM_CANON_V517_ESSENTIEL_RUBRIQUE",
    ),
    (
        "CANON-HTML-04-SURVEILLER-VIDE-V5.17.md",
        "SNUM_CANON_V517_SURVEILLER_VIDE",
    ),
)
ARCHIVE_FILES = (
    "PROMPT-SYSTEME-COLLECTE-SNUM-V5.17.md",
    "PROMPT-SYSTEME-RENDU-HTML-SNUM-V5.17.md",
    *(filename for filename, _ in RESOURCE_SPECS),
)


def fenced_block(marker, html):
    return f"{marker}_START\n```html\n{html}\n```\n{marker}_END"


def canonical_resources():
    blocks = canonical_blocks(SOURCE.read_text(encoding="utf-8"))
    coque = blocks["page"]
    split_at = coque.index('  <footer id="footer"')
    coque_a = coque[:split_at].rstrip("\n")
    coque_b = coque[split_at:]
    essentiel = blocks["essential"]
    rubrique = blocks["rubric"]
    surveiller = blocks["watch"]
    vide = blocks["empty"]

    contents = {
        RESOURCE_SPECS[0][0]: fenced_block(RESOURCE_SPECS[0][1], coque_a) + "\n",
        RESOURCE_SPECS[1][0]: fenced_block(RESOURCE_SPECS[1][1], coque_b) + "\n",
        RESOURCE_SPECS[2][0]: (
            f"{RESOURCE_SPECS[2][1]}_START\n"
            f"{fenced_block('SNUM_BLOC_V517_ESSENTIEL', essentiel)}\n"
            f"{fenced_block('SNUM_BLOC_V517_RUBRIQUE', rubrique)}\n"
            f"{RESOURCE_SPECS[2][1]}_END\n"
        ),
        RESOURCE_SPECS[3][0]: (
            f"{RESOURCE_SPECS[3][1]}_START\n"
            f"{fenced_block('SNUM_BLOC_V517_SURVEILLER', surveiller)}\n"
            f"{fenced_block('SNUM_BLOC_V517_VIDE', vide)}\n"
            f"{RESOURCE_SPECS[3][1]}_END\n"
        ),
    }
    if any(len(content) > 4500 for content in contents.values()):
        raise ValueError("Une ressource canonique dépasse 4 500 caractères")
    return contents


def archive_bytes(resources):
    contents = {
        name: (PROJECT / name).read_text(encoding="utf-8") for name in ARCHIVE_FILES[:2]
    }
    contents.update(resources)
    buffer = BytesIO()
    with ZipFile(buffer, "w", ZIP_DEFLATED) as archive:
        for name in ARCHIVE_FILES:
            info = ZipInfo(name, (2026, 10, 15, 0, 0, 0))
            info.compress_type = ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, contents[name].encode("utf-8"))
    return buffer.getvalue()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    check = parser.parse_args().check
    resources = canonical_resources()
    archive = archive_bytes(resources)
    drift = []
    for name, content in resources.items():
        path = PROJECT / name
        if not path.exists() or path.read_text(encoding="utf-8") != content:
            drift.append(name)
    if not ARCHIVE.exists() or ARCHIVE.read_bytes() != archive:
        drift.append(ARCHIVE.name)
    if check:
        if drift:
            print("KIT_DECOUPLE_DRIFT: " + ", ".join(drift), file=sys.stderr)
            return 1
        print("KIT_DECOUPLE_OK")
        return 0
    for name, content in resources.items():
        (PROJECT / name).write_text(content, encoding="utf-8")
    ARCHIVE.write_bytes(archive)
    print("KIT_DECOUPLE_GENERE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
