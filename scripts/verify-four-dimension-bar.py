#!/usr/bin/env python3
"""CEO verified test for the four 100-point dimensions.

Contract always runs. If a three-platform folder has linkedin.html, its
four-dimensions.json must show angle, hit, voice, and cite each >= 80,
and the LinkedIn body must contain exactly two indexed sources.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from integration.agents._four_dimensions import case_four_dimension_contract  # noqa: E402

FOLDER = ROOT / "content/evolution/00-manager/ceo-inbox/2026-11-03-artists-three"
PASS = 80


def main() -> int:
    ok, detail = case_four_dimension_contract()
    print(("PASS" if ok else "FAIL") + f" · contract · {detail}")
    if not ok:
        return 1
    html = FOLDER / "linkedin.html"
    report_path = FOLDER / "four-dimensions.json"
    if not html.is_file():
        print("PASS · no current three-platform draft to score")
        return 0
    if not report_path.is_file():
        print("FAIL · linkedin draft exists but four-dimensions.json is missing")
        return 1
    report = json.loads(report_path.read_text(encoding="utf-8"))
    failed = 0
    for name, item in (report.get("platforms") or {}).items():
        four = item.get("four") or {}
        for key in ("angle", "hit", "voice", "cite"):
            score = int(four.get(key) or 0)
            if score < PASS:
                print(f"FAIL · {name} {key} {score} < {PASS}")
                failed += 1
        stress = item.get("stress") or {}
        for key in ("voice", "angle_senior"):
            if key in stress and int(stress[key]) < PASS:
                print(f"FAIL · {name} stress {key} {stress[key]} < {PASS}")
                failed += 1
    if failed:
        return 1
    print("PASS · four dimensions >= 80")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
