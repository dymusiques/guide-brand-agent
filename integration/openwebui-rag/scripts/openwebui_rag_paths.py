"""Canonical paths for Open WebUI ↔ Drive RAG sync (inside danying-brand-agent)."""

from __future__ import annotations

import os
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
RAG_SCRIPTS = Path(__file__).resolve().parent

_LEGACY_MIRROR = Path(
    "/Users/danying/Desktop/未命名/LLM-Ollama/RAG/RAG/brand-knowledge-mirror"
)


def brand_knowledge_mirror() -> Path:
    env = os.environ.get("BRAND_KNOWLEDGE_MIRROR", "").strip()
    if env:
        return Path(env)
    local = REPO_ROOT / "var/brand-knowledge-mirror"
    if _LEGACY_MIRROR.is_dir():
        return _LEGACY_MIRROR
    return local


def rag_subdir(name: str) -> Path:
    return brand_knowledge_mirror() / "_rag" / name


def brand_drive_sync_env() -> Path:
    local = RAG_SCRIPTS / "brand-drive-sync.env"
    if local.is_file():
        return local
    legacy = Path(
        "/Users/danying/Desktop/未命名/LLM-Ollama/RAG/RAG/scripts/brand-drive-sync.env"
    )
    return legacy if legacy.is_file() else local
