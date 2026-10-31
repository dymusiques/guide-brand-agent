#!/usr/bin/env python3
"""Route Owner/CEO goals to Open WebUI (SKIP / RAG_ONLY / PIPE_COT / PIPE_DILIGENT / HYBRID)."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SKIP_PATTERNS = [
    r"gate\b",
    r"verify",
    r"验收",
    r"对抗",
    r"adversarial",
    r"只改",
    r"小改",
    r"修 typo",
    r"html",
    r"canva",
    r"封面",
    r"发帖",
]
COT_PATTERNS = [
    r"口播",
    r"视频文案",
    r"linkedin",
    r"系列",
    r"深度",
    r"提纲",
    r"outline",
    r"分节",
    r"长文",
    r"2000",
    r"3000",
    r"4000",
    r"co?t\b",
    r"写作",
    r"白皮书",
]
DILIGENT_PATTERNS = [
    r"翻译",
    r"translate",
    r"全文改写",
    r"整份",
    r"mirror",
    r"长文档",
]
RAG_PATTERNS = [
    r"只要事实",
    r"库里",
    r"引用",
    r"背书",
    r"检索",
    r"sources?",
    r"消费心理",
    r"品牌库",
    r"# brand",
]
WEBSITE_PATTERNS = [r"网站", r"landing", r"落地页", r"fluid", r"fluid body", r"seo", r"多 section"]
WBR_SQL_PATTERNS = [
    r"\bsql\b",
    r"sqlite",
    r"events\.db",
    r"数据表",
    r"execute_read_query",
    r"chart\.js",
    r"markdown table",
    r"wbr",
    r"周业务",
]


def context_hints_for(route: str, goal: str) -> list[str]:
    hints: list[str] = []
    if route in ("PIPE_COT", "HYBRID"):
        hints.append("Use Open WebUI CoT Pipe — split long output; avoid single-shot 3000+ chars in Cursor.")
    if route == "PIPE_DILIGENT":
        hints.append("Use Diligent Pipe for full-document translate/rewrite; verify head/mid/tail samples.")
    if route == "RAG_ONLY":
        hints.append("Chat with # brand-ip-knowledge; require Sources; spot-check Drive mirror.")
    if match_any(goal, WBR_SQL_PATTERNS):
        hints.append(
            "SQL/structured: Open WebUI llama3.2:3b + SQLite Tool (your db in Valve); cross-check tool CSV vs summary."
        )
    if route == "SKIP" and match_any(goal, COT_PATTERNS + DILIGENT_PATTERNS):
        hints.append("Long output detected but routed SKIP — consider rephrasing goal or use --brief for Manager.")
    return hints


def slugify(text: str, max_len: int = 48) -> str:
    s = re.sub(r"[^\w\u4e00-\u9fff]+", "-", text.strip().lower())
    s = re.sub(r"-+", "-", s).strip("-")
    return (s[:max_len] or "goal").strip("-")


def match_any(text: str, patterns: list[str]) -> bool:
    low = text.lower()
    return any(re.search(p, low, re.I) for p in patterns)


def decide_route(goal: str, *, platform: str, brief_path: str | None) -> dict:
    g = goal.strip()
    if not g:
        return {"route": "SKIP", "reason": "empty goal"}

    if match_any(g, SKIP_PATTERNS) and not match_any(g, COT_PATTERNS + DILIGENT_PATTERNS):
        return {"route": "SKIP", "reason": "gate/verify/small-edit task"}

    outbox_kind = "website" if platform == "website" or match_any(g, WEBSITE_PATTERNS) else "personal_ip"

    if match_any(g, RAG_PATTERNS) and not match_any(g, COT_PATTERNS + DILIGENT_PATTERNS):
        return {
            "route": "RAG_ONLY",
            "reason": "fact retrieval only",
            "outbox_kind": outbox_kind,
        }

    if match_any(g, DILIGENT_PATTERNS):
        return {
            "route": "PIPE_DILIGENT",
            "reason": "long translation/rewrite",
            "outbox_kind": outbox_kind,
        }

    if match_any(g, COT_PATTERNS) or len(g) > 400:
        route = "HYBRID" if match_any(g, RAG_PATTERNS + [r"brief", r"小红书", r"xhs", r"ip"]) else "PIPE_COT"
        return {
            "route": route,
            "reason": "long structured writing",
            "outbox_kind": outbox_kind,
        }

    if brief_path and Path(brief_path).is_file():
        return {"route": "SKIP", "reason": "existing brief path — use Manager pipeline directly"}

    return {"route": "SKIP", "reason": "default short task — Cursor/CEO only"}


def attach_hints(payload: dict, goal: str) -> dict:
    payload["context_hints"] = context_hints_for(payload.get("route", "SKIP"), goal)
    payload["data_access"] = {
        "drive_rag": "# brand-ip-knowledge (sync: LLM-Ollama/RAG/RAG/scripts)",
        "sqlite_tool": "Open WebUI yage_sqlite — configure db path for your data",
        "cursor_drive_mcp": "google-auth-status PASS → gdocs CLI / Drive MCP",
    }
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description="Open WebUI router for CEO/Manager goals")
    parser.add_argument("--goal", "-g", required=True, help="Owner or CEO goal text")
    parser.add_argument("--brief", default="", help="Optional brief path if known")
    parser.add_argument("--platform", choices=("auto", "personal_ip", "website"), default="auto")
    parser.add_argument("--slug", default="", help="Override output slug")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()

    platform = args.platform
    if platform == "auto":
        platform = "website" if match_any(args.goal, WEBSITE_PATTERNS) else "personal_ip"

    decision = decide_route(args.goal, platform=platform, brief_path=args.brief or None)
    slug = args.slug or slugify(args.goal)
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    payload = {
        "version": 1,
        "created_at": ts,
        "goal": args.goal,
        "brief_path": args.brief or None,
        "platform": platform,
        "slug": slug,
        "status": "planned" if args.dry_run else "pending",
        **decision,
    }
    payload = attach_hints(payload, args.goal)

    if args.as_json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(f"route={payload['route']} reason={payload['reason']} slug={slug} platform={platform}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
