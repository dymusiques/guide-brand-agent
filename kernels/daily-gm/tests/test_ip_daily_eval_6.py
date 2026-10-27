#!/usr/bin/env python3
"""GM11 IP daily eval · 6 schema/hygiene cases (L1)."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "kernels" / "daily-gm"))

from ip_daily_eval_schema import (  # noqa: E402
    validate_challenge_log,
    validate_eval_doc,
    validate_gold_reference,
)

EVAL_CASES = [
    ("正例 · 完整 eval", {
        "date": "2026-10-27",
        "rollup_present": True,
        "briefs_missing_redteam_pre": [],
        "challenge_pass": True,
    }, True),
    ("负例 · 缺 date", {
        "rollup_present": True,
        "briefs_missing_redteam_pre": [],
        "challenge_pass": True,
    }, False),
    ("负例 · missing 非 list", {
        "date": "2026-10-27",
        "rollup_present": True,
        "briefs_missing_redteam_pre": "x",
        "challenge_pass": True,
    }, False),
    ("边界 · challenge_pass false", {
        "date": "2026-10-27",
        "rollup_present": True,
        "briefs_missing_redteam_pre": ["a.md"],
        "challenge_pass": False,
    }, True),
]

OTHER_CASES = [
    ("负例 · rollup 未 present", lambda: validate_eval_doc({
        "date": "2026-10-27",
        "rollup_present": False,
        "briefs_missing_redteam_pre": [],
        "challenge_pass": True,
    }), False),
    ("challenge · 两条 X trap", lambda: validate_challenge_log(
        "# GM11\n\n- X9: a\n- X2: b\n"
    ), True),
]


def main() -> int:
    print("=== GM11 IP daily eval 6 cases ===\n")
    failed = 0
    for title, payload, want_pass in EVAL_CASES:
        errs = validate_eval_doc(payload)
        ok = not errs
        if ok != want_pass:
            print(f"  FAIL · {title}: expected pass={want_pass} got errs={errs}")
            failed += 1
        else:
            print(f"  PASS · {title}")

    for title, fn, want_pass in OTHER_CASES:
        errs = fn()
        ok = not errs
        if ok != want_pass:
            print(f"  FAIL · {title}: expected pass={want_pass} got errs={errs}")
            failed += 1
        else:
            print(f"  PASS · {title}")

    # gold hygiene (included in fused artifact check; one inline regression)
    g_errs = validate_gold_reference("x" * 100)
    if g_errs:
        print("  FAIL · gold sanity")
        failed += 1
    else:
        print("  PASS · gold sanity")

    total = len(EVAL_CASES) + len(OTHER_CASES) + 1
    print(f"\n=== Summary ===\n{total - failed} passed, {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
