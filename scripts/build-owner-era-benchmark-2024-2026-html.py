#!/usr/bin/env python3
"""Interactive HTML · 2024-2026 era-adjusted benchmark creators (modal per person)."""

from __future__ import annotations

import html
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
JSON_PATH = ROOT / "integration/handoff/owner-era-benchmark-2024-2026-creators.json"
INBOX = ROOT / "content/evolution/00-manager/ceo-inbox"
DRIVE_DOC = "https://docs.google.com/document/d/1eVHpsMOI3JLEwGq4F3ItnXuUpWsYoyhbivgwqWLA7Nc/edit"


def esc(s: str) -> str:
    return html.escape(str(s))


def build(out: Path) -> None:
    data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    rebuilt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    creators = data.get("creators") or []

    cards = ""
    modals = ""
    for c in creators:
        cid = esc(c["id"])
        handle = esc(c.get("handle", ""))
        plat = esc(c.get("platform_primary", ""))
        region = "国内" if c.get("region") == "domestic_cn" else "国际"
        fol = esc(c.get("followers_approx", ""))
        cross = c.get("cross_platform_approx")
        cross_s = f" · 跨平台约 {esc(cross)}" if cross else ""

        why_li = "".join(f"<li>{esc(x)}</li>" for x in c.get("why_learn_now") or [])
        path_rows = ""
        for step in c.get("growth_path") or []:
            path_rows += f"""<tr>
<td>{esc(step.get('phase',''))}</td>
<td>{esc(step.get('when',''))}</td>
<td>{esc(step.get('what',''))}</td>
<td>{esc(step.get('filming',''))}</td>
</tr>"""

        hits = ""
        for h in c.get("hit_topics") or []:
            src = h.get("source", "")
            link = f'<a href="{esc(src)}" target="_blank" rel="noopener">来源链接</a>' if src else "—"
            hits += f"""<tr>
<td><strong>{esc(h.get('title',''))}</strong></td>
<td>{esc(h.get('type',''))}</td>
<td class="note">{esc(h.get('note',''))}</td>
<td>{link}</td>
</tr>"""

        links_li = "".join(
            f'<li><a href="{esc(u)}" target="_blank" rel="noopener">{esc(u)}</a></li>'
            for u in c.get("profile_urls") or []
        )

        cards += f"""<button type="button" class="card" data-modal="{cid}" aria-haspopup="dialog">
  <span class="region">{region}</span>
  <h3>{handle}</h3>
  <p class="meta">{plat} · 约 {fol} 粉{cross_s}</p>
  <p class="hint">点击查看：原因 · 成长路径 · 爆款选题</p>
</button>"""

        modals += f"""<div id="modal-{cid}" class="modal" role="dialog" aria-labelledby="title-{cid}" hidden>
  <div class="modal-inner">
    <button type="button" class="modal-close" data-close="{cid}" aria-label="关闭">×</button>
    <h2 id="title-{cid}">{handle}</h2>
    <p class="sub">{region} · {plat} · 约 {fol} 粉{cross_s}</p>
    <p class="prof"><strong>本来是干什么的：</strong>{esc(c.get('original_profession',''))}</p>

    <h3>为什么 2024–2026 仍值得学</h3>
    <ul>{why_li}</ul>

    <h3>成长路径（起初拍什么 → 怎么 gradually 火）</h3>
    <table class="path">
      <tr><th>阶段</th><th>时间</th><th>发生了什么</th><th>拍摄/形式</th></tr>
      {path_rows}
    </table>

    <h3>爆款 / 高互动选题（公开报道汇总 · 非全量爬取）</h3>
    <table class="hits">
      <tr><th>选题/标题</th><th>类型</th><th>说明</th><th>链接</th></tr>
      {hits}
    </table>

    <h3>主页 / 报道链接</h3>
    <ul class="urls">{links_li}</ul>
  </div>
</div>"""

    doc = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>2024–2026 时代校正对标 · 交互详情 · {rebuilt[:10]}</title>
<style>
:root {{ --bg:#0d1117; --panel:#161b22; --border:#30363d; --text:#e6edf3; --muted:#8b949e; --accent:#58a6ff; --dom:#3fb950; --int:#d29922; }}
* {{ box-sizing:border-box; }}
body {{ margin:0; font-family:"PingFang SC",system-ui,sans-serif; background:var(--bg); color:var(--text); line-height:1.55; }}
.wrap {{ max-width:1200px; margin:0 auto; padding:24px 20px 80px; }}
h1 {{ font-size:1.45rem; margin:0 0 8px; }}
.lead {{ color:var(--muted); font-size:0.92rem; margin-bottom:20px; }}
.lead a {{ color:var(--accent); }}
.grid {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(260px,1fr)); gap:14px; }}
.card {{
  text-align:left; cursor:pointer; background:var(--panel); border:1px solid var(--border);
  border-radius:12px; padding:16px; color:inherit; transition:border-color .15s, transform .1s;
}}
.card:hover {{ border-color:var(--accent); transform:translateY(-2px); }}
.card h3 {{ margin:8px 0 6px; font-size:1.05rem; }}
.card .meta {{ color:var(--muted); font-size:0.85rem; margin:0; }}
.card .hint {{ font-size:0.8rem; color:var(--accent); margin:10px 0 0; }}
.region {{
  font-size:11px; padding:2px 8px; border-radius:999px; background:#21262d;
}}
.card .region {{ background:#1f3a5f; color:#79c0ff; }}
.modal {{
  position:fixed; inset:0; z-index:1000; background:rgba(0,0,0,.72);
  display:flex; align-items:flex-start; justify-content:center; padding:24px 12px;
  overflow-y:auto;
}}
.modal[hidden] {{ display:none !important; }}
.modal-inner {{
  background:var(--panel); border:1px solid var(--border); border-radius:14px;
  max-width:920px; width:100%; padding:22px 24px 28px; position:relative;
}}
.modal-close {{
  position:absolute; top:12px; right:14px; border:none; background:#21262d;
  color:var(--text); font-size:1.4rem; width:36px; height:36px; border-radius:8px; cursor:pointer;
}}
.modal h2 {{ margin:0 40px 4px 0; font-size:1.25rem; }}
.modal .sub {{ color:var(--muted); margin:0 0 12px; }}
.modal .prof {{ background:#0d1117; padding:10px 12px; border-radius:8px; font-size:0.9rem; }}
.modal h3 {{ margin:20px 0 10px; font-size:1rem; color:#79c0ff; }}
table {{ width:100%; border-collapse:collapse; font-size:0.82rem; }}
th,td {{ border-bottom:1px solid var(--border); padding:8px 6px; text-align:left; vertical-align:top; }}
th {{ color:var(--muted); font-weight:600; }}
td.note {{ color:var(--muted); }}
.urls {{ word-break:break-all; font-size:0.85rem; }}
footer {{ margin-top:32px; color:var(--muted); font-size:0.8rem; }}
</style>
</head>
<body>
<div class="wrap">
  <h1 id="owner-latest">2024–2026 仍值得学 · 大 V 对标（点击每人弹窗）</h1>
  <p class="lead">
    重建 {esc(rebuilt)} · 真源 <code>{esc(JSON_PATH.relative_to(ROOT))}</code> ·
    {esc(data.get('data_note',''))} ·
    <a href="{esc(DRIVE_DOC)}" target="_blank" rel="noopener">Google Doc 双线对标</a>
  </p>
  <p class="lead"><strong>用法：</strong>点卡片 → 原因 / 成长路径 / 爆款选题（带外链）。Esc 或点遮罩关闭。</p>
  <div class="grid">{cards}</div>
  <footer>CEO · pivot IP · 时代校正（非 COVID 主红利模板）· build: scripts/build-owner-era-benchmark-2024-2026-html.py</footer>
</div>
{modals}
<script>
document.querySelectorAll('.card').forEach(btn => {{
  btn.addEventListener('click', () => {{
    const id = btn.getAttribute('data-modal');
    const m = document.getElementById('modal-' + id);
    if (m) {{ m.hidden = false; document.body.style.overflow = 'hidden'; }}
  }});
}});
function closeModal(cid) {{
  const m = document.getElementById('modal-' + cid);
  if (m) {{ m.hidden = true; document.body.style.overflow = ''; }}
}}
document.querySelectorAll('.modal-close').forEach(b => {{
  b.addEventListener('click', () => closeModal(b.getAttribute('data-close')));
}});
document.querySelectorAll('.modal').forEach(m => {{
  m.addEventListener('click', e => {{
    if (e.target === m) {{
      m.hidden = true; document.body.style.overflow = '';
    }}
  }});
}});
document.addEventListener('keydown', e => {{
  if (e.key === 'Escape') {{
    document.querySelectorAll('.modal:not([hidden])').forEach(m => {{ m.hidden = true; }});
    document.body.style.overflow = '';
  }}
}});
</script>
</body>
</html>"""
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(doc, encoding="utf-8")
    latest = INBOX / "OWNER-ERA-BENCHMARK-2024-2026-DELIVERABLE-latest.html"
    latest.write_text(doc, encoding="utf-8")
    print(f"PASS {out}")
    print(f"PASS {latest}")


if __name__ == "__main__":
    day = datetime.now().strftime("%Y-%m-%d")
    build(INBOX / f"OWNER-ERA-BENCHMARK-2024-2026-DELIVERABLE-{day}.html")
