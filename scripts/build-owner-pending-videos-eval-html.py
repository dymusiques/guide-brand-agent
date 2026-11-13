#!/usr/bin/env python3
"""Build HTML table from owner-pending-videos-eval-latest.json."""

from __future__ import annotations

import html
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
JSON_PATH = ROOT / "integration/handoff/owner-pending-videos-eval-latest.json"
INBOX = ROOT / "content/evolution/00-manager/ceo-inbox"


def esc(s: str) -> str:
    return html.escape(str(s))


def build(out: Path) -> None:
    if not JSON_PATH.is_file():
        data = {"status": "missing", "items": [], "message": "Run evaluate-owner-pending-videos.py first"}
    else:
        data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    rebuilt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    rows = ""
    for it in data.get("items") or []:
        m = it.get("metrics") or {}
        bar = lambda v: f'<div class="bar"><span style="width:{int(v)}%"></span></div> {int(v)}'
        tier = it.get("promote_tier", "—")
        tc = "t-a" if tier == "A" else ("t-b" if tier == "B" else "t-c")
        basis_li = "".join(f"<li>{esc(x)}</li>" for x in (it.get("scoring_basis") or []))
        rows += f"""<tr class="click-row" data-id="{esc(it.get('id',''))}" tabindex="0">
<td>{it.get('rank','')}</td>
<td><strong>{esc(it.get('title',''))}</strong><br/><span class="muted">{esc(it.get('file',''))} · 点击行看依据</span></td>
<td>{esc(it.get('track',''))}</td>
<td><strong>{m.get('match_overall','')}</strong></td>
<td>{bar(m.get('story_fit',0))}</td>
<td>{bar(m.get('data_fit',0))}</td>
<td>{bar(m.get('hook_strength',0))}</td>
<td>{bar(m.get('completion_risk',0))}</td>
<td><span class="tier {tc}">{esc(tier)}</span></td>
<td class="note">{esc(it.get('promote_note',''))}</td>
</tr>
<tr class="basis-row" data-for="{esc(it.get('id',''))}"><td colspan="10"><ul class="basis">{basis_li}</ul></td></tr>"""
    empty = ""
    if not rows:
        rows = f'<tr><td colspan="10">{esc(data.get("message", "inbox 无 .md — 见 docs/OWNER-PENDING-VIDEOS-EVAL-SOP.md"))}</td></tr>'
    winner = esc(data.get("promote_winner") or "—")
    count = data.get("item_count", 0)
    doc = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>待发口播评估 · {rebuilt[:10]}</title>
<style>
:root {{ --bg:#0d1117; --panel:#161b22; --border:#30363d; --text:#e6edf3; --muted:#8b949e; --accent:#58a6ff; --green:#3fb950; }}
body {{ margin:0; font-family:"PingFang SC",system-ui,sans-serif; background:var(--bg); color:var(--text); padding:20px; }}
.wrap {{ max-width:1100px; margin:0 auto; }}
h1 {{ font-size:1.25rem; }}
.lead {{ color:var(--muted); font-size:0.88rem; }}
.bar {{ display:inline-block; width:50px; height:6px; background:#21262d; border-radius:3px; vertical-align:middle; margin-right:4px; }}
.bar span {{ display:block; height:100%; background:linear-gradient(90deg,#238636,#58a6ff); border-radius:3px; }}
table {{ width:100%; border-collapse:collapse; font-size:0.82rem; margin-top:16px; }}
th,td {{ border-bottom:1px solid var(--border); padding:8px; text-align:left; vertical-align:top; }}
th {{ color:var(--muted); }}
.muted {{ color:var(--muted); font-size:0.75rem; }}
.click-row {{ cursor:pointer; }}
.basis-row {{ display:none; background:#0d1117; }}
.basis-row.open {{ display:table-row; }}
.basis {{ margin:6px 0; padding-left:1.2rem; font-size:0.85rem; color:var(--muted); }}
.note {{ max-width:220px; color:var(--muted); }}
.tier {{ padding:2px 8px; border-radius:4px; font-weight:700; }}
.t-a {{ background:#1f3d2f; color:#3fb950; }}
.t-b {{ background:#3d3520; color:#d29922; }}
.t-c {{ background:#3d2020; color:#f85149; }}
.win {{ border:1px solid var(--green); padding:12px; border-radius:8px; margin:12px 0; }}
</style>
</head>
<body>
<div class="wrap">
<h1 id="owner-latest">待发口播评估 · 匹配度 & 薯条建议</h1>
<p class="lead">重建 {esc(rebuilt)} · inbox 条目数 {count} · 真源 {esc(JSON_PATH.relative_to(ROOT))}</p>
<div class="win"><strong>薯条优先试探（规则层）：</strong> {winner} · 详见 promote_note 列 · Drive 参考：如何投放好小红书薯条.md</div>
<table>
<tr><th>#</th><th>标题</th><th>轨</th><th>综合匹配</th><th>故事</th><th>数据像</th><th>钩子</th><th>完播风险</th><th>投流</th><th>说明</th></tr>
{rows}
</table>
<p class="lead">新增/修改口播 MD 后重跑：<code>bash scripts/run-owner-pending-videos-eval.sh</code> ·
SOP：<code>docs/OWNER-PENDING-VIDEOS-EVAL-SOP.md</code> · Inbox：<code>content/xiaohongshu/inbox/pending-videos/</code></p>
</div>
<script>
document.querySelectorAll('tr.click-row').forEach(row => {{
  row.addEventListener('click', () => {{
    const id = row.getAttribute('data-id');
    const br = document.querySelector('tr.basis-row[data-for="'+id+'"]');
    if (br) br.classList.toggle('open');
  }});
}});
</script>
</body>
</html>"""
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(doc, encoding="utf-8")
    latest = INBOX / "OWNER-PENDING-VIDEOS-EVAL-latest.html"
    latest.write_text(doc, encoding="utf-8")
    print(f"PASS {latest}")


if __name__ == "__main__":
    day = datetime.now().strftime("%Y-%m-%d")
    build(INBOX / f"OWNER-PENDING-VIDEOS-EVAL-{day}.html")
