#!/usr/bin/env python3
"""Construit les deux paquets V5.18 des Projets Assistant DINUM."""

import argparse
import sys
from io import BytesIO
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

from newsletter_render import canonical_blocks

PROJECT = Path(__file__).resolve().parents[1]
SOURCE = PROJECT / "05-BLOCS-HTML-CANONIQUES.md"
COLLECTE_PROJECT = "Newsletter SNUM - Collecte"
RENDU_PROJECT = "Newsletter SNUM - Rendu HTML"
COLLECTE_ARCHIVE = PROJECT / f"{COLLECTE_PROJECT}.zip"
RENDU_ARCHIVE = PROJECT / f"{RENDU_PROJECT}.zip"
LEGACY_ARCHIVE = PROJECT / "kit-dinum-snum-v5-18-deux-projets-6-fichiers.zip"
RESOURCE_SPECS = (
    ("21-CANON-HTML-COQUE-A-V5.18.md", "SNUM_CANON_V518_COQUE_A"),
    ("22-CANON-HTML-COQUE-B-V5.18.md", "SNUM_CANON_V518_COQUE_B"),
    (
        "23-CANON-HTML-ESSENTIEL-RUBRIQUE-V5.18.md",
        "SNUM_CANON_V518_ESSENTIEL_RUBRIQUE",
    ),
    (
        "24-CANON-HTML-SURVEILLER-VIDE-V5.18.md",
        "SNUM_CANON_V518_SURVEILLER_VIDE",
    ),
)
COLLECTE_FILES = ("01-PROMPT-SYSTEME-COLLECTE-SNUM-V5.18.md",)
RENDU_FILES = (
    "20-PROMPT-SYSTEME-RENDU-HTML-SNUM-V5.18.md",
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
            f"{fenced_block('SNUM_BLOC_V518_ESSENTIEL', essentiel)}\n"
            f"{fenced_block('SNUM_BLOC_V518_RUBRIQUE', rubrique)}\n"
            f"{RESOURCE_SPECS[2][1]}_END\n"
        ),
        RESOURCE_SPECS[3][0]: (
            f"{RESOURCE_SPECS[3][1]}_START\n"
            f"{fenced_block('SNUM_BLOC_V518_SURVEILLER', surveiller)}\n"
            f"{fenced_block('SNUM_BLOC_V518_VIDE', vide)}\n"
            f"{RESOURCE_SPECS[3][1]}_END\n"
        ),
    }
    if any(len(content) > 4500 for content in contents.values()):
        raise ValueError("Une ressource canonique dépasse 4 500 caractères")
    return contents


def archive_bytes(project_name, filenames, resources):
    buffer = BytesIO()
    with ZipFile(buffer, "w", ZIP_DEFLATED) as archive:
        folder_info = ZipInfo(f"{project_name}/", (2026, 10, 15, 0, 0, 0))
        folder_info.external_attr = (0o40755 << 16) | 0x10
        archive.writestr(folder_info, b"")
        for name in filenames:
            content = resources.get(name)
            if content is None:
                content = (PROJECT / name).read_text(encoding="utf-8")
            info = ZipInfo(f"{project_name}/{name}", (2026, 10, 15, 0, 0, 0))
            info.compress_type = ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, content.encode("utf-8"))
    return buffer.getvalue()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    check = parser.parse_args().check
    resources = canonical_resources()
    archives = {
        COLLECTE_ARCHIVE: archive_bytes(COLLECTE_PROJECT, COLLECTE_FILES, resources),
        RENDU_ARCHIVE: archive_bytes(RENDU_PROJECT, RENDU_FILES, resources),
    }
    drift = []
    for name, content in resources.items():
        path = PROJECT / name
        if not path.exists() or path.read_text(encoding="utf-8") != content:
            drift.append(name)
    for path, content in archives.items():
        if not path.exists() or path.read_bytes() != content:
            drift.append(path.name)
    if LEGACY_ARCHIVE.exists():
        drift.append(LEGACY_ARCHIVE.name)
    if check:
        if drift:
            print("KIT_DECOUPLE_DRIFT: " + ", ".join(drift), file=sys.stderr)
            return 1
        print("KIT_DECOUPLE_OK")
        return 0
    for name, content in resources.items():
        (PROJECT / name).write_text(content, encoding="utf-8")
    for path, content in archives.items():
        path.write_bytes(content)
    LEGACY_ARCHIVE.unlink(missing_ok=True)
    print("KITS_DECOUPLES_GENERES")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
