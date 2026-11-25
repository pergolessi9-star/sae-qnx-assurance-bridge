# SAE QNX Assurance Bridge — Host Tool

Version: 0.1.0  
Status: prototype; QNX 8.0 cross-compilation is verified for AArch64 and x86_64. Runtime on a QNX target is pending.

## Purpose
A Windows/Linux host utility to inspect QNX SDP 8.0, detect missing compiler components, invoke qcc for AArch64 or x86_64, and produce SHA-256-backed evidence. It never claims runtime success from a host-side build.

## Requirements
- Python 3.10+
- QNX SDP 8.0 installed and licensed for intended use
- QNX Software Center for installation verification/repair
- Windows: qnxsdp-env.bat at SDK root

## Important Windows path note
Run the project from an ASCII-only path. The installed QNX Windows toolchain's command-line path handling failed with the original Desktop folder name containing an em dash. The validated working copy is:
`C:\Users\manue\qnx-work\sae-qnx-assurance-bridge`

## Run on Windows
```powershell
Set-Location C:\Users\manue\qnx-work\sae-qnx-assurance-bridge
python -m unittest discover -s tests -v
python .\sae_qnx_assurance.py inspect
python .\sae_qnx_assurance.py build --arch aarch64
python .\sae_qnx_assurance.py build --arch x86_64
```

## Evidence levels
- READY_FOR_BUILD: expected SDK files are present and non-empty.
- CROSS_COMPILE_PASS_RUNTIME_NOT_TESTED: qcc created a non-empty ELF output and the ELF header was inspected; target execution is not implied.
- Runtime verification requires booting QNX 8.0 on QEMU or supported hardware and capturing OS version and probe output.

## Repair procedure
Use QNX Software Center > select qnx800 > Advanced > Verify Installation. Review the report and repair only damaged packages, starting with QNX GCC. Do not manually copy compiler executables or delete the existing SDK/cache.
Official guide: https://www.qnx.com/developers/docs/qsc/com.qnx.doc.qsc.user_guide/topic/repair_packages.html

## Competition readiness
The QNX Global Hackathon requires a public repository, an open-source license, English build/run instructions and a public YouTube demonstration under three minutes. This folder is not yet a submission and does not claim QNX runtime success.
