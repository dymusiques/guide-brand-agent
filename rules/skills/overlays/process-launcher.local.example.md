---
context_version: "2026-10-30-l012"
repo_path: "rules/skills/overlays/process-launcher.local.example.md"
goal: "process-launcher · Local Overlay (example)"
openwebui_route: "rag_l1"
cursor_route: "read"
content_sha256: "d93bef2527f633ec"
---

# process-launcher · Local Overlay (example)

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** 复制为 `process-launcher.local.md`（gitignored）。真实 job、路径、`.env` **只**写在此或 `vendor/process-launcher/config/launcher.yaml`。
- **Path:** `rules/skills/overlays/process-launcher.local.example.md`
- **Open WebUI:** `rag_l1`
- **Cursor:** `read`

## 章节锚点
- **预留配方（默认未启用）**: Git 内可复制的 YAML 片段（**全部 `enabled: false`**）：
- **与 Cursor Agent 的关系**: - OpenCode `opencode_skill append` 示例 **不适用** 本仓；Patrol 若要用，改为延时触发 **shell 脚本 + 固定 prompt 文件** 或 Own…


---

## L2 正文

# process-launcher · Local Overlay (example)

复制为 `process-launcher.local.md`（gitignored）。真实 job、路径、`.env` **只**写在此或 `vendor/process-launcher/config/launcher.yaml`。

| Key | Value（示例 · 按机器改） |
|-----|---------------------------|
| Vendored repo | `vendor/process-launcher/` |
| Local config | `vendor/process-launcher/config/launcher.yaml`（由 `launcher.example.yaml` 复制） |
| Default API | `http://127.0.0.1:7997` |
| Workspace root | `~/Desktop/danying-brand-agent` |
| venv python | `<workspace>/.venv/bin/python` |

## 预留配方（默认未启用）

Git 内可复制的 YAML 片段（**全部 `enabled: false`**）：  
`integration/templates/process-launcher-reserved-jobs.example.yaml` → 合并进 `vendor/process-launcher/config/launcher.yaml`。

| label 前缀 | 用途 | command 示意 |
|------------|------|----------------|
| `dba_autopilot_` | 可选定时跑 CEO 仪表盘（**不**替代会话内 Manager / Owner 发帖） | `["bash", "scripts/manager-autopilot.sh"]` |
| `dba_verify_release_` | 交班前 release verify（需 GEMINI key） | 包装脚本或数组 argv，勿 inline secrets |
| `dba_analytics_` | CSV 进 inbox 后的 pipeline | `["bash", "scripts/analytics-pipeline.sh"]` |

扩展登记：[integration/EXTENSION-POINTS.md](../../integration/EXTENSION-POINTS.md)

周期任务只写在 YAML `periodic_jobs:`；**不要**用 HTTP 创建 periodic。听见 Daily / Playwright 等 TCC 敏感任务若需 launcher 桥接，launcher 本身必须从 **GUI 终端** 启动。

## 与 Cursor Agent 的关系

- OpenCode `opencode_skill append` 示例 **不适用** 本仓；Patrol 若要用，改为延时触发 **shell 脚本 + 固定 prompt 文件** 或 Owner 手动开新 Cursor 会话。
- 私密 token、Gemini key、OAuth 路径 **不得** 写进 scheduled `command` 字符串；用 `env_file` 或 shell 包装脚本。