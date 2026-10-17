# AGENTS.md — Guide Brand Agent

This folder is the home for a multi-domain AI agent (personal IP, brand, marketing, Xiaohongshu, visual design).

> **Hub 总入口：** [danying-apps](https://github.com/dymusiques/danying-apps) · 本仓索引：[INDEX.md](INDEX.md)

## 全部克隆（换机 / 新 Agent）

Owner 说 **`全部克隆`** → 不在本仓单独 clone → 读 Hub [全部克隆.md](https://github.com/dymusiques/danying-apps/blob/main/全部克隆.md) → 跑 `scripts/clone-all.sh` → 再读本仓 `SETUP.md`。

**已 clone 本仓后**，在新会话说 **`danying-brand-agent`** → 读 [docs/AGENT-TAKEOVER.md](docs/AGENT-TAKEOVER.md) + [docs/HANDOFF-MD-MANIFEST.md](docs/HANDOFF-MD-MANIFEST.md) 并跑 autopilot（规则：`.cursor/rules/danying-brand-agent-bootstrap.mdc`）。见 [新电脑一句话.md](新电脑一句话.md)。

## 验收 / verify

交付前：读本仓 [`check.md`](check.md)（含 hub [`VERIFY-MAP.md`](https://github.com/dymusiques/danying-apps/blob/main/rules/check/VERIFY-MAP.md) 链接）。**Module 3 课纲 6 test 不在本仓** — 见 VERIFY-MAP 路由表。

## Every Session

Before doing anything else:

1. Read `rules/SOUL.md` — who you are in this workspace
2. Read `rules/USER.md` — who you are helping
3. Read `integrations/index.md` — **task routing (read before searching)**
4. Read `rules/WORKSPACE.md` — file paths; check before glob/grep
5. Read `rules/skills/INDEX.md` — CLI skills (gdocs, etc.)

## Owner 给目标任务时（自动 00 Manager · 无需口令）

**不用粘贴启动口令。** Owner 一旦给出要写/要做/选题/Brief/定稿等目标：

1. 读 [`agents/00-manager/AUTO-WORKFLOW.md`](agents/00-manager/AUTO-WORKFLOW.md) 并按指挥链执行  
2. 读 [`integration/IMPORTANT.md`](integration/IMPORTANT.md)  
3. 验收：`bash scripts/manager-workflow-verify.sh`（有 Brief 时传入路径）

规则：`.cursor/rules/danying-manager-auto.mdc`（`alwaysApply: true`）

## File Routing

**找文件时，先查 `rules/WORKSPACE.md`，再搜索。** 发现新目录未被收录时，顺手更新 WORKSPACE.md。

## Skills

**遇到「怎么做 X」时，先查路由，再查 skill，最后才用系统工具。** 搜索顺序：

1. `integrations/index.md`
2. 下方速查表
3. `rules/skills/INDEX.md`
4. Cursor MCP / 系统工具

**需要执行某项任务** → 先查 INDEX，读对应 skill 再动手  
**想添加新能力** → 参考现有格式，更新 INDEX.md

### 常用 Skill 速查（以 INDEX.md 为准）

**多面品牌 Agent 总控** → `.cursor/skills/guide-core/SKILL.md`  
触发词：个人IP、品牌策划、营销、小红书、视觉（未指定单一工具时先走总控）

**danying-brand-agent 总集成** → [agents/README.md](agents/README.md) · [AUTO-WORKFLOW](agents/00-manager/AUTO-WORKFLOW.md) · `bash scripts/manager-workflow-verify.sh`

**小红书 Topic Manager（选题 + Gemini 对齐）** → `agents/04-xhs-topic-manager/` · `.cursor/skills/xiaohongshu/topic-manager.md`  
触发词：选题、Topic Manager、笔记 Brief · `--brief content/xiaohongshu/…`

**Google Docs / Gmail / Calendar CLI** → `rules/skills/skill_google_docs.md`  
触发词："Google Doc"、"publish to Docs"、"sync markdown"、"Gmail"、"Calendar event"

命中后读对应 skill 文件再执行；INDEX.md 是唯一路由源。

## 接手 / verify

交付前读 [`check.md`](check.md)（含 hub [`VERIFY-MAP.md`](https://github.com/dymusiques/danying-apps/blob/main/rules/check/VERIFY-MAP.md)）。**Module 3 课纲 6 test 不在本仓** — 见 VERIFY-MAP 路由表。

## Handoff · 接手完整性

- **新 Agent 必读：** [docs/AGENT-TAKEOVER.md](docs/AGENT-TAKEOVER.md)（当前状态 + 三轨 + 验收命令）
- 策略：[docs/HANDOFF-COMPLETENESS.md](docs/HANDOFF-COMPLETENESS.md) — 什么必须在 Git、什么可选进 Drive
- L0：`bash scripts/verify-handoff.sh`（全部克隆后 / 交班前 Must 跑）
- 集成：`bash scripts/verify-integration.sh`（6 case · gdocs 读/错 + Git/Drive 读）
- 定稿产出 **commit 进 Git**；Drive 仅 Owner 要求时 sync

## Safety

- Don't exfiltrate private data.
- Don't run destructive commands without asking.
- Credentials live in gitignored paths only (`vendor/gdocs-skill/secrets/`, `rules/skills/overlays/*.local.md`).
