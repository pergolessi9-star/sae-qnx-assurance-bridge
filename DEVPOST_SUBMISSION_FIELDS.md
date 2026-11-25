# QNX Global Hackathon — Devpost form answers (prepared draft)

Existing project: https://devpost.com/software/sae-qnx-assurance-bridge  
Project repository: https://github.com/pergolessi9-star/sae-qnx-assurance-bridge  
Category: Developer Tooling & Host Tools

This file prepares the custom answers returned by the Devpost submission requirements. It is not a submitted entry. The public demo video is still mandatory and has not yet been recorded/uploaded.

## Required fields — prepared values

| Devpost field ID | Label | Prepared answer | Basis / status |
|---|---|---|---|
| 29214 | Submitter Type | Individual | Single-person project entry; no team or organization submission is intended. |
| 29215 | Submitter Country of Residence | Spain | User's established residence context; dropdown accepts a list, use `Spain`. |
| 29216 | Organization name | Leave blank | Not submitting on behalf of an organization. |
| 29217 | New or existed before 2 November 2026? | New | The SAE QNX Assurance Bridge Devpost project was created 13 November 2026; the local repository's first commit is 25 November 2026. No evidence found of this specific QNX Bridge project existing before 2 November. Other SAE projects are distinct. |
| 29218 | If it existed before, explain changes | N/A | Required instruction for a new project. |
| 29219 | Category | Developer Tooling & Host Tools | Exact category for a host-side QNX development tool. |
| 29220 | Public repository URL | https://github.com/pergolessi9-star/sae-qnx-assurance-bridge | Public GitHub repository, MIT license. |
| 29221 | Build and run instructions | See prepared text below. | Specifies QNX 8.0, Windows 11 host, qcc toolchain, AArch64/x86_64 cross-builds and QEMU x86_64 runtime. |
| 29222 | Main technology requirement | See prepared text below. | Identifies QNX SDP 8.0, qcc, QNX Neutrino IPC and exact source/evidence files. |
| 29223 | Upstream project URL | Leave blank | Not entering Open-Source Contribution & Ports. |
| 29224 | Pull request URL | Leave blank | Not entering Open-Source Contribution & Ports. |
| 29225 | Codelab URL | Leave blank | Not entering Best Codelab / Tutorial bonus prize. |
| 29090 | Likelihood of using QNX again | USER TO SELECT | Personal assessment; not inferred or preselected. |
| 29089 | How much the hackathon helped develop skills | USER TO SELECT | Personal assessment; not inferred or preselected. |
| 29285 | AI tools used | See prepared text below. | Disclose actual AI assistance without claiming AI performed the QNX runtime test. |
| 29226 | Age of Majority | USER MUST CONFIRM | Personal legal attestation. |
| 29227 | Eligible Jurisdiction | USER MUST CONFIRM | Personal legal attestation. Spain is not among the listed excluded jurisdictions in the current rules. |
| 29228 | Conflict of interest | USER MUST CONFIRM | Personal legal attestation. No conflict is identified in available project context, but this checkbox must be personally confirmed. |

## Field 29221 — Build and run instructions

QNX version: QNX SDP 8.0 (QNX Everywhere). Host: Windows 11 x86_64 with Python 3.13.17 and the QNX SDP 8.0 Windows host toolchain. Target variants: `gcc_ntoaarch64le` (AArch64) and `gcc_ntox86_64` (x86_64), invoked through `qcc` with `-Wall -Wextra -Werror`. Run the host checks from the repository root with `python -m unittest discover -s tests -v`, `python .\\sae_qnx_assurance.py self-test` and `python .\\sae_qnx_assurance.py inspect`. Cross-build using `python .\\sae_qnx_assurance.py build --arch aarch64` and `python .\\sae_qnx_assurance.py build --arch x86_64`. The resulting ELF64 files are validated for their expected machine architecture. Runtime verification was performed on a QNX 8.0.0 x86_64 guest under QEMU 10.2.1 in WSL2 Ubuntu 26.04.1; the probe reports the QNX guest identity, performs a Neutrino IPC round trip and exits with code 0. See `README.md` and `QEMU_RUNTIME.md` for the complete instructions. AArch64 runtime execution has not been tested.

## Field 29222 — Main technology requirement

This is a Windows host-based developer tool that directly supports software targeting QNX 8.0. It inspects the QNX SDP 8.0 installation and the presence of the qcc driver, target headers and GCC 12.2.0 compiler front-ends; invokes QNX `qcc` for AArch64 and x86_64; validates ELF64 class, endianness and machine identifiers; and records build logs, JSON evidence and SHA-256 hashes. The QNX-specific probe in `src/sae_qnx_probe.c` uses QNX Neutrino APIs `ChannelCreate`, `ConnectAttach`, `MsgSend`, `MsgReceive` and `MsgReply` to perform a message-passing round trip. The recorded QNX 8.0.0 x86_64 QEMU execution and IPC result are in `evidence/qnx-runtime-output.txt`. The build orchestration and SDK checks are in `sae_qnx_assurance.py`; the five host-side tests are in `tests/test_bridge.py`; cross-build records are in `evidence/qcc-build-aarch64.log`, `evidence/qcc-build-x86_64.log`, `evidence/build-evidence-aarch64.json` and `evidence/build-evidence-x86_64.json`. The reproducible runtime procedure is in `QEMU_RUNTIME.md`. AArch64 has been cross-compiled and ELF-validated, but runtime execution on AArch64 has not been tested.

## Field 29285 — AI tools leveraged

OpenAI ChatGPT was used as an AI-assisted development and documentation aid for architecture discussion, code review, test planning, technical writing and preparation of the hackathon submission. All claimed build, test and runtime results are based on recorded command execution and evidence files; AI-generated text is not presented as a substitute for QNX execution or validation.

## Submission blockers

1. Record the real project demonstration, under 3 minutes, showing the live QNX 8.0.0 guest and Neutrino IPC result.
2. Upload the video to YouTube and set it to Public.
3. Enter the public YouTube URL as the demo video for the existing QNX hackathon entry.
4. The entrant must personally choose fields 29090 and 29089 and confirm the legal declarations 29226–29228.
5. Submit the existing project entry and verify Devpost returns `Submitted` with a non-null `submitted_at`.

Do not create a second Devpost project or mark the entry submitted before Devpost confirms it.
