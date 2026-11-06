#!/usr/bin/env python3
"""Simon (data flow) + Anthropic (quotes / memory) fusion for Drive-backed long context.

Writes integration/handoff/drive-long-context-fusion.json and optional per-task bindings.
CEO / Agent Must read the manifest before longform + Drive 背书.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FUSION_PATH = ROOT / "integration/handoff/drive-long-context-fusion.json"
TASK_LATEST = ROOT / "content/evolution/00-manager/ceo-inbox/drive-fusion-task-latest.json"
SCREEN_MD = ROOT / "content/evolution/00-manager/ceo-inbox/xhs-drive-screen-latest.md"
SCREEN_JSON = ROOT / "content/evolution/00-manager/ceo-inbox/xhs-drive-screen-latest.json"
CEO_MANIFEST = ROOT / "content/evolution/00-manager/ceo-inbox/CEO-RUN-MANIFEST-latest.json"
MIRROR_DIR = ROOT / "content/personal-ip/intake/_mirror/drive-fusion"
GDOCS_PY = ROOT / ".venv/bin/python"
SECRETS = ROOT / "vendor/gdocs-skill/secrets"
WRITING_GOAL = re.compile(
    r"写|笔记|Brief|brief|小红书|Drive|背书|口播|定稿|LinkedIn|Medium|长稿|艺术家|文案|种草",
    re.I,
)


def fusion_manifest() -> dict:
    return {
        "version": "2026-11-05",
        "tagline": "Simon：数据少进 LLM；Anthropic：先进 LLM 的必须引用优先、外置 memory。Drive 背书两条都要。",
        "docs_human": "docs/DRIVE-LONG-CONTEXT-FUSION.md",
        "docs_must_read": [
            "docs/AGENT-DRIVE-CONTEXT-EXTERNALIZATION.md",
            "docs/PROMPT-CONTEXT-STANDARD.md",
            "docs/CONTEXT-WINDOW-AND-DATA-ROUTING.md",
            "rules/skills/skill_google_docs.md",
        ],
        "drive_tiers": {
            "T0_git": {
                "what": "content/ docs/ agents/ 定稿与 SOP",
                "agent": "Must 优先读 Git，不复制整段 chat",
            },
            "T1_curated": {
                "what": "drive-context-manifest.json tier1 文件夹",
                "agent": "可 Open WebUI brand-ip-knowledge RAG 短问，必须 Sources",
                "never": "代替 T2 精读",
            },
            "T2_ocean": {
                "what": "Drive 书海 / 小红书资料库等海量文件",
                "agent": "screen → 按需 gdocs 打开 → 写入 evidence scratchpad",
                "never": "全量 embedding、整库贴进 prompt",
            },
        },
        "lines": {
            "simon_willison": {
                "focus": "数据怎么流动（少进 LLM）",
                "practices": [
                    "先目录/元数据（listing、screen shortlist），再按需读单个文件",
                    "正文用 gdocs CLI / Drive MCP 落到磁盘或 mirror，不粘贴进 chat",
                    "多文件用脚本步骤串联；大段正文可不经过模型",
                    "可选：Drive listing → sqlite/JSON 索引（google-drive-to-sqlite 思路）",
                ],
                "references": [
                    "https://simonwillison.net/2024/Aug/26/long-context-prompting-tips/",
                    "https://simonwillison.net/2025/Nov/4/code-execution-with-mcp/",
                ],
            },
            "anthropic": {
                "focus": "进 LLM 的那一段怎么写、多轮怎么不丢",
                "practices": [
                    "长材料在 prompt 上方，问题与指令在下方",
                    "阶段 A：只抽 direct quotes（原文「…」），再阶段 B 合成",
                    "事实、数字、Owner 约束写入 Git evidence/intake，不靠 compaction 摘要",
                    "可重新拉取的 tool 结果不要长期堆在 context（tool-result clearing 思路）",
                ],
                "references": [
                    "https://www.anthropic.com/news/prompting-long-context",
                    "https://www.anthropic.com/research/effective-context-engineering-for-ai-agents",
                ],
            },
            "merged_iron_rules": [
                "禁止把整片 Google Drive 或整篇长 chat 当作定稿 prompt",
                "禁止无 drive_file_id / 无原文摘录的 Drive 事实写进 Brief 或 HTML",
                "T2 必须 screen → 打开 ≤max_files_per_task 个原件 → evidence scratchpad",
                "长文输出可走 Open WebUI Pipe；事实只认 Git 里的 evidence/intake",
                "合成前 Must 完成 phase_a_extract_quotes；不够则继续读或标未解决，禁止硬编",
            ],
        },
        "artifacts": {
            "fusion_manifest": "integration/handoff/drive-long-context-fusion.json",
            "ceo_corpus_folders": "integration/handoff/ceo-drive-corpus-folders.json",
            "ceo_catalog_live": "content/personal-ip/intake/_raw/ceo-drive-catalog-live.json",
            "refresh_catalog_script": "scripts/refresh-ceo-drive-catalog.py",
            "drive_context_manifest": "integration/handoff/drive-context-manifest.json",
            "screen_script": "scripts/ceo-task-drive-corpus-screen.py",
            "corpus_screen_lib": "scripts/ceo_corpus_screen_lib.py",
            "corpus_screens_dir": "content/evolution/00-manager/ceo-inbox/corpus-screens",
            "screen_md": "content/evolution/00-manager/ceo-inbox/xhs-drive-screen-latest.md",
            "screen_json": "content/evolution/00-manager/ceo-inbox/xhs-drive-screen-latest.json",
            "task_binding_latest": "content/evolution/00-manager/ceo-inbox/drive-fusion-task-latest.json",
            "evidence_path_template": "content/personal-ip/intake/{slug}-drive-evidence.md",
            "intake_path_template": "content/personal-ip/intake/{slug}.md",
            "brief_drive_section": "## Drive 背书",
        },
        "limits": {
            "max_files_per_task": 8,
            "max_open_files_without_evidence_update": 0,
            "min_quote_chars": 8,
            "max_excerpt_chars_per_file": 12000,
        },
        "text_extraction": {
            "script": "scripts/drive_corpus_extract_text.py",
            "formats": [
                "pdf (pdftotext / optional pypdf)",
                "docx pptx xlsx",
                "epub fb2",
                "mobi azw azw3 (calibre ebook-convert if installed)",
                "txt md html csv json xml rtf",
            ],
            "fallback": "Google Docs/Sheets/Slides export via gdocs drive download then extract",
        },
        "ceo_pipeline_order": [
            {
                "order": 0,
                "id": "read_fusion_manifest",
                "action": "读 fusion JSON（本文件）",
                "path": "integration/handoff/drive-long-context-fusion.json",
                "must_not_skip": True,
            },
            {
                "order": 1,
                "id": "screen_catalog",
                "action": "按 goal 筛文件名（不写 body 进 prompt）",
                "script": "python3 scripts/screen-xhs-drive-corpus.py --goal \"<Owner原话>\"",
                "outputs": [
                    "content/evolution/00-manager/ceo-inbox/xhs-drive-screen-latest.md",
                ],
                "must_not_skip": True,
            },
            {
                "order": 2,
                "id": "bind_task",
                "action": "自动 bind（从 manifest/brief/screen 读 goal，无需 Owner 重复原话）",
                "script": "python3 scripts/build-drive-long-context-fusion.py --auto --phase ceo_dispatch",
                "outputs": ["content/evolution/00-manager/ceo-inbox/drive-fusion-task-latest.json"],
                "must_not_skip": True,
            },
            {
                "order": 2.5,
                "id": "pre_delivery_gate",
                "action": "定稿前：hydrate（如需）+ validate evidence",
                "script": "python3 scripts/build-drive-long-context-fusion.py --auto --phase pre_delivery [--brief path]",
                "must_not_skip": True,
            },
            {
                "order": 3,
                "id": "read_originals",
                "action": "对 shortlist 逐个 gdocs/Drive 读原件（Simon）",
                "skill": "rules/skills/skill_google_docs.md",
                "must_not_skip": True,
            },
            {
                "order": 4,
                "id": "phase_a_quotes",
                "action": "写入 evidence scratchpad：仅原文摘录 + file id（Anthropic）",
                "path_template": "content/personal-ip/intake/{slug}-drive-evidence.md",
                "must_not_skip": True,
            },
            {
                "order": 5,
                "id": "phase_b_synthesize",
                "action": "写稿/Brief 只引用 evidence；长输出走 Open WebUI Pipe",
                "router": "scripts/run-openwebui-router-pipeline.sh",
                "must_not_skip": False,
            },
            {
                "order": 6,
                "id": "cross_check_t1",
                "action": "可选：T1 RAG 短问交叉核对，要 Sources",
                "must_not_skip": False,
            },
            {
                "order": 7,
                "id": "ceo_gate_evolution",
                "action": "evolution / gate；analyze-brief-evolution-gap 查 Drive 摘录",
                "script": "scripts/analyze-brief-evolution-gap.py",
                "must_not_skip": True,
            },
        ],
        "prompt_templates": {
            "phase_a_extract_quotes": (
                "你正在做阶段 A（只抽取，不写作）。\n"
                "文件：{file_name} · drive_file_id={file_id}\n"
                "目标：{goal_one_line}\n"
                "只输出与目标相关的 direct quotes：每条用中文书名号「…」包住原文，"
                "每条注明来自该文件的哪一段（小节/页码若可知）。\n"
                "若无相关内容，只写 NONE。禁止总结、禁止结论。"
            ),
            "phase_b_synthesize": (
                "你正在做阶段 B（合成）。\n"
                "只能使用 evidence 文件中的 quote id 与原文；"
                "每条主张必须指向 evidence 里的一条 quote。\n"
                "evidence 路径：{evidence_path}\n"
                "目标：{goal_one_line}\n"
                "禁止引入 evidence 中未出现的 Drive 事实。"
            ),
        },
        "evidence_file_schema": {
            "required_frontmatter_keys": ["goal_one_line", "drive_files", "created_at"],
            "required_sections": ["## 摘录（原文）", "## 用于本任务的判断（须指向摘录）", "## 未解决 / 待读"],
            "quote_pattern": "「",
        },
        "forbidden": [
            "跳读 fusion manifest 直接写长稿",
            "screen 后不开原件就写 Drive 背书",
            "把 gdocs 全文贴进 Cursor chat",
            "用 Open WebUI RAG 代替 T2 精读",
            "用 chat 摘要代替 evidence 文件",
            "无「」原文摘录就定稿",
        ],
        "verify": {
            "write_manifest": "python3 scripts/build-drive-long-context-fusion.py --write-manifest",
            "auto_ceo": "python3 scripts/build-drive-long-context-fusion.py --auto --phase ceo_dispatch",
            "auto_pre_delivery": "python3 scripts/build-drive-long-context-fusion.py --auto --phase pre_delivery",
            "auto_full": "bash scripts/run-drive-long-context-fusion-auto.sh",
            "shell": "bash scripts/verify-drive-long-context-fusion.sh",
        },
        "auto_phases": {
            "ceo_dispatch": "CEO 派活：screen 后 bind + task-latest（不 validate）",
            "pre_delivery": "定稿前：bind 刷新 + gdocs hydrate + validate（FAIL→exit 42）",
            "full": "ceo_dispatch 然后 pre_delivery",
        },
        "related_handoff": [
            "integration/handoff/ceo-full-execution-cycle.json",
            "integration/handoff/cursor-openwebui-task-routing.json",
        ],
    }


def slugify(goal: str) -> str:
    s = re.sub(r"[^\w\u4e00-\u9fff]+", "-", goal.strip()).strip("-")[:48]
    return s or "task"


def evidence_template(slug: str, goal: str) -> str:
    return f"""# drive-evidence · {slug}

- goal_one_line: {goal}
- drive_files: []
- created_at: {datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}
- fusion_manifest: integration/handoff/drive-long-context-fusion.json

## 摘录（原文）

<!-- 每个文件一小节；每条必须是 direct quote，用「」包住 -->

### file: <名称> · id=<drive_file_id>

- q1: 「…原文…」

## 用于本任务的判断（须指向摘录）

- c1: （对应 q1）…

## 未解决 / 待读

- …
"""


def bind_task(goal: str, brief: str = "") -> dict:
    slug = slugify(goal)
    if brief:
        slug = Path(brief).name.replace("-brief.md", "") or slug
    evidence_rel = f"content/personal-ip/intake/{slug}-drive-evidence.md"
    evidence_path = ROOT / evidence_rel
    binding = {
        "bound_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "goal": goal.strip(),
        "brief": brief.strip(),
        "slug": slug,
        "manifest": str(FUSION_PATH.relative_to(ROOT)),
        "ceo_must_read_first": [
            "integration/handoff/drive-long-context-fusion.json",
            "content/evolution/00-manager/ceo-inbox/drive-fusion-task-latest.json",
        ],
        "paths": {
            "screen_md": str(SCREEN_MD.relative_to(ROOT)),
            "screen_json": str(SCREEN_JSON.relative_to(ROOT)),
            "evidence_md": evidence_rel,
            "task_latest": str(TASK_LATEST.relative_to(ROOT)),
        },
        "checklist": [
            {"step": 1, "done_when": "xhs-drive-screen-latest.md 存在且已读 shortlist"},
            {"step": 2, "done_when": f"已打开 shortlist 文件并更新 {evidence_rel}"},
            {"step": 3, "done_when": "摘录节至少一条「」且含 drive_file_id"},
            {"step": 4, "done_when": "阶段 B 写稿仅引用 evidence"},
        ],
        "prompts": {
            "phase_a": fusion_manifest()["prompt_templates"]["phase_a_extract_quotes"],
            "phase_b": fusion_manifest()["prompt_templates"]["phase_b_synthesize"].format(
                evidence_path=evidence_rel,
                goal_one_line=goal.strip() or "(见 brief)",
            ),
        },
        "forbidden": fusion_manifest()["forbidden"],
    }
    if not evidence_path.is_file() and goal.strip():
        evidence_path.parent.mkdir(parents=True, exist_ok=True)
        evidence_path.write_text(
            evidence_template(slug, goal.strip()),
            encoding="utf-8",
        )
        binding["evidence_created"] = True
    else:
        binding["evidence_created"] = False
    return binding


def resolve_context(brief_arg: str = "", goal_arg: str = "") -> dict:
    brief = (brief_arg or os.environ.get("CEO_SIX_CASE_BRIEF") or os.environ.get("CEO_OWNER_EXTRA_BRIEF") or "").strip()
    goal = (goal_arg or os.environ.get("CEO_GOAL") or "").strip()
    if TASK_LATEST.is_file():
        try:
            task = json.loads(TASK_LATEST.read_text(encoding="utf-8"))
            goal = goal or str(task.get("goal") or "")
            brief = brief or str(task.get("brief") or "")
        except json.JSONDecodeError:
            pass
    if CEO_MANIFEST.is_file():
        try:
            manifest = json.loads(CEO_MANIFEST.read_text(encoding="utf-8"))
            goal = goal or str(manifest.get("goal") or "")
            brief = brief or str(manifest.get("brief") or "")
        except json.JSONDecodeError:
            pass
    if SCREEN_JSON.is_file():
        try:
            screen = json.loads(SCREEN_JSON.read_text(encoding="utf-8"))
            goal = goal or str(screen.get("goal") or "")
        except json.JSONDecodeError:
            pass
    slug = slugify(goal)
    if brief:
        bp = Path(brief)
        if not bp.is_absolute():
            bp = ROOT / bp
        if bp.is_file():
            slug = bp.name.replace("-brief.md", "") or slug
            brief = str(bp.relative_to(ROOT)) if bp.is_relative_to(ROOT) else str(bp)
    evidence_rel = f"content/personal-ip/intake/{slug}-drive-evidence.md"
    needs = bool(brief)
    if not needs and goal and WRITING_GOAL.search(goal):
        needs = True
    if not needs and SCREEN_JSON.is_file():
        try:
            sel = json.loads(SCREEN_JSON.read_text(encoding="utf-8")).get("selected") or []
            needs = needs or (len(sel) > 0 and bool(goal))
        except json.JSONDecodeError:
            pass
    return {
        "goal": goal,
        "brief": brief,
        "slug": slug,
        "evidence_md": evidence_rel,
        "evidence_path": ROOT / evidence_rel,
        "needs_fusion": needs,
    }


def brief_drive_screen(brief: str) -> Path | None:
    if not brief:
        return None
    slug = Path(brief).name.replace("-brief.md", "")
    path = ROOT / "content/evolution/04-xhs-topic-manager" / slug / "drive-screen.json"
    return path if path.is_file() else None


def load_screen_selected(brief: str) -> list[dict]:
    bound = brief_drive_screen(brief)
    if bound:
        return json.loads(bound.read_text(encoding="utf-8")).get("selected") or []
    if SCREEN_JSON.is_file():
        return json.loads(SCREEN_JSON.read_text(encoding="utf-8")).get("selected") or []
    return []


def ensure_brief_screen(brief: str, goal: str) -> None:
    if not brief or brief_drive_screen(brief):
        return
    if not goal:
        return
    py = GDOCS_PY if GDOCS_PY.is_file() else Path(sys.executable)
    cmd = [str(py), "scripts/screen-xhs-drive-corpus.py", "--goal", goal, "--brief", brief]
    subprocess.run(cmd, cwd=ROOT, check=False)


def _load_text_extractor():
    spec = importlib.util.spec_from_file_location(
        "drive_corpus_extract_text", ROOT / "scripts/drive_corpus_extract_text.py"
    )
    if spec is None or spec.loader is None:
        return None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def gdocs_download_text(file_id: str) -> str:
    py = GDOCS_PY if GDOCS_PY.is_file() else Path(sys.executable)
    out = MIRROR_DIR / file_id
    out.mkdir(parents=True, exist_ok=True)
    cmd = [
        str(py),
        "-m",
        "gdocs",
        "--secrets-dir",
        str(SECRETS),
        "drive",
        "download",
        file_id,
        "--output-dir",
        str(out),
    ]
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    if r.returncode != 0:
        return ""
    extract = _load_text_extractor()
    if extract is None:
        return ""
    limit = fusion_manifest()["limits"].get("max_excerpt_chars_per_file", 12000)
    return extract.collect_text_from_tree(out, max_chars=int(limit))


def gemini_extract_quotes(goal: str, file_name: str, file_id: str, body: str) -> list[str]:
    if not body.strip():
        return []
    spec = importlib.util.spec_from_file_location("evolve_hits", ROOT / "scripts/evolve-platform-hits.py")
    if spec is None or spec.loader is None:
        return []
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    prompt = fusion_manifest()["prompt_templates"]["phase_a_extract_quotes"].format(
        file_name=file_name,
        file_id=file_id,
        goal_one_line=goal,
    )
    prompt += f"\n\n--- 文件正文（截断）---\n{body[:8000]}\n\n只输出 JSON：{{\"quotes\": [\"…\", \"…\"]}} 每条必须是原文子串，用中文「」包住。"
    try:
        data = mod.gemini_json(prompt)
    except Exception:
        return []
    raw = data.get("quotes") or data.get("quote") or []
    if isinstance(raw, str):
        raw = [raw]
    out: list[str] = []
    for item in raw:
        s = str(item).strip()
        if not s:
            continue
        if "「" not in s:
            s = f"「{s.strip('「」')}」"
        out.append(s)
    return out[:6]


def hydrate_evidence(ctx: dict) -> dict:
    goal = ctx["goal"]
    brief = ctx["brief"]
    path: Path = ctx["evidence_path"]
    selected = load_screen_selected(brief)
    report = {"hydrated_files": 0, "skipped": [], "errors": []}
    if not selected:
        report["errors"].append("screen shortlist 为空，无法 hydrate")
        return report
    sections: list[str] = []
    drive_files: list[dict] = []
    for item in selected[:8]:
        fid = str(item.get("id") or "")
        name = str(item.get("name") or fid)
        if not fid:
            continue
        body = gdocs_download_text(fid)
        quotes = gemini_extract_quotes(goal, name, fid, body) if body else []
        if not quotes and body:
            snippet = body.strip().replace("\n", " ")[:200]
            if len(snippet) >= 20:
                quotes = [f"「{snippet}」"]
        if not quotes:
            report["skipped"].append(name)
            continue
        drive_files.append({"name": name, "id": fid})
        sections.append(f"### file: {name} · id={fid}\n")
        for i, q in enumerate(quotes, 1):
            sections.append(f"- q{i}: {q}\n")
        report["hydrated_files"] += 1
    header = evidence_template(ctx["slug"], goal or brief or ctx["slug"])
    if drive_files:
        header = header.replace("drive_files: []", f"drive_files: {json.dumps(drive_files, ensure_ascii=False)}")
    excerpt = "## 摘录（原文）\n\n" + "".join(sections) if sections else "## 摘录（原文）\n\n（hydrate 未拉到原文，见未解决）\n"
    rest = "\n## 用于本任务的判断（须指向摘录）\n\n- （Agent 定稿前补）\n\n## 未解决 / 待读\n\n"
    if report["skipped"]:
        rest += "- 未能 hydrate：" + "；".join(report["skipped"][:8]) + "\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(header.split("## 摘录（原文）")[0] + excerpt + rest, encoding="utf-8")
    return report


def run_auto(phase: str, *, brief: str = "", goal: str = "", hydrate: bool = True) -> int:
    if not FUSION_PATH.is_file():
        write_manifest()
    ctx = resolve_context(brief, goal)
    result = {
        "phase": phase,
        "needs_fusion": ctx["needs_fusion"],
        "goal": ctx["goal"],
        "brief": ctx["brief"],
        "slug": ctx["slug"],
        "evidence_md": ctx["evidence_md"],
    }
    if not ctx["needs_fusion"]:
        print(json.dumps({**result, "skip": True, "reason": "非写作/Drive 背书任务"}, ensure_ascii=False))
        return 0

    if phase in ("ceo_dispatch", "full"):
        binding = bind_task(ctx["goal"], ctx["brief"])
        TASK_LATEST.write_text(json.dumps(binding, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        result["bind"] = "ok"

    if phase in ("pre_delivery", "full"):
        ensure_brief_screen(ctx["brief"], ctx["goal"])
        bind_task(ctx["goal"], ctx["brief"])
        path = ctx["evidence_path"]
        ok, errs = validate_evidence(path)
        if not ok and hydrate:
            hydrate_evidence(ctx)
            ok, errs = validate_evidence(path)
        if not ok:
            result["validate"] = "FAIL"
            result["errors"] = errs
            print(json.dumps(result, ensure_ascii=False), file=sys.stderr)
            print("NEEDS_WORK: drive evidence 未过线 — Agent 补 gdocs 摘录或检查 Google CLI", file=sys.stderr)
            return 42
        result["validate"] = "PASS"

    print(json.dumps(result, ensure_ascii=False))
    return 0


def validate_evidence(path: Path) -> tuple[bool, list[str]]:
    errors: list[str] = []
    if not path.is_file():
        return False, [f"缺少 evidence 文件: {path}"]
    text = path.read_text(encoding="utf-8")
    for section in fusion_manifest()["evidence_file_schema"]["required_sections"]:
        if section not in text:
            errors.append(f"缺少节: {section}")
    if "goal_one_line:" not in text and "goal_one_line" not in text:
        errors.append("缺少 goal_one_line")
    if "drive_files" not in text:
        errors.append("缺少 drive_files")
    quotes = text.count("「")
    if quotes < 2:
        errors.append("摘录至少需要一条「…」原文（找到少于 2 个「）")
    if errors:
        return False, errors
    return True, []


def write_manifest() -> None:
    FUSION_PATH.parent.mkdir(parents=True, exist_ok=True)
    payload = fusion_manifest()
    payload["generated_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    FUSION_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"wrote": str(FUSION_PATH.relative_to(ROOT))}, ensure_ascii=False))


def main() -> int:
    parser = argparse.ArgumentParser(description="Drive long-context fusion manifest")
    parser.add_argument("--write-manifest", action="store_true", help="Write fusion JSON to integration/handoff/")
    parser.add_argument("--bind-task", action="store_true", help="Write drive-fusion-task-latest.json for CEO")
    parser.add_argument("--goal", default="", help="Owner goal for bind-task")
    parser.add_argument("--brief", default="", help="Optional brief path for slug")
    parser.add_argument("--validate-evidence", type=Path, help="Validate an evidence markdown file")
    parser.add_argument(
        "--auto",
        action="store_true",
        help="Resolve goal/brief from env + manifest; run bind and/or validate without Owner retyping",
    )
    parser.add_argument(
        "--phase",
        default="full",
        choices=("ceo_dispatch", "pre_delivery", "full"),
        help="ceo_dispatch=派活 bind; pre_delivery=定稿前 hydrate+validate; full=both",
    )
    parser.add_argument(
        "--no-hydrate",
        action="store_true",
        help="With --auto pre_delivery: do not call gdocs/Gemini hydrate",
    )
    args = parser.parse_args()

    if args.write_manifest:
        write_manifest()
        return 0

    if args.bind_task:
        if not FUSION_PATH.is_file():
            write_manifest()
        binding = bind_task(args.goal, args.brief)
        TASK_LATEST.parent.mkdir(parents=True, exist_ok=True)
        TASK_LATEST.write_text(json.dumps(binding, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({"wrote": str(TASK_LATEST.relative_to(ROOT)), "slug": binding["slug"]}, ensure_ascii=False))
        return 0

    if args.validate_evidence:
        ok, errs = validate_evidence(args.validate_evidence if args.validate_evidence.is_absolute() else ROOT / args.validate_evidence)
        if ok:
            print("RESULT: PASS validate-evidence")
            return 0
        for e in errs:
            print(f"FAIL: {e}", file=sys.stderr)
        return 1

    if args.auto:
        return run_auto(args.phase, brief=args.brief, goal=args.goal, hydrate=not args.no_hydrate)

    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
