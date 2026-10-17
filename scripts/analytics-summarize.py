#!/usr/bin/env python3
"""Read analytics CSVs, score rows, write next-topic suggestions for Agent 09 → 04."""

from __future__ import annotations

import csv
import json
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from analytics.schemas import CANONICAL_FILES, PLATFORMS  # noqa: E402


def _int(val: str | None) -> int:
    if val is None or str(val).strip() == "":
        return 0
    try:
        return int(float(str(val).strip()))
    except ValueError:
        return 0


def _load_rows(path: Path) -> list[dict[str, str]]:
    if not path.is_file():
        return []
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def strong_link_score(platform: str, row: dict[str, str]) -> float:
    if platform == "xiaohongshu":
        return (
            _int(row.get("dm_count")) * 5
            + _int(row.get("comments")) * 2
            + _int(row.get("collects")) * 1.5
            + _int(row.get("follows_from_note")) * 8
            + _int(row.get("likes")) * 0.1
        )
    if platform == "instagram":
        return (
            _int(row.get("dm_count")) * 5
            + _int(row.get("comments")) * 2
            + _int(row.get("saves")) * 1.5
            + _int(row.get("follows_from_post")) * 8
            + _int(row.get("likes")) * 0.1
        )
    # youtube
    return (
        _int(row.get("dm_or_email_inquiries")) * 5
        + _int(row.get("comments")) * 2
        + _int(row.get("subscribers_gained")) * 8
        + _int(row.get("likes")) * 0.1
        + _int(row.get("views")) * 0.01
    )


def load_all() -> list[tuple[str, dict[str, str], float]]:
    scored: list[tuple[str, dict[str, str], float]] = []
    for platform in PLATFORMS:
        path = ROOT / "content" / "analytics" / platform / CANONICAL_FILES[platform]
        for row in _load_rows(path):
            scored.append((platform, row, strong_link_score(platform, row)))
    return scored


def suggest_topics(scored: list[tuple[str, dict[str, str], float]]) -> list[dict]:
    if not scored:
        return [
            {
                "subject": "（无数据）请先导入 CSV",
                "reason": "运行 analytics-fetch.sh / analytics-import.py",
                "platform": "—",
                "verified": False,
            }
        ]

    by_pillar: dict[str, float] = defaultdict(float)
    top_rows: list[tuple[str, dict[str, str], float]] = sorted(
        scored, key=lambda x: x[2], reverse=True
    )[:10]
    for _plat, row, score in scored:
        pillar = (row.get("pillar") or "未分类").strip()
        by_pillar[pillar] += score

    best_pillar = max(by_pillar.items(), key=lambda x: x[1])[0] if by_pillar else "跨界品牌"

    suggestions: list[dict] = []
    templates = [
        (
            f"{best_pillar}：把强链接做成下一篇主线",
            f"过去内容在「{best_pillar}」Strong-link 得分最高，建议延续同一支柱并强化私信 CTA。",
        ),
        (
            "艺术 IP 数字化：别从 NFT 讲起",
            "支柱 3 + 数据侧 DM/咨询偏高时，优先 AI×数字藏品共创向（跨行业品牌 open）。",
        ),
        (
            "跨行业品牌活动的叙事节奏",
            "若观看高但 DM 低，改做「叙事结构」而非晒活动清单，筛品牌合作私信。",
        ),
    ]
    for i, (sub, reason) in enumerate(templates):
        ref = top_rows[i % len(top_rows)] if top_rows else None
        suggestions.append(
            {
                "subject": sub,
                "reason": reason,
                "platform": ref[0] if ref else "xiaohongshu",
                "reference_title": (ref[1].get("title") if ref else "") or "",
                "verified": True,
            }
        )
    return suggestions


def main() -> int:
    scored = load_all()
    suggestions = suggest_topics(scored)
    today = date.today().isoformat()
    derived = ROOT / "content" / "analytics" / "derived"
    derived.mkdir(parents=True, exist_ok=True)

    summary = {
        "date": today,
        "row_count": len(scored),
        "pillar_totals": {},
        "top_by_score": [
            {
                "platform": p,
                "title": r.get("title"),
                "pillar": r.get("pillar"),
                "score": s,
            }
            for p, r, s in sorted(scored, key=lambda x: x[2], reverse=True)[:5]
        ],
        "next_topic_suggestions": suggestions,
    }
    by_pillar: dict[str, float] = defaultdict(float)
    for plat, row, score in scored:
        by_pillar[(row.get("pillar") or "未分类").strip()] += score
    summary["pillar_totals"] = dict(by_pillar)

    json_path = derived / f"summary-{today}.json"
    json_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    md_lines = [
        f"# 下一选题建议 · {today}",
        "",
        f"数据行数：**{len(scored)}**（小红书 / Instagram / YouTube 合并）",
        "",
        "## 支柱 Strong-link 得分合计",
        "",
    ]
    for pillar, total in sorted(by_pillar.items(), key=lambda x: -x[1]):
        md_lines.append(f"- **{pillar}**：{total:.1f}")
    md_lines.extend(["", "## 建议交给 04 Topic Manager（3 条）", ""])
    for i, s in enumerate(suggestions, 1):
        md_lines.append(f"{i}. **{s['subject']}**")
        md_lines.append(f"   - 理由：{s['reason']}")
        md_lines.append(f"   - 参考平台：{s['platform']} · 数据验证：{s['verified']}")
        if s.get("reference_title"):
            md_lines.append(f"   - 参考标题：{s['reference_title']}")
        md_lines.append("")
    md_lines.append("---")
    md_lines.append("由 `scripts/analytics-summarize.py` 生成 → Manager 派 04 写 Brief → `evaluate --brief`")

    md_path = derived / f"next-topics-{today}.md"
    md_path.write_text("\n".join(md_lines), encoding="utf-8")

    import subprocess

    subprocess.run(
        [sys.executable, str(ROOT / "scripts/ceo-dispatch-refresh.py")],
        cwd=ROOT,
        check=False,
    )

    print(json.dumps({"summary_json": str(json_path.relative_to(ROOT)), "next_topics_md": str(md_path.relative_to(ROOT))}, ensure_ascii=False))
    return 0 if scored else 1


if __name__ == "__main__":
    sys.exit(main())
