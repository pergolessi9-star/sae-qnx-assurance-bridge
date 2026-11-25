#!/usr/bin/env bash
# Optional SSH transport. The verified QNX QSTI run used the serial console and
# temporary HTTP transfer documented in QEMU_RUNTIME.md.
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="${SAE_PROJECT_DIR:-$(dirname "$SCRIPT_DIR")}"
BIN="$PROJECT_DIR/build/sae_qnx_probe_x86_64.elf"
EVIDENCE_DIR="$PROJECT_DIR/evidence"
PORT="${QNX_SSH_PORT:-22222}"
USER="${QNX_SSH_USER:-qnxuser}"
HOST="${QNX_SSH_HOST:-127.0.0.1}"

: "${QNX_GUEST_PASSWORD:?Set QNX_GUEST_PASSWORD in this shell; never store it in the repository.}"
[[ -f "$BIN" ]] || { echo "Missing x86_64 ELF: $BIN" >&2; exit 2; }

mkdir -p "$EVIDENCE_DIR"
export SSHPASS="$QNX_GUEST_PASSWORD"
SSH_OPTS=(-p "$PORT" -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o ConnectTimeout=8)
SCP_OPTS=(-P "$PORT" -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o ConnectTimeout=8)

echo "Deploying $(basename "$BIN") to $USER@$HOST:$PORT"
sshpass -e scp "${SCP_OPTS[@]}" "$BIN" "$USER@$HOST:/tmp/sae_qnx_probe"

RESULT="$EVIDENCE_DIR/qnx-runtime-output-ssh.txt"
set +e
sshpass -e ssh "${SSH_OPTS[@]}" "$USER@$HOST" 'chmod 755 /tmp/sae_qnx_probe && /tmp/sae_qnx_probe' 2>&1 | tee "$RESULT"
RC=${PIPESTATUS[0]}
set -e

{
  echo "runtime_exit_code=$RC"
  echo "probe_sha256=$(sha256sum "$BIN" | awk '{print $1}')"
  echo "probe_bytes=$(stat -c '%s' "$BIN")"
} >> "$RESULT"

if [[ "$RC" -ne 0 ]]; then
  echo "RUNTIME_FAIL: probe returned $RC; see $RESULT" >&2
  exit "$RC"
fi

grep -q '^compile_target_qnx=1$' "$RESULT"
grep -q '^runtime_sysname=QNX$' "$RESULT"
grep -q '^runtime_qnx=1$' "$RESULT"
grep -q '^qnx_msgsend=1$' "$RESULT"
echo "RUNTIME_PASS: QNX uname and Neutrino message-passing round trip verified"
