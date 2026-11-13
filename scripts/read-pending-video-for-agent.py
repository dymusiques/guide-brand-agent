#!/usr/bin/env python3
"""单条口播全文结构化输出（给 Agent 定向核对）。决策须与 facts manifest 一致."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INBOX = ROOT / "content/xiaohongshu/inbox/pending-videos"

from pending_video_md_lib import parse_pending_video  # noqa: E402


def resolve_path(arg: str) -> Path:
    p = Path(arg)
    if p.is_file():
        return p
    p2 = INBOX / arg
    if p2.is_file():
        return p2
    p3 = INBOX / f"{arg}.md"
    if p3.is_file():
        return p3
    raise FileNotFoundError(arg)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("file", nargs="?", help="inbox 下的 .md 或 stem")
    ap.add_argument("--all", action="store_true", help="输出全 inbox JSON")
    ap.add_argument("--gate", action="store_true", help="跑硬门禁（推荐给建议前）")
    args = ap.parse_args()

    if args.gate:
        import subprocess

        cmd = [sys.executable, str(ROOT / "scripts/agent-gate-pending-videos-advice.py")]
        if args.file and not args.all:
            cmd.extend(["--files", args.file])
        return subprocess.call(cmd, cwd=ROOT)

    if args.all:
        skip = {"readme.md", "template.md"}
        items = [
            parse_pending_video(p, ROOT)
            for p in sorted(INBOX.glob("*.md"))
            if p.name.lower() not in skip
        ]
        print(json.dumps({"items": items}, ensure_ascii=False, indent=2))
        return 0

    if not args.file:
        ap.error("需要 file 或 --all 或 --gate")

    item = parse_pending_video(resolve_path(args.file), ROOT)
    print("Agent 须基于【全文解析】再给建议；禁止仅用开头/ preview。")
    print(json.dumps(item, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
