---
context_version: "2026-10-30-l012"
repo_path: "rules/skills/overlays/temporal-search.local.example.md"
goal: "Temporal 验证 · 本地 overlay（示例）"
openwebui_route: "rag_l1"
cursor_route: "read"
content_sha256: "a2f959e1807b6730"
---

# Temporal 验证 · 本地 overlay（示例）

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** 复制为 `temporal-search.local.md`（gitignored）仅当需要记录 **私有** 检索偏好。
- **Path:** `rules/skills/overlays/temporal-search.local.example.md`
- **Open WebUI:** `rag_l1`
- **Cursor:** `read`


---

## L2 正文

# Temporal 验证 · 本地 overlay（示例）

复制为 `temporal-search.local.md`（gitignored）仅当需要记录 **私有** 检索偏好。

| 项 | 本 workspace 默认 |
|----|-------------------|
| 检索 | Cursor WebSearch / WebFetch；Owner 提供的 URL |
| 可选 CLI | [tavily-skill](https://github.com/grapeot/tavily-skill) vendor 后在此写命令 |
| 勿 commit | API key、内部-only 信源 |

未配置 overlay 时，以 [bestpractice_temporal_info_verification.md](../bestpractice_temporal_info_verification.md) 为准。