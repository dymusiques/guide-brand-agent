#!/usr/bin/env python3
"""Fingerprint Drive「我的小红书数据」listing · 有变则可选 sync + 写 action-needed."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HANDOFF = ROOT / "integration/handoff/owner-xhs-data-drive.json"
FP = ROOT / "integration/handoff/owner-xhs-drive-watch-fingerprint.json"
LISTING = ROOT / "content/personal-ip/intake/_raw/owner-xhs-data/drive-listing-latest.json"
ACTION = ROOT / "content/evolution/00-manager/ceo-inbox/ceo-action-needed.md"
REFRESH = ROOT / "scripts/refresh-owner-xhs-drive-listing.py"


def fingerprint_listing(data: dict) -> str:
    parts = []
    for f in sorted(data.get("files") or [], key=lambda x: x.get("id") or ""):
        parts.append(f"{f.get('id')}|{f.get('modifiedTime')}|{f.get('size')}")
    raw = "\n".join(parts).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()[:24]


def append_action(line: str) -> None:
    ACTION.parent.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    block = f"\n- [{stamp}] {line}\n"
    if ACTION.is_file():
        ACTION.write_text(ACTION.read_text(encoding="utf-8") + block, encoding="utf-8")
    else:
        ACTION.write_text(f"# CEO action needed\n{block}", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sync", action="store_true", help="on change run sync-owner-xhs-data-from-drive.sh")
    ap.add_argument("--refresh", action="store_true", default=True, help="refresh listing first")
    args = ap.parse_args()

    py = ROOT / ".venv/bin/python3"
    if not py.is_file():
        py = Path(sys.executable)

    if args.refresh:
        r = subprocess.run([str(py), str(REFRESH)], cwd=ROOT, capture_output=True, text=True)
        if r.returncode != 0:
            print((r.stderr or r.stdout)[-500:], file=sys.stderr)
            return r.returncode

    if not LISTING.is_file():
        print("FAIL no drive-listing-latest.json", file=sys.stderr)
        return 2

    data = json.loads(LISTING.read_text(encoding="utf-8"))
    fp_new = fingerprint_listing(data)
    prev = {}
    if FP.is_file():
        prev = json.loads(FP.read_text(encoding="utf-8"))
    fp_old = prev.get("fingerprint")
    changed = fp_old is not None and fp_old != fp_new
    first_run = fp_old is None

    payload = {
        "as_of": datetime.now(timezone.utc).isoformat(),
        "fingerprint": fp_new,
        "previous_fingerprint": fp_old,
        "changed": changed,
        "file_count": data.get("file_count"),
        "listing": str(LISTING.relative_to(ROOT)),
    }
    FP.parent.mkdir(parents=True, exist_ok=True)
    FP.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    sync_ec = None
    if changed and args.sync:
        r = subprocess.run(
            ["bash", "scripts/sync-owner-xhs-data-from-drive.sh"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=600,
        )
        sync_ec = r.returncode
        append_action(
            "Drive 小红书数据文件夹有变更 · 已跑 sync-owner-xhs-data-from-drive"
            if r.returncode == 0
            else f"Drive 变更但 sync FAIL ec={r.returncode}"
        )
    elif changed:
        append_action("Drive「我的小红书数据」有变更 · Agent 应跑 sync-owner-xhs-data-from-drive.sh")

    if first_run:
        print(f"PASS drive-watch init fingerprint={fp_new} files={data.get('file_count')}")
        return 0
    if changed:
        print(f"PASS drive-watch CHANGED fingerprint={fp_new} sync_ec={sync_ec}")
        return 0
    print(f"PASS drive-watch unchanged fingerprint={fp_new}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())