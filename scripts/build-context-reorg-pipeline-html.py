#!/usr/bin/env python3
"""Single-page HTML: Open WebUI ↔ Cursor pipeline + clickable mind map (no CDN)."""

from __future__ import annotations

import html
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HANDOFF = ROOT / "integration/handoff/openwebui-context-reorg-latest.json"
OUT = ROOT / "content/evolution/00-manager/ceo-inbox/CONTEXT-REORG-PIPELINE-LATEST.html"
MINDMAP_COPY = ROOT / "docs/owner-stack-openwebui-mindmap.html"

MINDMAP_NODES = [
    {
        "id": "clone-hub",
        "col": "Git · 克隆 · 双推",
        "title": "全部克隆（新电脑整包）",
        "desc": "Hub 脚本拉齐 danying-apps + 本仓",
        "role": "换机时第一次：不在本仓单独 git clone，走 Hub 全部克隆.md",
        "md": ["新电脑一句话.md", "https://github.com/dymusiques/danying-apps/blob/main/全部克隆.md"],
        "cmd": ["全部克隆", "bash ~/danying-apps/scripts/clone-all.sh"],
    },
    {
        "id": "clone-repo",
        "col": "Git · 克隆 · 双推",
        "title": "唯一工作仓 danying-brand-agent",
        "desc": "Cursor 只开这一文件夹",
        "role": "代码与 MD 的「定稿真相源」；写稿、脚本、规则、handoff 都在 Git",
        "md": ["新电脑一句话.md", "docs/AGENT-TAKEOVER.md", "SETUP.md"],
        "cmd": ["danying-brand-agent", "bash scripts/new-machine-bootstrap.sh"],
    },
    {
        "id": "dual-push",
        "col": "Git · 克隆 · 双推",
        "title": "双推 github + origin",
        "desc": "GitHub 与 Cursor Origin 同一 main",
        "role": "备份、换机、新 Agent 从云端拉同一套 MD；Open WebUI 不自动读远程，需本机 sync",
        "md": ["docs/HANDOFF-COMPLETENESS.md"],
        "cmd": ["git push github main", "git push origin main"],
    },
    {
        "id": "new-agent",
        "col": "Git · 克隆 · 双推",
        "title": "新 Agent 一键接手",
        "desc": "口令 + verify，不依赖旧 chat",
        "role": "读 HANDOFF 链 → autopilot；规则 danying-manager-auto 自动当 00 CEO",
        "md": ["docs/HANDOFF-MD-MANIFEST.md", "docs/NEW-AGENT-WORKFLOW-SOP.md", "docs/workflow-handoff-mindmap.html"],
        "cmd": ["bash scripts/verify-handoff.sh", "bash scripts/verify-agent-takeover.sh"],
    },
    {
        "id": "cursor-ceo",
        "col": "Cursor · CEO",
        "title": "00 Manager / CEO 执行面",
        "desc": "写、改、验、交 HTML",
        "role": "Owner 给目标 → ceo-full-execution → gate/evolution → Owner 交付页",
        "md": ["agents/00-manager/AUTO-WORKFLOW.md", "docs/CEO-FULL-EXECUTION-MANDATE.md"],
        "cmd": ["bash scripts/ceo-full-execution-pipeline.sh --goal \"…\""],
    },
    {
        "id": "cursor-refine",
        "col": "Cursor · CEO",
        "title": "Cursor 做「提炼 / 定稿」",
        "desc": "改 MD、跑 verify、commit",
        "role": "老师说的「用 Cursor 提炼」= 在这里改仓库正文 + 脚本验收；适合结构化定稿与进化",
        "md": ["docs/PROMPT-CONTEXT-STANDARD.md", "docs/OWNER-LONGFORM-DE-AI-VOICE.md"],
        "cmd": ["bash scripts/manager-workflow-verify.sh <brief>"],
    },
    {
        "id": "owui-role",
        "col": "Open WebUI",
        "title": "Open WebUI 干什么",
        "desc": "本机 RAG + Pipe 长文，不是 Git 浏览器",
        "role": "读 Knowledge 四包：问 SOP、问 corpus、问 workflow 命令、问 Drive 背书；长文可出 outbox 给 Cursor",
        "md": ["docs/OPENWEBUI-CEO-ROUTER.md", "integration/openwebui-rag/README.md"],
        "cmd": ["python3 integration/openwebui-rag/scripts/verify_openwebui_knowledge_status.py"],
    },
    {
        "id": "kb-corpus",
        "col": "Open WebUI",
        "title": "Knowledge · cursor-brand-corpus",
        "desc": "本仓 MD 的 L0/L1/L2 镜像",
        "role": "Open WebUI 侧「读你品牌仓上下文」；由 reorganize 导出 + sync 脚本灌入",
        "md": ["docs/CONTEXT-WINDOW-AND-DATA-ROUTING.md"],
        "cmd": ["python3 scripts/reorganize-brand-corpus-l012.py", "python3 integration/openwebui-rag/scripts/sync_cursor_brand_corpus_to_openwebui.py"],
    },
    {
        "id": "kb-drive",
        "col": "Open WebUI",
        "title": "Knowledge · brand-ip-knowledge",
        "desc": "Google Drive 资料库镜像",
        "role": "你说的「Drive 后续资料库」主要在这包；与 Git 仓分离，靠 Drive sync 进 RAG",
        "md": ["docs/OPENWEBUI-CEO-ROUTER.md"],
        "cmd": ["python3 integration/openwebui-rag/scripts/sync_brand_drive_to_openwebui.py"],
    },
    {
        "id": "kb-prompt",
        "col": "Open WebUI",
        "title": "Knowledge · agent-prompt-pack",
        "desc": "INTEGRATION-PROMPT / 路由短答",
        "role": "新 Agent 在 WebUI 里问「04 小红书 GM 怎么接」",
        "md": ["docs/PROMPT-CONTEXT-STANDARD.md"],
        "cmd": ["bash scripts/export-agent-prompt-pack.sh", "python3 integration/openwebui-rag/scripts/sync_agent_prompt_pack_to_openwebui.py"],
    },
    {
        "id": "kb-wf",
        "col": "Open WebUI",
        "title": "Knowledge · workflow-automation-pack",
        "desc": "L0–L4 可跑命令清单",
        "role": "问「CEO 开始执行跑什么」→ manifest 层",
        "md": ["docs/WORKFLOW-AUTOMATION-MATRIX.md"],
        "cmd": ["python3 scripts/run-workflow-from-manifest.py --list-layers"],
    },
    {
        "id": "mirror",
        "col": "镜像 · L012",
        "title": "brand-knowledge-mirror",
        "desc": "本机 _rag 目录（非 Git 远程）",
        "role": "reorganize 写出 L0/L1/L2；Open WebUI sync 读磁盘；路径见 openwebui_rag_paths.py",
        "md": ["integration/openwebui-rag/scripts/openwebui_rag_paths.py"],
        "cmd": ["export BRAND_KNOWLEDGE_MIRROR=…（可选）"],
    },
    {
        "id": "pipeline",
        "col": "镜像 · L012",
        "title": "run-context-reorg-pipeline",
        "desc": "导出 → 四包 sync → 本 HTML",
        "role": "全链路刷新；含 --apply-repo 会大批量改 MD，日常可只跑 verify/sync",
        "md": ["scripts/run-context-reorg-pipeline.sh"],
        "cmd": ["bash scripts/run-context-reorg-pipeline.sh"],
    },
    {
        "id": "router",
        "col": "Open WebUI ↔ Cursor",
        "title": "CEO Router（步 −1）",
        "desc": "RAG/Pipe → outbox / intake",
        "role": "Cursor 派长文或 intake 时走 Open WebUI，结果回 handoff/outbox",
        "md": ["docs/OPENWEBUI-CEO-ROUTER.md"],
        "cmd": ["bash scripts/run-openwebui-router-pipeline.sh --goal \"…\""],
    },
    {
        "id": "deploy",
        "col": "Open WebUI ↔ Cursor",
        "title": "deploy-learning-stack",
        "desc": "Ollama URL · Knowledge 基线",
        "role": "Docker Open WebUI + embedding 修复 + 栈验收",
        "md": ["scripts/deploy-learning-stack.sh"],
        "cmd": ["bash scripts/deploy-learning-stack.sh"],
    },
]


def git_short(ref: str) -> str:
    r = subprocess.run(
        ["git", "rev-parse", ref],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    return r.stdout.strip()[:12] if r.returncode == 0 else "?"


def dual_push_status() -> dict:
    head = git_short("HEAD")
    gh = git_short("github/main")
    og = git_short("origin/main")
    unified = head == gh == og and "?" not in (head, gh, og)
    diff_names = subprocess.run(
        ["git", "diff", "--name-only", "github/main"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    local_only = [ln for ln in diff_names.stdout.splitlines() if ln.strip()]
    return {
        "head": head,
        "github_main": gh,
        "origin_main": og,
        "unified": unified,
        "local_diff_vs_github": local_only,
    }


def render_page(data: dict, catalog: dict, sync: dict) -> str:
    counts = data.get("counts", {})
    infra = data.get("infrastructure", {})
    agents = data.get("agents_gm_ceo", {})
    kbs = data.get("knowledge_collections", {})
    tags = data.get("openwebui_chat_tags", [])
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    repo_s = str(ROOT)
    nodes_json = json.dumps(MINDMAP_NODES, ensure_ascii=False)
    sync_json = json.dumps(sync, ensure_ascii=False)

    layer_rows = ""
    for ly in catalog.get("layers_l1", [])[:8]:
        layer_rows += (
            f"<tr><td><code>{html.escape(ly.get('id', ''))}</code></td>"
            f"<td>{html.escape(ly.get('name', ''))}</td>"
            f"<td><code>{html.escape(ly.get('primary_command', '')[:80])}</code></td></tr>"
        )
    kb_rows = "".join(
        f"<tr><td><code>{html.escape(k)}</code></td><td>{html.escape(v)}</td></tr>"
        for k, v in kbs.items()
    )
    sample = data.get("entries_sample", [])[:12]
    sample_rows = "".join(
        f"<tr><td><code>{html.escape(e.get('path', ''))}</code></td>"
        f"<td>{html.escape(e.get('owui', ''))}</td></tr>"
        for e in sample
    )

    sync_pre = html.escape("\n".join(data.get("sync_commands", [])))
    unified_badge = (
        '<span class="badge ok">双推与本地 HEAD 一致</span>'
        if sync["unified"]
        else '<span class="badge warn">本地与 github/main 有差异（见下）</span>'
    )
    diff_ul = ""
    if sync["local_diff_vs_github"]:
        diff_ul = "<ul>" + "".join(
            f"<li><code>{html.escape(p)}</code></li>" for p in sync["local_diff_vs_github"][:20]
        ) + "</ul>"
    else:
        diff_ul = "<p>无未 push 差异（相对 github/main）。</p>"

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>Brand Agent · Open WebUI ↔ Cursor · 思维导图</title>
<style>
  :root {{ font-family: "PingFang SC", system-ui, sans-serif; line-height: 1.5; color: #1a1a1a; }}
  body {{ margin: 0; background: #f0f2f5; }}
  .topbar {{
    position: sticky; top: 0; z-index: 20; background: #1f6feb; color: #fff;
    padding: 10px 16px; display: flex; flex-wrap: wrap; gap: 10px; align-items: center;
  }}
  .topbar button {{ background: #fff; color: #1f6feb; border: 0; padding: 8px 14px; border-radius: 8px; font-weight: 700; cursor: pointer; }}
  .topbar a {{ color: #fff; font-size: 13px; }}
  .wrap {{ max-width: 1100px; margin: 0 auto; padding: 16px 16px 220px; }}
  h1 {{ font-size: 1.35rem; margin: 0 0 8px; }}
  h2 {{ margin-top: 1.5rem; border-bottom: 1px solid #ccc; padding-bottom: 0.3rem; font-size: 1.1rem; }}
  .card {{ background: #fff; border-radius: 10px; padding: 1rem 1.2rem; margin: 1rem 0; box-shadow: 0 1px 3px rgba(0,0,0,.08); }}
  .badge {{ display: inline-block; padding: 4px 10px; border-radius: 999px; font-size: 12px; font-weight: 700; }}
  .badge.ok {{ background: #dafbe1; color: #116329; }}
  .badge.warn {{ background: #fff8c5; color: #7d4e00; }}
  table {{ border-collapse: collapse; width: 100%; font-size: 0.88rem; }}
  th, td {{ border: 1px solid #ddd; padding: 0.35rem 0.5rem; text-align: left; }}
  th {{ background: #eee; }}
  code {{ font-size: 0.85em; word-break: break-all; }}
  pre {{ background: #222; color: #eee; padding: 1rem; overflow-x: auto; border-radius: 6px; font-size: 12px; }}
  .hub {{ text-align: center; margin: 12px 0; }}
  .hub span {{ display: inline-block; background: #238636; color: #fff; padding: 12px 24px; border-radius: 999px; font-weight: 800; }}
  .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 10px; }}
  .col-title {{ grid-column: 1 / -1; color: #0969da; font-weight: 700; font-size: 13px; margin-top: 8px; }}
  .node {{
    background: #fff; border: 2px solid #d0d7de; border-radius: 10px; padding: 10px 12px;
    cursor: pointer; min-height: 72px;
  }}
  .node:hover, .node.on {{ border-color: #1f6feb; box-shadow: 0 0 0 2px rgba(31,111,235,.25); }}
  .node h3 {{ margin: 0 0 4px; font-size: 0.92rem; }}
  .node p {{ margin: 0; font-size: 0.78rem; color: #57606a; }}
  #panel {{
    position: fixed; left: 0; right: 0; bottom: 0; max-height: 38vh; overflow-y: auto;
    background: #161b22; color: #e6edf3; padding: 14px 18px; border-top: 3px solid #1f6feb;
    font-size: 14px;
  }}
  #panel h2 {{ margin: 0 0 8px; color: #79c0ff; border: 0; font-size: 1.05rem; }}
  #panel a {{ color: #58a6ff; }}
  .flow-row {{ display: flex; flex-wrap: wrap; gap: 8px; justify-content: center; margin: 12px 0; }}
  .flow-box {{ background: #ddf4ff; border: 1px solid #54aeff; border-radius: 8px; padding: 8px 12px; font-size: 12px; max-width: 140px; text-align: center; }}
  .flow-arrow {{ align-self: center; color: #656d76; }}
</style>
</head>
<body>
<div class="topbar">
  <button type="button" id="btn-popup">在新窗口打开</button>
  <a id="link-md" href="#">打开选中节点 MD（本机）</a>
  <span style="font-size:13px">仓：{html.escape(repo_s)}</span>
</div>
<div class="wrap">
<h1>Brand Agent · 克隆 / Cursor / Open WebUI 总流程</h1>
<p>生成：{html.escape(now)} · handoff <code>integration/handoff/openwebui-context-reorg-latest.json</code></p>

<div class="card">
  <strong>双推核对</strong> {unified_badge}<br/>
  HEAD <code>{html.escape(sync['head'])}</code> ·
  github/main <code>{html.escape(sync['github_main'])}</code> ·
  origin/main <code>{html.escape(sync['origin_main'])}</code>
  {diff_ul}
  <p style="font-size:13px;color:#57606a;margin-bottom:0">
    <strong>结论：</strong>Git 双推 = 新 Agent 与换机的「文档真相源」；
    Open WebUI = 本机 Docker + 磁盘镜像 + sync 脚本，<em>不会</em>因为你 push 就自动更新 Knowledge。
  </p>
</div>

<h2>简化主链（一眼）</h2>
<div class="card">
<div class="flow-row">
  <div class="flow-box">Owner 口令<br/>全部克隆 / danying-brand-agent</div>
  <span class="flow-arrow">→</span>
  <div class="flow-box">Git 仓<br/>写 MD · 脚本 · verify</div>
  <span class="flow-arrow">→</span>
  <div class="flow-box">L012 镜像<br/>reorganize</div>
  <span class="flow-arrow">→</span>
  <div class="flow-box">sync 脚本<br/>integration/openwebui-rag</div>
  <span class="flow-arrow">→</span>
  <div class="flow-box">Open WebUI<br/>4× Knowledge</div>
  <span class="flow-arrow">↔</span>
  <div class="flow-box">Cursor CEO<br/>定稿 · gate · HTML</div>
</div>
</div>

<h2 id="owner-latest">可点击思维导图（点节点 → 下方详情）</h2>
<p style="font-size:13px;color:#57606a">每个方块 = 一道工序；含「干什么 / 读哪些 MD / 跑什么命令」。</p>
<div class="hub"><span>你在这里 · 总控</span></div>
<div class="grid" id="mindmap-grid"></div>

<h2>Infrastructure</h2>
<ul>
<li>Open WebUI：{html.escape(str(infra.get('open_webui', 'http://localhost:3000')))}</li>
<li>Embedding：{html.escape(str(infra.get('embedding', 'ollama bge-m3')))}</li>
<li>Pipes：{html.escape(', '.join(infra.get('pipes', [])))}</li>
<li>Deploy：<code>{html.escape(str(infra.get('deploy', 'bash scripts/deploy-learning-stack.sh')))}</code></li>
</ul>

<h2>Knowledge 四包</h2>
<table><tr><th>集合</th><th>用途</th></tr>{kb_rows}</table>
<p>标签：{' · '.join(html.escape(t) for t in tags)}</p>

<h2>L0 / L1 / L2</h2>
<p>导出约 <strong>{counts.get('exported_l012', '?')}</strong> 文件 · mirror（handoff）：<code>{html.escape(data.get('mirror', ''))}</code></p>

<h2>Sync 命令（仓内路径）</h2>
<pre>{sync_pre}</pre>

<h2>Workflow L0–L4</h2>
<table><tr><th>layer</th><th>名称</th><th>主命令</th></tr>{layer_rows}</table>
<pre>{html.escape(catalog.get('run_layer', ''))}
{html.escape(catalog.get('run_owner_phrase', ''))}</pre>

<h2>路径样例</h2>
<table><tr><th>repo_path</th><th>OWUI</th></tr>{sample_rows}</table>

<h2>CEO / Eval</h2>
<p><code>{html.escape(agents.get('six_case_doc', ''))}</code></p>
<p>{html.escape(', '.join(agents.get('eval', [])))}</p>
</div>

<div id="panel"><h2>点击上方任意节点</h2><p>显示工序含义、MD 与命令。</p></div>

<script>
(function() {{
  var REPO = {json.dumps(repo_s)};
  var NODES = {nodes_json};
  var grid = document.getElementById("mindmap-grid");
  var panel = document.getElementById("panel");
  var linkMd = document.getElementById("link-md");
  var lastCol = "";
  var selected = null;

  function fileUrl(rel) {{
    if (!rel || rel.indexOf("http") === 0) return rel;
    return "file://" + REPO + "/" + rel;
  }}

  NODES.forEach(function(n) {{
    if (n.col !== lastCol) {{
      var t = document.createElement("div");
      t.className = "col-title";
      t.textContent = n.col;
      grid.appendChild(t);
      lastCol = n.col;
    }}
    var el = document.createElement("div");
    el.className = "node";
    el.innerHTML = "<h3>" + n.title + "</h3><p>" + n.desc + "</p>";
    el.addEventListener("click", function() {{
      document.querySelectorAll(".node.on").forEach(function(x) {{ x.classList.remove("on"); }});
      el.classList.add("on");
      selected = n;
      var h = "<h2>" + n.title + "</h2>";
      h += "<p><strong>这道工序是什么：</strong>" + (n.role || "") + "</p>";
      if (n.md && n.md.length) {{
        h += "<p><strong>相关 MD / 链接：</strong></p><ul>";
        n.md.forEach(function(p) {{
          if (p.indexOf("http") === 0) {{
            h += "<li><a href=\"" + p + "\" target=\"_blank\" rel=\"noopener\">" + p + "</a></li>";
          }} else {{
            h += "<li><a href=\"" + fileUrl(p) + "\"><code>" + p + "</code></a></li>";
          }}
        }});
        h += "</ul>";
      }}
      if (n.cmd && n.cmd.length) {{
        h += "<p><strong>命令 / 口令：</strong></p><ul>";
        n.cmd.forEach(function(c) {{ h += "<li><code>" + c + "</code></li>"; }});
        h += "</ul>";
      }}
      panel.innerHTML = h;
      var firstLocal = (n.md || []).find(function(p) {{ return p && p.indexOf("http") !== 0; }});
      if (firstLocal) {{
        linkMd.href = fileUrl(firstLocal);
        linkMd.style.display = "";
      }} else {{
        linkMd.style.display = "none";
      }}
      location.hash = "node-" + n.id;
    }});
    grid.appendChild(el);
  }});

  document.getElementById("btn-popup").addEventListener("click", function() {{
    window.open(location.href.split("#")[0] + "?popup=1#owner-latest", "dba-context-mindmap", "width=1024,height=900,scrollbars=yes");
  }});
  if (location.search.indexOf("popup=1") !== -1 || location.search.indexOf("open=1") !== -1) {{
    setTimeout(function() {{ document.getElementById("btn-popup").click(); }}, 300);
  }}
}})();
</script>
</body>
</html>
"""


def main() -> int:
    data = json.loads(HANDOFF.read_text(encoding="utf-8")) if HANDOFF.is_file() else {}
    catalog_path = ROOT / "integration/handoff/workflow-automation-catalog-l1.json"
    catalog = json.loads(catalog_path.read_text(encoding="utf-8")) if catalog_path.is_file() else {}
    sync = dual_push_status()
    doc = render_page(data, catalog, sync)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(doc, encoding="utf-8")
    MINDMAP_COPY.write_text(doc, encoding="utf-8")
    print(str(OUT))
    print(str(MINDMAP_COPY))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
