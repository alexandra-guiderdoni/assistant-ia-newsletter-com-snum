#!/bin/bash
set -euo pipefail

script_dir="$(cd "$(dirname "$0")" && pwd)"

if [[ $# -gt 0 ]]; then
  input_file="$1"
  exec python3 "$script_dir/generer_revue.py" "$input_file" --sortie "$script_dir"
fi

if ! command -v pbpaste >/dev/null 2>&1; then
  echo "ERREUR : indiquez le fichier JSON en argument." >&2
  exit 1
fi

clipboard_file="$(mktemp -t revue-snum-dinum.XXXXXX)"
trap 'rm -f "$clipboard_file"' EXIT
pbpaste > "$clipboard_file"

if [[ ! -s "$clipboard_file" ]]; then
  echo "ERREUR : le presse-papiers est vide. Copiez d’abord toute la réponse DINUM." >&2
  exit 1
fi

python3 "$script_dir/generer_revue.py" "$clipboard_file" --sortie "$script_dir"
