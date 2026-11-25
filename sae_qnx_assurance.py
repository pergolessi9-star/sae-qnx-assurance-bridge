#!/usr/bin/env python3
"""SAE QNX Assurance Bridge: host-side diagnostics and reproducible QNX build evidence."""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import platform
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

VERSION = "0.2.0"
TARGETS = {"aarch64": "gcc_ntoaarch64le", "x86_64": "gcc_ntox86_64"}
EXPECTED_ELF_MACHINES = {"aarch64": 183, "x86_64": 62}
COMPILER_FLAGS = ["-Wall", "-Wextra", "-Werror"]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def elf_machine(path: Path) -> int:
    header = path.read_bytes()[:20]
    if len(header) < 20 or header[:4] != bytes([127, 69, 76, 70]):
        raise ValueError("Not a valid ELF header")
    if header[4] != 2 or header[5] != 1:
        raise ValueError("Expected a little-endian ELF64 binary")
    return int.from_bytes(header[18:20], "little")


def stage_source(source: Path, stage_dir: Path) -> Path:
    """Copy a source file to an ASCII-only staging directory for QNX Windows tools."""
    stage_dir.mkdir(parents=True, exist_ok=True)
    staged = stage_dir / "sae_qnx_probe.c"
    shutil.copy2(source, staged)
    return staged


def run(args, *, env=None, timeout=120, shell=False):
    try:
        p = subprocess.run(
            args,
            env=env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=timeout,
            shell=shell,
        )
        return p.returncode, p.stdout
    except (OSError, subprocess.TimeoutExpired) as exc:
        return 127, str(exc)


def sdk_candidates():
    values = [
        os.environ.get("QNX_BASE"),
        str(Path.home() / "qnx800_2"),
        str(Path.home() / "qnx800"),
        r"C:\\qnx800",
    ]
    seen = set()
    for value in values:
        if value and value.lower() not in seen:
            seen.add(value.lower())
            p = Path(value)
            if p.exists():
                yield p


def inspect_sdk():
    report = {
        "tool": "SAE QNX Assurance Bridge",
        "version": VERSION,
        "host": platform.platform(),
        "python": sys.version.split()[0],
        "checked_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "status": "NOT_VERIFIED",
        "checks": [],
    }
    sdk = next(
        (
            p
            for p in sdk_candidates()
            if (p / "qnxsdp-env.bat").exists() or (p / "qnxsdp-env.sh").exists()
        ),
        None,
    )
    if not sdk:
        report["checks"].append(
            {
                "id": "sdk_root",
                "status": "FAIL",
                "detail": "QNX SDP environment script not found",
            }
        )
        return report

    report["sdk_root"] = str(sdk)
    report["checks"].append(
        {"id": "sdk_root", "status": "PASS", "detail": "QNX SDP environment script found"}
    )

    host = sdk / "host" / "win64" / "x86_64"
    qcc = host / "usr" / "bin" / ("qcc.exe" if os.name == "nt" else "qcc")
    report["qcc"] = str(qcc)
    report["checks"].append(
        {
            "id": "qcc_driver",
            "status": "PASS" if qcc.is_file() and qcc.stat().st_size > 0 else "FAIL",
            "detail": f"present={qcc.is_file()}, bytes={qcc.stat().st_size if qcc.exists() else 0}",
        }
    )

    gccroot = host / "usr" / "lib" / "gcc"
    for arch, triplet in (
        ("aarch64", "aarch64-unknown-nto-qnx8.0.0"),
        ("x86_64", "x86_64-pc-nto-qnx8.0.0"),
    ):
        gccbase = gccroot / triplet / "12.2.0"
        cc1 = (
            [p for p in gccbase.glob("cc1*") if p.is_file() and p.stat().st_size > 0]
            if gccbase.exists()
            else []
        )
        report["checks"].append(
            {
                "id": f"{arch}_cc1",
                "status": "PASS" if cc1 else "FAIL",
                "detail": f"non-empty compiler frontend found={bool(cc1)}",
            }
        )

    headers = sdk / "target" / "qnx" / "usr" / "include"
    report["checks"].append(
        {
            "id": "qnx_target_headers",
            "status": "PASS" if headers.is_dir() else "FAIL",
            "detail": "QNX target headers directory",
        }
    )
    report["status"] = (
        "READY_FOR_BUILD"
        if all(check["status"] == "PASS" for check in report["checks"])
        else "BLOCKED"
    )
    return report


def build(arch: str) -> int:
    root = Path(__file__).resolve().parent
    source = root / "src" / "sae_qnx_probe.c"
    outdir = root / "build"
    evdir = root / "evidence"
    outdir.mkdir(exist_ok=True)
    evdir.mkdir(exist_ok=True)

    if not source.is_file():
        print(f"BUILD_BLOCKED: source file not found: {source}")
        return 19

    report = inspect_sdk()
    public_report = dict(report)
    if public_report.get("sdk_root"):
        public_report["sdk_root"] = "<QNX_SDP_ROOT>"
    if public_report.get("qcc"):
        public_report["qcc"] = "<QNX_SDP_ROOT>/host/win64/x86_64/usr/bin/qcc.exe"
    (evdir / "environment-report.json").write_text(
        json.dumps(public_report, indent=2) + "\n", encoding="utf-8"
    )
    if report["status"] != "READY_FOR_BUILD":
        print("BUILD_BLOCKED: SDK validation failed; see evidence/environment-report.json")
        return 20

    target = TARGETS[arch]
    source_hash = sha256(source)
    binary = outdir / f"sae_qnx_probe_{arch}.elf"
    log_path = evdir / f"qcc-build-{arch}.log"

    with tempfile.TemporaryDirectory(prefix="sae_qnx_") as temp_name:
        stage_dir = Path(temp_name)
        staged_source = stage_source(source, stage_dir)
        staged_binary = stage_dir / f"sae_qnx_probe_{arch}.elf"
        env_script = Path(report["sdk_root"]) / "qnxsdp-env.bat"

        if os.name == "nt":
            command = (
                f'cd /d "{stage_dir}" && call "{env_script}" >nul 2>&1 && '
                f'qcc -V{target} {" ".join(COMPILER_FLAGS)} '
                f'-o "{staged_binary}" "{staged_source}"'
            )
            rc, output = run(command, timeout=120, shell=True)
            command_record = command
        else:
            command_args = [
                report["qcc"],
                f"-V{target}",
                *COMPILER_FLAGS,
                "-o",
                str(staged_binary),
                str(staged_source),
            ]
            rc, output = run(command_args, env=os.environ.copy(), timeout=120)
            command_record = subprocess.list2cmdline(command_args)

        display_command = command_record.replace(str(stage_dir), "<TEMP>")
        display_command = display_command.replace(str(env_script), "<QNX_SDP_ROOT>/qnxsdp-env.bat")
        display_command = display_command.replace(str(report["sdk_root"]), "<QNX_SDP_ROOT>")
        log = (
            "SAE QNX Assurance Bridge build log\n"
            f"tool_version={VERSION}\n"
            "sdk_root=<QNX_SDP_ROOT>\n"
            f"target={target}\n"
            "source=<PROJECT_ROOT>/src/sae_qnx_probe.c\n"
            f"source_sha256={source_hash}\n"
            f"compiler_flags={' '.join(COMPILER_FLAGS)}\n"
            f"command={display_command}\n"
            f"exit_code={rc}\n"
            "----- compiler output -----\n"
            f"{output}\n"
        )
        log_path.write_text(log, encoding="utf-8")

        if rc != 0 or not staged_binary.is_file() or staged_binary.stat().st_size == 0:
            print("BUILD_FAIL: compiler returned an error or produced no ELF binary")
            print(output[-3000:])
            return 21

        shutil.copy2(staged_binary, binary)

    machine = elf_machine(binary)
    expected_machine = EXPECTED_ELF_MACHINES[arch]
    if machine != expected_machine:
        print(f"BUILD_FAIL: ELF machine {machine} does not match {arch} ({expected_machine})")
        return 22

    evidence = {
        "schema": "sae-qnx-assurance-evidence-v1",
        "tool_version": VERSION,
        "generated_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "status": "CROSS_COMPILE_PASS_RUNTIME_NOT_TESTED",
        "target": f"QNX SDP 8.0 {arch} ({target})",
        "source": {
            "path": "src/sae_qnx_probe.c",
            "sha256": source_hash,
        },
        "compiler_flags": COMPILER_FLAGS,
        "build_log": str(log_path.relative_to(root)),
        "binary": {
            "path": str(binary.relative_to(root)),
            "bytes": binary.stat().st_size,
            "sha256": sha256(binary),
            "elf_class": "ELF64",
            "elf_machine": machine,
            "architecture": arch,
        },
        "environment_report": "evidence/environment-report.json",
    }
    (evdir / f"build-evidence-{arch}.json").write_text(
        json.dumps(evidence, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(evidence, indent=2))
    return 0


def self_test() -> int:
    assert TARGETS["aarch64"] == "gcc_ntoaarch64le"
    assert TARGETS["x86_64"] == "gcc_ntox86_64"
    assert len(sha256(Path(__file__))) == 64
    assert inspect_sdk()["status"] in {"BLOCKED", "READY_FOR_BUILD"}
    print("SELF_TEST_PASS: target mapping, SHA-256 and SDK inspection")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Diagnose QNX SDP 8.0 and build auditable target evidence."
    )
    parser.add_argument("command", choices=["inspect", "build", "self-test"])
    parser.add_argument("--arch", choices=["aarch64", "x86_64"], default="aarch64")
    args = parser.parse_args()

    if args.command == "inspect":
        result = inspect_sdk()
        print(json.dumps(result, indent=2))
        return 0 if result["status"] == "READY_FOR_BUILD" else 20
    if args.command == "build":
        return build(args.arch)
    return self_test()


if __name__ == "__main__":
    raise SystemExit(main())
