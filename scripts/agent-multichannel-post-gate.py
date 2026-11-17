#!/usr/bin/env python3
"""Gate layer: LinkedIn/Medium inbox → ingest → evaluate → baseline (empty inbox = PASS)."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "integration/handoff/owner-multichannel-post-gate-latest.json"
LI_INBOX = ROOT / "content/analytics/linkedin/inbox"
MD_INBOX = ROOT / "content/analytics/medium/inbox"
PASS_THRESHOLD = 58


def needs_multichannel(goal: str) -> bool:
    g = (goal or "").casefold()
    return bool(
        re.search(
            r"linkedin|medium|领英|多平台|发帖数据|multichannel|复盘|已发|数据分析",
            g,
        )
    )


def pending_inbox_files() -> list[Path]:
    out: list[Path] = []
    for d in (LI_INBOX, MD_INBOX):
        if not d.is_dir():
            continue
        for p in d.glob("*"):
            if p.suffix.lower() not in {".md", ".json", ".csv"}:
                continue
            if p.name.upper().startswith("TEMPLATE"):
                continue
            out.append(p)
    return sorted(out)


def run_py(args: list[str], timeout: int = 120) -> tuple[int, str]:
    r = subprocess.run(args, cwd=ROOT, capture_output=True, text=True, timeout=timeout)
    return r.returncode, ((r.stdout or "") + (r.stderr or "")).strip()[-2000:]


def main() -> int:
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument("--goal", default="")
    ap.add_argument("--force", action="store_true", help="run even if goal lacks keywords")
    args = ap.parse_args()

    py = ROOT / ".venv/bin/python3"
    if not py.is_file():
        py = Path(sys.executable)

    if not args.force and not needs_multichannel(args.goal):
        payload = {
            "schema": "owner_multichannel_post_gate_v1",
            "as_of": datetime.now(timezone.utc).isoformat(),
            "status": "SKIP",
            "reason": "goal 未命中 multichannel 触发词",
        }
        OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(payload))
        return 0

    files = pending_inbox_files()
    steps: list[dict] = []
    fail = 0

    if not files:
        payload = {
            "schema": "owner_multichannel_post_gate_v1",
            "as_of": datetime.now(timezone.utc).isoformat(),
            "status": "PASS",
            "mode": "empty_inbox",
            "note_zh": "尚无 LinkedIn/Medium 数据文件 · 架构就绪 · 不阻塞 gate",
            "templates": [
                "content/analytics/linkedin/inbox/TEMPLATE-post-metrics.md",
                "content/analytics/medium/inbox/TEMPLATE-post-metrics.md",
            ],
            "steps": [],
        }
        OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({"status": "PASS", "mode": "empty_inbox"}))
        return 0

    for f in files:
        script = (
            "scripts/ingest-owner-linkedin-metrics.py"
            if "linkedin" in f.as_posix()
            else "scripts/ingest-owner-medium-metrics.py"
        )
        ec, tail = run_py([str(py), script, "--file", str(f.relative_to(ROOT))])
        steps.append({"ingest": f.name, "exit_code": ec, "tail": tail})
        if ec != 0:
            fail += 1

    ec, tail = run_py([str(py), "scripts/agent-multichannel-eval-baseline-loop.py"], timeout=180)
    steps.append({"multichannel_eval_loop": ec, "tail": tail})
    if ec != 0:
        fail += 1

    status = "PASS" if fail == 0 else "FAIL"
    payload = {
        "schema": "owner_multichannel_post_gate_v1",
        "as_of": datetime.now(timezone.utc).isoformat(),
        "status": status,
        "files": [str(p.relative_to(ROOT)) for p in files],
        "pass_threshold": PASS_THRESHOLD,
        "steps": steps,
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": status, "fail": fail}))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())