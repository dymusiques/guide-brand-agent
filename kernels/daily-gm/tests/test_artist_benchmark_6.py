#!/usr/bin/env python3
"""GM10 artist benchmark · 6 schema/regression cases (L1)."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "kernels" / "daily-gm"))

from artist_benchmark_schema import validate_payload  # noqa: E402

SAMPLE_METRICS = {
    "directional_benchmarking": {"score": 70, "rationale": "跨界品牌与专业表演双轨并行，与 Owner 法派长笛×跨界策划战略方向同向。"},
    "pixel_level_deconstruction": {"score": 65, "rationale": "封面、标题钩子与栏目节奏可像素级拆解，迁移为听见 Daily+周更深度结构。"},
    "audience_persona_overlap": {"score": 60, "rationale": "品牌主与艺术爱好者有重叠，但须筛除纯 vanity 涨粉受众。"},
    "core_topic_density": {"score": 68, "rationale": "核心题集中在专业 moment 与跨界叙事，未锁死单一商品垂直。"},
}


def _base(**overrides):
    d = {
        "artist_slug": "a",
        "borrow_score": 72,
        "why_evaluate": "该艺术家以教育内容建立信任后再接品牌合作，与 Owner 认知期节奏接近，故给中等偏高借鉴分。",
        "alignment_points": ["认知先于转化", "跨界叙事", "强链接 CTA"],
        "timeline": [
            {"phase": "起步", "year_or_era": "Y1", "what_happened": "内容记录练习与审美"},
            {"phase": "转折", "year_or_era": "Y3", "what_happened": "首次品牌合作"},
            {"phase": "现状", "year_or_era": "Y5", "what_happened": "跨平台 IP 成型"},
        ],
        "benchmark_metrics": SAMPLE_METRICS,
    }
    d.update(overrides)
    return d


CASES = [
    ("正例 · 完整 JSON", _base(), True),
    ("负例 · 缺 timeline", _base(artist_slug="b", timeline=[]), False),
    ("负例 · 缺 benchmark_metrics", {k: v for k, v in _base().items() if k != "benchmark_metrics"}, False),
    ("负例 · 分超界", _base(artist_slug="c", borrow_score=150), False),
    ("负例 · 对齐点不足", _base(artist_slug="d", alignment_points=["one"]), False),
    ("边界 · 分 0", _base(
        artist_slug="e",
        borrow_score=0,
        why_evaluate="纯流量玩法与 Owner 强链接目标相反，借鉴分给 0。" + "补" * 20,
        alignment_points=["无", "无", "无"],
    ), True),
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
