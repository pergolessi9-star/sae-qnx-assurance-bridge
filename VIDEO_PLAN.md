# Demonstration video plan - under 3 minutes

**Target duration:** 2 minutes 30 seconds
**Language:** English
**Format:** direct screen recording of the real software and QNX guest; no simulated output.

1. **0:00-0:15 - Introduction.** Show the project name, purpose and QNX SDP 8.0 target.
2. **0:15-0:35 - Automated tests.** Run the test suite and show all five tests passing.
3. **0:35-1:00 - SDK inspection.** Show READY_FOR_BUILD and the qcc, AArch64, x86_64 and target-header checks.
4. **1:00-1:30 - Cross-build evidence.** Build both architectures; show ELF64 machine identifiers, source hashes and binary SHA-256 records.
5. **1:30-1:50 - QNX boot.** Show the QNX 8.0.0 guest in QEMU and the guest identity from uname.
6. **1:50-2:20 - Runtime and Neutrino IPC.** Download and execute the x86_64 probe in the QNX guest. Show runtime_sysname=QNX, runtime_qnx=1, qnx_msgsend=1 and exit code 0.
7. **2:20-2:30 - Close.** Show repository URL, MIT license and project title.

The final recording must be under three minutes and uploaded publicly to YouTube. Do not include QNX credentials, proprietary SDK files, the QNX system image, or private account information.


Detailed narration, timing and recording checklist: [VIDEO_SCRIPT_EN.md](VIDEO_SCRIPT_EN.md).

