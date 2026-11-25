# QNX 8.0 runtime verification with QEMU

This procedure uses the official QNX QSTI Quickstart image for QEMU. The image, QNX SDK and related proprietary packages are not part of this repository and must not be redistributed unless their license expressly permits it.

## Host prerequisites

- WSL2 with Ubuntu.
- QEMU system emulator for x86_64.
- The official QNX QSTI QEMU image, fully extracted.
- The Windows project directory mounted in WSL.
- Python 3 for the temporary HTTP transfer server.

The recorded test used Ubuntu 26.04.1 LTS and QEMU 10.2.1. QNX's published QSTI guidance referenced Ubuntu 22.04/24.04; Ubuntu 26.04.1 is not listed there. The successful run is evidence of this tested configuration, not a claim that it is an officially supported host.

## 1. Start the QNX guest

Set the path to the extracted QNX image:

```bash
export QNX_QEMU_IMAGE_DIR="$HOME/qnx-qemu-image/qemu"
bash scripts/run-qnx-qemu-wsl.sh
```

If the image is stored elsewhere, set `QNX_QEMU_IMAGE_DIR` to its `qemu` directory. The launcher checks for both `ifs.bin` and the VMDK descriptor before starting QEMU.

The guest presents a login prompt on the serial console. Sign in using the credentials supplied with the QNX QSTI image. Do not store passwords in the repository or evidence files.

## 2. Serve the x86_64 probe from WSL

In a second WSL terminal:

```bash
export SAE_PROJECT_DIR="/mnt/c/Users/<windows-user>/qnx-work/sae-qnx-assurance-bridge"
bash scripts/serve-probe-wsl.sh
```

The helper copies the x86_64 ELF into a temporary transfer directory and starts a local HTTP server on port 8080. Keep this process running while the guest downloads the file.

## 3. Download and execute inside QNX

At the QNX guest serial-console shell:

```sh
curl -f http://10.0.2.2:8080/sae_qnx_probe_x86_64.elf -o /tmp/sae_qnx_probe
chmod 755 /tmp/sae_qnx_probe
/tmp/sae_qnx_probe
echo PROBE_EXIT_CODE=$?
```

The address `10.0.2.2` is the QEMU user-network host gateway.

## 4. Runtime acceptance criteria

A successful QNX 8.0 run must report:

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

The IPC check creates a Neutrino channel, attaches a client connection, sends a PING message, receives it on a server thread, and returns PONG. A zero exit code is required.

The verified run is recorded in `evidence/qnx-runtime-output.txt`. It applies to the x86_64 QNX QEMU guest only. AArch64 runtime remains untested.
