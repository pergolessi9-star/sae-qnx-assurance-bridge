#!/usr/bin/env python3
"""SAE QNX Assurance Bridge: host-side diagnostics and reproducible QNX build evidence."""
from __future__ import annotations
import argparse, datetime as dt, hashlib, json, os, platform, subprocess, sys
from pathlib import Path

VERSION = "0.1.0"
TARGETS = {"aarch64": "gcc_ntoaarch64le", "x86_64": "gcc_ntox86_64"}

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()

def run(args, *, env=None, timeout=90, shell=False):
    try:
        p = subprocess.run(args, env=env, text=True, stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT, timeout=timeout, shell=shell)
        return p.returncode, p.stdout
    except (OSError, subprocess.TimeoutExpired) as exc:
        return 127, str(exc)

def sdk_candidates():
    values = [os.environ.get("QNX_BASE"), str(Path.home() / "qnx800_2"), str(Path.home() / "qnx800"), r"C:\qnx800"]
    seen = set()
    for value in values:
        if value and value.lower() not in seen:
            seen.add(value.lower())
            p = Path(value)
            if p.exists():
                yield p

def inspect_sdk():
    report = {"tool":"SAE QNX Assurance Bridge","version":VERSION,"host":platform.platform(),
              "python":sys.version.split()[0],"checked_utc":dt.datetime.now(dt.timezone.utc).isoformat(),
              "status":"NOT_VERIFIED","checks":[]}
    sdk = next((p for p in sdk_candidates() if (p/"qnxsdp-env.bat").exists() or (p/"qnxsdp-env.sh").exists()),None)
    if not sdk:
        report["checks"].append({"id":"sdk_root","status":"FAIL","detail":"QNX SDP environment script not found"})
        return report
    report["sdk_root"] = str(sdk)
    report["checks"].append({"id":"sdk_root","status":"PASS","detail":"QNX SDP environment script found"})
    host = sdk/"host"/"win64"/"x86_64"
    qcc = host/"usr"/"bin"/("qcc.exe" if os.name=="nt" else "qcc")
    report["qcc"] = str(qcc)
    report["checks"].append({"id":"qcc_driver","status":"PASS" if qcc.is_file() and qcc.stat().st_size>0 else "FAIL",
      "detail":f"present={qcc.is_file()}, bytes={qcc.stat().st_size if qcc.exists() else 0}"})
    gccroot = host/"usr"/"lib"/"gcc"
    for arch, triplet in (("aarch64","aarch64-unknown-nto-qnx8.0.0"),("x86_64","x86_64-pc-nto-qnx8.0.0")):
        gccbase = gccroot/triplet/"12.2.0"
        cc1 = [p for p in gccbase.glob("cc1*") if p.is_file() and p.stat().st_size>0] if gccbase.exists() else []
        report["checks"].append({"id":f"{arch}_cc1","status":"PASS" if cc1 else "FAIL",
          "detail":f"non-empty compiler frontend found={bool(cc1)}"})
    headers = sdk/"target"/"qnx"/"usr"/"include"
    report["checks"].append({"id":"qnx_target_headers","status":"PASS" if headers.is_dir() else "FAIL",
      "detail":"QNX target headers directory"})
    report["status"] = "READY_FOR_BUILD" if all(c["status"]=="PASS" for c in report["checks"]) else "BLOCKED"
    return report

def build(arch):
    root=Path(__file__).resolve().parent
    src=root/"src"/"sae_qnx_probe.c"
    outdir=root/"build"; evdir=root/"evidence"
    outdir.mkdir(exist_ok=True); evdir.mkdir(exist_ok=True)
    report=inspect_sdk()
    (evdir/"environment-report.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    if report["status"]!="READY_FOR_BUILD":
        print("BUILD_BLOCKED: SDK validation failed; see evidence/environment-report.json")
        return 20
    target=TARGETS[arch]
    binary=outdir/(f"sae_qnx_probe_{arch}.exe" if os.name=="nt" else f"sae_qnx_probe_{arch}")
    if os.name=="nt":
        cmd=f'call "{Path(report["sdk_root"])/"qnxsdp-env.bat"}" >nul 2>&1 && qcc -V{target} -Wall -Wextra -o "{binary}" "{src}"'
        rc,out=run(cmd,timeout=120,shell=True)
    else:
        rc,out=run([report["qcc"],f"-V{target}","-Wall","-Wextra","-o",str(binary),str(src)],env=os.environ.copy(),timeout=120)
    (evdir/f"qcc-build-{arch}.log").write_text(out,encoding="utf-8")
    if rc or not binary.is_file() or binary.stat().st_size==0:
        print("BUILD_FAIL: compiler returned an error or produced no binary")
        print(out[-3000:])
        return 21
    if binary.read_bytes()[:4] != b"\x7fELF":
        print("BUILD_FAIL: output is not an ELF executable")
        return 22
    evidence={"schema":"sae-qnx-assurance-evidence-v1","tool_version":VERSION,
      "generated_utc":dt.datetime.now(dt.timezone.utc).isoformat(),
      "status":"CROSS_COMPILE_PASS_RUNTIME_NOT_TESTED",
      "target":f"QNX SDP 8.0 {arch} ({target})",
      "binary":{"path":str(binary.relative_to(root)),"bytes":binary.stat().st_size,"sha256":sha256(binary)},
      "environment_report":"evidence/environment-report.json"}
    (evdir/f"build-evidence-{arch}.json").write_text(json.dumps(evidence,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(evidence,indent=2))
    return 0

def self_test():
    assert TARGETS["aarch64"]=="gcc_ntoaarch64le"
    assert TARGETS["x86_64"]=="gcc_ntox86_64"
    assert len(sha256(Path(__file__)))==64
    assert inspect_sdk()["status"] in {"BLOCKED","READY_FOR_BUILD"}
    print("SELF_TEST_PASS: target mapping, SHA-256 and SDK inspection")
    return 0

def main():
    ap=argparse.ArgumentParser(description="Diagnose QNX SDP 8.0 and build auditable target evidence.")
    ap.add_argument("command",choices=["inspect","build","self-test"])
    ap.add_argument("--arch",choices=["aarch64","x86_64"],default="aarch64")
    a=ap.parse_args()
    if a.command=="inspect":
        r=inspect_sdk(); print(json.dumps(r,indent=2)); return 0 if r["status"]=="READY_FOR_BUILD" else 20
    if a.command=="build": return build(a.arch)
    return self_test()
if __name__=="__main__": raise SystemExit(main())
