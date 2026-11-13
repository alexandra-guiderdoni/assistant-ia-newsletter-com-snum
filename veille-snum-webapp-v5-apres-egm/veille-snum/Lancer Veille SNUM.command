#!/bin/zsh
# Lance la webapp en local sur macOS. Aucune collecte n'est lancée avant clic.
set -eu
cd -- "$(dirname -- "$0")"
if ! command -v python3 >/dev/null 2>&1; then
  echo "Python 3 n'est pas installé sur ce Mac."
  read "?Appuyez sur Entrée pour fermer."
  exit 1
fi
# 8766 : le port 8765 peut être occupé par le service worker d’une autre application locale.
export SNUM_PORT="${SNUM_PORT:-8766}"
python3 -m veille_snum.web &
server_pid=$!
trap 'kill "$server_pid" >/dev/null 2>&1 || true' EXIT INT TERM
sleep 2
open "http://127.0.0.1:${SNUM_PORT}/"
wait "$server_pid"
