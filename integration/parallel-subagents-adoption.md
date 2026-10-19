# 并行 Subagent · 本仓采纳说明

> **Discovery：** [rules/skills/workflow_parallel_subagents.md](../rules/skills/workflow_parallel_subagents.md)  
> **勿与** [agents/00-manager/AUTO-WORKFLOW.md](../agents/00-manager/AUTO-WORKFLOW.md) **混淆**

## 两套「多 Agent」各管什么

| 维度 | **本仓 00 Manager + 01–09** | **并行 Subagent（Task）** |
|------|---------------------------|---------------------------|
| 本质 | **编排与验收**：Goal、IP 红线、Brief aligned、派活记录 | **执行隔离**：并行读、调研、独立 review |
| 运行方式 | 单 Cursor 会话内 **顺序扮演** 各 INTEGRATION-PROMPT | 多个 **后台/并行 Task** 子代理 |
| 真相源 | `content/` + evaluate JSON + verify 脚本 | `tmp/parallel/` 中间工件 → 合并后 **单 writer** 写定稿 |
| 适用 | 小红书 Brief、认知期触达、autopilot、Goal M4 | 竞品调研、宽口径搜证、大仓 explore、PR/Bugbot 审 |
| 默认 | Owner 给目标 → **必走** Manager 链（规则 `danying-manager-auto`） | **按需**；Brief 写稿 **不**默认并行 |
| 失败环 | Manager's Loop → 改 Brief/Skill/集成 prompt | 主线程整合冲突、补查、再决定是否重派 Task |

**结论：** 本仓 **指挥架构更好、更完整**（目标注册表、kernel gate、HANDOFF）；上游 **并行工作流更好** 在 **何时并行读、如何 file-first、反模式与 overlap**——已裁剪进 standalone skill，OpenCode/Antigravity 专用段落 **不采用**。

## 采纳清单

| 上游内容 | 本仓 |
|----------|------|
| 核心判断 + 委派边界 + 反模式 + overlap | ✅ skill 正文 |
| file-first 交接 + 语言继承 | ✅ |
| OpenCode `functions.task` JSON 示例 | ❌ 改为 Cursor Task 表 |
| `workflow_astra_coordinator` 续跑细节 | ❌ 不 vendor；Cursor 完成通知以产品为准 |
| Antigravity / 其他 CLI harness | ✅ [ai-agent-cli-adoption.md](./ai-agent-cli-adoption.md) · headless 时用 vendor focused skill |
| 与 00 Manager 分工 | ✅ 本文 + AUTO-WORKFLOW 脚注 |

## 推荐组合（认知期 / 多任务）

1. **选题前：** 轻量并行 Task → `tmp/parallel/<slug>/`；**需 Tier/claim/fact_check 时** 走 [workflow_deep_research_survey.md](../rules/skills/workflow_deep_research_survey.md) → `tmp/survey/<slug>/` + 可选 `content/marketing/research/` → **04** 写 Brief。
2. **定稿前：** 顺序 `evaluate-xhs-topic.py`；FAIL 走 Manager's Loop，**不**并行多个 writer 改 JSON。
3. **改 scripts/集成：** 可 `explore` 并行查调用链；**合并后** 一人改 + `verify-all`。
4. **交班前：** `manager-autopilot.sh` 仍 **单入口**；不与 Task 并行抢 CEO 逻辑。

## 扩展接口

| 改动 | 接哪里 |
|------|--------|
| session 落盘根目录 | `overlays/workflow-parallel-subagents.local.md` |
| 新「可并行」场景 | 先更新本文「推荐组合」+ skill 任务表一行 |
| 指挥链变更 | 只改 `AUTO-WORKFLOW.md`，不在 skill 里复制全套步序 |

## 验收

- `rules/skills/workflow_parallel_subagents.md` 存在
- 本文件存在
- `verify-handoff.sh` 检查通过
