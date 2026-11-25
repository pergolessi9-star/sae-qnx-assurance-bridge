#!/usr/bin/env bash
set -euo pipefail

IMAGE_DIR="${QNX_QEMU_IMAGE_DIR:-$HOME/qnx-qemu-image/qemu}"
if [[ ! -f "$IMAGE_DIR/output/ifs.bin" || ! -f "$IMAGE_DIR/output/disk-qemu.vmdk" ]]; then
  echo "QNX QEMU image not found or incomplete at: $IMAGE_DIR" >&2
  exit 2
fi
command -v qemu-system-x86_64 >/dev/null || { echo "Install qemu-system-x86 first." >&2; exit 3; }

cd "$IMAGE_DIR"
exec qemu-system-x86_64 \
  -m "${QNX_RAM_MB:-4096}" -smp "${QNX_CPUS:-4}" -cpu max \
  -kernel output/ifs.bin \
  -drive file=output/disk-qemu.vmdk,if=ide,id=drv0 \
  -netdev user,id=net0,hostfwd=tcp:127.0.0.1:22222-:22 \
  -device virtio-net-pci,netdev=net0,mac=52:54:00:12:34:56 \
  -object rng-random,filename=/dev/urandom,id=rng0 \
  -device virtio-rng-pci,rng=rng0 \
  -nographic -serial stdio -monitor none -no-reboot
