#!/usr/bin/env bash
set -euo pipefail
PROJECT_DIR="\${SAE_PROJECT_DIR:-/mnt/c/Users/manue/qnx-work/sae-qnx-assurance-bridge}"
BIN="$PROJECT_DIR/build/sae_qnx_probe_x86_64.exe"
PORT="\${QNX_SSH_PORT:-22222}"
USER="\${QNX_SSH_USER:-qnxuser}"
HOST="\${QNX_SSH_HOST:-127.0.0.1}"
: "\${QNX_GUEST_PASSWORD:?Set QNX_GUEST_PASSWORD in this shell (QSTI default is qnxuser; change it after first login).}"
[[ -f "$BIN" ]] || { echo "Missing x86_64 build: $BIN" >&2; exit 2; }
export SSHPASS="$QNX_GUEST_PASSWORD"
SSH_OPTS=(-p "$PORT" -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o ConnectTimeout=5)
SCP_OPTS=(-P "$PORT" -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o ConnectTimeout=5)
sshpass -e scp "\${SCP_OPTS[@]}" "$BIN" "$USER@$HOST:/tmp/sae_qnx_probe"
sshpass -e ssh "\${SSH_OPTS[@]}" "$USER@$HOST" 'chmod 755 /tmp/sae_qnx_probe && /tmp/sae_qnx_probe'
