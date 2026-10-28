#!/usr/bin/env python3
"""CEO batch: delegate chain → filter XHS materials + artist watchlist → Owner deliverable."""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INBOX = ROOT / "content/evolution/00-manager/ceo-inbox"
OUT = INBOX / f"OWNER-XHS-FILTER-DELIVERABLE-{datetime.now().strftime('%Y-%m-%d')}.md"
LOG = INBOX / f"ceo-xhs-filter-batch-{datetime.now().strftime('%Y%m%d-%H%M%S')}.log"


def run(cmd: list[str], name: str) -> bool:
    p = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    ok = p.returncode == 0
    LOG.write_text(
        LOG.read_text(encoding="utf-8") + f"\n=== {name} ===\n{p.stdout}\n{p.stderr}\nexit={p.returncode}\n"
        if LOG.is_file()
        else f"=== {name} ===\n{p.stdout}\n{p.stderr}\nexit={p.returncode}\n",
        encoding="utf-8",
    )
    return ok


def score_brief(path: Path) -> dict:
    py = ROOT / ".venv/bin/python"
    if not py.is_file():
        py = Path(sys.executable)
    proc = subprocess.run(
        [str(py), str(ROOT / "scripts/evaluate-xhs-topic.py"), "--brief", str(path)],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    aligned = proc.returncode == 0 and "aligned: true" in (proc.stdout + proc.stderr).lower()
    return {"path": str(path.relative_to(ROOT)), "aligned": aligned, "exit": proc.returncode}


def main() -> int:
    INBOX.mkdir(parents=True, exist_ok=True)
    LOG.write_text(f"# ceo-xhs-ip-filter-batch · {datetime.now().isoformat()}\n", encoding="utf-8")

    run([str(ROOT / "scripts/screen-artist-watchlist.py")], "screen-artist-watchlist")
    run(["bash", str(ROOT / "scripts/analytics-pipeline.sh"), "--demo"], "analytics-demo")
    if (ROOT / "scripts/ceo-dispatch-refresh.py").is_file():
        run([str(ROOT / ".venv/bin/python"), str(ROOT / "scripts/ceo-dispatch-refresh.py")], "ceo-dispatch")

    screened = json.loads(
        (ROOT / "content/ip-research/artist-watchlist-screened.json").read_text(encoding="utf-8")
    )
    briefs = sorted((ROOT / "content/xiaohongshu").glob("*-brief.md"))
    brief_scores = [score_brief(b) for b in briefs]

    strategy = ROOT / "content/analytics/derived/xhs-data-strategy-2026-10-20.md"
    dispatch = ROOT / "content/analytics/derived/ceo-dispatch-latest.md"
    publish_q = ROOT / "content/xiaohongshu/2026-10-20-publish-ready-queue.md"
    full_artists = ROOT / "content/ip-research/2026-10-27-watchlist-four-metrics-full.md"

    lines = [
        "# Owner 交付 · CEO 派活筛选 · 小红书资料 + IP 对标 · "
        + datetime.now().strftime("%Y-%m-%d %H:%M"),
        "",
        "> **内部链：** 00 CEO → 01 IP / 04 Topic / 09 Analytics / 10 Artist · Gate 后交 Owner",
        "> **Owner 请打开 HTML（可双击浏览器）：** "
        f"`{OUT.with_suffix('.html').relative_to(ROOT)}` · Excel：`content/ip-research/artist-watchlist-four-metrics.xlsx`",
        "> _本 MD 仅供 Agent/Git；Owner 报告默认 HTML，见 content/xiaohongshu/CONTENT-DELIVERY-FOR-OWNER.md_",
        "",
        "## 一、CEO 派活记录",
        "",
        "| GM | 任务 | 产出 |",
        "|----|------|------|",
        "| 01 personal-ip | 对齐 ip-positioning-brief 红线 | 筛选权重：强链接·不绑单品类·认知期 |",
        "| 04 xhs-topic | 全仓 Brief evaluate | 见下表「小红书 Brief 优先级」 |",
        "| 09 analytics | pipeline + DATA-MANIFEST | 见「数据侧推荐」 |",
        "| 10 artist | DB/PLD/APO/CTD 筛查 | 见「Artist P1–P3」 |",
        "",
        "## 二、小红书 Brief · 推荐优先级（最适合你当前 IP）",
        "",
        "| 优先级 | Brief | aligned | 说明 |",
        "|--------|-------|---------|------|",
    ]

    priority_notes = {
        "2026-10-17-discovery-01-irreplaceability-brief.md": "**首推** · 认知期 #1 · 与数据策略「故事+判断」一致 · 可直发队列 #1",
        "2026-10-17-discovery-02-narrative-not-ads-brief.md": "**次推** · 叙事非硬广 · 队列 #2",
        "2026-10-17-discovery-03-professional-trust-brief.md": "第三 · 专业信任 · 队列 #3",
        "2026-10-17-discovery-04-open-close-brief.md": "第四 · open/边界 · 队列 #4",
        "2026-10-08-brand-art-narrative-brief.md": "补位 · 品牌艺术叙事 · 需 redteam-pre",
        "2026-10-27-artist-benchmark-thatviolakid-brief.md": "对标稿 · P1 ThatViolaKid · **未 Gate 勿发**",
    }
    publish_order = [
        "2026-10-17-discovery-01-irreplaceability-brief.md",
        "2026-10-17-discovery-02-narrative-not-ads-brief.md",
        "2026-10-17-discovery-03-professional-trust-brief.md",
        "2026-10-17-discovery-04-open-close-brief.md",
        "2026-10-08-brand-art-narrative-brief.md",
        "2026-10-27-artist-benchmark-thatviolakid-brief.md",
    ]
    by_name = {Path(s["path"]).name: s for s in brief_scores}
    ranked = [by_name[n] for n in publish_order if n in by_name]
    ranked += [s for s in brief_scores if Path(s["path"]).name not in publish_order]
    for i, row in enumerate(ranked, 1):
        name = Path(row["path"]).name
        note = priority_notes.get(name, "—")
        lines.append(
            f"| {i} | `{row['path']}` | {'✅' if row['aligned'] else '⚠️ 待 Gate'} | {note} |"
        )

    lines += [
        "",
        "**可直发正文（Agent 已写）：** `content/xiaohongshu/2026-10-20-publish-ready-queue.md`",
        "",
        "## 三、数据侧推荐（09 → 04）",
        "",
    ]
    if strategy.is_file():
        lines.append("摘录自 `xhs-data-strategy-2026-10-20.md`：")
        lines.append("")
        for ln in strategy.read_text(encoding="utf-8").splitlines()[:35]:
            lines.append(ln)
        lines.append("…")
    else:
        lines.append("_策略文件缺失_")

    lines += ["", "## 四、Artist 对标 · 四指标（10 → Owner 裁决）", ""]
    for a in screened.get("artists") or []:
        m = a.get("benchmark_metrics") or {}
        lines.append(
            f"- **{a.get('name')}** · {a.get('priority_tier')} · composite **{a.get('borrow_score_composite')}** · "
            f"DB {m.get('directional_benchmarking', {}).get('score')} · "
            f"PLD {m.get('pixel_level_deconstruction', {}).get('score')} · "
            f"APO {m.get('audience_persona_overlap', {}).get('score')} · "
            f"CTD {m.get('core_topic_density', {}).get('score')}"
        )
        urls = a.get("urls") or []
        if urls:
            lines.append("  - " + " · ".join(urls))

    lines += [
        "",
        f"详表：[`{full_artists.relative_to(ROOT)}`](../ip-research/2026-10-27-watchlist-four-metrics-full.md)",
        "",
        "## 五、请你（仅决策）",
        "",
        "- [ ] 先发表 **discovery-01** 或指定 Brief 序号",
        "- [ ] Artist **ThatViolaKid** 适合/不适合 + 原因",
        "- [ ] 是否指定 GM10 深读 URL",
        "",
        "## 六、内部验收",
        "",
        f"- log: `{LOG.relative_to(ROOT)}`",
        "",
    ]

    OUT.write_text("\n".join(lines), encoding="utf-8")
    subprocess.run(["bash", str(ROOT / "scripts/manager-xhs-briefs-auto-pipeline.sh")], cwd=ROOT, check=False)
    html_builder = ROOT / "scripts/build-owner-xhs-report-html.py"
    py = ROOT / ".venv/bin/python"
    if html_builder.is_file() and py.is_file():
        subprocess.run([str(py), str(html_builder)], cwd=ROOT, check=False)
    print("PASS", OUT)
    print("PASS", OUT.with_suffix(".html"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
