#!/usr/bin/env python3
"""Visual Owner deliverable for FluteBuddy (metrics, benchmarks CSV, strategy)."""

from __future__ import annotations

import csv
import html
import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INBOX = ROOT / "content/evolution/00-manager/ceo-inbox"
BENCH_JSON = ROOT / "integration/handoff/owner-copy-benchmarks-tier2.json"
BENCH_CSV = ROOT / "integration/handoff/owner-copy-benchmarks-tier2.csv"
STRATEGY = INBOX / "2026-11-05-flutebuddy-xhs-strategy.md"
VIDEOS_JSON = INBOX / "flutebuddy-xhs-videos.json"
FLOOR = 2000


def load_benchmarks() -> list[dict]:
    data = json.loads(BENCH_JSON.read_text(encoding="utf-8"))
    return data.get("items") or []


def write_csv(items: list[dict]) -> None:
    rows: list[dict] = []
    for it in items:
        b = it.get("benchmark") or it
        eng = it.get("engagement") or b.get("engagement") or {}
        metric = eng.get("claps") or eng.get("reactions") or eng.get("likes") or eng.get("claps_label") or ""
        rows.append(
            {
                "platform": it.get("platform") or b.get("platform", ""),
                "author": b.get("author") or it.get("author", ""),
                "title": b.get("title") or it.get("title", ""),
                "url": b.get("url") or it.get("url", ""),
                "metric_value": metric,
                "pass_2000": it.get("pass_2000", ""),
                "steal_one_line": (it.get("steal") or [""])[0] if isinstance(it.get("steal"), list) else "",
            }
        )
    BENCH_CSV.parent.mkdir(parents=True, exist_ok=True)
    with BENCH_CSV.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else ["platform"])
        w.writeheader()
        w.writerows(rows)


def metric_num(item: dict) -> int:
    eng = item.get("engagement") or (item.get("benchmark") or {}).get("engagement") or {}
    for k in ("claps", "reactions", "likes"):
        v = eng.get(k)
        if isinstance(v, int):
            return v
    label = str(eng.get("claps_label") or eng.get("note") or "")
    m = re.search(r"(\d[\d,]*)\s*(K|k|万)?", label)
    if m:
        n = int(m.group(1).replace(",", ""))
        if m.group(2) in ("K", "k"):
            return n * 1000
        if m.group(2) == "万":
            return n * 10000
        return n
    return 0


def bar_width(n: int, cap: int = 50000) -> float:
    if n <= 0:
        return 4.0
    return max(4.0, min(100.0, 100.0 * n / cap))


def load_videos_payload() -> dict:
    if VIDEOS_JSON.is_file():
        return json.loads(VIDEOS_JSON.read_text(encoding="utf-8"))
    return {"videos": [], "notes_for_p0": [], "shoot_order": []}


def build(out: Path) -> None:
    day = datetime.now().strftime("%Y-%m-%d")
    rebuilt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    items = load_benchmarks()
    write_csv(items)
    vp = load_videos_payload()
    videos_list = vp.get("videos") or []
    notes_list = vp.get("notes_for_p0") or []
    shoot_order = vp.get("shoot_order") or [3, 2, 1, 5, 4]

    bench_rows = []
    pass_count = 0
    for it in items:
        b = it.get("benchmark") or it
        n = metric_num(it if it.get("engagement") else {"benchmark": b, "engagement": b.get("engagement")})
        if not n and it.get("pass_2000") is True:
            n = FLOOR
        ok = bool(it.get("pass_2000")) or n >= FLOOR
        if ok:
            pass_count += 1
        plat = (it.get("platform") or b.get("platform") or "?").upper()
        author = b.get("author") or it.get("author") or "—"
        title = b.get("title") or it.get("title") or "—"
        url = b.get("url") or it.get("url") or "#"
        steal = (it.get("steal") or ["—"])[0]
        bench_rows.append(
            f"""<tr>
  <td>{html.escape(plat)}</td>
  <td>{html.escape(author)}</td>
  <td><a href="{html.escape(url)}">{html.escape(title[:72])}</a></td>
  <td class="num">{n:,}</td>
  <td><div class="bar-wrap"><div class="bar" style="width:{bar_width(n):.1f}%"></div></div></td>
  <td>{'✅' if ok else '—'}</td>
  <td class="steal">{html.escape(str(steal)[:120])}</td>
</tr>"""
        )

    video_rows = "".join(
        f"""<tr>
  <td><strong>{v.get('id', '')}</strong><br><span class="steal">{html.escape(v.get('role', ''))}</span></td>
  <td><strong>{html.escape(v.get('title_publish', ''))}</strong>
    <br><span class="steal">封面：{html.escape(v.get('cover_main', ''))} · {html.escape(v.get('cover_sub', ''))}</span>
    <br><span class="steal">搜词：{html.escape(', '.join(v.get('search_keywords') or []))}</span>
    <br><span class="steal">首句：{html.escape(v.get('first_line', ''))}</span></td>
  <td>{html.escape(v.get('shoot', ''))}<br><span class="steal">筛 P0：{html.escape(v.get('filters_p0', ''))}</span></td>
</tr>"""
        for v in videos_list
    )
    note_rows = "".join(
        f"""<tr>
  <td>{html.escape(n.get('type', ''))}</td>
  <td><strong>{html.escape(n.get('title_publish', ''))}</strong></td>
  <td>{html.escape(n.get('hook', ''))}<br><span class="steal">CTA：{html.escape(n.get('cta', ''))}</span></td>
</tr>"""
        for n in notes_list
    )
    shoot_s = " → ".join(str(x) for x in shoot_order)

    doc = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>FluteBuddy · Owner 交付 · {day}</title>
<style>
  :root {{
    --bg: #0f1419;
    --card: #1a2332;
    --accent: #3d9ee5;
    --mint: #5eead4;
    --text: #e7ecf3;
    --muted: #94a3b8;
    --pass: #4ade80;
    --line: #334155;
  }}
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0; font-family: "SF Pro Display", "PingFang SC", sans-serif;
    background: radial-gradient(1200px 600px at 10% -10%, #1e3a5f 0%, var(--bg) 55%);
    color: var(--text); line-height: 1.55; padding: 24px;
  }}
  .wrap {{ max-width: 1100px; margin: 0 auto; }}
  h1 {{ font-size: 1.75rem; margin: 0 0 8px; }}
  .sub {{ color: var(--muted); font-size: 0.95rem; margin-bottom: 24px; }}
  .grid {{ display: grid; gap: 16px; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); margin-bottom: 28px; }}
  .kpi {{
    background: var(--card); border: 1px solid var(--line); border-radius: 14px;
    padding: 18px; position: relative; overflow: hidden;
  }}
  .kpi::after {{
    content: ""; position: absolute; inset: auto -20% -40% auto; width: 120px; height: 120px;
    background: linear-gradient(135deg, var(--accent), transparent); opacity: 0.25; border-radius: 50%;
  }}
  .kpi .label {{ font-size: 0.8rem; color: var(--muted); text-transform: uppercase; letter-spacing: 0.06em; }}
  .kpi .val {{ font-size: 2rem; font-weight: 700; color: var(--mint); }}
  section {{
    background: var(--card); border: 1px solid var(--line); border-radius: 14px;
    padding: 20px 22px; margin-bottom: 20px;
  }}
  h2 {{ font-size: 1.15rem; margin: 0 0 14px; border-left: 4px solid var(--accent); padding-left: 10px; }}
  table {{ width: 100%; border-collapse: collapse; font-size: 0.88rem; }}
  th, td {{ border-bottom: 1px solid var(--line); padding: 10px 8px; text-align: left; vertical-align: top; }}
  th {{ color: var(--muted); font-weight: 600; }}
  td.num {{ font-variant-numeric: tabular-nums; white-space: nowrap; }}
  .bar-wrap {{ background: #0b1220; border-radius: 999px; height: 10px; min-width: 80px; }}
  .bar {{ height: 100%; border-radius: 999px; background: linear-gradient(90deg, var(--accent), var(--mint)); }}
  a {{ color: #7dd3fc; }}
  .steal {{ color: var(--muted); font-size: 0.82rem; }}
  .pill {{
    display: inline-block; background: #243044; color: var(--mint); padding: 4px 10px;
    border-radius: 999px; font-size: 0.78rem; margin-right: 6px;
  }}
  .cta {{ margin-top: 12px; }}
  .cta a {{
    display: inline-block; background: var(--accent); color: #041018; font-weight: 600;
    padding: 10px 16px; border-radius: 8px; text-decoration: none;
  }}
  footer {{ color: var(--muted); font-size: 0.8rem; margin-top: 28px; }}
</style>
</head>
<body>
<div class="wrap">
  <h1>FluteBuddy · 一小撮练琴家庭</h1>
  <p class="sub">Owner 专用交付 · 重建 {rebuilt} · 非 Discovery FILTER 页 ·
  对标 CSV：<code>{html.escape(str(BENCH_CSV.relative_to(ROOT)))}</code></p>

  <div class="grid">
    <div class="kpi"><div class="label">过关范文（≥2k 互动）</div><div class="val">{pass_count}/{len(items)}</div></div>
    <div class="kpi"><div class="label">P0 内测目标家庭</div><div class="val">40</div></div>
    <div class="kpi"><div class="label">首发视频</div><div class="val">5</div></div>
    <div class="kpi"><div class="label">FluteBuddy 内容占比</div><div class="val">~30%</div></div>
  </div>

  <section>
    <h2>产品一句话</h2>
    <p><span class="pill">FluteBuddy</span> 乐谱 PDF + 录音 → 节奏 / 音准 / 音质 → 扣分明细 + 谱面定位 + 短句教练反馈。</p>
    <p>Essence：让老师重新当教授，让孩子敢自己练，让家长<strong>不必当裁判</strong>。</p>
    <p class="cta"><a href="#videos">↓ 五支视频脚本</a>
    <a href="#benchmarks" style="margin-left:8px;background:#243044;color:#e7ecf3">文案对标表</a></p>
    <p class="steal">文笔标准：V-Tier · 对齐 40–50 万粉大 V 写法（见 docs/OWNER-COPY-V-TIER-400K-MANDATE.md）· Owner 终检文笔。</p>
  </section>

  <section>
    <h2>P0 是谁</h2>
    <table>
      <tr><th>层级</th><th>人群</th><th>为什么 match</th></tr>
      <tr><td><strong>P0</strong></td><td>有 PDF 谱、练完问「对吗」的学生 + 陪伴型家长</td><td>路径 1:1 对齐产品</td></tr>
      <tr><td>P1</td><td>10–50 学生的长笛老师 / 工作室</td><td>基础问题在家解决，课上演音乐性</td></tr>
      <tr><td>P2</td><td>听见 Daily / 古典粉</td><td>认专业后再进 waitlist，不硬推</td></tr>
    </table>
  </section>

  <section id="videos">
    <h2>视频 · 5 条发布标题（定稿 · 筛一小撮 P0）</h2>
    <p class="steal">P0 一句话：{html.escape(vp.get('p0_one_line', ''))}</p>
    <table>
      <tr><th># / 用途</th><th><strong>小红书标题 + 封面 + 搜词 + 首句</strong></th><th>拍什么 · 怎么筛人</th></tr>
      {video_rows or "<tr><td colspan='3'>缺少 flutebuddy-xhs-videos.json</td></tr>"}
    </table>
    <p style="margin-top:12px;color:var(--muted)">拍摄顺序：{html.escape(shoot_s)} · 置顶 #{vp.get('pin_video', 1)}</p>
  </section>

  <section id="notes">
    <h2>笔记标题（3 篇 · 配合视频找对人）</h2>
    <table>
      <tr><th>类型</th><th>发布标题</th><th>钩子 · CTA</th></tr>
      {note_rows or "<tr><td colspan='3'>—</td></tr>"}
    </table>
  </section>

  <section id="benchmarks">
    <h2>文案对标 · 2000+ 互动（Agent 自搜 · 页面核对）</h2>
    <table>
      <tr>
        <th>平台</th><th>作者</th><th>作品</th><th>互动</th><th></th><th>≥2k</th><th>学一句</th>
      </tr>
      {''.join(bench_rows)}
    </table>
    <p class="cta"><a href="file://{BENCH_CSV.resolve()}">下载 CSV</a></p>
  </section>

  <section>
    <h2>小红书怎么找对人</h2>
    <ul>
      <li>搜词：长笛练习、居家练琴、错音、节奏、长笛家长</li>
      <li>简介：FluteBuddy：上传谱面+录音，练完就知道错在哪。</li>
      <li>评论筛问：错音 / 节奏 / 不敢问老师？</li>
      <li>私信三问 → 只邀 P0 内测 · 关键词 <strong>FluteBuddy</strong></li>
    </ul>
  </section>

  <footer>
    danying-brand-agent · <code>scripts/build-owner-flutebuddy-deliverable-html.py</code> ·
    策略全文：<code>{html.escape(str(STRATEGY.relative_to(ROOT)) if STRATEGY.is_file() else "")}</code> ·
    Brief：<code>content/xiaohongshu/2026-11-05-flutebuddy-practice-waitlist-brief.md</code>
  </footer>
</div>
</body>
</html>"""
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(doc, encoding="utf-8")


def main() -> int:
    day = datetime.now().strftime("%Y-%m-%d")
    out = INBOX / f"OWNER-FLUTEBUDDY-DELIVERABLE-{day}.html"
    build(out)
    print("PASS", out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
