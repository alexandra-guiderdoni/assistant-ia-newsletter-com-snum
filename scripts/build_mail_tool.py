"""Assemble le fichier autonome depuis le canon et les sources de l'interface."""

import argparse
import base64
import hashlib
import json

from newsletter_mail import PROJECT, blocks

OUTPUT = PROJECT / "outil-rendu-dsfr.html"


def build():
    sources = PROJECT / "_source"
    render = (sources / "mail-tool-render.js").read_text(encoding="utf-8")
    ui = (sources / "mail-tool-ui.js").read_text(encoding="utf-8")
    hashes = [
        "'sha256-"
        + base64.b64encode(hashlib.sha256(code.encode()).digest()).decode()
        + "'"
        for code in [render, ui]
    ]
    csp = (
        "default-src 'none'; script-src "
        + " ".join(hashes)
        + "; style-src 'unsafe-inline'; img-src data:; frame-src 'self' blob:; "
        "connect-src 'none'; base-uri 'none'; form-action 'none'"
    )
    canon = json.dumps(blocks(), ensure_ascii=False).replace("<", "\\u003c")
    shell = (sources / "mail-tool-shell.html").read_text(encoding="utf-8")
    for key, value in {"CSP": csp, "CANON": canon, "RENDER": render, "UI": ui}.items():
        shell = shell.replace("@@" + key + "@@", value)
    return shell


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    expected = build()
    if args.check:
        if not OUTPUT.exists() or OUTPUT.read_text(encoding="utf-8") != expected:
            raise ValueError("outil autonome absent ou différent des sources")
        print("OUTIL_MAIL_DSFR_OK")
    else:
        OUTPUT.write_text(expected, encoding="utf-8")
        print("OUTIL_MAIL_DSFR_GENERE")


if __name__ == "__main__":
    main()
