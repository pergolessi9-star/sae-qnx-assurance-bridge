# Codelab: Verify a QNX 8.0 Target from Windows

Duration: 10–15 minutes. Level: Intermediate.

## Goal
Inspect a QNX SDP 8.0 SDK, build AArch64 and x86_64 probes, validate ELF architecture, and exercise Neutrino microkernel message passing on a QNX target.

## Prerequisites
- Windows 11 x86_64 and Python 3.10+.
- QNX SDP 8.0 installed and licensed for your use.
- QNX Software Center.
- For runtime: the official QNX QSTI for QEMU, QEMU 10.x and a QNX-documented Ubuntu WSL release (currently 22.04/24.04).

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
The tool verifies ELF64 little-endian output and machine identifiers: AArch64=183; x86_64=62. It records a separate SHA-256 evidence manifest for each target.

## 3. Understand the QNX probe
The C probe calls uname() and exercises ChannelCreate, ConnectAttach, MsgSend, MsgReceive and MsgReply. A server thread receives a PING message and replies with PONG. The runtime test must pass this IPC round trip.

## 4. Run on QNX QEMU
Install the official QNX QSTI image through QNX Software Center. Start it with:
```bash
bash scripts/run-qnx-qemu-wsl.sh
```
In another WSL terminal, set QNX_GUEST_PASSWORD using the credentials supplied for your QSTI image, then run:
```bash
bash scripts/deploy-and-test-qnx.sh
```
Change default guest credentials after first login. Never commit passwords.

## Acceptance criteria
Expected output includes compile_target_qnx=1, runtime_sysname=QNX, runtime_qnx=1 and qnx_msgsend=1, with exit code 0. Retain the QNX release, console output and SHA-256 in evidence/. Cross-compilation alone is not runtime verification.
