---
context_version: "2026-10-30-l012"
repo_path: "content/evolution/00-manager/ceo-inbox/CEO-FULL-STACK-DISPATCH-2026-10-29.md"
goal: "CEO 全栈测试派活 · 2026-10-29"
openwebui_route: "intake_l2"
cursor_route: "read"
content_sha256: "10e4f5863e3592b5"
---

# CEO 全栈测试派活 · 2026-10-29

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** **Owner 主题：** NGV×MSO 动线策展 vs 门口四重奏 → LinkedIn 深度口播系列（Personal IP）
- **Path:** `content/evolution/00-manager/ceo-inbox/CEO-FULL-STACK-DISPATCH-2026-10-29.md`
- **Open WebUI:** `intake_l2`
- **Cursor:** `read`

## 章节锚点
- **步 −1 · Open WebUI（链 B · OpenRouter）**: ```bash
- **步 0–8 · Manager 链（链 A · Google Gemini）**: | Agent | 任务 |
- **一键全栈**: ```bash


---

## L2 正文

# CEO 全栈测试派活 · 2026-10-29

**Owner 主题：** NGV×MSO 动线策展 vs 门口四重奏 → LinkedIn 深度口播系列（Personal IP）

## 步 −1 · Open WebUI（链 B · OpenRouter）

```bash
bash scripts/run-openwebui-router-pipeline.sh \
  --goal "Personal IP：基于 intake，产出 LinkedIn 系列深度口播分节大纲（NGV×MSO 动线策展 vs 门口四重奏）；须结合 brand-ip-knowledge 事实" \
  --intake content/personal-ip/intake/2026-10-29-ngv-flute-curation-theme.md
```

**intake Must：** 见 `docs/OPENWEBUI-INTAKE-PROMPT-TEMPLATE.md`

## 步 0–8 · Manager 链（链 A · Google Gemini）

| Agent | 任务 |
|-------|------|
| 01 | 对齐 ip-positioning · CAPSTONE |
| 04 | outbox → Brief v0 或 LinkedIn 层（**非终稿**） |
| 03/02 | 若 campaign 触达 SWOT |
| 06 | verify-xhs-content-dir |
| 全员 | `run-ceo-ip-all-agents-campaign.sh` / round2 |

## 一键全栈

```bash
bash scripts/run-ceo-full-stack-workflow-test.sh
```

**Owner Gate · 交 Owner：否**（测试链）