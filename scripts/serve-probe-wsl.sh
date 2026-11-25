#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="${SAE_PROJECT_DIR:-$(dirname "$SCRIPT_DIR")}"
BIN="$PROJECT_DIR/build/sae_qnx_probe_x86_64.elf"
TRANSFER_DIR="${QNX_TRANSFER_DIR:-$HOME/sae-qnx-transfer}"
PORT="${QNX_HTTP_PORT:-8080}"

[[ -f "$BIN" ]] || { echo "Missing x86_64 ELF: $BIN" >&2; exit 2; }
mkdir -p "$TRANSFER_DIR"
install -m 0644 "$BIN" "$TRANSFER_DIR/sae_qnx_probe_x86_64.elf"

echo "Serving QNX probe over temporary HTTP on port $PORT"
echo "Guest URL: http://10.0.2.2:$PORT/sae_qnx_probe_x86_64.elf"
echo "SHA-256: $(sha256sum "$TRANSFER_DIR/sae_qnx_probe_x86_64.elf" | awk '{print $1}')"
echo "Stop this server after the guest has downloaded the binary."
exec python3 -m http.server "$PORT" --bind 0.0.0.0 --directory "$TRANSFER_DIR"
