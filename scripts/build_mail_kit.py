"""Génère uniquement les ressources du troisième Projet et son archive."""

import argparse
import textwrap
from io import BytesIO
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

from newsletter_mail import PROJECT, blocks

PROMPT = "30-PROMPT-SYSTEME-RENDU-DSFR-V1.0.md"
ARCHIVE = PROJECT / "Newsletter SNUM - rendu DSFR.zip"


def resource(name, value):
    return f"SNUM_MAIL_DSFR_{name}_START\n```html\n{value}\n```\nSNUM_MAIL_DSFR_{name}_END\n"


def resources():
    canon = blocks()
    files = {}
    for kind, key, size in [("COQUE", "PAGE", 4000), ("LOGO", "LOGO", 4200)]:
        content = canon[key]
        for index, start in enumerate(range(0, len(content), size), 1):
            fragment = content[start : start + size]
            if kind == "LOGO":
                fragment = "\n".join(textwrap.wrap(fragment, width=76))
            files[f"31-MAIL-DSFR-{kind}-{index:02d}-V1.0.md"] = resource(
                f"{kind}_{index:02d}", fragment
            )
    for number, name, keys in [
        (32, "ARTICLE", ["ARTICLE", "ESSENTIAL"]),
        (33, "RUBRIC", ["RUBRIC"]),
        (34, "WATCH", ["WATCH", "WATCH_ITEM", "EMPTY"]),
    ]:
        files[f"{number}-MAIL-DSFR-{name}-V1.0.md"] = "\n".join(
            resource(key, canon[key]) for key in keys
        )
    if any(len(content) > 4500 for content in files.values()):
        raise ValueError("ressource supérieure à 4 500 caractères")
    if len((PROJECT / PROMPT).read_text()) > 4000:
        raise ValueError("prompt supérieur à 4 000 caractères")
    return files


def archive(files):
    buffer = BytesIO()
    with ZipFile(buffer, "w", ZIP_DEFLATED) as output:
        for name, content in {PROMPT: (PROJECT / PROMPT).read_text(), **files}.items():
            info = ZipInfo(
                "Newsletter SNUM - rendu DSFR/" + name, (2026, 10, 21, 0, 0, 0)
            )
            info.compress_type = ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            output.writestr(info, content.encode("utf-8"))
    return buffer.getvalue()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    files = resources()
    zipped = archive(files)
    if args.check:
        assert all(
            (PROJECT / name).read_text() == content for name, content in files.items()
        )
        assert ARCHIVE.read_bytes() == zipped
        print("KIT_MAIL_DSFR_OK")
        return
    for name, content in files.items():
        (PROJECT / name).write_text(content, encoding="utf-8")
    ARCHIVE.write_bytes(zipped)
    print(f"KIT_MAIL_DSFR_GENERE : {len(files)} ressources")


if __name__ == "__main__":
    main()
