#!/usr/bin/env python3
"""Create a SHA-256 inventory of source, documentation and evidence files."""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "evidence" / "manifest.json"
EXCLUDED_DIRS = {".git", "__pycache__", "build"}
EXCLUDED_FILES = {"manifest.json"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    source = (ROOT / "sae_qnx_assurance.py").read_text(encoding="utf-8")
    match = re.search(r'^VERSION\s*=\s*"([^"]+)"', source, re.MULTILINE)
    version = match.group(1) if match else "unknown"

    files = []
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or path.name in EXCLUDED_FILES:
            continue
        relative = path.relative_to(ROOT)
        if any(part in EXCLUDED_DIRS for part in relative.parts):
            continue
        if path.suffix in {".pyc", ".pyo"}:
            continue
        files.append(
            {
                "path": relative.as_posix(),
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
        )

    manifest = {
        "schema": "sae-qnx-source-evidence-manifest-v1",
        "project": "SAE QNX Assurance Bridge",
        "version": version,
        "generated_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "scope": "source, tests, documentation and evidence; generated build binaries excluded",
        "file_count": len(files),
        "files": files,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"MANIFEST_PASS: {len(files)} files -> {OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
