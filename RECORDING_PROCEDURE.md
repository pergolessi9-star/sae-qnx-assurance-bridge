# Final recording procedure — QNX Global Hackathon

This procedure records the actual application and QNX guest. It does not generate synthetic footage or use prerecorded terminal output as a substitute for the live test.

## 1. Before recording

- Confirm that the QNX 8.0.0 guest is running in QEMU. The current machine has an active QEMU process and the QEMU SSH-forward port 22222 responds locally.
- Open the project directory in PowerShell:

```powershell
Set-Location C:\Users\manue\qnx-work\sae-qnx-assurance-bridge
```

- Close private windows and notifications. Do not display account settings, passwords, license credentials, personal email, private paths or the QNX system image.
- Open the Windows Game Bar with `Win + G`; confirm the Capture widget is available and microphone selection is correct.
- Game Bar shortcut: `Win + Alt + R` starts/stops recording. Captures are normally saved under `%USERPROFILE%\Videos\Captures`.
- Record only the application windows needed for the demonstration. Do not capture unrelated desktop activity.

## 2. Record the host-side checks

Start the recording, then run these commands in the project directory:

```powershell
python -m unittest discover -s tests -v
python .\sae_qnx_assurance.py self-test
python .\sae_qnx_assurance.py inspect
python .\sae_qnx_assurance.py build --arch aarch64
python .\sae_qnx_assurance.py build --arch x86_64
```

Keep the successful results visible. The expected unit-test result is five tests, all passing. The SDK inspection should report `READY_FOR_BUILD`. Both builds should complete successfully and validate the expected ELF machine identifiers. If a command fails in the recording session, stop and investigate; do not edit or replace the output to make it appear successful.

## 3. Record the QNX guest runtime

Switch to the actual QEMU QNX guest serial console. Show the guest identity:

```sh
uname -a
uname -m
```

If the x86_64 probe is already present in the guest, run:

```sh
/tmp/sae_qnx_probe
echo PROBE_EXIT_CODE=$?
```

If it is not present, follow the transfer steps in `QEMU_RUNTIME.md`; do not invent or paste expected output. Show the real output values `runtime_sysname=QNX`, `runtime_release=8.0.0`, `qnx_msgsend=1`, and `PROBE_EXIT_CODE=0` only if the live execution returns them.

## 4. Finish and publish

- Stop recording with `Win + Alt + R`.
- Review the entire MP4, its duration, sound and legibility. Target 2:30; absolute limit strictly below 3:00.
- Confirm that no credentials, personal information, proprietary SDK material or QNX image are visible or audible.
- Upload the reviewed MP4 to YouTube and set visibility to **Public**.
- Copy the final YouTube watch URL into the existing Devpost project and the QNX Global Hackathon submission. Do not create a second Devpost project.

## 5. Current submission state

- Public GitHub repository: https://github.com/pergolessi9-star/sae-qnx-assurance-bridge
- Existing Devpost project: https://devpost.com/software/sae-qnx-assurance-bridge
- Project linked to QNX Global Hackathon; `submitted_at` remains null until the formal submission is completed.
- Public demo video: not yet recorded or uploaded.
- Final formal submission: pending.
