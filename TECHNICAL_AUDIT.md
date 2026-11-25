# Technical audit — 25 November 2026

## Host and SDK

- Host: Windows 11, build 26200.
- Python: 3.13.17.
- Working QNX SDP 8.0 installation: C:\Users\manue\qnx800_2.
- The original C:\Users\manue\qnx800 installation has a damaged/incomplete GCC component: the AArch64 cc1 front-end was absent and some compiler files had zero length. It has been left untouched.
- The recovered qnx800_2 SDK has a non-empty qcc driver, AArch64 and x86_64 GCC front-ends, and QNX target headers.
- qcc exposes QNX 8.0 GCC 12.2.0 target variants: gcc_ntoaarch64le and gcc_ntox86_64.

## Automated tests and reproducible build evidence

- Automated unit tests: 4 passed, 0 failed.
- SDK inspection: READY_FOR_BUILD.
- AArch64 output: 14,288 bytes; SHA-256 dce8db8dcf367652352d0ec49006175b0a9fedf45ad824acbc8d0ecbb0cfaf8a.
- x86_64 output: 14,016 bytes; SHA-256 5a449cf7b4cc00505cddb153c5e42b4a839286145e63e0ba2f78df46fa50b3e5.
- ELF validation checks ELF64, little-endian encoding and the expected machine type: AArch64=183; x86_64=62.
- Each build creates a separate JSON evidence manifest and qcc log.
- Both target probes compile successfully. The manifests intentionally say CROSS_COMPILE_PASS_RUNTIME_NOT_TESTED until the probe runs inside QNX.

## QNX-specific technology in the probe

The C probe uses QNX Neutrino message-passing APIs:
- ChannelCreate
- ConnectAttach
- MsgSend
- MsgReceive
- MsgReply

It creates a local channel and a server thread, sends a PING request, receives it and replies with PONG. The runtime acceptance test requires the QNX kernel IPC round trip to succeed. Compilation is verified; runtime execution is pending.

## QEMU target preparation

- QNX Software Center package: com.qnx.qnx800.quickstart.qemu, version 0.5.0.00050T202609021847L.
- QEMU is installed in WSL.
- QNX QSTI archive parts total 2,561,493,652 bytes.
- The VMDK descriptor declares a 50,826,834,432-byte disk extent (47.3 GiB logical).
- The image is being extracted into WSL's Linux filesystem with a sparse-aware extractor to avoid writing zero-filled sectors to the Windows C: volume.
- An earlier QEMU boot was attempted before the disk image had finished extracting. It failed to mount /boot, /usr and /data. That attempt is invalid and is not counted as a runtime test.
- A clean QEMU boot and probe execution are still required.
- QNX's QSTI documentation lists Ubuntu 22.04 and 24.04 as supported. The installed WSL distribution must be checked against this before claiming a supported-host configuration.

## Repository and release

- Local Git repository initialized on main.
- Initial commits created for the host assurance utility, QEMU runtime harness, submission draft and audit.
- MIT license and English documentation are included.
- Codelab and under-three-minute video plan are prepared.
- Local source ZIP: C:\Users\manue\qnx-work\sae-qnx-assurance-bridge-v0.1.0.zip (regenerate after the latest IPC and ELF validation changes).
- Public GitHub repository has not been created or pushed. GitHub browser sign-in is pending.
- Demo video has not been recorded or uploaded to YouTube. Google sign-in is pending.

## Status

Cross-compilation for QNX 8.0 AArch64 and x86_64 is verified, including ELF architecture validation. The QNX-specific IPC probe compiles for both targets. QNX runtime, public repository publication, and public demo video remain open acceptance criteria. No QNX runtime or competition submission success is claimed.
