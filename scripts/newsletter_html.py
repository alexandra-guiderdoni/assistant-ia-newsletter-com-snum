#!/usr/bin/env python3
"""CLI de construction et de validation du HTML SNUM canonique."""

import argparse
import json
import sys
from pathlib import Path

from newsletter_render import build, canonical_blocks
from newsletter_validate import validate


def parser():
    root = argparse.ArgumentParser()
    commands = root.add_subparsers(dest="command", required=True)
    build_command = commands.add_parser("build")
    build_command.add_argument("--input", required=True, type=Path)
    build_command.add_argument("--output", required=True, type=Path)
    build_command.add_argument("--template", required=True, type=Path)
    validate_command = commands.add_parser("validate")
    validate_command.add_argument("--input", required=True, type=Path)
    validate_command.add_argument("--template", required=True, type=Path)
    return root


def main():
    arguments = parser().parse_args()
    try:
        blocks = canonical_blocks(arguments.template.read_text(encoding="utf-8"))
        if arguments.command == "build":
            payload = json.loads(arguments.input.read_text(encoding="utf-8"))
            html = build(payload, blocks)
            errors = validate(html, blocks)
            if errors:
                raise ValueError("validation HTML bloquante : " + "; ".join(errors))
            arguments.output.write_text(html, encoding="utf-8")
            return 0
        errors = validate(arguments.input.read_text(encoding="utf-8"), blocks)
        if errors:
            for error in errors:
                print(error, file=sys.stderr)
            return 1
        print("HTML_CANONIQUE_OK")
        return 0
    except (KeyError, OSError, TypeError, ValueError, json.JSONDecodeError) as error:
        print(f"ERREUR : {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
