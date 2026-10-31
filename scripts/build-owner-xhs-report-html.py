#!/usr/bin/env python3
"""Build Owner-facing HTML report (Discovery popups + artist table). MD = source only."""

from __future__ import annotations

import csv
import html
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from xhs_brief_longform import extract_longform_text  # noqa: E402
INBOX = ROOT / "content/evolution/00-manager/ceo-inbox"
IP = ROOT / "content/ip-research"
XHS = ROOT / "content/xiaohongshu"


def md_block(text: str) -> str:
    return html.escape(text).replace("\n", "<br>\n")


def extract_brief_sections(path: Path) -> dict[str, str]:
    raw = path.read_text(encoding="utf-8")
    title_m = re.search(r"^#\s+(.+)$", raw, re.M)
    subj_m = re.search(r'"subject":\s*"([^"]+)"', raw)
    body_m = re.search(r'"body":\s*"([^"]+)"', raw, re.S)
    return {
        "file": path.name,
        "heading": title_m.group(1) if title_m else path.stem,
        "subject": subj_m.group(1) if subj_m else "",
        "classifier_body": body_m.group(1) if body_m else "",
        "full_md": raw,
    }


def load_publish_sections() -> dict[str, str]:
    q = XHS / "2026-10-20-publish-ready-queue.md"
    if not q.is_file():
        return {}
    text = q.read_text(encoding="utf-8")
    out: dict[str, str] = {}
    for n in ("1", "2", "3"):
        pat = rf"## 篇 {n} ·[^\n]+\n([\s\S]*?)(?=\n---|\n## 篇|\Z)"
        m = re.search(pat, text)
        if m:
            out[f"discovery-0{n}"] = m.group(1).strip()
    return out


def write_artist_csv_xlsx() -> tuple[Path, Path]:
    screened = json.loads((IP / "artist-watchlist-screened.json").read_text(encoding="utf-8"))
    csv_path = IP / "artist-watchlist-four-metrics.csv"
    rows: list[dict] = []
    for a in screened.get("artists") or []:
        m = a.get("benchmark_metrics") or {}
        urls = " | ".join(a.get("urls") or [])
        rows.append(
            {
                "name": a.get("name"),
                "slug": a.get("slug"),
                "priority_tier": a.get("priority_tier"),
                "composite": a.get("borrow_score_composite"),
                "DB": m.get("directional_benchmarking", {}).get("score"),
                "PLD": m.get("pixel_level_deconstruction", {}).get("score"),
                "APO": m.get("audience_persona_overlap", {}).get("score"),
                "CTD": m.get("core_topic_density", {}).get("score"),
                "DB_rationale": m.get("directional_benchmarking", {}).get("rationale"),
                "PLD_rationale": m.get("pixel_level_deconstruction", {}).get("rationale"),
                "APO_rationale": m.get("audience_persona_overlap", {}).get("rationale"),
                "CTD_rationale": m.get("core_topic_density", {}).get("rationale"),
                "urls": urls,
            }
        )
    fields = list(rows[0].keys()) if rows else []
    with csv_path.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    xlsx_path = IP / "artist-watchlist-four-metrics.xlsx"
    venv_site = ROOT / ".venv"
    if venv_site.is_dir():
        import site

        site.addsitedir(str(venv_site / "lib" / f"python{sys.version_info.major}.{sys.version_info.minor}" / "site-packages"))
    try:
        import openpyxl  # noqa: F401

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Artist DB PLD APO CTD"
        ws.append(fields)
        for r in rows:
            ws.append([r.get(k) for k in fields])
        wb.save(xlsx_path)
    except ImportError:
        xlsx_path = csv_path  # fallback note in html
    return csv_path, xlsx_path


def latest_test_brief_block() -> tuple[str, str]:
    """Return (cards_html, modal_html) for workflow test brief, or empty."""
    cands = sorted(XHS.glob("*-test-brief.md"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not cands:
        return "", ""
    b = extract_brief_sections(cands[0])
    slug = cands[0].name.replace("-brief.md", "")
    gap_path = ROOT / "content/evolution/04-xhs-topic-manager" / slug / "EVOLUTION-GAP-latest.md"
    gap_status = "—"
    if gap_path.is_file():
        m = re.search(r"`(READY|NEEDS_WORK)`", gap_path.read_text(encoding="utf-8"))
        if m:
            gap_status = m.group(1)
    subj = b["subject"] or "—"
    body = b["classifier_body"] or ""
    test_href = f"OWNER-WORKFLOW-TEST-ARTICLE-{datetime.now().strftime('%Y-%m-%d')}.html"
    card = f"""
<article class="card" style="border:2px solid #0a7;grid-column:1/-1">
  <h3>工作流测试稿 · 全链路（最新）</h3>
  <p><strong>Evolution {html.escape(gap_status)}</strong> · 文件：<code>{html.escape(b['file'])}</code></p>
  <p class="title">标题：{html.escape(subj)}</p>
  <p style="font-size:0.9rem">{html.escape(body[:180])}{'…' if len(body) > 180 else ''}</p>
  <button onclick="openModal('modal-workflow-test')">弹出 · 测试稿全文</button>
  <a href="{html.escape(test_href)}" style="margin-left:12px">打开专用页 →</a>
</article>"""
    modal = f"""
<div id="modal-workflow-test" class="modal" onclick="if(event.target===this)closeModal('modal-workflow-test')">
  <div class="modal-inner">
    <button class="close" onclick="closeModal('modal-workflow-test')">×</button>
    <h2>工作流测试稿 · {html.escape(subj)}</h2>
    <p class="meta">Evolution {html.escape(gap_status)} · <code>{html.escape(b['file'])}</code></p>
    <h3>可发帖正文</h3>
    <div class="box">{md_block(body)}</div>
    <h3>Brief 全文</h3>
    <div class="box brief">{md_block(b['full_md'])}</div>
  </div>
</div>"""
    return card, modal


def _is_series_or_test_brief(path: Path) -> bool:
    name = path.name
    if name.endswith("-test-brief.md"):
        return True
    if re.match(r"2026-10-17-discovery-0[1-4]-", name):
        return True
    return False


def latest_owner_brief_block() -> tuple[str, str]:
    """Owner 指定新稿（非 Discovery / 非 test）· 弹出层卡片。"""
    extra = os.environ.get("CEO_OWNER_EXTRA_BRIEF", "").strip()
    path: Path | None = None
    if extra:
        p = ROOT / extra if not extra.startswith("/") else Path(extra)
        if p.is_file():
            path = p
    if path is None:
        cands = [
            p
            for p in XHS.glob("*-brief.md")
            if p.is_file() and not _is_series_or_test_brief(p)
        ]
        cands.sort(key=lambda p: p.stat().st_mtime, reverse=True)
        path = cands[0] if cands else None
    if path is None:
        return "", ""
    b = extract_brief_sections(path)
    slug = path.name.replace("-brief.md", "")
    gap_path = ROOT / "content/evolution/04-xhs-topic-manager" / slug / "EVOLUTION-GAP-latest.md"
    gap_status = "—"
    if gap_path.is_file():
        m = re.search(r"`(READY|NEEDS_WORK)`", gap_path.read_text(encoding="utf-8"))
        if m:
            gap_status = m.group(1)
    subj = b["subject"] or "—"
    body = b["classifier_body"] or ""
    longform = extract_longform_text(path)
    display_body = longform if longform else body
    card = f"""
<article class="card" id="owner-latest" style="border:2px solid #06c;grid-column:1/-1">
  <h3>Owner 指定新稿（最新）</h3>
  <p><strong>Evolution {html.escape(gap_status)}</strong> · 文件：<code>{html.escape(b['file'])}</code></p>
  <p class="title">标题：{html.escape(subj)}</p>
  <p style="font-size:0.9rem">{html.escape(display_body[:180])}{'…' if len(display_body) > 180 else ''}</p>
  <button onclick="openModal('modal-owner-latest')">弹出 · 新稿全文（长稿优先）</button>
</article>"""
    modal = f"""
<div id="modal-owner-latest" class="modal" onclick="if(event.target===this)closeModal('modal-owner-latest')">
  <div class="modal-inner">
    <button class="close" onclick="closeModal('modal-owner-latest')">×</button>
    <h2>Owner 指定新稿 · {html.escape(subj)}</h2>
    <p class="meta">Evolution {html.escape(gap_status)} · <code>{html.escape(b['file'])}</code></p>
    <h3>{'长稿 · Owner 发布版' if longform else '可发帖正文'}</h3>
    <div class="box">{md_block(display_body)}</div>
    {f'<h3>列表摘要（classifier）</h3><div class="box">{md_block(body)}</div>' if longform and body else ''}
    <h3>Brief 全文</h3>
    <div class="box brief">{md_block(b['full_md'])}</div>
  </div>
</div>"""
    return card, modal


def build_html(out_path: Path) -> None:
    date = datetime.now().strftime("%Y-%m-%d")
    rebuilt_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    csv_path, xlsx_path = write_artist_csv_xlsx()
    publish = load_publish_sections()
    test_card, test_modal = latest_test_brief_block()
    owner_card, owner_modal = latest_owner_brief_block()
    discoveries = [
        ("discovery-01", "认知期 #1 · 不可替代性", XHS / "2026-10-17-discovery-01-irreplaceability-brief.md", 1),
        ("discovery-02", "认知期 #2 · 叙事而非硬广", XHS / "2026-10-17-discovery-02-narrative-not-ads-brief.md", 2),
        ("discovery-03", "认知期 #3 · 专业信任", XHS / "2026-10-17-discovery-03-professional-trust-brief.md", 3),
        ("discovery-04", "认知期 #4 · 轻收口", XHS / "2026-10-17-discovery-04-open-close-brief.md", 4),
    ]

    modal_blocks = []
    cards = []
    for key, label, path, num in discoveries:
        b = extract_brief_sections(path)
        pub = publish.get(key) or b.get("classifier_body") or "_（正文见 Brief 全文）_"
        modal_id = f"modal-d{num:02d}"
        body_html = md_block(b["full_md"])
        pub_html = md_block(pub if isinstance(pub, str) else str(pub))
        modal_blocks.append(
            f"""
<div id="{modal_id}" class="modal" onclick="if(event.target===this)closeModal('{modal_id}')">
  <div class="modal-inner">
    <button class="close" onclick="closeModal('{modal_id}')">×</button>
    <h2>{html.escape(label)}</h2>
    <p class="meta">文件：<code>{html.escape(b['file'])}</code></p>
    <h3>可直发 / 正文区</h3>
    <div class="box">{pub_html}</div>
    <h3>Brief 全文</h3>
    <div class="box brief">{body_html}</div>
  </div>
</div>"""
        )
        rec = "首推发表" if num == 1 else f"队列 #{num}"
        cards.append(
            f"""
<article class="card">
  <h3>{html.escape(label)}</h3>
  <p><strong>Discovery 0{num}</strong> · 推荐：{rec}</p>
  <p class="title">标题：{html.escape(b['subject'] or '—')}</p>
  <button onclick="openModal('{modal_id}')">弹出全文 · Brief + 正文</button>
</article>"""
        )

    artist_rows = ""
    screened = json.loads((IP / "artist-watchlist-screened.json").read_text(encoding="utf-8"))
    for a in screened.get("artists") or []:
        m = a.get("benchmark_metrics") or {}
        artist_rows += f"""<tr>
          <td>{html.escape(str(a.get('priority_tier')))}</td>
          <td>{html.escape(str(a.get('name')))}</td>
          <td>{a.get('borrow_score_composite')}</td>
          <td>{m.get('directional_benchmarking',{}).get('score')}</td>
          <td>{m.get('pixel_level_deconstruction',{}).get('score')}</td>
          <td>{m.get('audience_persona_overlap',{}).get('score')}</td>
          <td>{m.get('core_topic_density',{}).get('score')}</td>
          <td>{html.escape(' · '.join(a.get('urls') or []))}</td>
        </tr>"""

    xlsx_link = xlsx_path.relative_to(ROOT) if xlsx_path.suffix == ".xlsx" else csv_path.relative_to(ROOT)

    doc = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>Owner 交付 · 小红书筛选 · {date}</title>
<style>
  :root {{ font-family: -apple-system, "PingFang SC", sans-serif; line-height: 1.5; }}
  body {{ max-width: 960px; margin: 0 auto; padding: 24px; background: #fafafa; color: #1a1a1a; }}
  h1 {{ font-size: 1.5rem; }}
  .glossary {{ background: #fff; border: 1px solid #ddd; border-radius: 8px; padding: 16px; margin: 16px 0; }}
  .cards {{ display: grid; gap: 12px; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); }}
  .card {{ background: #fff; border-radius: 8px; padding: 16px; box-shadow: 0 1px 3px rgba(0,0,0,.08); }}
  .card button {{ margin-top: 8px; padding: 8px 12px; cursor: pointer; background: #111; color: #fff; border: none; border-radius: 6px; }}
  table {{ width: 100%; border-collapse: collapse; background: #fff; font-size: 0.85rem; }}
  th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; vertical-align: top; }}
  th {{ background: #f0f0f0; }}
  .modal {{ display: none; position: fixed; inset: 0; background: rgba(0,0,0,.5); z-index: 100; overflow: auto; }}
  .modal.open {{ display: flex; align-items: flex-start; justify-content: center; padding: 40px 16px; }}
  .modal-inner {{ background: #fff; max-width: 720px; width: 100%; padding: 24px; border-radius: 12px; position: relative; }}
  .close {{ position: absolute; right: 12px; top: 8px; font-size: 28px; border: none; background: none; cursor: pointer; }}
  .box {{ background: #f6f6f6; padding: 12px; border-radius: 6px; max-height: 40vh; overflow: auto; font-size: 0.9rem; }}
  .brief {{ max-height: 50vh; }}
  a {{ color: #0645ad; }}
  .open-hint {{ background: #fff3cd; border: 1px solid #ffc107; padding: 12px; border-radius: 8px; }}
</style>
</head>
<body>
<h1>Owner 交付 · CEO 小红书资料筛选 · {date}</h1>
<p class="open-hint">HTML 重建时间：<strong>{rebuilt_at}</strong> · 脚本 <code>build-owner-xhs-report-html.py</code>。
若在 Cursor 里只看到代码：Finder 双击本文件。工作流测试稿（若有）在下方<strong>绿色边框</strong>卡片。</p>

<section class="glossary">
<h2>名词说明</h2>
<p><strong>Gate（Owner Gate）</strong>：内部质检，不是让你跑的命令。Agent 在交给你之前用
<code>manager-ceo-owner-gate.sh</code> + Brief 的 <code>evaluate-xhs-topic</code>（05 分类器）检查是否
<code>aligned: true</code>、redteam-pre 是否齐全。<strong>「待 Gate」</strong> = 当时批量脚本未重跑 Gate，不代表内容一定不合格；Discovery 01 在 Brief 里已有
<code>aligned: true</code> 记录（2026-10-17）。</p>
<p><strong>优先级（本报告）</strong>：按<strong>认知期发帖顺序 + 数据策略</strong>，不是 evaluate 退出码排序。
<strong>#1 Discovery 01</strong> = 不可替代性（首推）；02 叙事；03 专业信任；04 轻收口（#1–3 发后再发）。</p>
<p><strong>Discovery 01 是什么？</strong> 文件
<code>2026-10-17-discovery-01-irreplaceability-brief.md</code>，认知期 #1（与<strong>工作流测试稿</strong>同案例线：NGV×Cartier×MSO 等）。标题以 Brief 重建为准。</p>
<p><strong>系列统一：</strong> 测试稿 + Discovery 01–04 共用动线/三问语言；HTML 重建时从 classifier 读取。</p>
</section>

<h2>Owner 新稿 + 工作流测试 + Discovery 01–04 · 点击弹出</h2>
<div class="cards">
{owner_card}{test_card}{"".join(cards)}
</div>

<h2>Artist 四指标（DB / PLD / APO / CTD）</h2>
<p>Excel/CSV：<a href="../../../../ip-research/{xlsx_link.name}">{xlsx_link}</a>（用 Excel 或 Numbers 打开）</p>
<table>
<thead><tr><th>Tier</th><th>Artist</th><th>Composite</th><th>DB</th><th>PLD</th><th>APO</th><th>CTD</th><th>URLs</th></tr></thead>
<tbody>{artist_rows}</tbody>
</table>

<p style="margin-top:32px;color:#666;font-size:0.85rem">danying-brand-agent · HTML Owner 报告 · 以后 CEO 交付以 HTML 为准</p>
{owner_modal}{test_modal}{"".join(modal_blocks)}
<script>
function openModal(id) {{ document.getElementById(id).classList.add('open'); document.body.style.overflow='hidden'; }}
function closeModal(id) {{ document.getElementById(id).classList.remove('open'); document.body.style.overflow=''; }}
document.addEventListener('keydown', e => {{ if (e.key==='Escape') document.querySelectorAll('.modal.open').forEach(m => closeModal(m.id)); }});
(function() {{
  var h = (location.hash || '').replace(/^#/, '');
  if (h === 'owner-latest' && document.getElementById('modal-owner-latest')) {{
    openModal('modal-owner-latest');
  }}
}})();
</script>
</body>
</html>"""
    out_path.write_text(doc, encoding="utf-8")


def main() -> int:
    INBOX.mkdir(parents=True, exist_ok=True)
    day = datetime.now().strftime("%Y-%m-%d")
    out = INBOX / f"OWNER-XHS-FILTER-DELIVERABLE-{day}.html"
    build_html(out)
    print("PASS", out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
