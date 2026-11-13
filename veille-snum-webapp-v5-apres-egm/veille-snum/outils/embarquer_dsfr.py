"""Copie depuis le paquet officiel @gouvfr/dsfr les seuls fichiers utilisés par l'application.

Usage : python3 outils/embarquer_dsfr.py /chemin/vers/package
Le dossier `package` est celui du paquet npm @gouvfr/dsfr (contient package.json et dist/).
Le dossier cible veille_snum/dsfr/ est recréé ; MANIFEST.json garde version et empreintes.
"""

import hashlib
import json
import re
import shutil
import sys
from pathlib import Path

VERSION = "1.15.4"
BASE = [
    "dsfr.min.css",
    "dsfr.module.min.js",
    "dsfr.nomodule.min.js",
    "favicon/favicon.svg",
    "favicon/favicon.ico",
    "favicon/apple-touch-icon.png",
]


def main(package):
    package = Path(package).expanduser().resolve()
    meta = json.loads((package / "package.json").read_text(encoding="utf-8"))
    if meta.get("name") != "@gouvfr/dsfr" or meta.get("version") != VERSION:
        raise SystemExit(
            f"Paquet inattendu : {meta.get('name')} {meta.get('version')}, {VERSION} attendu"
        )
    dist = package / "dist"
    css = (dist / "dsfr.min.css").read_text(encoding="utf-8")
    used = {u.strip("'\"") for u in re.findall(r"url\(([^)]+)\)", css)}
    files = sorted(set(BASE) | {u for u in used if not u.startswith("data:")})
    target = Path(__file__).resolve().parents[1] / "veille_snum" / "dsfr"
    if target.exists():
        shutil.rmtree(target)
    manifest = {
        "package": "@gouvfr/dsfr",
        "version": VERSION,
        "source": "paquet npm officiel, dist/",
        "files": {},
    }
    for rel in files:
        source = (dist / rel).resolve()
        if dist not in source.parents or not source.is_file():
            raise SystemExit(f"Fichier absent ou hors du paquet : {rel}")
        destination = target / rel
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        manifest["files"][rel] = hashlib.sha256(destination.read_bytes()).hexdigest()
    (target / "MANIFEST.json").write_text(
        json.dumps(manifest, indent=1, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    size = sum((target / rel).stat().st_size for rel in files)
    print(
        f"{len(files)} fichiers DSFR {VERSION} copiés dans {target} ({size // 1024} Ko)"
    )


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    main(sys.argv[1])
