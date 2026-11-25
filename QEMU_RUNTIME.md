## QEMU runtime (WSL)

The official QNX QSTI for QEMU is provided by QNX Software Center. On this workstation it was installed under the Windows SDK and unpacked with sparse-file preservation to `/home/manue/qnx-qemu-image/qemu` because the virtual disk has a 47.3 GiB logical size.

Requirements: Ubuntu WSL, `qemu-system-x86`, and the official QNX QSTI image. The QNX QEMU guide currently documents Ubuntu 22.04/24.04; other releases are not officially listed.

Start the guest:
```bash
bash scripts/run-qnx-qemu-wsl.sh
```

In a second WSL terminal, set the guest password and deploy the x86_64 probe:
```bash
export QNX_GUEST_PASSWORD='qnxuser'
bash scripts/deploy-and-test-qnx.sh
```

The QSTI default account documented by QNX is `qnxuser` with password `qnxuser`. Change the password after first login. Do not store the password in the repository or evidence files.

The runtime test must print `runtime_sysname=QNX`, `compile_target_qnx=1`, and `runtime_qnx=1`, and return exit code 0. Until those exact conditions are observed, runtime status remains pending.
