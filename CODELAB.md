# Codelab: Verify a QNX 8.0 Target from Windows

**Version:** 0.2.0
**Duration:** 10-15 minutes, excluding QNX image download and extraction.
**Level:** Intermediate.

## Goal

Inspect a QNX SDP 8.0 SDK, build AArch64 and x86_64 probes, validate ELF architecture, and exercise Neutrino microkernel message passing on a running QNX target.

## Prerequisites

- Windows 10/11 x86_64 and Python 3.10+.
- QNX SDP 8.0 installed and licensed for your use.
- QNX Software Center.
- For runtime: official QNX QSTI image for QEMU, WSL2 and QEMU.

## 1. Inspect the SDK

```powershell
python .\sae_qnx_assurance.py inspect
```

The tool checks the SDK root, qcc driver, target headers and both GCC front-ends. A damaged SDK is reported as BLOCKED. Repair it through QNX Software Center; do not copy compiler binaries manually.

## 2. Run tests and build both targets

```powershell
python -m unittest discover -s tests -v
python .\sae_qnx_assurance.py build --arch aarch64
python .\sae_qnx_assurance.py build --arch x86_64
```

The tool stages the source into a temporary directory, invokes qcc with warning-as-error flags, validates ELF64 little-endian output and machine identifiers (AArch64=183; x86_64=62), and records SHA-256 evidence.

## 3. Understand the QNX probe

The C probe calls uname() and exercises ChannelCreate, ConnectAttach, MsgSend, MsgReceive and MsgReply. A server thread receives a PING message and replies with PONG. Runtime PASS requires the QNX identity checks and IPC round trip to succeed.

## 4. Run on QNX QEMU

Install the official QNX QSTI image through QNX Software Center and extract it outside the public repository. Start the guest from WSL:

```bash
export QNX_QEMU_IMAGE_DIR="/path/to/qnx-qemu-image/qemu"
bash scripts/run-qnx-qemu-wsl.sh
```

In a second WSL terminal, serve the probe:

```bash
bash scripts/serve-probe-wsl.sh
```

At the QNX guest serial console, download and run:

```sh
curl -f http://10.0.2.2:8080/sae_qnx_probe_x86_64.elf -o /tmp/sae_qnx_probe
chmod 755 /tmp/sae_qnx_probe
/tmp/sae_qnx_probe
echo PROBE_EXIT_CODE=$?
```

## Acceptance criteria

Expected output includes compile_target_qnx=1, runtime_sysname=QNX, runtime_qnx=1 and qnx_msgsend=1, with exit code 0. Retain the QNX release, console output and SHA-256 in evidence/. Cross-compilation alone is not runtime verification.
