# Demo video script — SAE QNX Assurance Bridge

**Target:** 2:30 maximum (leave 10 seconds of margin under the 3-minute limit)  
**Language:** English  
**Capture:** direct recording of the real Windows host, QNX SDP 8.0 toolchain and QNX 8.0.0 x86_64 guest in QEMU. Do not fabricate terminal output, composite simulated device footage, or use stock footage as proof.  
**Audio:** spoken narration only; no music.

## Shot list and narration

### 00:00–00:12 — Project and purpose
**On screen:** project title in the terminal or README, then the public GitHub repository.  
**Voice-over:** “This is SAE QNX Assurance Bridge, a host-side validation tool for software targeting QNX SDP 8.0. It makes toolchain checks, cross-builds and runtime evidence reproducible.”

### 00:12–00:32 — Automated tests
**On screen:** in the real project directory run `python -m unittest discover -s tests -v`. Keep the five passing tests visible.  
**Voice-over:** “First, the host-side test suite runs. All five automated tests pass. The command-line self-test is also part of the verification workflow.”

### 00:32–00:52 — SDK inspection
**On screen:** run `python .\sae_qnx_assurance.py inspect`. Show the actual SDK status and compiler target detection. Do not expose license credentials or personal paths.  
**Voice-over:** “The inspection checks the QNX SDP environment and the availability of the required compiler components. The recorded environment reports READY_FOR_BUILD.”

### 00:52–01:18 — Cross-compilation
**On screen:** run `python .\sae_qnx_assurance.py build --arch aarch64` and then `python .\sae_qnx_assurance.py build --arch x86_64`. Show both successful build summaries. If time is short, show the two recorded qcc logs and evidence JSON files after the commands.  
**Voice-over:** “The same C probe is cross-compiled for AArch64 and x86_64 with QNX qcc and strict warning flags. The tool validates the resulting ELF architecture and records hashes and build evidence. AArch64 is cross-compiled and validated; its runtime execution has not been tested.”

### 01:18–01:38 — Real QNX guest
**On screen:** switch to the live QEMU serial console. Show the actual QNX guest identity with `uname -a` and `uname -m`.  
**Voice-over:** “The runtime demonstration uses a QNX 8.0.0 x86_64 guest booted in QEMU. This is a real guest session, not a simulated terminal transcript.”

### 01:38–02:15 — Runtime probe and Neutrino IPC
**On screen:** in the guest, execute the actual transfer and probe commands from `QEMU_RUNTIME.md`: download the x86_64 ELF from the temporary host server, `chmod 755`, run `/tmp/sae_qnx_probe`, then `echo PROBE_EXIT_CODE=$?`. Keep `runtime_sysname=QNX`, `runtime_release=8.0.0`, `qnx_msgsend=1` and exit code 0 visible.  
**Voice-over:** “The probe executes inside QNX. It confirms the operating-system identity and performs a Neutrino message-passing round trip. The guest reports QNX 8.0.0, a successful IPC exchange and exit code zero. Runtime execution is verified for x86_64 only.”

### 02:15–02:30 — Repository and scope
**On screen:** public GitHub repository root, with MIT license and evidence directory visible.  
**Voice-over:** “Source code and reproducible evidence are public under the MIT license. This is an engineering validation aid, not a functional-safety certification.”

## Recording and publication checklist

- Record the actual host and QNX guest screens; no stock footage or generated terminal output.
- Keep the complete video below 2:50; the contest limit is strictly under 3:00.
- Use Windows Game Bar (`Win` + `Alt` + `R`) or another available screen recorder; check microphone input before the take.
- Hide Windows notifications, personal account details, QNX credentials, SDK license data and private paths.
- Do not show or distribute the QNX SDK, QNX system image, proprietary libraries or credentials.
- Use no copyrighted music, third-party logos or unlicensed branding.
- Review the complete exported MP4 before uploading.
- Upload to YouTube and set visibility to **Public**. Copy the final watch URL into the Devpost demo-video field and the hackathon submission.

## Verified scope to state accurately

- Five Python unit tests and the command-line self-test: PASS.
- QNX SDP 8.0 cross-builds: AArch64 and x86_64 PASS.
- ELF64 architecture validation: both targets PASS.
- QNX 8.0.0 x86_64 QEMU guest execution and Neutrino IPC: PASS.
- AArch64 runtime execution: not tested.
- QEMU host: WSL2 Ubuntu 26.04.1 with QEMU 10.2.1; Ubuntu 26.04.1 is an experimental host configuration relative to the QSTI host guidance consulted.
