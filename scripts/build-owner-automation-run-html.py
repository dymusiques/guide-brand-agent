#!/usr/bin/env python3
"""Build Owner Automation run HTML from integration/handoff/owner-automation-html/<slug>-latest.json."""

from __future__ import annotations

import argparse
import html
import json
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HANDOFF = ROOT / "integration/handoff/owner-automation-html"
OUT_DIR = ROOT / "content/evolution/00-manager/ceo-inbox/automation-runs"


def esc(s: str) -> str:
    return html.escape(s or "", quote=True)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True, help="automation slug, e.g. daily-ai-intel")
    ap.add_argument("--json", default="", help="override JSON path")
    args = ap.parse_args()

    jpath = Path(args.json) if args.json else HANDOFF / f"{args.slug}-latest.json"
    if not jpath.is_file():
        print(f"FAIL: missing {jpath}", file=sys.stderr)
        return 1

    data = json.loads(jpath.read_text(encoding="utf-8"))
    run_date = data.get("run_date") or date.today().isoformat()
    title = data.get("automation_title_zh") or args.slug
    status = data.get("status", "INFO")
    summary = data.get("summary_zh", "")
    items = data.get("items") or []

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_html = OUT_DIR / f"OWNER-AUTOMATION-{args.slug}-{run_date}.html"

    blocks = []
    for i, it in enumerate(items, 1):
        ex = esc(it.get("excerpt_zh", ""))
        sn = esc(it.get("source_name", ""))
        url = (it.get("url") or "").strip()
        idate = esc(it.get("info_date", ""))
        t = esc(it.get("title_zh", f"条目 {i}"))
        zone = esc(it.get("zone", ""))
        link = (
            f'<a href="{esc(url)}" target="_blank" rel="noopener">{esc(url)}</a>'
            if url.startswith("http")
            else f"<code>{esc(url)}</code>"
            if url
            else "—"
        )
        blocks.append(
            f"""<article class="item" id="item-{i}">
<h3>{i}. {t} <span class="zone">{zone}</span></h3>
<p class="excerpt">{ex}</p>
<p class="source">来源：{sn or "—"} · 链接：{link} · 日期：{idate or "—"}</p>
</article>"""
        )

    body = "\n".join(blocks) if blocks else '<p class="empty">（无条目）</p>'
    md_path = esc(data.get("md_path", ""))

    page = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>{esc(title)} · {esc(run_date)}</title>
<style>
body {{ font-family: system-ui, sans-serif; max-width: 52rem; margin: 2rem auto; padding: 0 1rem; line-height: 1.55; }}
h1 {{ font-size: 1.35rem; }}
.status {{ font-weight: 600; }}
.item {{ border-top: 1px solid #ddd; padding: 1rem 0; }}
.excerpt {{ margin: 0.5rem 0; }}
.source {{ font-size: 0.9rem; color: #444; }}
.zone {{ font-size: 0.75rem; color: #666; font-weight: normal; }}
footer {{ margin-top: 2rem; font-size: 0.85rem; color: #666; }}
</style>
</head>
<body>
<h1>{esc(title)}</h1>
<p class="status">状态：{esc(status)} · 日期：{esc(run_date)}</p>
<p class="summary">{esc(summary)}</p>
<p>Markdown：{f"<code>{md_path}</code>" if md_path else "—"}</p>
{body}
<footer>build: scripts/build-owner-automation-run-html.py · slug={esc(args.slug)} · json={esc(str(jpath.relative_to(ROOT)))}</footer>
</body>
</html>
"""
    out_html.write_text(page, encoding="utf-8")

    ptr = {
        "slug": args.slug,
        "run_date": run_date,
        "html_path": str(out_html.relative_to(ROOT)),
        "json_path": str(jpath.relative_to(ROOT)),
    }
    ptr_path = HANDOFF / f"{args.slug}-latest.html"
    ptr_path.write_text(json.dumps(ptr, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"OK {out_html.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())