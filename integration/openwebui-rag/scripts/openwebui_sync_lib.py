"""Shared Open WebUI Knowledge sync/diff client (used by yage + Drive folder sync)."""

from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path


@dataclass
class ManifestEntry:
    filename: str
    path: str
    checksum: str
    size: int
    local_file: Path


def load_env(path: Path) -> dict[str, str]:
    if not path.is_file():
        return {}
    out: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        out[k.strip()] = v.strip()
    return out


def cfg(env: dict[str, str], key: str, default: str = "") -> str:
    return os.environ.get(key, env.get(key, default))


class OpenWebUIClient:
    def __init__(self, base_url: str, token: str) -> None:
        self.base = base_url.rstrip("/")
        self.token = token

    def _request(
        self,
        method: str,
        path: str,
        *,
        data: dict | None = None,
        raw_body: bytes | None = None,
        content_type: str = "application/json",
        query: dict | None = None,
    ) -> object:
        url = f"{self.base}{path}"
        if query:
            url += "?" + urllib.parse.urlencode(query)
        headers = {"Authorization": f"Bearer {self.token}", "Accept": "application/json"}
        body = None
        if raw_body is not None:
            body = raw_body
        elif data is not None:
            body = json.dumps(data).encode("utf-8")
            headers["Content-Type"] = content_type
        req = urllib.request.Request(url, data=body, method=method, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=600) as resp:
                raw = resp.read()
                if not raw:
                    return None
                return json.loads(raw.decode("utf-8"))
        except urllib.error.HTTPError as e:
            detail = e.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"{method} {path} -> HTTP {e.code}: {detail[:500]}") from e

    @classmethod
    def sign_in(cls, base_url: str, email: str, password: str) -> OpenWebUIClient:
        url = f"{base_url.rstrip('/')}/api/v1/auths/signin"
        payload = json.dumps({"email": email, "password": password}).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=payload,
            method="POST",
            headers={"Content-Type": "application/json", "Accept": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        token = data.get("token")
        if not token:
            raise RuntimeError("Sign-in succeeded but no token in response")
        return cls(base_url, token)

    @classmethod
    def from_env(cls, env: dict[str, str], base_default: str = "http://127.0.0.1:3000") -> OpenWebUIClient:
        base = cfg(env, "OPENWEBUI_BASE_URL", base_default)
        token = os.environ.get("OPENWEBUI_API_KEY") or cfg(env, "OPENWEBUI_API_KEY")
        email = cfg(env, "OPENWEBUI_EMAIL")
        password = cfg(env, "OPENWEBUI_PASSWORD")
        if token:
            return cls(base, token)
        if email and password:
            return cls.sign_in(base, email, password)
        raise RuntimeError("Set OPENWEBUI_API_KEY or OPENWEBUI_EMAIL + OPENWEBUI_PASSWORD")

    def knowledge_id_by_name(self, name: str) -> str:
        page = 1
        while True:
            data = self._request("GET", "/api/v1/knowledge/", query={"page": page})
            if isinstance(data, list):
                items = data
                total = len(data)
            else:
                items = data.get("items") or []
                total = int(data.get("total") or 0)
            for kb in items:
                if kb.get("name") == name:
                    return kb["id"]
            if not items or page * 30 >= total:
                break
            page += 1
        raise RuntimeError(f"Knowledge base not found: {name!r}")

    def sync_diff(self, kb_id: str, manifest: list[ManifestEntry]) -> dict:
        body = {
            "manifest": [
                {"filename": m.filename, "path": m.path, "checksum": m.checksum, "size": m.size}
                for m in manifest
            ]
        }
        return self._request("POST", f"/api/v1/knowledge/{kb_id}/sync/diff", data=body)

    def create_directory(self, kb_id: str, name: str, parent_id: str | None) -> str:
        payload: dict = {"name": name}
        if parent_id:
            payload["parent_id"] = parent_id
        res = self._request("POST", f"/api/v1/knowledge/{kb_id}/dirs/create", data=payload)
        return res["id"]

    def upload_file(self, local: Path, checksum: str, mime: str = "text/plain") -> str:
        boundary = f"----OpenWebUISync{int(time.time())}"
        metadata = json.dumps({"file_hash": checksum})
        file_bytes = local.read_bytes()
        parts: list[bytes] = []
        parts.append(f"--{boundary}\r\n".encode())
        parts.append(b'Content-Disposition: form-data; name="metadata"\r\n\r\n')
        parts.append(metadata.encode("utf-8") + b"\r\n")
        parts.append(f"--{boundary}\r\n".encode())
        parts.append(
            f'Content-Disposition: form-data; name="file"; filename="{local.name}"\r\n'.encode()
        )
        parts.append(f"Content-Type: {mime}\r\n\r\n".encode())
        parts.append(file_bytes + b"\r\n")
        parts.append(f"--{boundary}--\r\n".encode())
        body = b"".join(parts)
        url = (
            f"{self.base}/api/v1/files/?"
            + urllib.parse.urlencode({"process": "true", "process_in_background": "false"})
        )
        req = urllib.request.Request(
            url,
            data=body,
            method="POST",
            headers={
                "Authorization": f"Bearer {self.token}",
                "Content-Type": f"multipart/form-data; boundary={boundary}",
            },
        )
        with urllib.request.urlopen(req, timeout=600) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        file_id = data.get("id")
        if not file_id:
            raise RuntimeError(f"Upload failed for {local.name}: {data}")
        self._wait_file_processed(file_id)
        return file_id

    def _wait_file_processed(self, file_id: str, timeout: int = 600) -> None:
        deadline = time.time() + timeout
        while time.time() < deadline:
            st = self._request("GET", f"/api/v1/files/{file_id}/process/status")
            status = (st or {}).get("status")
            if status in ("completed", "failed", None):
                if status == "failed":
                    raise RuntimeError(f"File processing failed: {file_id}")
                return
            time.sleep(1)
        raise RuntimeError(f"Timeout waiting for file processing: {file_id}")

    def add_file_to_knowledge(self, kb_id: str, file_id: str, directory_id: str | None) -> None:
        payload: dict = {"file_id": file_id}
        if directory_id:
            payload["directory_id"] = directory_id
        self._request("POST", f"/api/v1/knowledge/{kb_id}/file/add", data=payload)

    def update_file_content(self, file_id: str, content: str) -> None:
        self._request(
            "POST",
            f"/api/v1/files/{file_id}/data/content/update",
            data={"content": content},
        )

    def reindex_file_in_knowledge(self, kb_id: str, file_id: str) -> None:
        self._request("POST", f"/api/v1/knowledge/{kb_id}/file/update", data={"file_id": file_id})

    def sync_cleanup(self, kb_id: str, file_ids: list[str], dir_ids: list[str]) -> None:
        self._request(
            "POST",
            f"/api/v1/knowledge/{kb_id}/sync/cleanup",
            data={"file_ids": file_ids, "dir_ids": dir_ids},
        )


def ensure_directories(
    client: OpenWebUIClient, kb_id: str, mkdir_paths: list[str], dir_map: dict
) -> dict:
    dir_map = dict(dir_map or {})
    for full in sorted(mkdir_paths, key=lambda p: p.count("/")):
        if full in dir_map:
            continue
        parts = full.split("/")
        parent_id = None
        built = ""
        for part in parts:
            built = part if not built else f"{built}/{part}"
            if built in dir_map:
                parent_id = dir_map[built]
                continue
            parent_id = client.create_directory(kb_id, part, parent_id)
            dir_map[built] = parent_id
    return dir_map


def manifest_by_key(manifest: list[ManifestEntry]) -> dict[tuple[str, str], ManifestEntry]:
    return {(m.path, m.filename): m for m in manifest}


def run_sync(
    client: OpenWebUIClient,
    kb_id: str,
    manifest: list[ManifestEntry],
    *,
    continue_on_error: bool = False,
    skip_cleanup: bool = False,
) -> None:
    diff = client.sync_diff(kb_id, manifest)
    print(
        f"sync/diff: +{len(diff.get('added', []))} "
        f"~{len(diff.get('modified', []))} "
        f"-{len(diff.get('deleted', []))} "
        f"={diff.get('unmodified_count', 0)} unchanged"
    )
    dir_map = ensure_directories(client, kb_id, diff.get("mkdir") or [], diff.get("directory_map") or {})
    lookup = manifest_by_key(manifest)

    for item in diff.get("added") or []:
        key = (item.get("path") or "", item["filename"])
        entry = lookup.get(key)
        if not entry:
            print(f"  skip add (no local file): {key}")
            continue
        dir_id = dir_map.get(entry.path) if entry.path else None
        mime = _mime_for(entry.local_file)
        try:
            fid = client.upload_file(entry.local_file, entry.checksum, mime=mime)
            client.add_file_to_knowledge(kb_id, fid, dir_id)
            print(f"  added {entry.path}/{entry.filename}")
        except Exception as exc:
            if not continue_on_error:
                raise
            print(f"  FAILED add {entry.path}/{entry.filename}: {exc}")

    for item in diff.get("modified") or []:
        key = (item.get("path") or "", item["filename"])
        entry = lookup.get(key)
        stale_id = item.get("stale_file_id")
        if not entry or not stale_id:
            continue
        content = entry.local_file.read_text(encoding="utf-8", errors="replace")
        client.update_file_content(stale_id, content)
        client.reindex_file_in_knowledge(kb_id, stale_id)
        print(f"  updated {entry.path}/{entry.filename}")

    if skip_cleanup:
        deleted_ids = [x["file_id"] for x in (diff.get("deleted") or []) if x.get("file_id")]
        if deleted_ids:
            print(f"  skip cleanup ({len(deleted_ids)} would be removed)")
        return

    deleted_ids = [x["file_id"] for x in (diff.get("deleted") or []) if x.get("file_id")]
    rmdir_ids = list(reversed(diff.get("rmdir") or []))
    if deleted_ids or rmdir_ids:
        client.sync_cleanup(kb_id, deleted_ids, rmdir_ids)
        print(f"  cleanup: {len(deleted_ids)} files, {len(rmdir_ids)} dirs")


def _mime_for(path: Path) -> str:
    ext = path.suffix.lower()
    return {
        ".md": "text/markdown",
        ".txt": "text/plain",
        ".csv": "text/csv",
        ".json": "application/json",
        ".html": "text/html",
        ".htm": "text/html",
    }.get(ext, "text/plain")
