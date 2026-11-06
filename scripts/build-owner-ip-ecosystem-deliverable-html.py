#!/usr/bin/env python3
"""Visual Owner deliverable · personal IP ecosystem (XHS + LinkedIn + Medium)."""

from __future__ import annotations

import csv
import html
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INBOX = ROOT / "content/evolution/00-manager/ceo-inbox"
CONTENT = INBOX / "owner-ip-ecosystem-content.json"
TRACK = ROOT / "integration/handoff/owner-ip-track.json"
CREATORS_JSON = ROOT / "integration/handoff/owner-ip-benchmark-creators.json"
CSV_OUT = INBOX / "owner-ip-ecosystem-dimensions.csv"
CSV_CREATORS = INBOX / "owner-ip-benchmark-creators.csv"


def drive_url(file_id: str) -> str:
    return f"https://drive.google.com/file/d/{file_id}/view"


def build(out: Path) -> None:
    rebuilt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    day = datetime.now().strftime("%Y-%m-%d")
    data = json.loads(CONTENT.read_text(encoding="utf-8"))
    dims = data.get("dimensions") or []
    plats = data.get("platforms") or {}
    hydrate = data.get("drive_hydrate") or []
    story_sources = data.get("story_sources") or []
    creators: list[dict] = []
    if CREATORS_JSON.is_file():
        creators = json.loads(CREATORS_JSON.read_text(encoding="utf-8")).get("items") or []

    CSV_OUT.parent.mkdir(parents=True, exist_ok=True)
    with CSV_OUT.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["id", "label", "share_pct", "signal"])
        w.writeheader()
        for d in dims:
            w.writerow({k: d.get(k, "") for k in ("id", "label", "share_pct", "signal")})
    if creators:
        with CSV_CREATORS.open("w", encoding="utf-8", newline="") as f:
            fields = ["platform", "handle", "followers_approx", "persona", "steal_for_danying", "url"]
            w = csv.DictWriter(f, fieldnames=fields)
            w.writeheader()
            for c in creators:
                w.writerow(
                    {
                        "platform": c.get("platform", ""),
                        "handle": c.get("handle", ""),
                        "followers_approx": c.get("followers_approx", ""),
                        "persona": c.get("persona", ""),
                        "steal_for_danying": (c.get("steal_for_danying") or [""])[0]
                        if isinstance(c.get("steal_for_danying"), list)
                        else c.get("steal_for_danying", ""),
                        "url": c.get("url", ""),
                    }
                )

    story_li = "".join(f"<li>{html.escape(s)}</li>" for s in story_sources)
    creator_rows = "".join(
        f"""<tr>
  <td>{html.escape(c.get('platform', ''))}</td>
  <td><strong>{html.escape(c.get('handle', ''))}</strong><br><span class="steal">{html.escape(c.get('followers_approx', ''))}</span></td>
  <td>{html.escape(c.get('persona', ''))}<br><span class="steal">生态：{html.escape(', '.join(c.get('ecosystem') or []))}</span></td>
  <td class="steal">{html.escape((c.get('steal_for_danying') or [''])[0] if isinstance(c.get('steal_for_danying'), list) else c.get('steal_for_danying', ''))}</td>
  <td>{f'<a href="{html.escape(c.get("url", ""))}">链接</a>' if c.get('url') else '—'}</td>
</tr>"""
        for c in creators
    )

    dim_rows = "".join(
        f"""<tr>
  <td>{html.escape(d.get('label', ''))}</td>
  <td class="num">{d.get('share_pct', 0)}%</td>
  <td><div class="bar-wrap"><div class="bar" style="width:{min(100, int(d.get('share_pct', 0)))}%"></div></div></td>
  <td class="steal">{html.escape(d.get('signal', ''))}</td>
</tr>"""
        for d in dims
    )

    plat_blocks = []
    for key, label, color in (
        ("xiaohongshu", "小红书", "#f472b6"),
        ("linkedin", "LinkedIn", "#60a5fa"),
        ("medium", "Medium", "#a78bfa"),
    ):
        p = plats.get(key) or {}
        titles = p.get("starter_titles") or []
        li = "".join(f"<li><strong>{html.escape(t)}</strong></li>" for t in titles)
        plat_blocks.append(
            f"""<article class="plat" style="border-top:3px solid {color}">
  <h3>{label}</h3>
  <p class="steal">{html.escape(p.get('cadence', ''))}</p>
  <p class="steal">形态：{html.escape(', '.join(p.get('formats') or []))}</p>
  <ul>{li}</ul>
</article>"""
        )

    drive_rows = "".join(
        f"""<tr>
  <td><a href="{drive_url(h['file_id'])}">{html.escape(h.get('title', ''))}</a></td>
  <td><code>{html.escape(h.get('file_id', ''))}</code></td>
</tr>"""
        for h in hydrate
    )

    doc = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>张丹瀛 · 个人 IP 生态链 · {day}</title>
<style>
  :root {{
    --bg: #120f18; --card: #1f1a28; --text: #f3eef8; --muted: #a89bb8;
    --accent: #c084fc; --gold: #fbbf24; --line: #3d3450;
  }}
  body {{
    margin:0; font-family: "PingFang SC", -apple-system, sans-serif;
    background: radial-gradient(900px 500px at 90% 0%, #4c1d95 0%, var(--bg) 50%);
    color: var(--text); padding: 24px; line-height: 1.55;
  }}
  .wrap {{ max-width: 1100px; margin: 0 auto; }}
  h1 {{ font-size: 1.7rem; margin: 0 0 6px; }}
  .sub {{ color: var(--muted); margin-bottom: 22px; font-size: 0.92rem; }}
  .grid {{ display: grid; gap: 14px; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); margin-bottom: 22px; }}
  .kpi {{ background: var(--card); border: 1px solid var(--line); border-radius: 12px; padding: 16px; }}
  .kpi .v {{ font-size: 1.6rem; font-weight: 700; color: var(--gold); }}
  .kpi .l {{ font-size: 0.75rem; color: var(--muted); text-transform: uppercase; letter-spacing: .05em; }}
  section {{ background: var(--card); border: 1px solid var(--line); border-radius: 14px; padding: 18px 20px; margin-bottom: 18px; }}
  h2 {{ font-size: 1.1rem; margin: 0 0 12px; border-left: 4px solid var(--accent); padding-left: 10px; }}
  table {{ width: 100%; border-collapse: collapse; font-size: 0.88rem; }}
  th, td {{ border-bottom: 1px solid var(--line); padding: 9px 8px; text-align: left; vertical-align: top; }}
  th {{ color: var(--muted); }}
  .num {{ font-variant-numeric: tabular-nums; }}
  .bar-wrap {{ background: #0d0a12; border-radius: 999px; height: 8px; }}
  .bar {{ height: 100%; border-radius: 999px; background: linear-gradient(90deg, var(--accent), var(--gold)); }}
  .steal {{ color: var(--muted); font-size: 0.82rem; }}
  .plat-grid {{ display: grid; gap: 14px; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); }}
  .plat {{ background: #17121f; border-radius: 10px; padding: 14px; }}
  .plat ul {{ margin: 8px 0 0; padding-left: 18px; }}
  a {{ color: #e9d5ff; }}
  .pill {{ display:inline-block; background:#2e1065; color:#e9d5ff; padding:3px 10px; border-radius:999px; font-size:0.78rem; margin-right:6px; }}
  footer {{ color: var(--muted); font-size: 0.78rem; margin-top: 24px; }}
</style>
</head>
<body>
<div class="wrap">
  <h1>张丹瀛 / Danying · 个人 IP 生态链</h1>
  <p class="sub">Owner 专用 · 重建 {rebuilt} · 轨 <code>personal_ip_ecosystem</code> ·
  文笔 <strong>V-Tier 40–50万粉大 V</strong>（docs/OWNER-COPY-V-TIER-400K-MANDATE.md · Owner 终检）·
  FluteBuddy 产品轨见 <code>OWNER-FLUTEBUDDY-DELIVERABLE</code> · CSV：
  <code>{html.escape(str(CSV_OUT.relative_to(ROOT)))}</code></p>

  <div class="grid">
    <div class="kpi"><div class="l">Drive 参考</div><div class="v">434</div></div>
    <div class="kpi"><div class="l">内容维度</div><div class="v">{len(dims)}</div></div>
    <div class="kpi"><div class="l">产品露出上限</div><div class="v">30%</div></div>
    <div class="kpi"><div class="l">平台</div><div class="v">3</div></div>
  </div>

  <section>
    <h2>人即品牌</h2>
    <p><span class="pill">{html.escape(data.get('owner_zh', ''))}</span>
    <span class="pill">{html.escape(data.get('owner_en', ''))}</span></p>
    <p>{html.escape(data.get('one_line', ''))}</p>
    <p class="steal">{html.escape(data.get('ultimate_goal', ''))}</p>
    <p><strong>{html.escape(data.get('product_cap', ''))}</strong></p>
    <p class="steal" style="margin-top:10px">{html.escape(data.get('life_ecosystem_principle', ''))}</p>
  </section>

  <section id="life">
    <h2>真实生态链 · 写什么故事（≥40% 生活/关系/态度）</h2>
    <ul>{story_li}</ul>
    <p class="steal">对标账号学「结构+私人感」，不抄谢胜子式人设；你是法派长笛+听见，不是泛女性成长号。</p>
  </section>

  <section id="benchmarks">
    <h2>深扒对标博主 / 大 V（Agent 自搜 · 可复核）</h2>
    <table>
      <tr><th>平台</th><th>账号 · 粉丝约</th><th>人设 · 生态链</th><th>张丹瀛可学什么</th><th></th></tr>
      {creator_rows or "<tr><td colspan='5'>—</td></tr>"}
    </table>
    <p class="steal"><a href="file://{CSV_CREATORS.resolve() if CSV_CREATORS.is_file() else '#'}">下载对标 CSV</a> · JSON：integration/handoff/owner-ip-benchmark-creators.json</p>
  </section>

  <section id="dimensions">
    <h2>内容配比（生活+关系优先，专业托底）</h2>
    <table>
      <tr><th>切面</th><th>建议占比</th><th></th><th>读者应感受到</th></tr>
      {dim_rows}
    </table>
    <p class="steal"><a href="file://{CSV_OUT.resolve()}">下载维度 CSV</a></p>
  </section>

  <section id="platforms">
    <h2>三平台 · 首发选题（标题定稿级）</h2>
    <div class="plat-grid">{''.join(plat_blocks)}</div>
  </section>

  <section id="drive">
    <h2>Google Drive · hydrate 优先（IP / 小红书 / 创始人）</h2>
    <table>
      <tr><th>资料</th><th>file id</th></tr>
      {drive_rows}
    </table>
    <p class="steal">全库索引：{html.escape(data.get('corpus_screen_dir', ''))}/INDEX.md</p>
  </section>

  <footer>
    {html.escape(str(TRACK.relative_to(ROOT)))} ·
    {html.escape(str(CONTENT.relative_to(ROOT)))} ·
    docs/CEO-DUAL-TRACK-WORKFLOWS.md
  </footer>
</div>
</body>
</html>"""
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(doc, encoding="utf-8")


def main() -> int:
    day = datetime.now().strftime("%Y-%m-%d")
    out = INBOX / f"OWNER-IP-ECOSYSTEM-DELIVERABLE-{day}.html"
    build(out)
    print("PASS", out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
