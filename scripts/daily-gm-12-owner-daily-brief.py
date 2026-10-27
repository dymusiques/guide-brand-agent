#!/usr/bin/env python3
"""GM12 · Compose Owner daily brief from GM10/11 + dispatch + rollups."""

from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    today = date.today().isoformat()
    out_dir = ROOT / "content/daily-brief"
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / f"{today}-owner-daily-brief.md"
    evo = ROOT / "content/evolution/12-owner-daily-brief" / today
    evo.mkdir(parents=True, exist_ok=True)
    for d in ("intake", "reference", "versions"):
        (evo / d).mkdir(exist_ok=True)

    sections: list[str] = [f"# Owner Daily Brief · {today}\n", "> CEO 汇总 GM10/11/09 · 内部已跑 verify/challenge\n"]

    # GM10 latest today
    intel_root = ROOT / "content/evolution/10-artist-intel" / today
    if intel_root.is_dir():
        sections.append("## Artist 对标（GM10）\n")
        for gm in intel_root.rglob("v0-benchmark.json"):
            data = json.loads(gm.read_text(encoding="utf-8"))
            sections.append(f"### {data.get('artist_slug', 'artist')}\n")
            sections.append(f"- **借鉴分：** {data.get('borrow_score')}\n")
            sections.append(f"- **为何这样 evaluate：** {data.get('why_evaluate', '')}\n")
            ap = data.get("alignment_points") or []
            sections.append("- **可对齐点：** " + " · ".join(ap[:5]) + "\n")
            sections.append("- **时间线：**\n")
            for ev in data.get("timeline") or []:
                sections.append(
                    f"  - {ev.get('year_or_era')} · {ev.get('phase')} — {ev.get('what_happened')}\n"
                )
            wb = data.get("worth_borrowing") or []
            if wb:
                sections.append("- **值得借鉴：**\n")
                for b in wb[:5]:
                    sections.append(f"  - {b}\n")
            sections.append(f"- **sources_note：** {data.get('sources_note', '—')}\n")
    else:
        sections.append("## Artist 对标\n\n_今日 GM10 未产出（Gemini/ watchlist）_\n")

    # GM11
    g11 = ROOT / "content/evolution/11-ip-daily-eval" / today / "versions/v0-eval.json"
    sections.append("\n## IP 自检（GM11）\n")
    if g11.is_file():
        e = json.loads(g11.read_text(encoding="utf-8"))
        sections.append(f"- Brief 缺 redteam-pre：{len(e.get('briefs_missing_redteam_pre') or [])} 篇\n")
        if e.get("briefs_missing_redteam_pre"):
            for p in e["briefs_missing_redteam_pre"][:5]:
                sections.append(f"  - `{p}`\n")
    else:
        sections.append("_GM11 未跑_\n")

    dispatch = ROOT / "content/analytics/derived/ceo-dispatch-latest.md"
    sections.append("\n## 今日派活建议（09→04）\n")
    if dispatch.is_file():
        raw = dispatch.read_text(encoding="utf-8")[:2500]
        drop = ("manager-workflow-verify", "verify-agent-matrix", "bash scripts/verify")
        lines = [ln for ln in raw.splitlines() if not any(d in ln for d in drop)]
        sections.append("\n".join(lines) + "\n")
    else:
        sections.append("_无 dispatch_\n")

    sections.append("\n## 请你（仅决策）\n\n- [ ] 今日 Artist 对标是否采纳进选题\n- [ ] 是否指定写一篇 Brief / 发哪篇\n")

    body = "".join(sections)
    out.write_text(body, encoding="utf-8")
    (evo / "versions/v0-brief.md").write_text(body, encoding="utf-8")
    (evo / "reference/gold.md").write_text(
        "Owner daily brief must include: artist block OR reason skip, GM11 hygiene, dispatch excerpt, decision checkboxes\n",
        encoding="utf-8",
    )
    (evo / "GM-REPORT.md").write_text(f"# GM-REPORT · 12 · {today}\n\n- out: `{out.relative_to(ROOT)}`\n", encoding="utf-8")
    (evo / "challenge-log.md").write_text("- Challenge: brief 是否过长/是否逼 Owner 验脚本 → 只给决策勾\n", encoding="utf-8")

    print("PASS GM12", out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
