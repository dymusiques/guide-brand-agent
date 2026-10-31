#!/usr/bin/env python3
"""Single-page HTML: Open WebUI ↔ Cursor context reorg pipeline (Owner delivery)."""

from __future__ import annotations

import html
import json
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HANDOFF = ROOT / "integration/handoff/openwebui-context-reorg-latest.json"
OUT = ROOT / "content/evolution/00-manager/ceo-inbox/CONTEXT-REORG-PIPELINE-LATEST.html"


def main() -> int:
    data = json.loads(HANDOFF.read_text(encoding="utf-8")) if HANDOFF.is_file() else {}
    catalog_path = ROOT / "integration/handoff/workflow-automation-catalog-l1.json"
    catalog = json.loads(catalog_path.read_text(encoding="utf-8")) if catalog_path.is_file() else {}
    layer_rows = ""
    for ly in catalog.get("layers_l1", [])[:8]:
        layer_rows += (
            f"<tr><td><code>{html.escape(ly.get('id',''))}</code></td>"
            f"<td>{html.escape(ly.get('name',''))}</td>"
            f"<td><code>{html.escape(ly.get('primary_command','')[:80])}</code></td></tr>"
        )
    counts = data.get("counts", {})
    infra = data.get("infrastructure", {})
    agents = data.get("agents_gm_ceo", {})
    kbs = data.get("knowledge_collections", {})
    tags = data.get("openwebui_chat_tags", [])
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    kb_rows = "".join(
        f"<tr><td><code>{html.escape(k)}</code></td><td>{html.escape(v)}</td></tr>"
        for k, v in kbs.items()
    )
    sample = data.get("entries_sample", [])[:12]
    sample_rows = "".join(
        f"<tr><td><code>{html.escape(e.get('path',''))}</code></td>"
        f"<td>{html.escape(e.get('owui',''))}</td></tr>"
        for e in sample
    )

    doc = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>上下文重组 · Open WebUI ↔ Cursor</title>
<style>
  :root {{ font-family: system-ui, sans-serif; line-height: 1.5; color: #1a1a1a; }}
  body {{ max-width: 960px; margin: 2rem auto; padding: 0 1rem; }}
  h1 {{ font-size: 1.6rem; }}
  h2 {{ margin-top: 2rem; border-bottom: 1px solid #ddd; padding-bottom: 0.3rem; }}
  .card {{ background: #f6f8fa; border-radius: 8px; padding: 1rem 1.2rem; margin: 1rem 0; }}
  table {{ border-collapse: collapse; width: 100%; font-size: 0.92rem; }}
  th, td {{ border: 1px solid #ddd; padding: 0.4rem 0.6rem; text-align: left; }}
  th {{ background: #eee; }}
  code {{ font-size: 0.88em; }}
  pre {{ background: #222; color: #eee; padding: 1rem; overflow-x: auto; border-radius: 6px; }}
  .mermaid {{ background: #fff; padding: 1rem; border: 1px solid #ddd; border-radius: 8px; }}
</style>
</head>
<body>
<h1>Brand Agent · 上下文重组链路</h1>
<p>生成时间：{html.escape(now)} · handoff：<code>integration/handoff/openwebui-context-reorg-latest.json</code></p>

<div class="card">
<strong>Git / 双推说明：</strong> Open WebUI 同步读<strong>本机</strong> <code>reorganize-brand-corpus-l012.py</code> 导出的镜像，
不读 GitHub/Origin 远程。未 commit 的 MD 也会进 Knowledge；双推只为备份与换机，<em>不是</em>喂库前置条件。
</div>

<h2>1. Infrastructure</h2>
<ul>
<li>Open WebUI：{html.escape(str(infra.get('open_webui','http://localhost:3000')))}</li>
<li>Embedding：{html.escape(str(infra.get('embedding','ollama bge-m3')))}</li>
<li>Pipes：{html.escape(', '.join(infra.get('pipes', [])))}</li>
<li>Tools：{html.escape(', '.join(infra.get('tools', [])))}</li>
<li>Deploy： <code>{html.escape(str(infra.get('deploy','')))}</code></li>
</ul>

<h2>2. 数据流（Mermaid）</h2>
<div class="mermaid">
flowchart LR
  subgraph Cursor
    MD[danying-brand-agent MD]
    REORG[reorganize-brand-corpus-l012.py]
    HAND[handoff JSON]
    CEO[CEO verify / gate / HTML]
  end
  subgraph Mirror
    L0[L0 index]
    L1[L1 任务壳]
    L2[L2 正文]
  end
  subgraph OpenWebUI
    KB1[cursor-brand-corpus]
    KB2[agent-prompt-pack]
    KB3[brand-ip-knowledge]
    KB4[workflow-automation-pack]
    RAG[RAG + Pipe 长文]
  end
  WF[run-workflow-from-manifest.py]
  MD --> REORG
  REORG --> L0 & L1 & L2
  L1 --> KB1
  REORG --> HAND
  HAND --> CEO
  KB1 & KB2 & KB3 & KB4 --> RAG
  RAG -.->|outbox / intake 路径| CEO
  HAND --> WF
  WF --> CEO
</div>

<h2>3. Knowledge 集合</h2>
<table><tr><th>集合</th><th>用途</th></tr>{kb_rows}</table>
<p>聊天标签：{' · '.join(html.escape(t) for t in tags)}</p>

<h2>4. 三层上下文（L0 / L1 / L2）</h2>
<table>
<tr><th>层</th><th>内容</th><th>谁读</th></tr>
<tr><td>L0</td><td>路径 + 路由一行</td><td>索引 / RAG 定位</td></tr>
<tr><td>L1</td><td>Goal + 验收 + 章节锚点（≤~400 字）</td><td>Cursor 顶栏 · Open WebUI 任务</td></tr>
<tr><td>L2</td><td>正文全文</td><td>Open WebUI RAG · intake</td></tr>
</table>
<p>本次导出：<strong>{counts.get('exported_l012','?')}</strong> 文件 · 仓内重写：<strong>{counts.get('repo_rewritten','?')}</strong></p>

<h2>5. Agent / GM / CEO / 六项 test</h2>
<p>六项 6-case 文档：<code>{html.escape(agents.get('six_case_doc',''))}</code></p>
<ul>
<li>00 Manager / CEO：指挥链 · triple-eval · double-stress · Owner HTML</li>
<li>01–12 GM：各部门 INTEGRATION-PROMPT（已进 agent-prompt-pack）</li>
<li>Evaluation：{html.escape(', '.join(agents.get('eval', [])))}</li>
</ul>

<h2>6. 函数与胶水</h2>
<pre>{html.escape(chr(10).join(data.get('sync_commands', [])))}</pre>
<ul>
<li><code>scripts/route-openwebui-for-goal.py</code> — Cursor 路由长文</li>
<li><code>scripts/run-openwebui-router-pipeline.sh</code> — Pipe + intake</li>
<li><code>scripts/openwebui-pipe-to-outbox.py</code> — 回写 outbox 给 Cursor</li>
<li><code>scripts/deploy-learning-stack.sh</code> — 栈部署</li>
</ul>

<h2>7. Cursor 回喂（Must read）</h2>
<ol>
<li><code>integration/handoff/openwebui-context-reorg-latest.json</code></li>
<li><code>integration/handoff/cursor-openwebui-task-routing.json</code></li>
<li><code>docs/PROMPT-CONTEXT-STANDARD.md</code></li>
</ol>

<h2>8. 可自动化 Workflow（L0_BOOT → L4）</h2>
<p>机器目录：<code>integration/handoff/workflow-automation-catalog-l1.json</code> · 
脚本数：<strong>{catalog.get('script_inventory_count', '?')}</strong></p>
<pre>{html.escape(catalog.get('run_layer', ''))}
{html.escape(catalog.get('run_owner_phrase', ''))}</pre>
<table><tr><th>layer</th><th>名称</th><th>主命令</th></tr>{layer_rows}</table>
<p>Open WebUI：<code># workflow-automation-pack</code> · Cursor：<code>python3 scripts/run-workflow-from-manifest.py --list-layers</code></p>

<h2>9. 路径样例（L1 路由）</h2>
<table><tr><th>repo_path</th><th>OWUI</th></tr>{sample_rows}</table>

<script type="module">
import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
mermaid.initialize({{ startOnLoad: true, theme: 'neutral' }});
</script>
</body>
</html>
"""
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(doc, encoding="utf-8")
    print(str(OUT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
