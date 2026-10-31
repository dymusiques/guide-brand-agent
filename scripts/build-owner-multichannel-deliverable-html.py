#!/usr/bin/env python3
"""Owner multichannel HTML: XHS longform + LinkedIn carousel + images · popup delivery."""

from __future__ import annotations

import html
import re
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from xhs_brief_longform import extract_longform_text  # noqa: E402

INBOX = ROOT / "content/evolution/00-manager/ceo-inbox"
ASSETS = INBOX / "assets/2026-10-30-musicians-linkedin"
LINKEDIN_MD = ROOT / "content/marketing/linkedin/2026-10-30-musicians-business-cognition-carousel-en.md"
BRIEF = ROOT / "content/xiaohongshu/2026-10-30-musicians-who-love-music-brief.md"


def md_block(text: str) -> str:
    return html.escape(text).replace("\n", "<br>\n")


def parse_linkedin_slides(md: Path) -> tuple[list[dict], str]:
    text = md.read_text(encoding="utf-8")
    slides: list[dict] = []
    for chunk in re.split(r"\n---\n", text):
        if "## Slide" not in chunk:
            continue
        title_m = re.search(r"## (Slide \d+[^\n]*)", chunk)
        head_m = re.search(r"\*\*Headline:\*\*\s*(.+)", chunk)
        body_m = re.search(r"\*\*Body:\*\*\s*(.+)", chunk)
        img_m = re.search(r"\*\*Image:\*\*\s*`([^`]+)`", chunk)
        slides.append(
            {
                "title": title_m.group(1) if title_m else "Slide",
                "headline": head_m.group(1).strip() if head_m else "",
                "body": body_m.group(1).strip() if body_m else "",
                "image": img_m.group(1) if img_m else "",
            }
        )
    cap_m = re.search(r"## Long caption[^\n]*\n\n([\s\S]+?)(?=\n#|$)", text)
    caption = cap_m.group(1).strip() if cap_m else ""
    return slides, caption


def main() -> int:
    day = datetime.now().strftime("%Y-%m-%d")
    out = INBOX / f"OWNER-MULTICHANNEL-DELIVERABLE-{day}.html"
    longform = extract_longform_text(BRIEF) if BRIEF.is_file() else ""
    subj = "世界不缺音乐家，缺的是还热爱音乐的人"
    if BRIEF.is_file():
        m = re.search(r'"subject":\s*"([^"]+)"', BRIEF.read_text(encoding="utf-8"))
        if m:
            subj = m.group(1)
    slides, caption = parse_linkedin_slides(LINKEDIN_MD) if LINKEDIN_MD.is_file() else ([], "")

    slide_html = ""
    modals = ""
    for i, s in enumerate(slides, 1):
        img_path = ASSETS / s["image"] if s.get("image") else None
        img_src = f"assets/2026-10-30-musicians-linkedin/{s['image']}" if img_path and img_path.is_file() else ""
        mid = f"modal-li-{i}"
        slide_html += f"""
<article class="card">
  <h3>{html.escape(s['title'])}</h3>
  {f'<img src="{html.escape(img_src)}" alt="slide {i}" class="thumb"/>' if img_src else ''}
  <p><strong>{html.escape(s['headline'])}</strong></p>
  <button onclick="openModal('{mid}')">弹出 · LinkedIn Slide {i}</button>
</article>"""
        modals += f"""
<div id="{mid}" class="modal" onclick="if(event.target===this)closeModal('{mid}')">
  <div class="modal-inner wide">
    <button class="close" onclick="closeModal('{mid}')">×</button>
    {f'<img src="{html.escape(img_src)}" class="hero"/>' if img_src else ''}
    <h2>{html.escape(s['headline'])}</h2>
    <div class="box">{md_block(s['body'])}</div>
  </div>
</div>"""

    doc = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>Owner 多通道交付 · XHS + LinkedIn · {day}</title>
<style>
  body {{ font-family: -apple-system, "PingFang SC", sans-serif; max-width: 960px; margin: 0 auto; padding: 24px; background: #f4f4f4; }}
  .banner {{ background: #0a7; color: #fff; padding: 16px; border-radius: 8px; margin-bottom: 20px; }}
  .cards {{ display: grid; gap: 12px; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); }}
  .card {{ background: #fff; padding: 16px; border-radius: 8px; box-shadow: 0 1px 4px rgba(0,0,0,.08); }}
  .card button {{ margin-top: 8px; padding: 8px 12px; background: #111; color: #fff; border: none; border-radius: 6px; cursor: pointer; }}
  .thumb {{ width: 100%; border-radius: 6px; }}
  .modal {{ display: none; position: fixed; inset: 0; background: rgba(0,0,0,.55); z-index: 200; overflow: auto; }}
  .modal.open {{ display: flex; align-items: flex-start; justify-content: center; padding: 32px 16px; }}
  .modal-inner {{ background: #fff; max-width: 720px; width: 100%; padding: 24px; border-radius: 12px; position: relative; }}
  .modal-inner.wide {{ max-width: 840px; }}
  .close {{ position: absolute; right: 12px; top: 8px; font-size: 28px; border: none; background: none; cursor: pointer; }}
  .box {{ background: #f6f6f6; padding: 12px; border-radius: 6px; max-height: 55vh; overflow: auto; font-size: 0.92rem; line-height: 1.6; }}
  .hero {{ width: 100%; max-height: 360px; object-fit: cover; border-radius: 8px; margin-bottom: 12px; }}
  a {{ color: #0645ad; }}
</style>
</head>
<body>
<div class="banner">
  <strong>Owner 多通道交付 · v2 商业展开</strong> · 重建 {datetime.now().strftime("%Y-%m-%d %H:%M")}<br/>
  打开即弹窗：小红书长稿 + LinkedIn 图文。Canva/生图资产在 <code>assets/2026-10-30-musicians-linkedin/</code>
</div>

<h1>{html.escape(subj)}</h1>
<p><a href="OWNER-XHS-FILTER-DELIVERABLE-{day}.html#owner-latest">← 回到 FILTER 总页</a></p>

<h2>小红书 · 长稿（v2 含商业课 + 可拍案例）</h2>
<button onclick="openModal('modal-xhs')">弹出 · 小红书全文</button>

<h2>LinkedIn · Carousel（EN · 4 slides + caption）</h2>
<div class="cards">{slide_html}
<article class="card" style="grid-column:1/-1">
  <h3>Long caption</h3>
  <button onclick="openModal('modal-li-cap')">弹出 · LinkedIn 正文</button>
</article>
</div>

<div id="modal-xhs" class="modal" onclick="if(event.target===this)closeModal('modal-xhs')">
  <div class="modal-inner wide">
    <button class="close" onclick="closeModal('modal-xhs')">×</button>
    <h2>小红书长稿 · Owner 发布版 v2</h2>
    <div class="box">{md_block(longform)}</div>
  </div>
</div>

<div id="modal-li-cap" class="modal" onclick="if(event.target===this)closeModal('modal-li-cap')">
  <div class="modal-inner wide">
    <button class="close" onclick="closeModal('modal-li-cap')">×</button>
    <h2>LinkedIn long caption</h2>
    <div class="box">{md_block(caption)}</div>
  </div>
</div>
{modals}

<script>
function openModal(id) {{ document.getElementById(id).classList.add('open'); document.body.style.overflow='hidden'; }}
function closeModal(id) {{ document.getElementById(id).classList.remove('open'); document.body.style.overflow=''; }}
(function() {{
  var h = (location.hash || '').replace(/^#/, '');
  if (h === 'multichannel' || h === 'owner-latest') openModal('modal-xhs');
  else openModal('modal-xhs');
}})();
</script>
</body>
</html>"""
    out.write_text(doc, encoding="utf-8")
    print("PASS", out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
