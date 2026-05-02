#!/usr/bin/env bash
set -euo pipefail

SENDER_URL="${SENDER_URL:-https://raw.githubusercontent.com/mooooooooner/scripts/main/sender.py}"

if command -v python3 >/dev/null 2>&1; then
  PYTHON_BIN="python3"
elif command -v python >/dev/null 2>&1; then
  PYTHON_BIN="python"
else
  echo "python/python3 not found in PATH."
  exit 1
fi

TMP_DIR="$(mktemp -d)"
cleanup() {
  rm -rf "$TMP_DIR"
}
trap cleanup EXIT

curl -fsSL "$SENDER_URL" -o "$TMP_DIR/sender.py"
"$PYTHON_BIN" "$TMP_DIR/sender.py" "$@"
