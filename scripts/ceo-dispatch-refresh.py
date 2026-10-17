#!/usr/bin/env python3
"""09 → 04 CEO 派活块：从 derived next-topics + 待发 Brief 写 ceo-dispatch-latest.md."""

from __future__ import annotations

import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DERIVED = ROOT / "content/analytics/derived"
XHS = ROOT / "content/xiaohongshu"
QUEUE = ROOT / "content/marketing/discovery-phase-note-queue.md"


def _read(p: Path) -> str:
    return p.read_text(encoding="utf-8") if p.is_file() else ""


def _next_unpublished_brief() -> Path | None:
    for path in sorted(XHS.glob("*discovery*-brief.md")):
        text = _read(path)
        if re.search(r"状态[：:]\s*已发布", text):
            continue
        if re.search(r"发布日期[：:]\s*\d{4}-\d{2}-\d{2}", text):
            continue
        return path
    return None


def _latest_next_topics() -> Path | None:
    files = sorted(DERIVED.glob("next-topics-*.md"))
    return files[-1] if files else None


def main() -> int:
    today = date.today().isoformat()
    brief = _next_unpublished_brief()
    topics = _latest_next_topics()
    topics_body = _read(topics) if topics else "（尚无 next-topics — 跑 analytics-pipeline 或 --demo）"

    lines = [
        "# CEO 派活块 · 00 Manager → 04 Topic Manager",
        "",
        f"生成日：**{today}** · `scripts/ceo-dispatch-refresh.py`",
        "",
        "## Owner 边界（本块不代做）",
        "",
        "- **发帖**：小红书 / 其他平台由 Owner 操作",
        "- **数据**：CSV 放入 `content/analytics/inbox/`",
        "",
        "## 当前执行优先级",
        "",
    ]
    if brief:
        title = ""
        if m := re.search(r"^#\s+(.+)$", _read(brief), re.M):
            title = m.group(1).strip()
        lines.extend(
            [
                f"1. **定稿 / 视觉 / 发帖**：`{brief.relative_to(ROOT)}`",
                f"   - 标题：{title or '见 Brief'}",
                "   - 发帖后回填 Brief `## 发布状态`",
                "",
                "2. **04 下一 Brief**：见下方「数据选题」或 `discovery-phase-note-queue.md`",
                "",
            ]
        )
    else:
        lines.extend(
            [
                "1. 认知期 Brief 队列已发完或均已标记发布 — 请 04 开新选题",
                "",
            ]
        )

    lines.extend(
        [
            "## 数据选题（09 → 04）",
            "",
            f"来源：`{topics.relative_to(ROOT) if topics else '—'}`",
            "",
            topics_body,
            "",
            "## 派活口令（粘贴给 Agent / 04）",
            "",
            "```",
            "读 agents/00-manager/AUTO-WORKFLOW.md；",
            "若 Owner 未指定 Brief：优先处理 ceo-dispatch-latest 中「当前执行优先级」；",
            "写/改 Brief 后：bash scripts/manager-workflow-verify.sh content/xiaohongshu/<brief>.md",
            "```",
            "",
            "---",
            f"队列参考：`{QUEUE.relative_to(ROOT)}`",
        ]
    )

    out = DERIVED / "ceo-dispatch-latest.md"
    DERIVED.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines), encoding="utf-8")
    print(str(out.relative_to(ROOT)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
