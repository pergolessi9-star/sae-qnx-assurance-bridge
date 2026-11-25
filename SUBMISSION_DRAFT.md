# QNX Global Hackathon — Submission Draft

## Project
SAE QNX Assurance Bridge

## Category
Developer Tooling & Host Tools

## Short description
A host-side assurance utility for QNX SDP 8.0 that inspects the development environment, validates critical compiler components, builds reproducible target probes for AArch64 and x86_64, inspects ELF output, and generates SHA-256-backed evidence manifests.

## Problem
QNX development environments can appear installed while individual toolchain components are missing or damaged. A successful qcc driver invocation alone does not prove that the required target compiler front-end exists or that a produced artifact is a valid executable for the intended architecture. Teams need a repeatable preflight and evidence trail before attempting target deployment.

## What the project does
- Detects QNX SDP environment scripts and SDK root.
- Checks the qcc driver, target headers, and GCC front-ends for AArch64 and x86_64.
- Fails closed when a required compiler component is missing.
- Invokes qcc for the selected QNX target.
- Checks that the output is a non-empty ELF executable.
- Records build logs, artifact size, SHA-256 and machine-readable evidence.
- Distinguishes cross-compilation success from target runtime success.

## QNX 8.0 connection
The project uses the QNX SDP 8.0 Windows host toolchain and qcc target specifications:
- AArch64: gcc_ntoaarch64le
- x86_64: gcc_ntox86_64

The QNX-specific probe includes sys/utsname.h and uses uname() to identify the runtime OS. The host tool checks the installed QNX compiler components and produces target-specific ELF binaries.

## Verified results as of 25 November 2026
- Windows 11 host; Python 3.13.17.
- Three automated unit tests passed.
- SDK inspection returned READY_FOR_BUILD for the recovered qnx800_2 installation.
- qcc generated a 9,640-byte AArch64 ELF64 binary.
- qcc generated a 9,392-byte x86_64 ELF64 binary.
- ELF inspection confirmed AArch64 and Advanced Micro Devices X86-64 machine types.
- SHA-256 hashes are recorded in evidence/build-evidence-aarch64.json and evidence/build-evidence-x86_64.json.

## Explicit limitations
The QNX target runtime has not yet been demonstrated. The QNX QEMU quick-start image is being prepared. No claim of boot, deployment, runtime compatibility, safety certification, or production readiness is made.

## Build and test
See README.md. The required commands are:
- python -m unittest discover -s tests -v
- python sae_qnx_assurance.py inspect
- python sae_qnx_assurance.py build --arch aarch64
- python sae_qnx_assurance.py build --arch x86_64

## Existing-project update statement
The prior SAE QNX Assurance Bridge concept has been materially extended during the hackathon submission period with a new host-side diagnostic and build-evidence utility, dual-architecture QNX 8.0 compilation, ELF inspection, automated tests, fail-closed checks, and SHA-256 evidence generation. The dated local evidence files document the new work.

## Required before submission
- Complete QNX 8.0 QEMU boot and runtime test.
- Capture a public YouTube demo under three minutes.
- Verify the public GitHub repository and visible MIT license.
- Review all text and links in Devpost before submission.
