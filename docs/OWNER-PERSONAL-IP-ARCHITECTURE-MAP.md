# 个人 IP 架构全链路 · Owner / Agent 一览

> **机器索引：** [`integration/handoff/owner-personal-ip-architecture-chain.json`](../integration/handoff/owner-personal-ip-architecture-chain.json)  
> **接手：** [`AGENT-TAKEOVER.md`](AGENT-TAKEOVER.md) · **CEO 战役：** [`CEO-FULL-EXECUTION-MANDATE.md`](CEO-FULL-EXECUTION-MANDATE.md)  
> **最后更新：** 2026-11-18（蒸馏自 Refining Cursor Flow 对话）

## 这条链是不是都写进 Rule / MD / JSON 了？

**个人 IP 的「执行链」在品牌仓 `danying-brand-agent` 里已经闭合**（规则 + 文档 + handoff JSON + 脚本）。  
**Refining 对话里的「进站安检链」（①–⑤、slug、C1/C3）在 Agent 工作区**（仓库 `danying-agent-workspace`；本机路径常为 `~/Desktop/未命名`）—— 品牌任务仍可用，但若 **本机没有该工作区**，`research-gate` / `agent-workflow.py` 会断档（见下文缺口）。

## 可视化 vs 真源（新 Agent · 勿混）

| 层 | 是什么 | 何时信它 |
|----|--------|----------|
| **执行真源** | [OWNER-DELIVERABLE-PACK-MANDATE.md](OWNER-DELIVERABLE-PACK-MANDATE.md)（你说 Brief = **交付包四块**）· [WORKFLOW-AUTOMATION-MATRIX.md](WORKFLOW-AUTOMATION-MATRIX.md) · `integration/handoff/workflow-automation-manifest.json` | 写稿、gate、进化、能不能交 Owner |
| **Cursor Automation 粘贴真源** | [OWNER-CURSOR-AUTOMATIONS-INDEX.md](OWNER-CURSOR-AUTOMATIONS-INDEX.md) → 各 `OWNER-*-AUTOMATION-INSTRUCTIONS.md` | 配 Cron / 复制 Instructions |
| **人在环导图（Git）** | [CEO-EXECUTION-MINDMAP.html](CEO-EXECUTION-MINDMAP.html) · [workflow-handoff-mindmap.html](workflow-handoff-mindmap.html) | 接 CEO 战役时导航 |
| **可选全链 HTML（可未进 Git）** | `docs/OWNER-IP-WORKFLOW-FULL-MAP.html` + `scripts/open-owner-ip-workflow-full-map-html.sh` | **仅导航**；与 mandate/矩阵矛盾时 **以 mandate/矩阵为准** |

架构演进时：**先改 MD + rules + JSON**，大图可隔几轮再跟；**不必每改一行就 commit 图**。

---

## 从定位到交付（一张表）

| 阶段 | 干什么 | 真源（优先 JSON / rule） |
|------|--------|---------------------------|
| **定位** | 张丹瀛 / Danying 即品牌 | `rules/USER.md` · `content/personal-ip/ip-positioning-brief-*.md` · CAPSTONE playbook |
| **目标** | G-* 不丢 | `integration/goals/registry.json` · `GOALS-REGISTRY.md` |
| **接活** | Owner 说话 → **00 CEO** 默认接手 | `.cursor/rules/danying-manager-auto.mdc` · `AUTO-WORKFLOW.md` |
| **进站** | 防漏读、handoff 审计 | Agent 工作区：`agent-workflow.py brand content-session` · 品牌：`agent-owner-research-gate-contract.json` |
| **战役** | pipeline · 6-case · autopilot · HTML | `workflow-automation-manifest.json` · `ceo-full-execution-pipeline.sh` |
| **小红书** | 长稿 · 对抗 · evolution · Owner HTML | `OWNER-LONGFORM-XHS-SPEC.md` · `OWNER-XHS-ADVERSARIAL-AND-EVOLUTION-MANDATE.md` |
| **口吻** | yage-voice · 锚点 | `.cursor/skills/yage-voice/` · `VOICE-ANCHOR.md` |
| **三平台飞轮** | 阶段 0/1/2 · 周选题 | `owner-multichannel-flywheel-phase.json` · Automations 索引 MD |
| **数据闭环** | 09 → dispatch → 04 | `ceo-dispatch-latest.md` · Owner **CSV**（不进 kernel 硬断言） |
| **复核** | gate + **13-QC** | `DOUBLE-CHECK-SUBAGENT.md` · `workflow_double_check_subagent.md` |

**Open WebUI / Ollama：** 可选步 −1，**不**替代 Cursor CEO 主链（见 `OPENWEBUI-CEO-ROUTER.md`）。

---

## 双工作区（Must 别混）

| 工作区 | 放什么 |
|--------|--------|
| **`danying-brand-agent`** | CEO 派活、交付包（`*-brief.md`）、pipeline、品牌 Rules、本图与 chain JSON |
| **Agent 工作区**（`danying-agent-workspace` · 本机常为 `~/Desktop/未命名`） | ①–⑤ 统一进站、`AGENT-CURSOR-CEO-UNION.json`、`AGENT-STEP-01-WORKSPACE-REGISTRY.json`、检查单 HTML |

品牌仓 **不写** CEO 脚本真源到 Agent 工作区根目录；Agent 工作区 **不写** Brief 定稿到错误根目录。机械门禁：`docs/AGENT-WORKSPACE-GATE.md`。

---

## 仍有的「遗忘风险」（进了 Git 也会）

1. **两套根目录**：只开品牌仓时，Agent 可能 **不跑** research-gate（除非读 UNION 并 delegate Agent 工作区脚本）。  
2. **规则不读全仓**：`.mdc` 会进会话，但 **不会** 自动读 400 个 MD；要靠 `HANDOFF-MD-MANIFEST` 与 manifest。  
3. **接手文档漂移**：`verify-agent-takeover.sh` 与 `AGENT-TAKEOVER.md` 必须同步（已在本轮修补关键词）。  
4. **Layer C handoff**：`owner-weekly-*-latest.json` 等 **本机生成、不一定 commit** —— 新 Agent 要会 **重跑脚本** 再生。  
5. **后台灶**：`process-launcher` 未启动 → 09:00 cycle 不跑，dispatch 会旧。  
6. **Owner 仅动作**：发帖、CSV、OAuth 首次 —— 文档有，机器不能代做。

---

## Refining 对话里值得留的「档案」（非路由）

见 [`ARCHIVE-REFINING-CURSOR-FLOW-2026-11.md`](ARCHIVE-REFINING-CURSOR-FLOW-2026-11.md)（决策摘要 + chat id）。**不要**把整段 transcript JSONL 当 Agent 入口。

---

## 新 Agent 60 秒

1. 读本页 + `owner-personal-ip-architecture-chain.json`  
2. `AGENT-TAKEOVER.md` → `bash scripts/verify-handoff-program.sh`（或分项 verify）  
3. Owner 给 IP/内容目标 → **CEO 派活链**，勿只聊架构不跑 pipeline