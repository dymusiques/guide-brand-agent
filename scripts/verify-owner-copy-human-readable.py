#!/usr/bin/env python3
"""Fail if Owner-facing copy contains Agent scaffold (L1/锚点/YAML), not human prose."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from xhs_brief_longform import extract_longform_text, looks_like_agent_scaffold, strip_owner_facing_md  # noqa: E402

BANNED = re.compile(
    r"(## L1 任务|## 章节锚点|context_version|openwebui_route|"
    r"文章锚点|正文有没有|xhs-classifier|content_sha256)"
)


def check_text(label: str, text: str) -> list[str]:
    fails: list[str] = []
    if not text.strip():
        fails.append(f"{label}: empty")
        return fails
    if BANNED.search(text):
        fails.append(f"{label}: contains Agent scaffold (L1/锚点/YAML/classifier)")
    if looks_like_agent_scaffold(text[:1200]):
        fails.append(f"{label}: reads like repo metadata, not publishable copy")
    cjk = len(re.findall(r"[\u4e00-\u9fff]", text))
    if cjk < 80:
        fails.append(f"{label}: too short for longform ({cjk} CJK chars)")
    return fails


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--brief", action="append", default=[], help="XHS brief path(s)")
    p.add_argument("--md", action="append", default=[], help="Extra markdown paths")
    args = p.parse_args()
    fails: list[str] = []
    for b in args.brief:
        path = ROOT / b if not b.startswith("/") else Path(b)
        longform = extract_longform_text(path)
        if longform:
            fails.extend(check_text(path.name, longform))
        else:
            raw = path.read_text(encoding="utf-8") if path.is_file() else ""
            fails.extend(check_text(path.name, strip_owner_facing_md(raw)))
    for m in args.md:
        path = ROOT / m if not m.startswith("/") else Path(m)
        if path.is_file():
            fails.extend(check_text(path.name, strip_owner_facing_md(path.read_text(encoding="utf-8"))))
    if fails:
        for f in fails:
            print(f"FAIL: {f}")
        print("HINT: see integration/handoff/owner-copy-benchmarks-tier2.json · docs/OWNER-COPY-BENCHMARKS-TIER2.md")
        return 1
    print("PASS verify-owner-copy-human-readable")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
