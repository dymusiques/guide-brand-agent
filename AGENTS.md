# AGENTS.md — Guide Brand Agent

This folder is the home for a multi-domain AI agent (personal IP, brand, marketing, Xiaohongshu, visual design).

> **Hub 总入口：** [danying-apps](https://github.com/dymusiques/danying-apps) · 本仓索引：[INDEX.md](INDEX.md)

## 全部克隆（换机 / 新 Agent）

Owner 说 **`全部克隆`** → 不在本仓单独 clone → 读 Hub [全部克隆.md](https://github.com/dymusiques/danying-apps/blob/main/全部克隆.md) → 跑 `scripts/clone-all.sh` → 再读本仓 `SETUP.md`。

## Every Session

Before doing anything else:

1. Read `rules/SOUL.md` — who you are in this workspace
2. Read `rules/USER.md` — who you are helping
3. Read `integrations/index.md` — **task routing (read before searching)**
4. Read `rules/WORKSPACE.md` — file paths; check before glob/grep
5. Read `rules/skills/INDEX.md` — CLI skills (gdocs, etc.)

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

**Google Docs / Gmail / Calendar CLI** → `rules/skills/skill_google_docs.md`  
触发词："Google Doc"、"publish to Docs"、"sync markdown"、"Gmail"、"Calendar event"

命中后读对应 skill 文件再执行；INDEX.md 是唯一路由源。

## Safety

- Don't exfiltrate private data.
- Don't run destructive commands without asking.
- Credentials live in gitignored paths only (`vendor/gdocs-skill/secrets/`, `rules/skills/overlays/*.local.md`).
