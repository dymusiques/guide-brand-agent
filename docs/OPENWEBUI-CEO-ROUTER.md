---
context_version: "2026-10-30-l012"
repo_path: "docs/OPENWEBUI-CEO-ROUTER.md"
goal: "Open WebUI × CEO Router（Must）"
openwebui_route: "rag_l1"
cursor_route: "read"
content_sha256: "229b915ef4ec9ede"
---

# Open WebUI × CEO Router（Must）

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** > **机器入口：** `bash scripts/run-openwebui-router-pipeline.sh --goal "…"`  
> **验收：** `bash scripts/verify-openwebui-ceo-router.sh`  
> **E2E（CEO→Open WebUI→outbox→handoff）：** `bash s
- **Path:** `docs/OPENWEBUI-CEO-ROUTER.md`
- **Open WebUI:** `rag_l1`
- **Cursor:** `read`

## 章节锚点
- **步 −1（Manager 在 AUTO-WORKFLOW 之前）**: 1. Owner / CEO 给出 **目标句子**（与 dispatch 一致）。
- **Route 含义**: | route | Open WebUI |
- **Outbox**: | 平台 | 路径 |
- **Open WebUI 侧（已配置要求）**: - Connections：**OpenRouter** `https://openrouter.ai/api/v1` · Bearer · Enable


---

## L2 正文

# Open WebUI × CEO Router（Must）

> **机器入口：** `bash scripts/run-openwebui-router-pipeline.sh --goal "…"`  
> **验收：** `bash scripts/verify-openwebui-ceo-router.sh`  
> **E2E（CEO→Open WebUI→outbox→handoff）：** `bash scripts/run-ceo-openwebui-e2e-workflow-test.sh`
> **Pipe Valves 同步：** `python3 scripts/sync-openwebui-pipe-valves.py`（Router 实跑前会自动执行；从 Open WebUI 已启用的 OpenRouter 连接写入 CoT / Diligent）

## 步 −1（Manager 在 AUTO-WORKFLOW 之前）

1. Owner / CEO 给出 **目标句子**（与 dispatch 一致）。  
2. **Must** 跑 router pipeline（Agent 自跑，勿推 Owner）：

```bash
bash scripts/run-openwebui-router-pipeline.sh --goal "<原话目标>" [--intake content/.../intake.md]
```

3. 若输出 `SKIP` → 直接进入原有 00 Manager 指挥链。  
4. 若 `done` → 读 `integration/handoff/openwebui-jobs/<slug>.json` + Desktop outbox `.md`，在 **步 0 计划** 写 **intake: outbox**。  
5. 04 / CEO 把 outbox 当 **素材**，不是 PASS 终稿。

## Route 含义

| route | Open WebUI |
|-------|------------|
| SKIP | 不调用 |
| RAG_ONLY | `# brand-ip-knowledge` 单次问答 |
| PIPE_COT / HYBRID | CoT Pipe + Knowledge |
| PIPE_DILIGENT | Diligent Pipe + Knowledge |

## Outbox

| 平台 | 路径 |
|------|------|
| 个人 IP / 小红书 / LinkedIn / 口播 | `~/Desktop/Open WebUI Personal IP/outbox/` |
| 网站 / Fluid Body | `~/Desktop/Open WebUI Fluid Body/outbox/` |

## Open WebUI 侧（已配置要求）

- Connections：**OpenRouter** `https://openrouter.ai/api/v1` · Bearer · Enable  
- Functions：**yage_cot**、**yage_long_context** · Enable · Valves 填 OpenRouter URL + Key + 模型 slug  
- Knowledge：**brand-ip-knowledge** 保持同步（RAG 脚本）
- **Router RAG 模型**（`OPENWEBUI_RAG_MODEL`）：默认 `openai/gpt-4o-mini`（OpenRouter）。`google/gemini-*` 也会走 OpenRouter 并在 OR 账单显示 Gemini —— 见 [API-KEY-BOUNDARIES.md](./API-KEY-BOUNDARIES.md)

详见 Desktop：`Open WebUI Personal IP/OPENWEBUI-RULES.md`  
**Key 边界（必读）：** [API-KEY-BOUNDARIES.md](./API-KEY-BOUNDARIES.md) — CEO `GEMINI_API_KEY` 与 Open WebUI OpenRouter **禁止混用**。