#!/usr/bin/env python3
"""CI: orchestration 默认 B/C 档（方案 1）。"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    fail = 0
    sys.path.insert(0, str(ROOT / "scripts"))
    from gate_ceo_orchestration import orchestration_mode  # noqa: E402

    g_replay = "已发世界不需要这么多艺术家监督补全"
    if orchestration_mode(goal=g_replay) != "evaluate_post_gate":
        print(f"FAIL: supervision should be evaluate_post_gate, got {orchestration_mode(goal=g_replay)!r}", file=sys.stderr)
        fail += 1
    g_copy = "下一篇小红书笔记写稿"
    if orchestration_mode(goal=g_copy) != "copy_ceo_full":
        print("FAIL: 写稿 should be copy_ceo_full", file=sys.stderr)
        fail += 1
    g_both = "已发复盘并写下一篇口播文案"
    if orchestration_mode(goal=g_both) != "copy_ceo_full":
        print("FAIL: 复盘+写稿 should prefer copy_ceo_full", file=sys.stderr)
        fail += 1
    bundle = ROOT / "scripts/ceo-evaluate-post-gate-bundle.py"
    if not bundle.is_file():
        print("FAIL: missing ceo-evaluate-post-gate-bundle.py", file=sys.stderr)
        fail += 1
    if fail:
        return 1
    print("PASS verify-orchestration-modes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())