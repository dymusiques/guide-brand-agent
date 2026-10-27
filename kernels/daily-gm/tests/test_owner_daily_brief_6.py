#!/usr/bin/env python3
"""GM12 Owner daily brief · 6 structure/hygiene cases (L1)."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "kernels" / "daily-gm"))

from owner_daily_brief_schema import validate_brief_gold, validate_brief_markdown  # noqa: E402

GOOD = """# Owner Daily Brief · 2026-10-27

> CEO 汇总

## Artist 对标（GM10）

_略_

## IP 自检（GM11）

- Brief 缺 redteam-pre：0 篇

## 今日派活建议（09→04）

dispatch excerpt

## 请你（仅决策）

- [ ] 今日 Artist 对标是否采纳进选题
"""

CASES = [
    ("正例 · 完整结构", GOOD, True),
    ("负例 · 缺 Artist", GOOD.replace("## Artist", "## NO"), False),
    ("负例 · 无决策勾", GOOD.replace("- [ ]", "- done"), False),
    ("负例 · 逼 Owner 跑 verify", GOOD + "\n## 请你（仅决策）\n\n请 bash scripts/verify-all\n", False),
    ("边界 · Artist 占位段", GOOD.replace("_略_", "_今日 GM10 未产出_"), True),
    (
        "gold rubric",
        "Owner daily brief must include: artist block OR reason skip, "
        "gm11 hygiene, dispatch excerpt, decision checkboxes\n",
        True,
    ),
]


def main() -> int:
    print("=== GM12 owner daily brief 6 cases ===\n")
    failed = 0
    for item in CASES:
        title, text, want_pass = item
        if title == "gold rubric":
            errs = validate_brief_gold(text)
        else:
            errs = validate_brief_markdown(text)
        ok = not errs
        if ok != want_pass:
            print(f"  FAIL · {title}: expected pass={want_pass} got errs={errs}")
            failed += 1
        else:
            print(f"  PASS · {title}")

    print(f"\n=== Summary ===\n{len(CASES) - failed} passed, {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
