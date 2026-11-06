#!/usr/bin/env python3
"""HTML deliverable · domestic / international benchmark growth paths + Instagram."""

from __future__ import annotations

import html
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
JSON_PATH = ROOT / "integration/handoff/owner-benchmark-growth-paths.json"
DRIVE_HANDOFF = ROOT / "integration/handoff/owner-benchmark-paths-drive-latest.json"
INBOX = ROOT / "content/evolution/00-manager/ceo-inbox"
FOLDERS = ROOT / "integration/handoff/ceo-drive-corpus-folders.json"


def build(out: Path) -> None:
    data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    drive_link = ""
    if DRIVE_HANDOFF.is_file():
        drive_link = json.loads(DRIVE_HANDOFF.read_text(encoding="utf-8")).get("google_doc_link", "")
    folders = json.loads(FOLDERS.read_text(encoding="utf-8")).get("folders") or []

    def section(path_key: str) -> str:
        block = data["paths"][path_key]
        rows = ""
        for c in block.get("creators") or []:
            arc = c.get("growth_arc") or []
            if isinstance(arc, list):
                arc_s = " → ".join(html.escape(str(x)) for x in arc[:5])
                if len(arc) > 5:
                    arc_s += " …"
            else:
                arc_s = html.escape(str(arc))
            rows += f"""<tr>
<td>{html.escape(c.get('handle',''))}</td>
<td>{html.escape(c.get('platform',''))}</td>
<td class="num">{html.escape(str(c.get('followers_approx','')))}</td>
<td>{arc_s}</td>
<td>{html.escape((c.get('copy_steal') or [''])[0] if isinstance(c.get('copy_steal'), list) else c.get('copy_steal',''))}</td>
<td>{html.escape((c.get('visual_steal') or [''])[0] if isinstance(c.get('visual_steal'), list) else c.get('visual_steal',''))}</td>
</tr>"""
        plats = ", ".join(block.get("platforms") or [])
        return f"""<section><h2>{html.escape(block.get('label',''))} · {html.escape(plats)}</h2>
<table><tr><th>账号</th><th>平台</th><th>粉丝约</th><th>成长轨迹</th><th>文案</th><th>配图</th></tr>{rows}</table></section>"""

    rec_li = "".join(f"<li>{html.escape(r)}</li>" for r in (data.get("recommendations_for_ceo") or []))
    fold_li = "".join(
        f'<li><a href="{html.escape(f.get("drive_link",""))}">{html.escape(f.get("label",""))}</a></li>'
        for f in folders
    )
    day = datetime.now().strftime("%Y-%m-%d")
    doc_a = f'<a href="{html.escape(drive_link)}">Google Doc / Drive 同步</a>' if drive_link else "（运行 sync-owner-benchmark-paths-to-drive.sh）"

    body = f"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8"/>
<title>CEO 对标路径 · 国内/国际 · Instagram · {day}</title>
<style>
body{{font-family:"PingFang SC",system-ui;background:#0f1419;color:#e6edf3;margin:0;padding:24px;line-height:1.55}}
.wrap{{max-width:1100px;margin:0 auto}}
h1{{font-size:1.5rem}}
section{{background:#161b22;border:1px solid #30363d;border-radius:12px;padding:16px 18px;margin:18px 0}}
table{{width:100%;border-collapse:collapse;font-size:0.85rem}}
th,td{{border-bottom:1px solid #30363d;padding:8px;text-align:left;vertical-align:top}}
th{{color:#8b949e}}
.num{{font-variant-numeric:tabular-nums}}
a{{color:#58a6ff}}
.pill{{display:inline-block;background:#1f3a5f;padding:4px 10px;border-radius:999px;font-size:12px;margin:4px 4px 0 0}}
</style></head><body><div class="wrap">
<h1>CEO 派活 · 大 V 成长轨迹（含 Instagram）</h1>
<p>重建 {datetime.now():%Y-%m-%d %H:%M} · JSON <code>{JSON_PATH.relative_to(ROOT)}</code> · {doc_a}</p>
<p><span class="pill">国内路径</span><span class="pill">国际路径</span><span class="pill">≥40万粉或标注例外</span><span class="pill">Owner Drive 链接</span></p>
<h3>Drive 资料库（CEO screen）</h3><ul>{fold_li}</ul>
{section("domestic_cn")}
{section("international_en")}
<section><h2>CEO 建议</h2><ul>{rec_li}</ul></section>
<p style="color:#8b949e;font-size:13px">导图：<code>docs/CEO-EXECUTION-MINDMAP.html</code> · 每次派活先 attestation + Drive catalog refresh</p>
</div></body></html>"""
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(body, encoding="utf-8")
    print(f"PASS {out}")


if __name__ == "__main__":
    day = datetime.now().strftime("%Y-%m-%d")
    build(INBOX / f"OWNER-BENCHMARK-PATHS-DELIVERABLE-{day}.html")
