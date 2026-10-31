---
context_version: "2026-10-30-l012"
repo_path: "docs/OPENWEBUI-INTAKE-PROMPT-TEMPLATE.md"
goal: "Open WebUI · Intake 与 Prompt（何时要写）"
openwebui_route: "rag_l1"
cursor_route: "read"
content_sha256: "23930519bf601d5c"
---

# Open WebUI · Intake 与 Prompt（何时要写）

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** > **链 B 专用**（Open WebUI + OpenRouter）。CEO 链 A 的 Gemini **不读**本文件做生成，只读 **outbox 结果**。  
> **上下文标准：** [PROMPT-CONTEXT-STANDARD.md](./PROMPT-CONTEXT-STANDARD.md) · **输出窗口：** 长文 Must 
- **Path:** `docs/OPENWEBUI-INTAKE-PROMPT-TEMPLATE.md`
- **Open WebUI:** `rag_l1`
- **Cursor:** `read`

## 章节锚点
- **什么时候 Must 有 intake 文件？**: | 情况 | intake | Router 命令 |
- **intake 里写什么（最小模板）**: ```markdown
- **源稿要点**: （粘贴或摘要：案例、观点、禁止项）
- **Owner IP 对齐**: - 法派长笛 × 跨界策划 · 先观点后产品
- **CEO 目标（给 Router 的原话可抄这里）**: Personal IP：… LinkedIn 系列深度口播分节 … brand-ip-knowledge
- **Prompt 谁负责？**: | 层 | 谁写 | 说明 |
- **示例**: ```bash
- **输出窗口（课纲 · Must）**: | 症状 | 处理 |


---

## L2 正文

# Open WebUI · Intake 与 Prompt（何时要写）

> **链 B 专用**（Open WebUI + OpenRouter）。CEO 链 A 的 Gemini **不读**本文件做生成，只读 **outbox 结果**。  
> **上下文标准：** [PROMPT-CONTEXT-STANDARD.md](./PROMPT-CONTEXT-STANDARD.md) · **输出窗口：** 长文 Must 走 CoT/Diligent，**禁止**在 Cursor 单轮要 3000+ 字。

## 什么时候 Must 有 intake 文件？

| 情况 | intake | Router 命令 |
|------|--------|-------------|
| 长文/口播/LinkedIn **有明确源稿**（文章、Brief 块、KPI 笔记） | **Must** `content/personal-ip/intake/<slug>.md` | `--goal "<CEO 原话>" --intake <path>` |
| 只要品牌库 **事实**（无长文结构） | 可选 | `--goal "只要事实：…"` → RAG_ONLY |
| gate / verify / 小改 | **不要** Open WebUI | Router → SKIP |

## intake 里写什么（最小模板）

```markdown
# Intake · <主题>

## 源稿要点
（粘贴或摘要：案例、观点、禁止项）

## Owner IP 对齐
- 法派长笛 × 跨界策划 · 先观点后产品
- 见 ip-positioning-brief-2026-10-05.md

## CEO 目标（给 Router 的原话可抄这里）
Personal IP：… LinkedIn 系列深度口播分节 … brand-ip-knowledge
```

## Prompt 谁负责？

| 层 | 谁写 | 说明 |
|----|------|------|
| **Owner/CEO 目标句** | 你或 Manager 步 0 | 传给 `--goal` |
| **intake 正文** | Owner 或 Collector | 传给 `--intake` |
| **术语 / 格式 Must** | `openwebui-pipe-to-outbox.py` 内置 | personal-ip、LinkedIn 口播等 |
| **HYBRID RAG 预取** | 脚本自动 | 品牌库 bullet，再 CoT |

**不必**单独写 Pipe JSON；Functions 已在 Open WebUI 内。

## 示例

```bash
bash scripts/run-openwebui-router-pipeline.sh \
  --goal "Personal IP：NGV×MSO 动线策展 vs 门口四重奏，产出 LinkedIn 系列深度口播分节大纲；结合 brand-ip-knowledge" \
  --intake content/personal-ip/intake/2026-10-29-ngv-flute-curation-theme.md
```

见 [`OPENWEBUI-CEO-ROUTER.md`](./OPENWEBUI-CEO-ROUTER.md) · [`API-KEY-BOUNDARIES.md`](./API-KEY-BOUNDARIES.md)

## 输出窗口（课纲 · Must）

| 症状 | 处理 |
|------|------|
| 长翻译后半段跳过 | **Diligent Pipe**，intake 放全文 |
| 长文写到一半敷衍 | **CoT Pipe**，goal 含「先 outline 再分节写」 |
| 只要短摘要 | **不要** Pipe；Cursor 或 RAG 单次问答 |

导出 Prompt 进 Knowledge：`bash scripts/export-agent-prompt-pack.sh` → sync brand-ip-knowledge → 问 `# brand-ip-knowledge`「INTEGRATION-PROMPT 路由规则」