"""Load Gemini API key from Guide/0/.env (primary) or environment.

Agent workflow: Owner fills ``.env`` on disk → Python scripts read it at startup →
Agent runs verify in Terminal without pasting keys into chat.

Load order:
  1. ``Guide/0/.env`` via python-dotenv (GEMINI_API_KEY, GEMINI_MODEL)
  2. Optional ``Guide/0/.local-config.json`` (gemini_api_key / gemini_model)
  3. Process environment (export GEMINI_API_KEY=...)
"""

from __future__ import annotations

import json
import os
from pathlib import Path

DEFAULT_MODEL = "gemini-3.5-flash"


def find_project_root() -> Path:
    """Guide/0 root — directory containing AGENTS.md."""
    here = Path(__file__).resolve()
    for parent in [here, *here.parents]:
        if (parent / "AGENTS.md").is_file():
            return parent
    raise RuntimeError("Could not find Guide project root (AGENTS.md)")


def load_dotenv_for_project() -> Path:
    """Load ``.env`` from project root if present. Returns root path."""
    root = find_project_root()
    env_file = root / ".env"
    if env_file.is_file():
        try:
            from dotenv import load_dotenv

            load_dotenv(env_file, override=False)
        except ImportError as exc:
            raise RuntimeError(
                "python-dotenv not installed. Run: "
                "source .venv/bin/activate && pip install -r requirements-gemini.txt"
            ) from exc
    return root


def _local_config_path(root: Path) -> Path:
    return root / ".local-config.json"


def load_local_config(root: Path) -> dict:
    path = _local_config_path(root)
    if path.is_file():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}


def get_api_key() -> str:
    root = load_dotenv_for_project()
    config = load_local_config(root)
    key = config.get("gemini_api_key") or os.environ.get("GEMINI_API_KEY")
    if not key or key == "REPLACE_WITH_YOUR_KEY":
        raise RuntimeError(
            f"Missing Gemini API key. Copy .env.example → {root / '.env'} "
            "and set GEMINI_API_KEY, or use .local-config.json / export."
        )
    return key


def get_model() -> str:
    root = load_dotenv_for_project()
    config = load_local_config(root)
    return (
        config.get("gemini_model")
        or os.environ.get("GEMINI_MODEL")
        or DEFAULT_MODEL
    )
