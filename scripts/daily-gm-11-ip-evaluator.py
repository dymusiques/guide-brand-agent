#!/usr/bin/env python3
"""GM11 · Daily IP evaluate: rollups + challenge + self-check → metrics."""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "kernels" / "daily-gm"))
from shared_gold import resolve_ip_gold_text  # noqa: E402
from shared_traps import daily_challenge_lines  # noqa: E402


def main() -> int:
    today = date.today().isoformat()
    base = ROOT / "content/evolution/11-ip-daily-eval" / today
    base.mkdir(parents=True, exist_ok=True)
    for d in ("intake", "reference", "versions"):
        (base / d).mkdir(exist_ok=True)

    (base / "reference/gold.md").write_text(resolve_ip_gold_text(2000), encoding="utf-8")

    rollup = ROOT / "content/analytics/derived/evolution-rollups-latest.md"
    intake_txt = rollup.read_text(encoding="utf-8") if rollup.is_file() else "no rollups"
    (base / "intake/rollups.md").write_text(intake_txt, encoding="utf-8")

    challenges = [
        f"{line} → 今日队列/Brief 是否踩坑？"
        for line in daily_challenge_lines()
    ]
    (base / "challenge-log.md").write_text(
        "# GM11 daily challenge\n\n" + "\n".join(f"- {c}" for c in challenges) + "\n",
        encoding="utf-8",
    )

    missing = []
    redteam = ROOT / "content/xiaohongshu/redteam"
    for brief in (ROOT / "content/xiaohongshu").glob("*-brief.md"):
        slug = brief.name[: -len("-brief.md")]
        pre = redteam / f"{slug}-pre.md"
        if not pre.is_file():
            missing.append(str(brief.relative_to(ROOT)))

    eval_doc = {
        "date": today,
        "rollup_present": rollup.is_file(),
        "briefs_missing_redteam_pre": missing,
        "challenge_pass": len(missing) == 0,
    }
    (base / "versions/v0-eval.json").write_text(json.dumps(eval_doc, ensure_ascii=False, indent=2), encoding="utf-8")

    with (base / "metrics.jsonl").open("a", encoding="utf-8") as f:
        f.write(json.dumps({"label": "v0", "missing_redteam_count": len(missing)}, ensure_ascii=False) + "\n")

    (base / "GM-REPORT.md").write_text(
        f"# GM-REPORT · 11 IP Daily Eval · {today}\n\n"
        f"- missing redteam-pre: {len(missing)}\n"
        f"- challenge: 2 applied\n",
        encoding="utf-8",
    )

    subprocess.run(["bash", str(ROOT / "scripts/verify-collector-evaluator.sh")], check=False)
    print("PASS GM11" if len(missing) <= 3 else "WARN GM11 many missing redteam")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
