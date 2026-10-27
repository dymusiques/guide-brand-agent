#!/usr/bin/env python3
"""Screen artist-watchlist.json with DB/PLD/APO/CTD (heuristic; GM10 Gemini refines daily)."""

from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "kernels" / "daily-gm"))

from benchmark_framework import (  # noqa: E402
    METRIC_LABELS,
    composite_borrow_score,
    metrics_to_dict,
    screen_artist_heuristic,
    tier_from_composite,
)

WATCH = ROOT / "content/ip-research/artist-watchlist.json"
OUT_JSON = ROOT / "content/ip-research/artist-watchlist-screened.json"
OUT_MD = ROOT / "content/ip-research/artist-watchlist-screened.md"


def main() -> int:
    watch = json.loads(WATCH.read_text(encoding="utf-8"))
    artists = watch.get("artists") or []
    rows: list[dict] = []

    for a in artists:
        metrics = metrics_to_dict(screen_artist_heuristic(a))
        composite = composite_borrow_score(metrics)
        tier = tier_from_composite(composite)
        rows.append(
            {
                "slug": a.get("slug"),
                "name": a.get("name"),
                "urls": a.get("urls") or [],
                "priority_tier": tier,
                "borrow_score_composite": composite,
                "benchmark_metrics": metrics,
            }
        )

    rows.sort(key=lambda r: (-r["borrow_score_composite"], r.get("slug") or ""))

    out = {
        "framework": "DB+PLD+APO+CTD",
        "screened_at": date.today().isoformat(),
        "owner_direction_ref": watch.get("owner_baseline_ref"),
        "artists": rows,
    }
    OUT_JSON.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        f"# Artist watchlist screened · {out['screened_at']}",
        "",
        "> 指标：Directional Benchmarking · Pixel-Level Deconstruction · Audience Persona Overlap · Core Topic Density",
        "> 程序：`kernels/daily-gm/benchmark_framework.py` · 本表为 **启发式筛查**；GM10 日更 Gemini 可 override",
        "",
        "| tier | composite | slug | DB | PLD | APO | CTD | urls |",
        "|------|-----------|------|----|----|-----|-----|------|",
    ]
    for r in rows:
        m = r["benchmark_metrics"]
        urls = " · ".join(r["urls"][:2])
        if len(r["urls"]) > 2:
            urls += " …"
        lines.append(
            f"| {r['priority_tier']} | {r['borrow_score_composite']} | {r['slug']} | "
            f"{m['directional_benchmarking']['score']} | {m['pixel_level_deconstruction']['score']} | "
            f"{m['audience_persona_overlap']['score']} | {m['core_topic_density']['score']} | {urls} |"
        )
    lines.append("")
    lines.append("## Rationale per artist")
    lines.append("")
    for r in rows:
        lines.append(f"### {r['name']} (`{r['slug']}`) · {r['priority_tier']} · composite {r['borrow_score_composite']}")
        for mid, label in METRIC_LABELS.items():
            block = r["benchmark_metrics"][mid]
            lines.append(f"- **{label}** ({block['score']}): {block['rationale']}")
        lines.append("")

    OUT_MD.write_text("\n".join(lines), encoding="utf-8")

    tier_by_slug = {r["slug"]: r["priority_tier"] for r in rows}
    metrics_by_slug = {r["slug"]: r["benchmark_metrics"] for r in rows}
    composite_by_slug = {r["slug"]: r["borrow_score_composite"] for r in rows}
    for a in artists:
        sl = a.get("slug")
        if sl in tier_by_slug:
            a["priority_tier"] = tier_by_slug[sl]
            a["last_screened_composite"] = composite_by_slug[sl]
            a["last_screened_metrics"] = metrics_by_slug[sl]
    watch["screening_framework"] = "DB+PLD+APO+CTD"
    watch["last_screened_at"] = out["screened_at"]
    watch["artists"] = sorted(
        artists,
        key=lambda x: -composite_by_slug.get(x.get("slug") or "", 0),
    )
    WATCH.write_text(json.dumps(watch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"PASS: wrote {OUT_JSON.relative_to(ROOT)} ({len(rows)} artists)")
    print(f"PASS: updated {WATCH.relative_to(ROOT)} priority_tier + sort")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
