#!/usr/bin/env python3
"""
Export + optional in-repo rewrite: Brand Agent MD → L0/L1/L2 for Open WebUI Knowledge.

L0: one-screen index stubs · L1: ≤400 char task shell + section one-liners · L2: full body (RAG).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
def _default_mirror() -> Path:
    import sys

    sys.path.insert(0, str(ROOT / "integration/openwebui-rag/scripts"))
    from openwebui_rag_paths import rag_subdir

    return rag_subdir("cursor-brand-corpus")
HANDOFF = ROOT / "integration/handoff/openwebui-context-reorg-latest.json"

SKIP_DIRS = {
    ".git",
    "node_modules",
    ".venv",
    "vendor",
    "__pycache__",
    "verify-logs",
}
SKIP_PARTS = ("/assets/", "/challenge-html/")

HEADER_BLOCK = re.compile(
    r"^> \*\*上下文（L0/L1/L2）\*\*[\s\S]*?(?=\n# |\n## |\Z)",
    re.MULTILINE,
)
FM_RE = re.compile(r"^---\n[\s\S]*?\n---\n", re.MULTILINE)
H1_RE = re.compile(r"^#\s+(.+)$", re.MULTILINE)
H2_RE = re.compile(r"^##\s+(.+)$", re.MULTILINE)


def repo_rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def route_openwebui(rel: str) -> str:
    if rel.startswith("content/xiaohongshu/") and "brief" in rel:
        return "intake_l2"
    if rel.startswith("scripts/") or rel.endswith(".sh"):
        return "skip"
    if "INTEGRATION-PROMPT" in rel:
        return "rag_l1"
    if rel.startswith("docs/") or rel.startswith("rules/"):
        return "rag_l1"
    if rel.startswith("content/"):
        return "intake_l2"
    return "rag_l2"


def route_cursor(rel: str) -> str:
    if "verify" in rel or rel.startswith("scripts/"):
        return "exec"
    if "brief" in rel:
        return "exec_gate"
    return "read"


def first_title(text: str, fallback: str) -> str:
    m = H1_RE.search(text)
    return m.group(1).strip() if m else fallback


def section_one_liners(text: str, limit: int = 8) -> list[str]:
    lines = text.splitlines()
    out: list[str] = []
    i = 0
    while i < len(lines) and len(out) < limit:
        m = H2_RE.match(lines[i])
        if m:
            title = m.group(1).strip()
            body = []
            i += 1
            while i < len(lines) and not lines[i].startswith("#"):
                t = lines[i].strip()
                if t and not t.startswith(">"):
                    body.append(t)
                    break
                i += 1
            snippet = (body[0][:100] + "…") if body and len(body[0]) > 100 else (body[0] if body else "")
            out.append(f"- **{title}**" + (f": {snippet}" if snippet else ""))
            continue
        i += 1
    return out


def extract_l1(text: str, rel: str, title: str) -> str:
    stripped = HEADER_BLOCK.sub("", text)
    stripped = FM_RE.sub("", stripped).strip()
    if "## L2 正文" in stripped:
        stripped = stripped.split("## L2 正文", 1)[1].strip()
    paras = [p.strip() for p in re.split(r"\n\s*\n", stripped) if p.strip() and not p.startswith("#")]
    if "brief" in rel or "xhs-classifier" in text or any(p.startswith("```json") for p in paras[:2]):
        goal = title
    else:
        goal = paras[0][:200] if paras else title
    bullets = section_one_liners(stripped)
    lines = [
        f"# {title}",
        "",
        "## L1 任务（压缩 · Open WebUI / Cursor 顶栏）",
        f"- **Goal:** {goal[:180]}",
        f"- **Path:** `{rel}`",
        f"- **Open WebUI:** `{route_openwebui(rel)}`",
        f"- **Cursor:** `{route_cursor(rel)}`",
        "",
    ]
    if bullets:
        lines.append("## 章节锚点")
        lines.extend(bullets[:8])
        lines.append("")
    body = "\n".join(lines)
    if len(body) > 1200:
        body = body[:1190] + "\n…"
    return body


def build_l0(rel: str, title: str) -> str:
    return (
        f"- `{rel}` · **{title[:80]}** · OWUI={route_openwebui(rel)} · Cursor={route_cursor(rel)}"
    )


def build_frontmatter(rel: str, title: str, sha: str) -> str:
    return (
        "---\n"
        f"context_version: \"2026-10-30-l012\"\n"
        f"repo_path: \"{rel}\"\n"
        f'goal: "{title.replace(chr(34), chr(39))[:120]}"\n'
        f"openwebui_route: \"{route_openwebui(rel)}\"\n"
        f"cursor_route: \"{route_cursor(rel)}\"\n"
        f"content_sha256: \"{sha}\"\n"
        "---\n\n"
    )


def strip_for_l2(text: str) -> str:
    if "## L2 正文" in text:
        return text.split("## L2 正文", 1)[1].strip()
    text = HEADER_BLOCK.sub("", text)
    return FM_RE.sub("", text).strip()


def should_scan(path: Path) -> bool:
    rel = repo_rel(path)
    if any(part in path.parts for part in SKIP_DIRS):
        return False
    if any(p in rel for p in SKIP_PARTS):
        return False
    if path.suffix.lower() != ".md":
        return False
    return True


def discover_md() -> list[Path]:
    out: list[Path] = []
    for p in ROOT.rglob("*.md"):
        if should_scan(p):
            out.append(p)
    return sorted(out, key=lambda x: repo_rel(x))


def apply_repo(path: Path, fm: str, l1: str, raw: str) -> None:
    if "## L2 正文" in raw:
        body = raw.split("## L2 正文", 1)[1].strip()
    else:
        body = HEADER_BLOCK.sub("", raw)
        body = FM_RE.sub("", body).lstrip()
        if "## L1 任务（压缩 · Open WebUI / Cursor 顶栏）" in body:
            body = re.split(r"\n## L1 任务（压缩", body, maxsplit=1)[0].rstrip()
    new_text = fm + l1 + "\n\n---\n\n## L2 正文\n\n" + body
    path.write_text(new_text, encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--mirror", type=Path, default=None)
    ap.add_argument("--apply-repo", action="store_true", help="Rewrite MD in repo with L1 shell + L2 body")
    ap.add_argument("--max-bytes", type=int, default=1_500_000, help="Skip L2 export above this size")
    args = ap.parse_args()
    mirror = args.mirror or _default_mirror()

    l0_dir = mirror / "l0"
    l1_dir = mirror / "l1"
    l2_dir = mirror / "l2"
    for d in (l0_dir, l1_dir, l2_dir):
        d.mkdir(parents=True, exist_ok=True)

    files = discover_md()
    l0_lines = [
        "# Cursor Brand Corpus · L0 主索引",
        "",
        f"Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%MZ')} UTC",
        "",
        "## 用法",
        "- Open WebUI：`# cursor-brand-corpus` + 问 L1 路由或某路径",
        "- Cursor：只读 handoff `integration/handoff/openwebui-context-reorg-latest.json`",
        "",
    ]
    entries: list[dict] = []
    skipped_size = 0
    applied = 0

    for path in files:
        rel = repo_rel(path)
        raw = path.read_text(encoding="utf-8", errors="replace")
        if len(raw.encode("utf-8")) > args.max_bytes:
            skipped_size += 1
            continue
        title = first_title(raw, path.stem)
        sha = hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]
        fm = build_frontmatter(rel, title, sha)
        l1 = extract_l1(raw, rel, title)
        l2 = strip_for_l2(raw)

        safe = rel.replace("/", "__")
        (l0_dir / f"{safe}.md").write_text(build_l0(rel, title) + "\n", encoding="utf-8")
        (l1_dir / f"{safe}.md").write_text(l1, encoding="utf-8")
        (l2_dir / f"{safe}.md").write_text(l2, encoding="utf-8")
        l0_lines.append(build_l0(rel, title))
        entries.append({"path": rel, "title": title, "sha16": sha, "owui": route_openwebui(rel)})

        if args.apply_repo:
            apply_repo(path, fm, l1, raw)
            applied += 1

    (mirror / "MASTER-L0-INDEX.md").write_text("\n".join(l0_lines) + "\n", encoding="utf-8")
    (l1_dir / "MASTER-L0-INDEX.md").write_text((mirror / "MASTER-L0-INDEX.md").read_text(encoding="utf-8"), encoding="utf-8")

    handoff = {
        "version": "2026-10-30",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "repo": str(ROOT),
        "mirror": str(mirror),
        "git_note": "Open WebUI sync reads local mirror + working tree; git push 非必须，但未 commit 的改动仅在本机。",
        "knowledge_collections": {
            "workflow-automation-pack": "可自动化 workflow · manifest L0–L4 · gate/CEO 命令",
            "agent-prompt-pack": "SOP / INTEGRATION 路由（短）",
            "cursor-brand-corpus": "本仓全部 MD 的 L0/L1/L2（上下文编排）",
            "brand-ip-knowledge": "Google Drive 背书库（与 Cursor 仓分离）",
        },
        "cursor_must_read_after_reorg": [
            "integration/handoff/openwebui-context-reorg-latest.json",
            "docs/PROMPT-CONTEXT-STANDARD.md",
            "integration/handoff/cursor-openwebui-task-routing.json",
        ],
        "openwebui_chat_tags": [
            "# workflow-automation-pack",
            "# agent-prompt-pack",
            "# cursor-brand-corpus",
            "# brand-ip-knowledge",
        ],
        "workflow_automation": {
            "manifest": "integration/handoff/workflow-automation-manifest.json",
            "catalog_l1": "integration/handoff/workflow-automation-catalog-l1.json",
            "runner": "python3 scripts/run-workflow-from-manifest.py",
            "export": "bash scripts/export-workflow-automation-pack.sh",
        },
        "counts": {
            "md_scanned": len(files),
            "exported_l012": len(entries),
            "skipped_oversize": skipped_size,
            "repo_rewritten": applied,
        },
        "entries_sample": entries[:40],
        "infrastructure": {
            "open_webui": "http://localhost:3000",
            "embedding": "ollama bge-m3 @ host.docker.internal:11434",
            "pipes": ["yage_cot", "yage_long_context"],
            "tools": ["yage_sqlite"],
            "deploy": "bash scripts/deploy-learning-stack.sh",
        },
        "agents_gm_ceo": {
            "manager": "agents/00-manager",
            "gms": [f"agents/{i:02d}-*" for i in range(1, 13)],
            "six_case_doc": "docs/CEO-SIX-CASE-GM-TO-CEO-WORKFLOW.md",
            "eval": [
                "scripts/ceo-triple-eval-baseline-loop.sh",
                "scripts/ceo-double-stress.sh",
                "scripts/evaluate-xhs-brief-complete.py",
            ],
        },
        "sync_commands": [
            "python3 integration/openwebui-rag/scripts/fix_openwebui_rag_ollama_url.py",
            "python3 integration/openwebui-rag/scripts/sync_cursor_brand_corpus_to_openwebui.py",
            "python3 integration/openwebui-rag/scripts/sync_agent_prompt_pack_to_openwebui.py",
        ],
    }
    HANDOFF.parent.mkdir(parents=True, exist_ok=True)
    HANDOFF.write_text(json.dumps(handoff, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"SCAN {len(files)} md")
    print(f"EXPORT {len(entries)} → {mirror}")
    print(f"APPLY_REPO {applied}")
    print(f"HANDOFF {HANDOFF}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
