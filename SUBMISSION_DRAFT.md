# QNX Global Hackathon 2026 - Submission Draft

## Project

SAE QNX Assurance Bridge 0.2.0

## Category

Developer Tooling & Host Tools

## Short description

A host-side assurance utility for QNX SDP 8.0 that inspects the SDK, validates required compiler components, builds reproducible AArch64 and x86_64 target probes, verifies ELF architecture, and generates SHA-256-backed build evidence. Its QNX-specific probe also exercises Neutrino microkernel message passing on a running QNX target.

## Problem

A QNX development environment can appear installed while essential compiler components are missing or damaged. A successful qcc driver invocation alone does not prove that the target compiler front-end is present, that the resulting binary is an ELF executable for the intended architecture, or that the program actually runs on QNX.

Teams need a repeatable preflight and evidence trail that separates SDK readiness, cross-compilation, binary validation and target runtime execution.

## Solution

SAE QNX Assurance Bridge provides a small, auditable host-side workflow:

- Detects the QNX SDP environment and SDK root.
- Checks the qcc driver, QNX target headers and GCC 12.2.0 front-ends for AArch64 and x86_64.
- Fails closed when required SDK components are missing.
- Stages source files into a temporary ASCII-only path to avoid Windows toolchain path-handling failures.
- Invokes qcc with -Wall, -Wextra and -Werror.
- Validates ELF64, little-endian format and the expected machine identifier.
- Records source and binary SHA-256 hashes, compiler flags, build logs and machine-readable JSON evidence.
- Distinguishes cross-compilation success from target runtime success.
- Runs a QNX-specific Neutrino IPC probe using ChannelCreate, ConnectAttach, MsgSend, MsgReceive and MsgReply.

## QNX 8.0 integration

The project uses QNX SDP 8.0 target variants:

- AArch64: gcc_ntoaarch64le
- x86_64: gcc_ntox86_64

The C probe uses uname() to identify the target runtime. When compiled for QNX, it creates a Neutrino channel, starts a server thread, sends a PING message, receives it, and returns PONG. Runtime acceptance requires the QNX identity checks and the IPC round trip to succeed.

## Verified results

Verification performed on 26 November 2026:

- Windows 11 host; Python 3.13.17.
- QNX SDP 8.0 SDK inspection: READY_FOR_BUILD.
- Automated tests: 5 passed, 0 failed.
- AArch64 cross-build: PASS; ELF64 machine 183; 14,288 bytes.
- x86_64 cross-build: PASS; ELF64 machine 62; 14,016 bytes.
- Both builds use -Wall -Wextra -Werror.
- QNX 8.0 x86_64 QEMU boot: PASS.
- QNX guest identity: QNX 8.0.0, x86pc / x86_64.
- Runtime probe: compile_target_qnx=1, runtime_sysname=QNX, runtime_qnx=1.
- Neutrino IPC: qnx_msgsend=1.
- Runtime probe exit code: 0.
- SHA-256 evidence is stored in evidence/.

## Runtime test environment and qualification

The QNX guest was run with QEMU 10.2.1 under WSL2 Ubuntu 26.04.1 LTS. The QNX QSTI documentation consulted for this project referenced Ubuntu 22.04/24.04; Ubuntu 26.04.1 is not listed in that guidance. The actual guest boot and probe execution succeeded, but the host distribution is therefore described as an experimental configuration rather than an officially supported one.

Runtime was verified on x86_64 only. AArch64 cross-compilation and ELF validation are verified; execution on an AArch64 QNX target remains untested.

## Existing-project update

The earlier SAE QNX Assurance Bridge prototype was materially extended during the hackathon period. Version 0.2.0 adds fail-closed SDK component inspection, Unicode-path staging, warning-as-error builds, ELF machine validation, expanded automated tests, per-build logs, source and binary hashes, and a successful QNX 8.0 Neutrino IPC runtime demonstration.

## License and distribution

The project-owned source and documentation carry the MIT License. The QNX SDK, QNX QSTI image, proprietary libraries and other third-party components are not included in the repository. Users must obtain and license those components independently.

## Explicit limitations

- No AArch64 QNX runtime execution has been demonstrated.
- No functional-safety certification, security certification or production-readiness claim is made.
- The successful QEMU runtime result applies to the recorded QNX 8.0 x86_64 guest configuration.
- The public GitHub repository and public demonstration video must be verified before the Devpost submission is finalized.

## Build and test

See README.md and QEMU_RUNTIME.md. Core commands:

- python -m unittest discover -s tests -v
- python sae_qnx_assurance.py inspect
- python sae_qnx_assurance.py build --arch aarch64
- python sae_qnx_assurance.py build --arch x86_64
