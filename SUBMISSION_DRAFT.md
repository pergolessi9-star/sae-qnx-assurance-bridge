# QNX Global Hackathon — Submission Draft

## Project
SAE QNX Assurance Bridge

## Category
Developer Tooling & Host Tools

## Short description
A host-side assurance utility for QNX SDP 8.0 that inspects the development environment, validates critical compiler components, builds reproducible target probes for AArch64 and x86_64, verifies ELF machine types, and generates SHA-256-backed evidence manifests. Its QNX probe exercises Neutrino microkernel message passing.

## Problem
QNX development environments can appear installed while individual toolchain components are missing or damaged. A successful qcc driver invocation alone does not prove that the required target compiler front-end exists or that a produced artifact is a valid executable for the intended architecture. Teams need a repeatable preflight and evidence trail before attempting target deployment.

## What the project does
- Detects QNX SDP environment scripts and SDK root.
- Checks the qcc driver, target headers, and GCC front-ends for AArch64 and x86_64.
- Fails closed when a required compiler component is missing.
- Invokes qcc for the selected QNX target.
- Validates ELF64, little-endian format and the expected machine type.
- Records build logs, artifact size, SHA-256 and machine-readable evidence.
- Includes a QNX-specific IPC probe using ChannelCreate, ConnectAttach, MsgSend, MsgReceive and MsgReply.
- Distinguishes cross-compilation success from target runtime success.

## QNX 8.0 connection
The project uses the QNX SDP 8.0 Windows host toolchain and qcc target specifications:
- AArch64: gcc_ntoaarch64le
- x86_64: gcc_ntox86_64

The QNX probe calls uname() and uses the Neutrino message-passing API to create a channel, attach a local connection, exchange a PING/PONG message and reply. The host tool checks QNX compiler components and validates target-specific ELF outputs.

## Verified results as of 25 November 2026
- Windows 11 host; Python 3.13.17.
- Four automated unit tests passed.
- SDK inspection returned READY_FOR_BUILD for the recovered qnx800_2 installation.
- qcc generated a 14,288-byte AArch64 ELF64 binary (machine 183); SHA-256 dce8db8dcf367652352d0ec49006175b0a9fedf45ad824acbc8d0ecbb0cfaf8a.
- qcc generated a 14,016-byte x86_64 ELF64 binary (machine 62); SHA-256 5a449cf7b4cc00505cddb153c5e42b4a839286145e63e0ba2f78df46fa50b3e5.
- Both builds include the QNX Neutrino IPC probe and pass the ELF architecture gate.

## Explicit limitations
The QNX target runtime has not yet been demonstrated. The official QNX QSTI for QEMU has been installed and its 47.3 GiB virtual disk is being unpacked with sparse-file handling. No claim of QNX boot, runtime IPC success, safety certification or production readiness is made until the probe runs on the target.

## Build and test
See README.md and CODELAB.md. Required commands:
- python -m unittest discover -s tests -v
- python sae_qnx_assurance.py inspect
- python sae_qnx_assurance.py build --arch aarch64
- python sae_qnx_assurance.py build --arch x86_64

## Existing-project update statement
The prior SAE QNX Assurance Bridge concept has been materially extended during the hackathon submission period with a new host-side diagnostic and build-evidence utility, dual-architecture QNX 8.0 compilation, ELF machine validation, automated tests, fail-closed checks, SHA-256 evidence generation, and a QNX Neutrino IPC probe. The new source, tests, documentation and dated evidence files document this work.

## Required before submission
- Complete QNX 8.0 QEMU boot and run the IPC probe successfully.
- Capture a public YouTube demo under three minutes.
- Verify the public GitHub repository and visible MIT license.
- Review applicant eligibility, intellectual-property ownership and all Devpost submission answers.
- Review all text and links in Devpost before submitting.
