#!/usr/bin/env python3
"""Benchmark framework · 4 metrics + composite."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "kernels" / "daily-gm"))

from benchmark_framework import (  # noqa: E402
    composite_borrow_score,
    metrics_to_dict,
    screen_artist_heuristic,
    tier_from_composite,
    validate_benchmark_metrics,
)


def main() -> int:
    failed = 0
    bad = validate_benchmark_metrics({})
    if not bad:
        print("FAIL: empty metrics should error")
        failed += 1
    else:
        print("PASS: validate empty metrics")

    sample = {
        "directional_benchmarking": {"score": 80, "rationale": "x" * 20},
        "pixel_level_deconstruction": {"score": 70, "rationale": "y" * 20},
        "audience_persona_overlap": {"score": 60, "rationale": "z" * 20},
        "core_topic_density": {"score": 75, "rationale": "w" * 20},
    }
    c = composite_borrow_score(sample)
    if not (70 <= c <= 75):
        print(f"FAIL: composite {c}")
        failed += 1
    else:
        print(f"PASS: composite {c}")

    artist = {"slug": "grace-xhs-visual-ip", "domain": "绘画 × 小红书", "notes": "小红书", "urls": ["http://x"]}
    m = metrics_to_dict(screen_artist_heuristic(artist))
    if tier_from_composite(composite_borrow_score(m)) not in ("P1", "P2", "P3"):
        failed += 1
    else:
        print("PASS: heuristic screen grace")

    print(f"RESULT: {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
