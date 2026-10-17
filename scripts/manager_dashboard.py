#!/usr/bin/env python3
"""00 Manager CEO dashboard — one-page status for Owner + Agent."""

from __future__ import annotations

import json
import re
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DERIVED = ROOT / "content/analytics/derived"
INBOX = ROOT / "content/analytics/inbox"
XHS = ROOT / "content/xiaohongshu"
MARKETING = ROOT / "content/marketing"
BUSINESS = ROOT / "content/business-brand"
STATE = DERIVED / ".manager-dashboard-state.json"
GOALS = ROOT / "integration/goals/registry.json"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.is_file() else ""


def _brief_aligned(text: str) -> bool:
    return "aligned: true" in text or "aligned: true" in text.replace("**", "")


def _brief_published(text: str) -> tuple[str, str | None, str | None]:
    """Returns status, publish_date, note_url."""
    if m := re.search(r"发布日期[：:]\s*(\d{4}-\d{2}-\d{2})", text):
        pub_date = m.group(1)
        url = None
        if u := re.search(r"笔记链接[：:]\s*(https?://\S+)", text):
            url = u.group(1).rstrip(")")
        return "已发布", pub_date, url
    if re.search(r"状态[：:]\s*已发布", text):
        return "已发布", None, None
    return "待发", None, None


def _discovery_briefs() -> list[dict]:
    rows = []
    for path in sorted(XHS.glob("*discovery*-brief.md")):
        text = _read(path)
        st, pd, url = _brief_published(text)
        rows.append(
            {
                "file": path.name,
                "aligned": _brief_aligned(text),
                "publish_status": st,
                "publish_date": pd,
                "note_url": url,
            }
        )
    return rows


def _inbox_status() -> tuple[int, list[str]]:
    files = [
        p.name
        for p in INBOX.glob("*")
        if p.is_file() and p.suffix.lower() in (".csv", ".tsv") and not p.name.startswith(".")
    ]
    return len(files), files[:5]


def _latest_derived() -> tuple[str | None, str | None]:
    topics = sorted(DERIVED.glob("next-topics-*.md"), reverse=True)
    summary = sorted(DERIVED.glob("summary-*.json"), reverse=True)
    return (
        topics[0].name if topics else None,
        summary[0].name if summary else None,
    )


def _fifteen_day_hint(briefs: list[dict]) -> str:
    dates = [b["publish_date"] for b in briefs if b.get("publish_date")]
    if not dates:
        return "尚未记录首发「发布日期」→ 发 Brief #1 后在 md 里填 ## 发布状态（见模板）"
    first = min(dates)
    try:
        d0 = datetime.strptime(first, "%Y-%m-%d").date()
    except ValueError:
        return f"发布日期格式需 YYYY-MM-DD（当前: {first}）"
    due = d0 + timedelta(days=15)
    today = date.today()
    if today < due:
        return f"15 天快检日: {due.isoformat()}（首发 {first}，还剩 {(due - today).days} 天）"
    if today == due:
        return f"**今天 = 15 天快检**（首发 {first}）→ 对照 OPERATING-PLAN §2.1"
    return f"15 天快检已到期（{due.isoformat()}）→ 请做快检并反馈 Agent"


def _load_state() -> dict:
    if STATE.is_file():
        try:
            return json.loads(STATE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            pass
    return {}


def _goal_ids() -> list[str]:
    if not GOALS.is_file():
        return []
    data = json.loads(GOALS.read_text(encoding="utf-8"))
    return [g["id"] for g in data.get("owner_goals", [])]


def build_markdown() -> str:
    briefs = _discovery_briefs()
    inbox_n, inbox_sample = _inbox_status()
    next_md, sum_json = _latest_derived()
    state = _load_state()
    lines = [
        "# 00 Manager · CEO 仪表盘",
        "",
        f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "## 认知期深度 Brief（discovery 队列）",
        "",
        "| # | 文件 | evaluate | 发布 | 发布日期 |",
        "|---|------|----------|------|----------|",
    ]
    for i, b in enumerate(briefs, 1):
        al = "✅ aligned" if b["aligned"] else "❌ 未过/待跑"
        lines.append(
            f"| {i} | `{b['file']}` | {al} | {b['publish_status']} | {b['publish_date'] or '—'} |"
        )
    if not briefs:
        lines.append("| — | 无 discovery brief | — | — | — |")

    lines.extend(
        [
            "",
            "## 15 天快检",
            "",
            _fifteen_day_hint(briefs),
            "",
            "## 数据 · 09",
            "",
            f"- inbox CSV 文件数: **{inbox_n}**"
            + (f"（例: {', '.join(inbox_sample)}）" if inbox_sample else " → 建议导出进 `content/analytics/inbox/`"),
            f"- 最新 next-topics: `{next_md or '无（跑 analytics-pipeline）'}`",
            f"- 最新 summary: `{sum_json or '无'}`",
            "",
            "## 战略文档",
            "",
            f"- 触达计划: `content/marketing/2026-10-brand-discovery-phase.md`",
            f"- SWOT: `content/business-brand/2026-10-17-brand-positioning-swot.md`",
            f"- 队列: `content/marketing/discovery-phase-note-queue.md`",
            "",
            "## Goal Registry（摘要）",
            "",
            ", ".join(_goal_ids()) or "（未读到 registry）",
            "",
            "## 集成构建",
            "",
        ]
    )
    if lv := state.get("last_verify_all"):
        lines.append(f"- 上次 verify-all: **{lv.get('tier', '?')}** · {lv.get('at', '?')} · {lv.get('result', '?')}")
    else:
        lines.append("- 上次 verify-all: 未记录 → 交班前跑 `VERIFY_TIER=release bash scripts/verify-all.sh`")

    lines.extend(
        [
            "",
            "## 建议下一步（00 派活）",
            "",
        ]
    )
    next_actions = []
    for b in briefs:
        if b["aligned"] and b["publish_status"] == "待发":
            next_actions.append(f"Owner 发布 `{b['file']}`（见 PUBLISH-AND-DATA-CHECKLIST.md）")
            break
    if inbox_n == 0:
        next_actions.append("导出小红书 CSV → inbox → `bash scripts/analytics-pipeline.sh`")
    if not next_actions:
        next_actions.append("维持 Daily + 按队列发下一篇；15 天/轮检对照 OPERATING-PLAN")
    for a in next_actions:
        lines.append(f"- {a}")

    lines.append("")
    lines.append("---")
    lines.append("刷新: `bash scripts/manager-dashboard.sh`")
    return "\n".join(lines)


def main() -> int:
    md = build_markdown()
    DERIVED.mkdir(parents=True, exist_ok=True)
    out = DERIVED / f"manager-dashboard-{date.today().isoformat()}.md"
    out.write_text(md, encoding="utf-8")
    print(md)
    print("")
    print(f"（已写入 {out.relative_to(ROOT)}）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
