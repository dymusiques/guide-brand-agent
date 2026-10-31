---
context_version: "2026-10-30-l012"
repo_path: "integration/ai-agent-cli-adoption.md"
goal: "AI Agent CLI Skill · 本仓采纳说明"
openwebui_route: "rag_l2"
cursor_route: "read"
content_sha256: "a6adf6fa58911196"
---

# AI Agent CLI Skill · 本仓采纳说明

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** - `vendor/ai-agent-cli-skill/skills/skill_ai_agent_cli.md` 存在  
- Router + 本 adoption 存在  
- `verify-handoff.sh` PASS
- **Path:** `integration/ai-agent-cli-adoption.md`
- **Open WebUI:** `rag_l2`
- **Cursor:** `read`

## 章节锚点
- **L1 任务（压缩 · Open WebUI / Cursor 顶栏）**: - **Goal:** > **Discovery：** [rules/skills/skill_ai_agent_cli.md](../rules/skills/skill_ai_agent_cli…
- **章节锚点**: - **0. 运行策略（Owner · 2026-10）**: | 项 | 选择 |
- **5. 验收**: - `vendor/ai-agent-cli-skill/skills/skill_ai_agent_cli.md` 存在


---

## L2 正文

# AI Agent CLI Skill · 本仓采纳说明

> **Discovery：** [rules/skills/skill_ai_agent_cli.md](../rules/skills/skill_ai_agent_cli.md)  
> **Upstream：** [grapeot/ai-agent-cli-skill](https://github.com/grapeot/ai-agent-cli-skill)（**仅 Markdown**，无 pip package）

## 0. 运行策略（Owner · 2026-10）

| 项 | 选择 |
|----|------|
| 主交互 | **Cursor IDE** + 00 Manager + Task subagent（见 parallel-subagents adoption） |
| ai-agent-cli | **已 vendor · 按需加载** — 自动化/headless/跨 CLI 路由时读 root + focused skill |
| 默认 | 在 IDE 里写 Brief/verify **不**绕 `cursor agent -p` |
| 启用场景 | 批量 headless、writing-skill 外链 `agy`、将来 CI 调 agent、要 **file-response** 硬验收的 pipeline |


## 2. 与本仓框架对比 · 谁更好、怎么叠

| 维度 | **本仓（00 Manager + verify + content/）** | **ai-agent-cli（headless CLI）** | **结论** |
|------|-------------------------------------------|----------------------------------|----------|
| IP / Brief / aligned | ✅ 完整指挥链 + kernel | ❌ 无 | **定稿必用本仓** |
| IDE 内并行读 | Cursor **Task** + workflow_parallel_subagents | 可再开 `cursor agent -p` 隔离 turn | **IDE 内优先 Task**；headless 用 CLI skill |
| 验收 | `evaluate-xhs-topic.py`、verify 脚本 | 进程 exit + **结果文件读回** | **Brief 用本仓**；CLI 任务用 file-response |
| 写作外稿 | writing-skill workflow | agy / cursor / claude 路由 | **writing-skill 定流程**；CLI 细节 **agy/cursor_cli** |
| 订阅 vs API | `.env` Gemini evaluate | 各 CLI 订阅配额 | evaluate **仍 Gemini 脚本**；探索可用 Cursor CLI 订阅 |
| 自动化层 | manager-autopilot、process-launcher `/run` | `cursor agent -p` 可被 launcher 调度 | **Launcher 调 shell 包装 CLI**（overlay 配方） |

**留下两套：** 本仓 = **品牌真相与门控**；ai-agent-cli = **可验证的 headless 执行合同**。


## 4. 文件与接口（接手不乱）

| 类型 | 路径 | Git |
|------|------|-----|
| Submodule | `vendor/ai-agent-cli-skill/` | ✅ |
| Discovery | `rules/skills/skill_ai_agent_cli.md` | ✅ |
| 本文件 | `integration/ai-agent-cli-adoption.md` | ✅ |
| Focused skills | `vendor/.../skills/*.md` | ✅（随 submodule） |
| 私有 | `overlays/ai-agent-cli.local.md` | ❌ |
| CLI scratch | `tmp/ai-agent-cli/<job>/`（prompt.md, result.md, logs） | ❌ gitignore |

**扩展：** 新 CLI 配方只改 overlay + 可选 `integration/templates/` 包装脚本；指挥链改 `AUTO-WORKFLOW`，不在 vendor 里写 Owner 路径。

---

## 5. 验收

- `vendor/ai-agent-cli-skill/skills/skill_ai_agent_cli.md` 存在  
- Router + 本 adoption 存在  
- `verify-handoff.sh` PASS  

可选：`cursor agent about`（CLI 已 login 时）