# Technical audit — 25 November 2026

## Host and SDK

- Host: Windows 11, build 26200.
- Python: 3.13.17.
- Working QNX SDP 8.0 installation: C:\Users\manue\qnx800_2.
- The original C:\Users\manue\qnx800 installation has a damaged/incomplete GCC component: the AArch64 cc1 front-end was absent and some compiler files had zero length. It has been left untouched.
- The recovered qnx800_2 SDK has a non-empty qcc driver, AArch64 and x86_64 GCC front-ends, and QNX target headers.
- QNX qcc reports GCC 12.2.0 target variants for gcc_ntoaarch64le and gcc_ntox86_64.

## Reproducible build evidence

- Automated tests: 3 passed, 0 failed.
- SDK inspection: READY_FOR_BUILD.
- AArch64 output: 9,640 bytes; SHA-256 2ab2603013f88d29e9329d21c5b2f892b06bc3b8cc59def7c7bb1317935aae63.
- x86_64 output: 9,392 bytes; SHA-256 df1c2a934e160d85d4d11aa8ed8229c5ca0235eb702317e6c589ae3860831400.
- Both outputs were checked as ELF executables and their machine architecture was inspected.
- The evidence files intentionally say CROSS_COMPILE_PASS_RUNTIME_NOT_TESTED until the target probe executes inside QNX.

## QEMU target preparation

- QNX Software Center package: com.qnx.qnx800.quickstart.qemu, version 0.5.0.00050T202609021847L.
- QEMU is installed in WSL.
- QNX's QSTI archive is 2.5 GiB compressed; its virtual disk has a 47.3 GiB logical size.
- The image is being extracted to WSL's Linux filesystem using a sparse-aware extractor. This avoids writing zero-filled sectors to the Windows C: volume.
- First QEMU boot was attempted before the disk image had finished extracting. It failed to mount /boot, /usr and /data. That attempt is invalid and is not counted as a runtime test.
- A clean QEMU boot and probe execution are still required.
- QNX's current QSTI documentation lists Ubuntu 22.04 and 24.04 as supported. The installed WSL distribution should be checked against this requirement before claiming supported-host status.

## Repository and release

- Local Git repository initialized on main.
- Commit fdec466: initial host assurance utility.
- Commit 9b6fe8a: QEMU runtime harness and submission draft.
- MIT license and English documentation are included.
- Local source ZIP: C:\Users\manue\qnx-work\sae-qnx-assurance-bridge-v0.1.0.zip.
- Public GitHub repository has not been created or pushed. The GitHub browser sign-in step is pending.
- Demo video has not been recorded or uploaded to YouTube.

## Status

Cross-compilation for QNX 8.0 AArch64 and x86_64 is verified. QNX runtime, public repository publication, and public demo video remain open acceptance criteria. No QNX runtime or competition submission success is claimed.
