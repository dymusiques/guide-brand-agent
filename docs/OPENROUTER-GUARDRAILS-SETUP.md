---
context_version: "2026-10-30-l012"
repo_path: "docs/OPENROUTER-GUARDRAILS-SETUP.md"
goal: "OpenRouter Guardrails · 逐步设置（链 B · Open WebUI 专用 Key）"
openwebui_route: "rag_l1"
cursor_route: "read"
content_sha256: "63cc17143db4035e"
---

# OpenRouter Guardrails · 逐步设置（链 B · Open WebUI 专用 Key）

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** - [API-KEY-BOUNDARIES.md](./API-KEY-BOUNDARIES.md)
- [OPENWEBUI-CEO-ROUTER.md](./OPENWEBUI-CEO-ROUTER.md)
- **Path:** `docs/OPENROUTER-GUARDRAILS-SETUP.md`
- **Open WebUI:** `rag_l1`
- **Cursor:** `read`

## 章节锚点
- **L1 任务（压缩 · Open WebUI / Cursor 顶栏）**: - **Goal:** > **作用：** 只限制 **Open WebUI 用的那把 OpenRouter API Key**（如 `openweb-ui-01`）。**不**影响 CEO 仓 `G…
- **章节锚点**: - **0. 先对齐本机 slug（与 Guardrail 白名单一致）**: 编辑 `RAG/RAG/scripts/brand-drive-sync.env`（勿提交 git）：
- **相关**: - [API-KEY-BOUNDARIES.md](./API-KEY-BOUNDARIES.md)


---

## L2 正文

# OpenRouter Guardrails · 逐步设置（链 B · Open WebUI 专用 Key）

> **作用：** 只限制 **Open WebUI 用的那把 OpenRouter API Key**（如 `openweb-ui-01`）。**不**影响 CEO 仓 `GEMINI_API_KEY`。  
> 官方：[Guardrails 指南](https://openrouter.ai/docs/guides/features/guardrails)

## 0. 先对齐本机 slug（与 Guardrail 白名单一致）

编辑 `RAG/RAG/scripts/brand-drive-sync.env`（勿提交 git）：

- `OPENWEBUI_RAG_MODEL`
- `OPENWEBUI_PIPE_UPSTREAM_MODEL`

当前示例：`deepseek/deepseek-v4.1-flash-1017`  
Guardrail 的 **Model allowlist** 必须 **包含** 这里写的 slug，否则 Open WebUI 会 **403**。


## 2. 进入 Guardrails 页面

1. 左侧或顶部进入 **Workspaces**。
2. 选你用的 workspace（个人一般是 **Default**）。
3. 打开 **Guardrails**（路径类似：**Workspaces → Default → Guardrails**）。

组织账号需 **Org Admin** 才能建 Guardrail。


## 4. 绑到 API Key（关键：不绑 = 不生效）

1. 打开刚建的 Guardrail 详情。
2. 找到 **API Keys**（或 **Assign**）区域。
3. 选中 **Open WebUI 用的那把 Key**（Activity 里显示的 **`openweb-ui-01`** 或你在 Open WebUI Connections 里贴的那条）。
4. 保存分配。

**规则：** Guardrail **创建后不会自动生效**，必须 **Assign 到 Key 或 Member**。

若一把 Key 同时有 **Member 级** 和 **Key 级** Guardrail：**模型/Provider 取交集（更严）**。


## 6. 验收

1. **允许的路径：**  
   `bash scripts/run-openwebui-router-pipeline.sh --goal "只要事实：smoke" --dry-run`  
   再去掉 `--dry-run` 跑一条短 RAG；OpenRouter Activity 应只有 allowlist 内的 model。

2. **拒绝的路径（可选）：** 在 Open WebUI 聊天里 **手动选** 不在 allowlist 的模型（如 `openai/gpt-4o-mini`）并发一条消息 → 应 **失败 / 403**（Guardrail 拦截）。

3. **CEO 链不受影响：** `danying-brand-agent` 里 verify / Brief 仍走 **Google**；与 OpenRouter Guardrail 无关。


## 8. API 方式（可选）

需 **Management Key**（与推理 Key 不同）。见 [Create guardrail](https://openrouter.ai/docs/api/api-reference/guardrails/create-guardrail) · [Guardrails API](https://openrouter.ai/docs/guides/features/guardrails#api-access)。

示例 body 字段：`allowed_models`、`allowed_providers`、`limit_usd`、`reset_interval`；创建后同样要 **assign 到 API key**。

---

## 相关

- [API-KEY-BOUNDARIES.md](./API-KEY-BOUNDARIES.md)
- [OPENWEBUI-CEO-ROUTER.md](./OPENWEBUI-CEO-ROUTER.md)