#!/usr/bin/env bash
# Serve this reveal.js deck locally and open it in a browser.
#
# The deck is fully self-contained (reveal.js and all images are vendored
# inside this folder), so it's served directly rather than from the repo root.
#
# Usage:
#   ./serve.sh [port]              (default port 8000)
#   ./serve.sh --pdf [port]        open the print-to-PDF view (?print-pdf)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DECK_DIR="${SCRIPT_DIR}"

QUERY=""
ARGS=()
for a in "$@"; do
  case "${a}" in
    --pdf) QUERY="?print-pdf" ;;
    *)     ARGS+=("${a}") ;;
  esac
done

PORT="${ARGS[0]:-${PORT:-8000}}"

if ! command -v python3 >/dev/null 2>&1; then
  echo "ERROR: python3 not found (needed for the static server)." >&2
  exit 1
fi

URL="http://localhost:${PORT}/${QUERY}"

echo "[serve] serving ${DECK_DIR}"
echo "[serve] open ${URL}"
echo "[serve] keys: [S] speaker notes  [Esc/O] overview  [F] fullscreen  ·  Ctrl-C to stop"

(
  sleep 1
  if command -v open >/dev/null 2>&1; then
    open "${URL}"
  elif command -v xdg-open >/dev/null 2>&1; then
    xdg-open "${URL}"
  fi
) &

exec python3 -m http.server "${PORT}" --bind localhost --directory "${DECK_DIR}"
