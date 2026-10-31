---
context_version: "2026-10-30-l012"
repo_path: "content/evolution/00-manager/ceo-inbox/CEO-OPENWEBUI-E2E-TEST-2026-10-29.md"
goal: "CEO Open WebUI E2E Test · 2026-10-29"
openwebui_route: "intake_l2"
cursor_route: "read"
content_sha256: "ff9f72a756c27ea9"
---

# CEO Open WebUI E2E Test · 2026-10-29

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** E2E workflow test：基于 personal-ip intake（KPI Publish×法派长笛跨界），产出 LinkedIn 系列深度口播分节大纲；须结合 brand-ip-knowledge 事实，长文结构化输出
- **Path:** `content/evolution/00-manager/ceo-inbox/CEO-OPENWEBUI-E2E-TEST-2026-10-29.md`
- **Open WebUI:** `intake_l2`
- **Cursor:** `read`

## 章节锚点
- **Owner 目标（原话）**: E2E workflow test：基于 personal-ip intake（KPI Publish×法派长笛跨界），产出 LinkedIn 系列深度口播分节大纲；须结合 brand-ip-know…
- **步 −1 · Router**: | 项 | 值 |
- **步 0 · Manager 计划（模拟派活）**: | Agent | 动作 |
- **API Key 边界**: - Open WebUI 段：**OpenRouter**
- **下一步迭代**: 1. Manager 读 outbox → Brief / LinkedIn v0


---

## L2 正文

# CEO Open WebUI E2E Test · 2026-10-29

## Owner 目标（原话）

E2E workflow test：基于 personal-ip intake（KPI Publish×法派长笛跨界），产出 LinkedIn 系列深度口播分节大纲；须结合 brand-ip-knowledge 事实，长文结构化输出

## 步 −1 · Router

| 项 | 值 |
|----|-----|
| route | **HYBRID** |
| job | `e2e-workflow-test-基于-personal-ip-intake-kpi-publ` |
| outbox | `/Users/danying/Desktop/Open WebUI Personal IP/outbox/e2e-workflow-test-基于-personal-ip-intake-kpi-publ.md` |
| intake 源 | `content/personal-ip/intake/2026-10-29-e2e-kpi-longform-source.md` |

## 步 0 · Manager 计划（模拟派活）

| Agent | 动作 |
|-------|------|
| **01 personal-ip** | 核对 outbox 提纲 vs CAPSTONE / ip-positioning-brief |
| **04 xhs-topic-manager** | 若转小红书：三镜头 Brief v0（**不**直接发 outbox 终稿） |

## API Key 边界

- Open WebUI 段：**OpenRouter**
- CEO 后续改稿：**GEMINI_API_KEY**（`.env`）

## 下一步迭代

1. Manager 读 outbox → Brief / LinkedIn v0  
2. `manager-ceo-gate-one-round.sh --brief …`  
3. 可选：`bash scripts/ceo-workflow-test-round2-finish.sh`