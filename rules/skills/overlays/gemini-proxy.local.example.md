---
context_version: "2026-10-30-l012"
repo_path: "rules/skills/overlays/gemini-proxy.local.example.md"
goal: "Gemini 代理 overlay（复制为 gemini-proxy.local.md · gitignore）"
openwebui_route: "rag_l1"
cursor_route: "read"
content_sha256: "6f7bc32797b62de2"
---

# Gemini 代理 overlay（复制为 gemini-proxy.local.md · gitignore）

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** 在 `.env` 增加一行（推荐）：
- **Path:** `rules/skills/overlays/gemini-proxy.local.example.md`
- **Open WebUI:** `rag_l1`
- **Cursor:** `read`


---

## L2 正文

# Gemini 代理 overlay（复制为 gemini-proxy.local.md · gitignore）

在 `.env` 增加一行（推荐）：

```bash
GEMINI_HTTP_PROXY=http://127.0.0.1:3213
```

或在本文件同目录创建 `gemini-proxy.local.md` 仅作备忘；**生效以 `.env` / `.local-config.json` 的 `gemini_http_proxy` 为准。

验证：

```bash
bash scripts/verify-xhs-topic.sh
```