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


def _detect_local_proxy() -> str | None:
    """Same default as scripts/verify_integration.py — only if port is open."""
    import socket

    host, port = "127.0.0.1", 3213
    try:
        with socket.create_connection((host, port), timeout=0.4):
            return f"http://{host}:{port}"
    except OSError:
        return None


def _proxy_reachable(proxy: str, timeout_s: float = 0.4) -> bool:
    """True if http(s) proxy host:port accepts a TCP connection."""
    import socket
    from urllib.parse import urlparse

    parsed = urlparse(proxy if "://" in proxy else f"http://{proxy}")
    host = parsed.hostname or "127.0.0.1"
    port = parsed.port or (443 if parsed.scheme == "https" else 80)
    try:
        with socket.create_connection((host, port), timeout=timeout_s):
            return True
    except OSError:
        return False


def configure_gemini_network() -> None:
    """Pick a reachable proxy, else direct (Owner global VPN).

    Owner 常见：全局 VPN + .env 里写了 3213 但本地代理未开。
    旧行为：仍走 3213 → Connection refused。
    现行为：3213 不通则 **不** 设 HTTP(S)_PROXY，走系统网络（VPN 在则直连 Gemini）。
    """
    root = load_dotenv_for_project()
    config = load_local_config(root)
    candidates: list[str] = []
    for raw in (
        os.environ.get("GEMINI_HTTP_PROXY"),
        config.get("gemini_http_proxy"),
        os.environ.get("HTTPS_PROXY"),
        os.environ.get("HTTP_PROXY"),
        _detect_local_proxy(),
    ):
        if raw and raw not in candidates:
            candidates.append(str(raw).strip())

    proxy: str | None = None
    for cand in candidates:
        if _proxy_reachable(cand):
            proxy = cand
            break

    if proxy:
        os.environ.setdefault("HTTPS_PROXY", proxy)
        os.environ.setdefault("HTTP_PROXY", proxy)
    else:
        # Avoid stale .env forcing httpx at a dead local port
        for key in ("HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy"):
            val = os.environ.get(key, "")
            if val and "127.0.0.1" in val and not _proxy_reachable(val):
                os.environ.pop(key, None)


def get_api_key() -> str:
    root = load_dotenv_for_project()
    configure_gemini_network()
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
    configure_gemini_network()
    config = load_local_config(root)
    return (
        config.get("gemini_model")
        or os.environ.get("GEMINI_MODEL")
        or DEFAULT_MODEL
    )
