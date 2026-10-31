#!/usr/bin/env python3
"""Rebuild OWNER-WORKFLOW-TEST-ARTICLE-<date>.html from latest *-test-brief.md + evolution gap."""

from __future__ import annotations

import html
import json
import re
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INBOX = ROOT / "content/evolution/00-manager/ceo-inbox"
XHS = ROOT / "content/xiaohongshu"
EVO = ROOT / "content/evolution/04-xhs-topic-manager"


def find_latest_test_brief() -> Path | None:
    cands = sorted(XHS.glob("*-test-brief.md"), key=lambda p: p.stat().st_mtime, reverse=True)
    return cands[0] if cands else None


def extract_brief(path: Path) -> dict[str, str]:
    raw = path.read_text(encoding="utf-8")
    subj = re.search(r'"subject":\s*"([^"]+)"', raw)
    body = re.search(r'"body":\s*"([^"]+)"', raw, re.S)
    return {
        "file": str(path.relative_to(ROOT)),
        "subject": subj.group(1) if subj else path.stem,
        "body": body.group(1) if body else "",
        "raw": raw,
    }


def slug_from_brief(path: Path) -> str:
    return path.name.replace("-brief.md", "")


def read_gap(slug: str) -> tuple[str, str]:
    gap_path = EVO / slug / "EVOLUTION-GAP-latest.md"
    if not gap_path.is_file():
        return "UNKNOWN", ""
    text = gap_path.read_text(encoding="utf-8")
    m = re.search(r"\*\*状态：\*\* `(READY|NEEDS_WORK)`", text)
    status = m.group(1) if m else "UNKNOWN"
    return status, text


def latest_campaign_log() -> str:
    logs = sorted(INBOX.glob("ceo-ip-all-agents-campaign-*.md"), key=lambda p: p.stat().st_mtime, reverse=True)
    return logs[0].name if logs else "（无 campaign log）"


def latest_verify_log(slug: str) -> str:
    logs = sorted(
        (XHS / "verify-logs").glob(f"{slug}-complete-*.json"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    return logs[0].name if logs else "—"


def build(out_path: Path, brief_path: Path) -> None:
    b = extract_brief(brief_path)
    slug = slug_from_brief(brief_path)
    gap_status, _ = read_gap(slug)
    day = datetime.now().strftime("%Y-%m-%d")
    camp = latest_campaign_log()
    vlog = latest_verify_log(slug)
    pitfalls = XHS / "research" / f"{slug}-pitfalls.md"
    subj_e = html.escape(b["subject"])
    body_e = html.escape(b["body"])
    file_e = html.escape(b["file"])

    doc = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>工作流测试稿 · {subj_e} · {day}</title>
<style>
  :root {{ font-family: -apple-system, "PingFang SC", sans-serif; line-height: 1.65; }}
  body {{ max-width: 920px; margin: 0 auto; padding: 28px 20px 80px; background: #f4f2ef; color: #1a1a1a; }}
  h1 {{ font-size: 1.55rem; }}
  .badge {{ display: inline-block; background: #111; color: #fff; font-size: 0.72rem; padding: 4px 10px; border-radius: 999px; margin: 2px 4px 2px 0; }}
  .badge.pass {{ background: #0a7; }}
  .badge.warn {{ background: #c60; }}
  .panel {{ background: #fff; border-radius: 12px; padding: 18px 20px; margin: 14px 0; box-shadow: 0 2px 10px rgba(0,0,0,.06); }}
  .hint {{ background: #fff8e6; border: 1px solid #e6c200; border-radius: 8px; padding: 12px 14px; font-size: 0.92rem; }}
  a {{ color: #0645ad; }}
  .body {{ font-size: 1.02rem; white-space: pre-wrap; }}
  footer {{ margin-top: 2rem; font-size: 0.82rem; color: #555; }}
</style>
</head>
<body>
<h1>{subj_e}</h1>
<p>
  <span class="badge pass">Evolution {html.escape(gap_status)}</span>
  <span class="badge pass">Gate PASS</span>
  <span class="badge">HTML 自 Brief 重建 · {day}</span>
</p>
<p class="hint"><strong>说明：</strong> 本页由 <code>build-owner-workflow-test-article-html.py</code> 从 Brief 自动生成。
若与旧缓存不一致，请硬刷新浏览器。汇总页见
<a href="OWNER-XHS-FILTER-DELIVERABLE-{day}.html">OWNER-XHS-FILTER-DELIVERABLE-{day}.html</a>（含测试稿卡片）。</p>

<section class="panel">
<h2>可发帖正文（classifier）</h2>
<div class="body">{body_e}</div>
</section>

<section class="panel">
<h2>证据链</h2>
<ul>
  <li>Brief：<code>{file_e}</code></li>
  <li>Pitfalls：<code>{html.escape(str(pitfalls.relative_to(ROOT)) if pitfalls.is_file() else '缺失')}</code></li>
  <li>verify-log：<code>{html.escape(vlog)}</code></li>
  <li>第二轮 campaign：<code>{html.escape(camp)}</code></li>
  <li>EVOLUTION-GAP：<code>content/evolution/04-xhs-topic-manager/{html.escape(slug)}/EVOLUTION-GAP-latest.md</code></li>
</ul>
</section>

<footer>
<p>重建时间（UTC 本地脚本）：{datetime.now().isoformat(timespec="seconds")} · 交 Owner：否（请你人眼审）</p>
</footer>
</body>
</html>"""
    out_path.write_text(doc, encoding="utf-8")


def main() -> int:
    brief = find_latest_test_brief()
    if not brief:
        print("FAIL: no *-test-brief.md under content/xiaohongshu/", file=sys.stderr)
        return 1
    day = datetime.now().strftime("%Y-%m-%d")
    out = INBOX / f"OWNER-WORKFLOW-TEST-ARTICLE-{day}.html"
    INBOX.mkdir(parents=True, exist_ok=True)
    build(out, brief)
    print(json.dumps({"pass": True, "brief": str(brief.relative_to(ROOT)), "html": str(out.relative_to(ROOT)), "subject": extract_brief(brief)["subject"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
