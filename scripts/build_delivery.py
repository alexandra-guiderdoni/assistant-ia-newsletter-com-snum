"""Assemble les trois livraisons documentées sans modifier les kits historiques."""

import argparse
import hashlib
import sys
from io import BytesIO
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

from build_mail_kit import PROMPT as MAIL_PROMPT
from build_mail_kit import resources as mail_resources
from build_split_kit import COLLECTE_FILES, RENDU_FILES

PROJECT = Path(__file__).resolve().parents[1]
OUTPUT = PROJECT / "livraison"


def packages():
    common = ("MODE-OPERATOIRE.md", "EXEMPLE-PAQUET-RENDU-V5.19.json")
    return {
        "Newsletter SNUM - Collecte": (
            "INSTALLATION-COLLECTE.md",
            *common,
            "NOTICE-V5.23.md",
            *COLLECTE_FILES,
        ),
        "Newsletter SNUM - Rendu HTML": (
            "INSTALLATION-RENDU-HTML.md",
            *common,
            "NOTICE-V5.23.md",
            *RENDU_FILES,
        ),
        "Newsletter SNUM - rendu DSFR": (
            "INSTALLATION-RENDU-DSFR.md",
            *common,
            "NOTICE-RENDU-DSFR-V1.0.md",
            "outil-rendu-dsfr.html",
            "_documentation/recette-mail-dsfr/RAPPORT.md",
            MAIL_PROMPT,
            *mail_resources(),
        ),
    }


def archive(project_name, names):
    buffer = BytesIO()
    with ZipFile(buffer, "w", ZIP_DEFLATED) as output:
        for name in names:
            info = ZipInfo(f"{project_name}/{name}", (2026, 10, 21, 0, 0, 0))
            info.compress_type = ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            output.writestr(info, (PROJECT / name).read_bytes())
    return buffer.getvalue()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--output-dir", type=Path, default=OUTPUT)
    args = parser.parse_args()
    payloads = {
        f"{name}.zip": archive(name, names) for name, names in packages().items()
    }
    hashes = "".join(
        f"{hashlib.sha256(data).hexdigest()}  {name}\n"
        for name, data in payloads.items()
    )
    payloads["SHA256SUMS.txt"] = hashes.encode("utf-8")
    if args.check:
        drift = [
            name
            for name, data in payloads.items()
            if not (args.output_dir / name).is_file()
            or (args.output_dir / name).read_bytes() != data
        ]
        if drift:
            print("LIVRAISON_DRIFT: " + ", ".join(drift), file=sys.stderr)
            return 1
        print("LIVRAISON_OK : 3 ZIP documentés et empreintes cohérentes")
        return 0
    args.output_dir.mkdir(parents=True, exist_ok=True)
    for name, data in payloads.items():
        (args.output_dir / name).write_bytes(data)
    print("LIVRAISON_GENEREE : 3 ZIP documentés et SHA256SUMS.txt")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
