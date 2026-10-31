#!/usr/bin/env python3
"""Build L1 workflow catalog from workflow-automation-manifest.json (+ script inventory)."""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "integration/handoff/workflow-automation-manifest.json"
OUT_JSON = ROOT / "integration/handoff/workflow-automation-catalog-l1.json"
OUT_MD = ROOT / "docs/WORKFLOW-AUTOMATION-L1-INDEX.md"
MIRROR = Path(
    "/Users/danying/Desktop/未命名/LLM-Ollama/RAG/RAG/brand-knowledge-mirror/_rag/workflow-automation-pack"
)


def scan_scripts() -> list[dict]:
    scripts_dir = ROOT / "scripts"
    entries: list[dict] = []
    for path in sorted(scripts_dir.rglob("*")):
        if not path.is_file():
            continue
        if path.suffix not in (".sh", ".py"):
            continue
        rel = path.relative_to(ROOT).as_posix()
        if "__pycache__" in rel:
            continue
        first = ""
        try:
            for line in path.read_text(encoding="utf-8", errors="replace").splitlines()[:30]:
                if line.startswith("#") and not line.startswith("#!"):
                    first = line.lstrip("# ").strip()
                    break
        except OSError:
            pass
        entries.append(
            {
                "path": rel,
                "kind": path.suffix[1:],
                "summary": first[:160],
            }
        )
    return entries


def layer_l1(layer: dict) -> dict:
    lid = layer.get("id", "")
    name = layer.get("name", "")
    triggers = layer.get("owner_phrases") or []
    script = layer.get("script") or ""
    scripts = layer.get("scripts") or []
    cmd = script or (scripts[0] if scripts else "")
    return {
        "id": lid,
        "name": name,
        "owner_phrases": triggers,
        "primary_command": cmd,
        "openwebui": layer.get("openwebui_router"),
        "extras": {k: layer[k] for k in layer if k not in ("id", "name", "owner_phrases", "script", "scripts", "openwebui_router")},
    }


def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    layers = [layer_l1(x) for x in manifest.get("layers", [])]
    playbook = manifest.get("agent_playbook", {})
    catalog = {
        "version": manifest.get("version", "2026-10-30"),
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "source_manifest": "integration/handoff/workflow-automation-manifest.json",
        "run_layer": "python3 scripts/run-workflow-from-manifest.py --layer <ID> [--goal \"...\"] [--brief path]",
        "run_owner_phrase": "python3 scripts/run-workflow-from-manifest.py --phrase \"CEO 开始执行\" [--goal \"...\"]",
        "verify": "bash scripts/verify-workflow-automation.sh",
        "coverage": manifest.get("coverage_summary", {}),
        "layers_l1": layers,
        "agent_playbook_l1": {
            "session_start": playbook.get("session_start", []),
            "on_brief_gate_exit_42": playbook.get("on_brief_gate_exit_42", []),
            "must_not": playbook.get("must_not", []),
        },
        "script_inventory_count": 0,
        "script_inventory_sample": [],
    }
    inv = scan_scripts()
    catalog["script_inventory_count"] = len(inv)
    catalog["script_inventory_sample"] = inv[:60]

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# Workflow 自动化 · L1 索引（机器 + 人）",
        "",
        f"> 生成 UTC：`{catalog['generated_utc']}` · JSON：`integration/handoff/workflow-automation-catalog-l1.json`",
        "",
        "## 一键执行",
        "",
        "```bash",
        "python3 scripts/run-workflow-from-manifest.py --list-layers",
        "python3 scripts/run-workflow-from-manifest.py --layer L2_CEO_START --goal \"<Owner 原话>\"",
        "python3 scripts/run-workflow-from-manifest.py --phrase \"CEO 开始执行\" --goal \"<Owner 原话>\"",
        "bash scripts/run-context-reorg-pipeline.sh   # Open WebUI 上下文全量同步",
        "```",
        "",
        "## 层级（L0_BOOT → L4_CAMPAIGN）",
        "",
    ]
    for ly in layers:
        phrases = " · ".join(f"「{p}」" for p in ly.get("owner_phrases", [])[:4])
        lines.append(f"### `{ly['id']}` — {ly['name']}")
        if phrases:
            lines.append(f"- **Owner 触发：** {phrases}")
        if ly.get("primary_command"):
            lines.append(f"- **命令：** `{ly['primary_command']}`")
        ow = ly.get("openwebui")
        if ow:
            lines.append(f"- **Open WebUI 步 −1：** `{ow.get('script', '')}`")
        lines.append("")

    lines.extend(
        [
            "## Open WebUI Knowledge",
            "",
            "- 聊天：`# workflow-automation-pack` — 问「L3 brief gate  exit 42 怎么办」",
            "- 与 `# cursor-brand-corpus` · `# agent-prompt-pack` 并用",
            "",
            "## 验收",
            "",
            "```bash",
            "bash scripts/verify-workflow-automation.sh",
            "```",
            "",
        ]
    )
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")

    MIRROR.mkdir(parents=True, exist_ok=True)
    for src in [
        MANIFEST,
        OUT_JSON,
        OUT_MD,
        ROOT / "docs/WORKFLOW-AUTOMATION-MATRIX.md",
        ROOT / "agents/00-manager/AUTO-WORKFLOW.md",
        ROOT / "docs/CEO-FULL-EXECUTION-MANDATE.md",
        ROOT / "docs/CEO-SIX-CASE-GM-TO-CEO-WORKFLOW.md",
        ROOT / "integration/handoff/ceo-full-execution-cycle.json",
        ROOT / "integration/handoff/ceo-xhs-delivery-cycle.json",
        ROOT / "integration/handoff/cursor-openwebui-task-routing.json",
    ]:
        if src.is_file():
            (MIRROR / src.name).write_bytes(src.read_bytes())

    print(f"CATALOG {OUT_JSON} layers={len(layers)} scripts={len(inv)}")
    print(f"MIRROR {MIRROR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
