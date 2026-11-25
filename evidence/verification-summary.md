# Verification summary - SAE QNX Assurance Bridge 0.2.0

## Verified

- QNX SDP 8.0 SDK inspection: READY_FOR_BUILD.
- Automated unit tests: 5/5 PASS.
- Self-test: PASS.
- AArch64 cross-compilation: PASS; ELF64, machine 183, 14,288 bytes.
- x86_64 cross-compilation: PASS; ELF64, machine 62, 14,016 bytes.
- Compiler flags: -Wall -Wextra -Werror.
- Source SHA-256: 55a9b541ff3663840d54dc69513f394e08a6f06a8cadf001d8d02fb6b2c390dc.
- AArch64 binary SHA-256: dce8db8dcf367652352d0ec49006175b0a9fedf45ad824acbc8d0ecbb0cfaf8a.
- x86_64 binary SHA-256: 5a449cf7b4cc00505cddb153c5e42b4a839286145e63e0ba2f78df46fa50b3e5.
- QNX 8.0.0 x86_64 QEMU guest boot: PASS.
- QNX guest identity: QNX qnxqemu 8.0.0, x86pc / x86_64.
- Runtime probe: compile_target_qnx=1, runtime_sysname=QNX, runtime_qnx=1.
- QNX Neutrino IPC: qnx_msgsend=1.
- Runtime process exit code: 0.

## Evidence files

- build-evidence-aarch64.json
- build-evidence-x86_64.json
- environment-report.json
- qcc-build-aarch64.log
- qcc-build-x86_64.log
- qnx-runtime-output.txt
- manifest.json (source, documentation and evidence inventory; build binaries excluded)

## Scope and limitations

- Runtime execution is verified for x86_64 only.
- AArch64 runtime execution remains untested.
- QEMU host: WSL2 Ubuntu 26.04.1 with QEMU 10.2.1. Ubuntu 26.04.1 is not listed in the QNX QSTI host guidance consulted; the configuration is experimental, despite the successful guest run.
- No safety certification, security certification or production-readiness claim is made.
- The QNX SDK and QSTI image are excluded from the source repository.
- Public GitHub repository: https://github.com/pergolessi9-star/sae-qnx-assurance-bridge (publication to be verified after push).
- Public video upload and final Devpost submission remain separate release steps.


