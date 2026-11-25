# SAE QNX Assurance Bridge

**Version:** 0.2.0
**Category:** Developer Tooling & Host Tools
**License:** MIT
**Project status:** QNX 8.0 cross-compilation verified for AArch64 and x86_64; QNX 8.0 x86_64 runtime and Neutrino IPC probe verified in QEMU.

## Overview

SAE QNX Assurance Bridge is a host-side validation utility for QNX SDP 8.0. It inspects the SDK installation, checks required compiler components, builds target-specific C probes, validates ELF architecture, and creates machine-readable evidence containing source and binary SHA-256 hashes.

The included target probe identifies the runtime operating system and, when compiled for QNX, exercises a Neutrino message-passing round trip using ChannelCreate, ConnectAttach, MsgSend, MsgReceive and MsgReply.

The tool deliberately separates host-side cross-compilation evidence from target runtime evidence. A successful build is never represented as proof that the program has executed on QNX.

## Verified results

| Check | Result |
|---|---|
| QNX SDP 8.0 SDK inspection | PASS |
| Automated unit tests | 5/5 PASS |
| AArch64 cross-compilation | PASS; ELF64, machine 183 |
| x86_64 cross-compilation | PASS; ELF64, machine 62 |
| QNX 8.0 x86_64 runtime in QEMU | PASS |
| QNX Neutrino IPC round trip | PASS; qnx_msgsend=1 |
| Runtime probe exit code | 0 |

Runtime evidence is in `evidence/qnx-runtime-output.txt`. Cross-build evidence is in `evidence/build-evidence-aarch64.json` and `evidence/build-evidence-x86_64.json`.

## Requirements

- Windows 10/11 x86_64 host.
- Python 3.10 or later.
- QNX SDP 8.0 installed and licensed for the intended use.
- QNX Software Center for SDK installation and repair.
- Optional runtime demonstration: QNX QSTI image for QEMU, WSL2, and QEMU.

The QNX SDK and QSTI image are not included in this repository. Obtain them through the official QNX distribution channels and comply with their license terms.

## Build and test on Windows

Open PowerShell in the project directory:

```powershell
python -m unittest discover -s tests -v
python .\sae_qnx_assurance.py inspect
python .\sae_qnx_assurance.py build --arch aarch64
python .\sae_qnx_assurance.py build --arch x86_64
```

The build command loads the QNX SDP environment, stages the source into a temporary directory to avoid non-ASCII path issues in the Windows toolchain, invokes qcc with `-Wall -Wextra -Werror`, validates the ELF64 header and expected machine identifier, and writes a JSON evidence record plus a build log.

Target binaries are written to `build/sae_qnx_probe_<architecture>.elf`. They are QNX ELF binaries, not Windows executables.

## Runtime demonstration with QEMU

See [QEMU_RUNTIME.md](QEMU_RUNTIME.md) for the reproducible QNX 8.0 boot and probe procedure. The verified x86_64 probe was transferred to the guest over the QEMU user-network host address and executed from the QNX serial console.

The QNX guest returned:

```text
SAE_QNX_PROBE_V2
compile_target_qnx=1
runtime_sysname=QNX
runtime_release=8.0.0
runtime_machine=x86pc
runtime_qnx=1
qnx_msgsend=1
PROBE_EXIT_CODE=0
```

## Evidence model

- `READY_FOR_BUILD`: required SDK files and compiler components are present.
- `CROSS_COMPILE_PASS_RUNTIME_NOT_TESTED`: qcc produced a non-empty ELF64 binary with the expected machine type. This status does not imply target execution.
- Runtime PASS: the probe has run inside QNX, reports `runtime_sysname=QNX`, `runtime_qnx=1`, `qnx_msgsend=1`, and exits with code 0.

Evidence files are generated locally. Review them before sharing, and do not include credentials, proprietary SDK files, QNX system images, or third-party materials that are not licensed for redistribution.

## Limitations

- QNX runtime has been demonstrated on x86_64 only. AArch64 is cross-compiled and ELF-validated but has not been run on an AArch64 QNX target.
- The QEMU host used for the recorded test was Ubuntu 26.04.1 under WSL2 with QEMU 10.2.1. QNX's QSTI documentation referenced Ubuntu 22.04/24.04; Ubuntu 26.04.1 is therefore an experimental host configuration, even though the recorded QNX runtime test succeeded.
- This project is a development and evidence utility. It does not provide functional-safety certification, security certification, or production-readiness assurance.

## Project links`r`n`r`n- Devpost project: https://devpost.com/software/sae-qnx-assurance-bridge`r`n- Public source repository: https://github.com/pergolessi9-star/sae-qnx-assurance-bridge`r`n- Hackathon: https://qnx.devpost.com/`r`n`r`n## Competition material

The project description and submission narrative are in [SUBMISSION_DRAFT.md](SUBMISSION_DRAFT.md). The video outline is in [VIDEO_PLAN.md](VIDEO_PLAN.md). The public source repository is published at the GitHub URL above. The public demonstration video remains a separate release requirement.

