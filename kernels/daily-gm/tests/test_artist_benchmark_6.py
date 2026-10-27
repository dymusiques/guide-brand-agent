#!/usr/bin/env python3
"""GM10 artist benchmark · 6 schema/regression cases (L1)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "kernels" / "daily-gm"))

from artist_benchmark_schema import validate_payload  # noqa: E402

CASES = [
    ("正例 · 完整 JSON", {
        "artist_slug": "a",
        "borrow_score": 72,
        "why_evaluate": "该艺术家以教育内容建立信任后再接品牌合作，与 Owner 认知期节奏接近，故给中等偏高借鉴分。",
        "alignment_points": ["认知先于转化", "跨界叙事", "强链接 CTA"],
        "timeline": [
            {"phase": "起步", "year_or_era": "Y1", "what_happened": "内容记录练习与审美"},
            {"phase": "转折", "year_or_era": "Y3", "what_happened": "首次品牌合作"},
            {"phase": "现状", "year_or_era": "Y5", "what_happened": "跨平台 IP 成型"},
        ],
    }, True),
    ("负例 · 缺 timeline", {
        "artist_slug": "b",
        "borrow_score": 50,
        "why_evaluate": "x" * 40,
        "alignment_points": ["a", "b", "c"],
        "timeline": [],
    }, False),
    ("负例 · 分超界", {
        "artist_slug": "c",
        "borrow_score": 150,
        "why_evaluate": "y" * 40,
        "alignment_points": ["a", "b", "c"],
        "timeline": [
            {"phase": "a", "year_or_era": "1", "what_happened": "x"},
            {"phase": "b", "year_or_era": "2", "what_happened": "x"},
            {"phase": "c", "year_or_era": "3", "what_happened": "x"},
        ],
    }, False),
    ("负例 · 对齐点不足", {
        "artist_slug": "d",
        "borrow_score": 30,
        "why_evaluate": "z" * 40,
        "alignment_points": ["one"],
        "timeline": [
            {"phase": "a", "year_or_era": "1", "what_happened": "x"},
            {"phase": "b", "year_or_era": "2", "what_happened": "x"},
            {"phase": "c", "year_or_era": "3", "what_happened": "x"},
        ],
    }, False),
    ("边界 · 分 0", {
        "artist_slug": "e",
        "borrow_score": 0,
        "why_evaluate": "纯流量玩法与 Owner 强链接目标相反，借鉴分给 0。" + "补" * 20,
        "alignment_points": ["无", "无", "无"],
        "timeline": [
            {"phase": "a", "year_or_era": "?", "what_happened": "unknown"},
            {"phase": "b", "year_or_era": "?", "what_happened": "unknown"},
            {"phase": "c", "year_or_era": "?", "what_happened": "unknown"},
        ],
    }, True),
    ("歧义 · 短 why", {
        "artist_slug": "f",
        "borrow_score": 55,
        "why_evaluate": "太短",
        "alignment_points": ["a", "b", "c"],
        "timeline": [
            {"phase": "a", "year_or_era": "1", "what_happened": "x"},
            {"phase": "b", "year_or_era": "2", "what_happened": "x"},
            {"phase": "c", "year_or_era": "3", "what_happened": "x"},
        ],
    }, False),
]


def main() -> int:
    print("=== GM10 artist benchmark 6 cases ===\n")
    failed = 0
    for title, payload, want_pass in CASES:
        errs = validate_payload(payload)
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
