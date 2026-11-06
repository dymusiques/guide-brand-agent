"""Extract Owner longform body from XHS brief or linked draft."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DRAFT_LINK = re.compile(r"长稿见[：:]\s*`([^`]+)`")

# Repo / Open WebUI boilerplate — must never ship as Owner-facing copy
_OWNER_JUNK = re.compile(
    r"(context_version|repo_path|openwebui_route|cursor_route|content_sha256|"
    r"## L1 任务|## 章节锚点|xhs-classifier|文章锚点|正文有没有)"
)


def strip_owner_facing_md(text: str) -> str:
    """Human-readable body only: drop YAML frontmatter and L1/锚点 blocks."""
    text = text.strip()
    if text.startswith("---"):
        text = re.sub(r"^---\n.*?\n---\n", "", text, count=1, flags=re.S)
    m = re.search(r"^## L2 正文\s*\n([\s\S]*)", text, re.M)
    if m:
        return m.group(1).strip()
    # Brief without L2 wrapper: skip duplicate H1 + classifier block
    parts = re.split(r"^## L2 正文\s*\n", text, maxsplit=1, flags=re.M)
    if len(parts) == 2:
        return parts[1].strip()
    return text.strip()


def looks_like_agent_scaffold(text: str) -> bool:
    if not text.strip():
        return True
    if _OWNER_JUNK.search(text[:800]):
        return True
    if text.lstrip().startswith("---") and "context_version" in text[:400]:
        return True
    return False


def extract_longform_text(brief: Path) -> str:
    if not brief.is_file():
        return ""
    text = brief.read_text(encoding="utf-8")
    link = DRAFT_LINK.search(text)
    if link:
        p = ROOT / link.group(1).strip()
        if p.is_file():
            raw = p.read_text(encoding="utf-8").strip()
            body = strip_owner_facing_md(raw)
            if body and not looks_like_agent_scaffold(body):
                return body
    m = re.search(r"^## 正文（长稿[^\n]*\n([\s\S]*?)(?=\n## |\Z)", text, re.M)
    if m:
        body = m.group(1).strip()
        if body and not body.startswith("（") and not body.startswith("长稿见"):
            return strip_owner_facing_md(body)
    return ""


def extract_classifier_body(brief: Path) -> str:
    if not brief.is_file():
        return ""
    text = brief.read_text(encoding="utf-8")
    body_m = re.search(r'"body":\s*"([^"]+)"', text, re.S)
    return body_m.group(1) if body_m else ""


def count_cjk_chars(s: str) -> int:
    """Count CJK unified + fullwidth punctuation (rough 汉字量)."""
    return len(re.findall(r"[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]", s))
