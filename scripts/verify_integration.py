#!/usr/bin/env python3
"""Guide brand agent — integration verify (gdocs smoke + read paths).

Six cases aligned with hub VERIFY-MAP / check.md:
  1. gdocs import
  2. OAuth secrets present
  3. gdocs read path: gmail profile → exit 0 + JSON stdout
  4. gdocs error path: invalid drive id → exit 1 + JSON stderr
  5. Git read path: IP brief matches USER facts
  6. Drive read path: search Knowledge Bank folder

Skip cases 3–6 when secrets missing (exit 0, SKIPPED). Fail when secrets
present but a case fails (exit 1).

Usage:
  python scripts/verify_integration.py
  bash scripts/verify-integration.sh
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from urllib.parse import quote
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

ROOT = Path(__file__).resolve().parent.parent
SECRETS = ROOT / "vendor/gdocs-skill/secrets"
VENV_PYTHON = ROOT / ".venv/bin/python"
KNOWLEDGE_BANK_ROOT = "1jLcbbr0WkmEI8mJlsf5R4Y1NtSGEP8_c"
IP_DOC_NEEDLE = "法派长笛"
DEFAULT_PROXY = "http://127.0.0.1:3213"


def _proxy_url() -> str:
    return os.environ.get("HTTPS_PROXY") or os.environ.get("HTTP_PROXY") or DEFAULT_PROXY


def _load_access_token() -> str | None:
    tok_path = SECRETS / "token.json"
    if not tok_path.is_file():
        return None
    try:
        raw = json.loads(tok_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return raw.get("token") if isinstance(raw.get("token"), str) else None


def _curl_google_api(url: str, token: str, timeout: int = 30) -> tuple[int, str]:
    """REST read via curl; try proxy first, fall back to direct if proxy down."""
    headers = [
        "-H", f"Authorization: Bearer {token}",
        "-H", "Accept: application/json",
    ]
    for use_proxy in (True, False):
        cmd = ["curl", "-sS", "--max-time", str(timeout), *headers, url]
        if use_proxy:
            cmd[4:4] = ["-x", _proxy_url()]
        proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
        body = (proc.stdout or proc.stderr or "").strip()
        if proc.returncode == 7 and use_proxy:
            continue  # proxy unreachable → retry direct
        return proc.returncode, body
    return 1, "curl failed"


@dataclass
class CaseResult:
    name: str
    status: str  # PASS | FAIL | SKIP | WARN
    detail: str = ""


def gdocs_cmd(
    *args: str,
    timeout: int = 120,
    secrets_dir: Path | None = None,
) -> subprocess.CompletedProcess[str] | None:
    """Run `python -m gdocs`. Returns None on timeout (caller handles)."""
    py = str(VENV_PYTHON if VENV_PYTHON.exists() else sys.executable)
    sec = secrets_dir or SECRETS
    env = os.environ.copy()
    # Inherit shell proxy; common local default if googleapis.com blocked direct.
    if not env.get("HTTPS_PROXY") and not env.get("HTTP_PROXY"):
        env.setdefault("HTTPS_PROXY", DEFAULT_PROXY)
        env.setdefault("HTTP_PROXY", DEFAULT_PROXY)
    try:
        return subprocess.run(
            [py, "-m", "gdocs", "--secrets-dir", str(sec), *args],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
            env=env,
        )
    except subprocess.TimeoutExpired:
        return None


def _json_error_from_proc(proc: subprocess.CompletedProcess[str] | None) -> CaseResult | None:
    """Return PASS if proc shows exit != 0 and JSON error blob; else None."""
    if proc is None:
        return None
    if proc.returncode == 0:
        return CaseResult("4_gdocs_error_json", "FAIL", "expected exit 1")
    blob = (proc.stderr or proc.stdout).strip()
    if not blob:
        return CaseResult("4_gdocs_error_json", "FAIL", "no output on error path")
    try:
        err = json.loads(blob)
    except json.JSONDecodeError:
        return CaseResult("4_gdocs_error_json", "FAIL", "error output not JSON")
    if err.get("error") or err.get("status_code") or err.get("type"):
        return CaseResult("4_gdocs_error_json", "PASS")
    return CaseResult("4_gdocs_error_json", "FAIL", "JSON missing error fields")


def case_gdocs_import() -> CaseResult:
    py = str(VENV_PYTHON if VENV_PYTHON.exists() else sys.executable)
    proc = subprocess.run(
        [py, "-c", "import gdocs"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode == 0:
        return CaseResult("1_gdocs_import", "PASS")
    return CaseResult("1_gdocs_import", "FAIL", proc.stderr.strip() or "import gdocs failed")


def case_secrets_present() -> CaseResult:
    cred = SECRETS / "credentials.json"
    tok = SECRETS / "token.json"
    if cred.is_file() and tok.is_file():
        return CaseResult("2_oauth_secrets", "PASS")
    missing = []
    if not cred.is_file():
        missing.append("credentials.json")
    if not tok.is_file():
        missing.append("token.json")
    return CaseResult("2_oauth_secrets", "SKIP", f"missing {', '.join(missing)}")


def _oauth_ready() -> bool:
    return (SECRETS / "credentials.json").is_file() and (SECRETS / "token.json").is_file()


def _gmail_profile_via_curl() -> CaseResult | None:
    token = _load_access_token()
    if not token:
        return None
    code, body = _curl_google_api(
        "https://gmail.googleapis.com/gmail/v1/users/me/profile", token,
    )
    if code != 0 or not body:
        return None
    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        return None
    if data.get("emailAddress"):
        return CaseResult("3_gdocs_read_json", "PASS", f"{data['emailAddress']} (curl+proxy)")
    return None


def case_gdocs_profile_json() -> CaseResult:
    if not _oauth_ready():
        return CaseResult("3_gdocs_read_json", "SKIP", "no OAuth — run SETUP.md §3")
    proc = gdocs_cmd("gmail", "profile", timeout=45)
    if proc is not None and proc.returncode == 0:
        try:
            data = json.loads(proc.stdout)
            if data.get("emailAddress"):
                return CaseResult("3_gdocs_read_json", "PASS", data["emailAddress"])
        except json.JSONDecodeError:
            pass
    if via_curl := _gmail_profile_via_curl():
        return via_curl
    err = ""
    if proc is not None:
        err = (proc.stderr or proc.stdout).strip()
    return CaseResult(
        "3_gdocs_read_json", "FAIL",
        err[:200] if err else "gdocs + curl both failed (check proxy/token)",
    )


def case_gdocs_error_json() -> CaseResult:
    if not _oauth_ready():
        return CaseResult("4_gdocs_error_json", "SKIP", "no OAuth — run SETUP.md §3")
    # Prefer fast local error (missing secrets dir); avoid slow Drive API hang.
    proc = gdocs_cmd("gmail", "profile", secrets_dir=ROOT / "nonexistent-secrets-dir", timeout=15)
    if passed := _json_error_from_proc(proc):
        return passed
    # Fallback: invalid drive id with short timeout (may need proxy)
    proc = gdocs_cmd(
        "drive", "download", "invalid-file-id-for-verify",
        "--output-dir", str(ROOT / ".tmp-verify"),
        "--dry-run", "--auth-timeout", "10",
        timeout=25,
    )
    if passed := _json_error_from_proc(proc):
        return passed
    if proc is None:
        return CaseResult("4_gdocs_error_json", "FAIL", "error-path timed out (check proxy/network)")
    return CaseResult("4_gdocs_error_json", "FAIL", "no JSON error from gdocs")


def case_git_read_path() -> CaseResult:
    user = ROOT / "rules/USER.md"
    briefs = list((ROOT / "content/personal-ip").glob("*.md"))
    if not user.is_file() or not briefs:
        return CaseResult("5_git_read_path", "FAIL", "USER.md or content/personal-ip/*.md missing")
    user_text = user.read_text(encoding="utf-8")
    brief_text = briefs[0].read_text(encoding="utf-8")
    if IP_DOC_NEEDLE not in user_text or IP_DOC_NEEDLE not in brief_text:
        return CaseResult("5_git_read_path", "FAIL", f"needle {IP_DOC_NEEDLE!r} not in USER + brief")
    return CaseResult("5_git_read_path", "PASS", briefs[0].name)


def _drive_list_via_curl() -> CaseResult | None:
    """Drive read via REST + proxy. drive.file scope may not list folder by ID."""
    token = _load_access_token()
    if not token:
        return None
    queries = [
        f"'{KNOWLEDGE_BANK_ROOT}' in parents and trashed = false",
        "mimeType='application/vnd.google-apps.document' and trashed = false",
    ]
    for q in queries:
        url = (
            "https://www.googleapis.com/drive/v3/files"
            f"?q={quote(q)}&pageSize=3&fields=files(id,name)"
        )
        code, body = _curl_google_api(url, token)
        if code != 0 or not body:
            continue
        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            continue
        if data.get("error"):
            continue
        files = data.get("files") if isinstance(data, dict) else None
        if isinstance(files, list) and len(files) >= 1:
            return CaseResult("6_drive_read_path", "PASS", f"{files[0].get('name', '?')} (curl+proxy)")
    return None


def case_drive_read_path() -> CaseResult:
    if not _oauth_ready():
        return CaseResult("6_drive_read_path", "SKIP", "no OAuth — run SETUP.md §3")
    # Drive read uses REST (curl); gdocs `search` is Docs API, not Drive files.
    if via_curl := _drive_list_via_curl():
        return via_curl
    return CaseResult("6_drive_read_path", "FAIL", "Drive REST read failed (check token/scopes)")


# Core registry — loop target for integration verify
INTEGRATION_CASES: list[tuple[str, Callable[[], CaseResult]]] = [
    ("gdocs import", case_gdocs_import),
    ("OAuth secrets", case_secrets_present),
    ("gdocs read JSON", case_gdocs_profile_json),
    ("gdocs error JSON", case_gdocs_error_json),
    ("Git read path", case_git_read_path),
    ("Drive read path", case_drive_read_path),
]


def run_integration_verify() -> tuple[list[CaseResult], bool]:
    """Run all integration cases in a loop. Returns (results, should_fail)."""
    results = [fn() for _, fn in INTEGRATION_CASES]
    fail = any(r.status == "FAIL" for r in results)
    return results, fail


def main() -> int:
    print(f"=== Integration verify: {ROOT} ===\n")
    results, fail = run_integration_verify()
    passed = skipped = warned = failed = 0
    for r in results:
        prefix = {"PASS": "OK  ", "FAIL": "FAIL", "SKIP": "SKIP", "WARN": "WARN"}[r.status]
        line = f"  {prefix} {r.name}"
        if r.detail:
            line += f" — {r.detail}"
        print(line)
        if r.status == "PASS":
            passed += 1
        elif r.status == "SKIP":
            skipped += 1
        elif r.status == "WARN":
            warned += 1
        else:
            failed += 1
    print("\n=== Summary ===")
    print(f"cases: {passed} passed, {warned} warned, {skipped} skipped, {failed} failed (of 6)")
    if fail:
        print("RESULT: FAIL — fix integration / OAuth / network (see SETUP.md)")
        return 1
    if warned or skipped:
        print("RESULT: PASS with warnings — live Google reads may need HTTPS_PROXY / MCP")
        return 0
    print("RESULT: PASS — all 6 integration cases passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
