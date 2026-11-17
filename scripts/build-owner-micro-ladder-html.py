#!/usr/bin/env python3
"""Interactive HTML · micro ladder · click each item for full detail modal."""

from __future__ import annotations

import html
import json
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from owner_micro_ladder_expand import (  # noqa: E402
    BENCHMARK_EXPAND,
    MICRO_EXPAND,
    QUEUE_ITEMS,
    STEP_EXPAND,
    TAB_INTROS,
)

JSON_PATH = ROOT / "integration/handoff/owner-micro-ladder-matrix.json"
INBOX = ROOT / "content/evolution/00-manager/ceo-inbox"
MD_SOURCE = INBOX / "2026-11-07-owner-micro-ladder-ip-volume.md"


def esc(s: str) -> str:
    return html.escape(str(s))


def translate_fit(mv: dict) -> int:
    return round(
        0.35 * mv["fit_experience"]
        + 0.35 * mv["fit_your_data"]
        + 0.15 * mv["ease_shoot"]
        + 0.15 * mv["volume_priority"]
    )


def sections_html(sections: list[tuple[str, str]]) -> str:
    out = ""
    for h, p in sections:
        out += f"<h3>{esc(h)}</h3><p>{esc(p)}</p>"
    return out


def step_sections_html(t: tuple) -> str:
    # title, h1, p1, h2, p2, h3, p3, h4, p4
    title = t[0]
    body = f"<h3>{esc(t[1])}</h3><p>{esc(t[2])}</p>"
    body += f"<h3>{esc(t[3])}</h3><p>{esc(t[4])}</p>"
    body += f"<h3>{esc(t[5])}</h3><p>{esc(t[6])}</p>"
    body += f"<h3>{esc(t[7])}</h3><p>{esc(t[8])}</p>"
    return title, body


def build(out: Path) -> None:
    data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    rebuilt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    pillars = {p["id"]: p for p in data.get("pillars") or []}

    benchmarks = data.get("benchmarks") or []
    micros = data.get("micro_videos") or []
    for mv in micros:
        mv["_fit"] = translate_fit(mv)
    micros_sorted = sorted(micros, key=lambda x: x["_fit"], reverse=True)

    all_modals = ""

    n_b = len(benchmarks)
    bench_nodes = ""
    matrix_lines = ""
    for i, b in enumerate(benchmarks):
        angle = -1.57 + (i / max(n_b, 1)) * 3.14
        bx = 0.5 + 0.38 * __import__("math").cos(angle)
        by = 0.5 + 0.38 * __import__("math").sin(angle)
        bid = b["id"]
        bid_esc = esc(bid)
        label = esc(b["handle"].split("/")[0][:10])
        bench_nodes += f"""
<g class="bench-node" data-open="bench-{bid_esc}" role="button" tabindex="0" style="cursor:pointer">
  <circle cx="{bx*100:.2f}%" cy="{by*100:.2f}%" r="28" fill="#21262d" stroke="#58a6ff" stroke-width="2"/>
  <text x="{bx*100:.2f}%" y="{by*100:.2f}%" text-anchor="middle" dominant-baseline="middle" class="bench-label">{label}</text>
</g>"""
        for link in b.get("matrix_links") or []:
            pid = link.get("pillar")
            if pid not in pillars:
                continue
            px, py = pillars[pid]["x"], pillars[pid]["y"]
            strength = float(link.get("strength") or 0.5)
            matrix_lines += f"""
<line x1="{bx*100:.2f}%" y1="{by*100:.2f}%" x2="{px*100:.2f}%" y2="{py*100:.2f}%"
  stroke="#58a6ff" stroke-width="{1 + strength * 4:.1f}" stroke-opacity="{0.35 + strength * 0.55:.2f}"/>"""

        exp = BENCHMARK_EXPAND.get(bid, {})
        sec = exp.get("sections") or [
            ("重叠", b.get("overlap", "")),
            ("说明", "详情待补充"),
        ]
        all_modals += f"""
<div id="modal-bench-{bid_esc}" class="modal" role="dialog" hidden>
  <div class="modal-inner">
    <button type="button" class="modal-close" data-close="bench-{bid_esc}">×</button>
    <h2>{esc(exp.get('title') or b.get('handle',''))}</h2>
    <p class="sub">{esc(b.get('region',''))} · {esc(b.get('overlap',''))}</p>
    {sections_html(sec)}
  </div>
</div>"""

    pillar_nodes = ""
    for p in data.get("pillars") or []:
        pillar_nodes += f"""
<g><rect x="{p['x']*100-6:.2f}%" y="{p['y']*100-4:.2f}%" width="12%" height="8%" rx="6" fill="#1f3a5f" stroke="#79c0ff"/>
<text x="{p['x']*100:.2f}%" y="{p['y']*100:.2f}%" text-anchor="middle" dominant-baseline="middle" class="pillar-label">{esc(p['label'])}</text></g>"""

    owner_lines = ""
    for p in data.get("pillars") or []:
        owner_lines += f"""
<line x1="50%" y1="50%" x2="{p['x']*100:.2f}%" y2="{p['y']*100:.2f}%"
  stroke="#3fb950" stroke-width="1.5" stroke-dasharray="4 4" opacity="0.5"/>"""

    rows = ""
    for rank, mv in enumerate(micros_sorted, 1):
        fit = mv["_fit"]
        mid = mv["id"]
        mid_esc = esc(mid)

        def bar(v):
            return f'<div class="bar"><span style="width:{v}%"></span></div><span class="num">{v}</span>'

        track = mv.get("track", "IP")
        tclass = "track-ip" if track == "IP" else "track-fb"
        rows += f"""<tr class="click-row" data-open="mv-{mid_esc}" data-track="{esc(track)}" tabindex="0">
<td><span class="rank-btn">{rank}</span></td>
<td><strong>{esc(mv.get('your_title',''))}</strong>
  <span class="open-hint">点击看：怎么拍 · 口播 · 分镜</span><br/>
  <span class="muted">{esc(mv.get('their_format',''))}</span></td>
<td>{esc(mv.get('source_creator',''))}</td>
<td><span class="badge {tclass}">{esc(track)}</span></td>
<td class="fit-cell"><strong>{fit}</strong></td>
<td>{bar(mv.get('fit_experience',0))}</td>
<td>{bar(mv.get('fit_your_data',0))}</td>
<td>{bar(mv.get('ease_shoot',0))}</td>
<td>{bar(mv.get('volume_priority',0))}</td>
<td class="note">{esc(mv.get('owner_evidence',''))}</td>
</tr>"""

        sec = MICRO_EXPAND.get(mid, [("说明", "详情待补充")])
        all_modals += f"""
<div id="modal-mv-{mid_esc}" class="modal" role="dialog" hidden>
  <div class="modal-inner">
    <button type="button" class="modal-close" data-close="mv-{mid_esc}">×</button>
    <h2>{esc(mv.get('your_title',''))}</h2>
    <p class="sub">平移综合 <strong>{fit}</strong> · {esc(track)} 轨 · {esc(mv.get('duration',''))} · 学 {esc(mv.get('source_creator',''))}</p>
    <p class="evidence"><strong>你的数据：</strong>{esc(mv.get('owner_evidence',''))}</p>
    {sections_html(sec)}
  </div>
</div>"""

    steps_html = ""
    for s in data.get("steps") or []:
        sid = s["id"]
        sid_esc = esc(sid)
        st = STEP_EXPAND.get(sid)
        if st:
            st_title, st_body = step_sections_html(st)
        else:
            st_title = s.get("title", "")
            st_body = f"<p>{esc(s.get('detail',''))}</p>"

        all_modals += f"""
<div id="modal-step-{sid_esc}" class="modal" role="dialog" hidden>
  <div class="modal-inner">
    <button type="button" class="modal-close" data-close="step-{sid_esc}">×</button>
    <h2>{esc(st_title)}</h2>
    <p class="sub">微步 · 块 {s.get('block')} · {esc(s.get('track',''))}</p>
    {st_body}
  </div>
</div>"""

        steps_html += f"""
<div class="step" data-block="{s.get('block',1)}">
  <input type="checkbox" data-step-id="{sid_esc}" aria-label="完成"/>
  <button type="button" class="step-open" data-open="step-{sid_esc}">
    <strong>{esc(s.get('title',''))}</strong>
    <span class="badge track-{esc(s.get('track','IP')).lower()}">{esc(s.get('track',''))}</span>
    <p class="teaser">{esc(s.get('detail',''))} — <span class="open-hint">点击看完整说明</span></p>
  </button>
</div>"""

    bench_cards = ""
    for b in benchmarks:
        bid_esc = esc(b["id"])
        bench_cards += f"""<button type="button" class="bcard" data-open="bench-{bid_esc}">
<h4>{esc(b.get('handle',''))}</h4>
<p class="muted">{esc(b.get('region',''))} · {esc(b.get('overlap',''))}</p>
<p class="open-hint">点击查看：怎么做的 · 怎么平移</p>
</button>"""

    queue_cards = ""
    for i, q in enumerate(QUEUE_ITEMS, 1):
        qid = esc(q["id"])
        queue_cards += f"""<button type="button" class="qcard" data-open="queue-{qid}">
<span class="qnum">{i}</span>
<strong>{esc(q['title'])}</strong>
<p class="open-hint">点击展开本周怎么做</p>
</button>"""
        all_modals += f"""
<div id="modal-queue-{qid}" class="modal" role="dialog" hidden>
  <div class="modal-inner">
    <button type="button" class="modal-close" data-close="queue-{qid}">×</button>
    <h2>{esc(q['title'])}</h2>
    <div class="rich">{q['body']}</div>
  </div>
</div>"""

    ws = data.get("week_min_success") or {}
    tab_matrix_intro = TAB_INTROS["matrix"]
    tab_translate_intro = TAB_INTROS["translate"]
    tab_steps_intro = TAB_INTROS["steps"]
    tab_queue_intro = TAB_INTROS["queue"]

    doc = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>微步阶梯 · 点击每条看详解 · {rebuilt[:10]}</title>
<style>
:root {{ --bg:#0d1117; --panel:#161b22; --border:#30363d; --text:#e6edf3; --muted:#8b949e; --accent:#58a6ff; --green:#3fb950; }}
* {{ box-sizing:border-box; }}
body {{ margin:0; font-family:"PingFang SC",system-ui,sans-serif; background:var(--bg); color:var(--text); line-height:1.55; }}
.wrap {{ max-width:1280px; margin:0 auto; padding:20px 16px 64px; }}
h1 {{ font-size:1.35rem; margin:0 0 6px; }}
.lead {{ color:var(--muted); font-size:0.88rem; margin-bottom:12px; }}
.tab-intro {{ background:#0d1117; border:1px solid var(--border); border-radius:8px; padding:12px 14px; margin-bottom:14px; font-size:0.88rem; }}
.tab-intro p {{ margin:0 0 8px; }}
nav.tabs {{ display:flex; flex-wrap:wrap; gap:8px; margin-bottom:16px; }}
nav.tabs button {{
  background:var(--panel); border:1px solid var(--border); color:var(--text);
  padding:8px 14px; border-radius:8px; cursor:pointer; font-size:0.88rem;
}}
nav.tabs button.active {{ border-color:var(--accent); color:var(--accent); }}
section.panel {{ display:none; background:var(--panel); border:1px solid var(--border); border-radius:12px; padding:18px; margin-bottom:16px; }}
section.panel.active {{ display:block; }}
.matrix-wrap {{ max-width:720px; margin:0 auto; aspect-ratio:1; }}
.matrix-wrap svg {{ width:100%; height:100%; }}
.owner-center circle {{ fill:#238636; stroke:#3fb950; stroke-width:3; }}
.bench-label, .pillar-label {{ fill:var(--text); font-size:9px; pointer-events:none; }}
.bench-grid {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(240px,1fr)); gap:10px; margin-top:16px; }}
.bcard, .qcard {{
  text-align:left; cursor:pointer; background:#0d1117; border:1px solid var(--border);
  border-radius:8px; padding:12px; color:inherit; width:100%;
}}
.bcard:hover, .qcard:hover, .click-row:hover {{ border-color:var(--accent); }}
.bcard h4 {{ margin:0 0 6px; }}
.qcard {{ display:block; margin-bottom:10px; }}
.qnum {{ display:inline-block; background:#238636; color:#fff; width:28px; height:28px; line-height:28px; text-align:center; border-radius:50%; margin-right:8px; font-weight:700; }}
.open-hint {{ color:var(--accent); font-size:0.75rem; }}
table {{ width:100%; border-collapse:collapse; font-size:0.78rem; }}
th,td {{ border-bottom:1px solid var(--border); padding:8px 4px; text-align:left; vertical-align:top; }}
th {{ color:var(--muted); position:sticky; top:0; background:var(--panel); }}
.click-row {{ cursor:pointer; }}
.click-row:focus {{ outline:2px solid var(--accent); }}
.rank-btn {{ color:var(--accent); font-weight:700; text-decoration:underline; }}
.bar {{ display:inline-block; width:56px; height:6px; background:#21262d; border-radius:3px; vertical-align:middle; margin-right:4px; }}
.bar span {{ display:block; height:100%; background:linear-gradient(90deg,#238636,#58a6ff); border-radius:3px; }}
.fit-cell strong {{ color:var(--green); }}
.badge {{ font-size:0.68rem; padding:2px 6px; border-radius:4px; }}
.track-ip {{ background:#3d2a5f; color:#d2a8ff; }}
.track-fb {{ background:#4a3018; color:#ffa657; }}
.muted {{ color:var(--muted); font-size:0.75rem; }}
.step {{ display:flex; gap:10px; padding:10px 0; border-bottom:1px solid var(--border); align-items:flex-start; }}
.step-open {{ flex:1; background:none; border:none; color:inherit; text-align:left; cursor:pointer; padding:0; font:inherit; }}
.step-open p.teaser {{ margin:6px 0 0; font-size:0.82rem; color:var(--muted); }}
.goal-box {{ background:#0d1117; border:1px solid var(--green); border-radius:8px; padding:12px; margin-bottom:14px; }}
.modal {{
  position:fixed; inset:0; z-index:2000; background:rgba(0,0,0,.75);
  display:flex; align-items:flex-start; justify-content:center; padding:20px 12px; overflow-y:auto;
}}
.modal[hidden] {{ display:none !important; }}
.modal-inner {{
  background:var(--panel); border:1px solid var(--border); border-radius:14px;
  max-width:720px; width:100%; padding:22px 24px 28px; position:relative;
}}
.modal-close {{
  position:absolute; top:12px; right:14px; border:none; background:#21262d;
  color:var(--text); font-size:1.4rem; width:36px; height:36px; border-radius:8px; cursor:pointer;
}}
.modal h2 {{ margin:0 40px 12px 0; font-size:1.15rem; }}
.modal h3 {{ margin:16px 0 6px; font-size:0.95rem; color:#79c0ff; }}
.modal p {{ margin:0 0 10px; font-size:0.9rem; }}
.modal .sub, .modal .evidence {{ color:var(--muted); font-size:0.85rem; }}
.modal .rich ul, .modal .rich ol {{ margin:8px 0; padding-left:1.2rem; }}
footer {{ color:var(--muted); font-size:0.75rem; margin-top:24px; }}
</style>
</head>
<body>
<div class="wrap">
  <h1 id="owner-latest">微步阶梯 · 点序号/标题/卡片看详解</h1>
  <p class="lead">重建 {esc(rebuilt)} · Esc 关闭弹窗 · 勾选微步会保存在本机浏览器</p>
  <div class="goal-box">
    <strong>目标：</strong>{esc(data.get('owner_goal_short',''))}<br/>
    <strong>本周：</strong>发布 ≥{ws.get('publish_min',5)} · IP ≥{ws.get('ip_min',3)} · FB ≤{ws.get('fb_max',2)}
  </div>
  <nav class="tabs">
    <button type="button" class="active" data-tab="matrix">① 对标矩阵</button>
    <button type="button" data-tab="translate">② 平移小视频</button>
    <button type="button" data-tab="steps">③ 18 微步</button>
    <button type="button" data-tab="queue">④ 本周顺序</button>
  </nav>

  <section id="tab-matrix" class="panel active">
    <div class="tab-intro">{tab_matrix_intro}</div>
    <div class="matrix-wrap">
      <svg viewBox="0 0 100 100" preserveAspectRatio="xMidYMid meet">
        {owner_lines}{matrix_lines}{pillar_nodes}
        <g class="owner-center"><circle cx="50%" cy="50%" r="32"/><text x="50%" y="50%" text-anchor="middle" dominant-baseline="middle" fill="#fff" font-size="11px">你</text></g>
        {bench_nodes}
      </svg>
    </div>
    <div class="bench-grid">{bench_cards}</div>
  </section>

  <section id="tab-translate" class="panel">
    <div class="tab-intro">{tab_translate_intro}</div>
    <div class="filter">
      <button type="button" data-filter="all">全部</button>
      <button type="button" data-filter="IP">只看 IP</button>
      <button type="button" data-filter="FB">只看 FB</button>
    </div>
    <div style="overflow-x:auto">
    <table id="fit-table">
      <tr><th>#</th><th>标题（可点）</th><th>对标</th><th>轨</th><th>综合</th><th>经历</th><th>数据</th><th>好拍</th><th>提量</th><th>依据</th></tr>
      {rows}
    </table>
    </div>
  </section>

  <section id="tab-steps" class="panel">
    <div class="tab-intro">{tab_steps_intro}</div>
    {steps_html}
  </section>

  <section id="tab-queue" class="panel">
    <div class="tab-intro">{tab_queue_intro}</div>
    {queue_cards}
  </section>
  <footer>build: build-owner-micro-ladder-html.py · expand: owner_micro_ladder_expand.py</footer>
</div>
{all_modals}
<script>
function openModal(key) {{
  const m = document.getElementById('modal-' + key);
  if (m) {{ m.hidden = false; document.body.style.overflow = 'hidden'; }}
}}
function closeModal(key) {{
  const m = document.getElementById('modal-' + key);
  if (m) {{ m.hidden = true; document.body.style.overflow = ''; }}
}}
document.querySelectorAll('[data-open]').forEach(el => {{
  el.addEventListener('click', e => {{
    if (e.target.closest('input[type=checkbox]')) return;
    openModal(el.getAttribute('data-open'));
  }});
  if (el.classList.contains('click-row') || el.classList.contains('bench-node')) {{
    el.addEventListener('keydown', e => {{ if (e.key === 'Enter' || e.key === ' ') {{ e.preventDefault(); openModal(el.getAttribute('data-open')); }} }});
  }}
}});
document.querySelectorAll('.modal-close').forEach(b => {{
  b.addEventListener('click', () => closeModal(b.getAttribute('data-close')));
}});
document.querySelectorAll('.modal').forEach(m => {{
  m.addEventListener('click', e => {{ if (e.target === m) {{ m.hidden = true; document.body.style.overflow = ''; }} }});
}});
document.addEventListener('keydown', e => {{
  if (e.key === 'Escape') document.querySelectorAll('.modal:not([hidden])').forEach(m => {{ m.hidden = true; document.body.style.overflow = ''; }});
}});
document.querySelectorAll('nav.tabs button').forEach(btn => {{
  btn.addEventListener('click', () => {{
    document.querySelectorAll('nav.tabs button').forEach(b => b.classList.remove('active'));
    document.querySelectorAll('section.panel').forEach(p => p.classList.remove('active'));
    btn.classList.add('active');
    document.getElementById('tab-' + btn.dataset.tab).classList.add('active');
  }});
}});
document.querySelectorAll('.filter button').forEach(btn => {{
  btn.addEventListener('click', () => {{
    const f = btn.dataset.filter;
    document.querySelectorAll('#fit-table tr[data-track]').forEach(tr => {{
      tr.style.display = (f === 'all' || tr.dataset.track === f) ? '' : 'none';
    }});
  }});
}});
const KEY = 'owner-micro-ladder-steps-v2';
document.querySelectorAll('.step input').forEach(inp => {{
  inp.addEventListener('click', e => e.stopPropagation());
  const id = inp.dataset.stepId;
  if (localStorage.getItem(KEY + id) === '1') inp.checked = true;
  inp.addEventListener('change', () => localStorage.setItem(KEY + id, inp.checked ? '1' : '0'));
}});
</script>
</body>
</html>"""
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(doc, encoding="utf-8")
    latest = INBOX / "OWNER-MICRO-LADDER-DELIVERABLE-latest.html"
    latest.write_text(doc, encoding="utf-8")
    print(f"PASS {out}")
    print(f"PASS {latest}")


if __name__ == "__main__":
    day = datetime.now().strftime("%Y-%m-%d")
    build(INBOX / f"OWNER-MICRO-LADDER-DELIVERABLE-{day}.html")
