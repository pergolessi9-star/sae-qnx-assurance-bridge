# Technical audit - 26 November 2026

## Host and SDK

- Host: Windows 11 x86_64.
- Python: 3.13.17.
- Working QNX SDP 8.0 installation: recovered secondary SDK profile (absolute local path omitted from public evidence).
- The original SDK installation remains untouched; the recovered secondary SDK installation is used.
- qcc driver, AArch64 and x86_64 GCC 12.2.0 front-ends, and QNX target headers are present.
- qcc target variants: gcc_ntoaarch64le and gcc_ntox86_64.

## Tool version 0.2.0

- SDK inspection: READY_FOR_BUILD.
- Automated tests: 5 passed, 0 failed.
- Self-test: PASS.
- Builds use -Wall -Wextra -Werror.
- Source staging copies the C probe into a temporary directory before invoking the Windows QNX toolchain, avoiding source-path Unicode handling issues.
- ELF validation checks ELF64, little-endian encoding and machine type: AArch64=183; x86_64=62.
- Build logs record SDK root, target, source SHA-256, compiler flags, command, exit code and compiler output.

## Cross-compilation evidence

- Source SHA-256: 55a9b541ff3663840d54dc69513f394e08a6f06a8cadf001d8d02fb6b2c390dc.
- AArch64 output: 14,288 bytes; SHA-256 dce8db8dcf367652352d0ec49006175b0a9fedf45ad824acbc8d0ecbb0cfaf8a.
- x86_64 output: 14,016 bytes; SHA-256 5a449cf7b4cc00505cddb153c5e42b4a839286145e63e0ba2f78df46fa50b3e5.
- Both build evidence JSON files parse successfully.
- Build statuses remain CROSS_COMPILE_PASS_RUNTIME_NOT_TESTED because the host build tool itself does not infer runtime success.

## QNX 8.0 runtime verification

- Official QNX QSTI Quickstart archive parts: 2,561,493,652 bytes total.
- Extracted VMDK extent: 50,826,834,432 bytes (47.3 GiB logical); sparse disk allocation approximately 5.01 GiB.
- QEMU: 10.2.1.
- WSL distribution: Ubuntu 26.04.1 LTS. QNX QSTI documentation referenced Ubuntu 22.04/24.04; 26.04.1 is not listed and is recorded as an experimental host.
- QEMU boot completed and the guest login prompt appeared on the serial console.
- Guest uname: QNX qnxqemu 8.0.0 2026/06/05-16:26:03EDT x86pc x86_64.
- Guest uname -m: x86pc.
- /boot, /usr and /data were accessible after boot.
- The x86_64 ELF was transferred to the guest over QEMU user networking using HTTP; the host server returned HTTP 200 for 14,016 bytes.
- Guest probe output:
  - compile_target_qnx=1
  - runtime_sysname=QNX
  - runtime_release=8.0.0
  - runtime_machine=x86pc
  - runtime_qnx=1
  - qnx_msgsend=1
  - PROBE_EXIT_CODE=0
- The QNX Neutrino message-passing round trip succeeded.
- Full captured result: evidence/qnx-runtime-output.txt.

## Transport qualification

The attempted SSH connection through QEMU host forwarding was reset by the guest. It was not used as runtime evidence. The successful transfer and execution used the QNX serial console and a temporary HTTP server reachable at 10.0.2.2 from the guest.

## Repository and release

- Canonical working copy: local qnx-work checkout (absolute path intentionally omitted).
- The older OneDrive copy is not canonical and must not overwrite the working copy.
- Local Git history exists on branch main.
- No Git remote is configured; no public GitHub repository has been created or pushed.
- MIT license is present and the copyright-holder encoding was corrected.
- English README, QEMU runtime guide, technical audit, submission draft and video plan are maintained locally.
- QNX SDK and QSTI image are excluded from the repository.
- Public demo video has not yet been recorded or uploaded.
- Devpost submission has not been sent.

## Status

QNX SDP 8.0 SDK inspection, five automated tests, AArch64 and x86_64 cross-compilation, ELF architecture validation, and QNX 8.0 x86_64 runtime including Neutrino IPC are verified. AArch64 runtime, public GitHub publication, public video and Devpost submission remain open.
