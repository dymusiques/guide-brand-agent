# Workflow · CEO 架构 · 分层与文件地图

> **思维导图（须浏览器渲染，勿在 Cursor 里当代码打开）：** 终端 `bash scripts/open-workflow-mindmap.sh` → [workflow-mindmap.html](./workflow-mindmap.html) · **Agent 生态：** [agent-ecosystem-map.html](./agent-ecosystem-map.html)（同上可 `python3 -m http.server 8765 --directory docs` 后开 `/agent-ecosystem-map.html`）  
> **是否凌乱（审计表）：** [SYSTEM-CLARITY-AUDIT.md](./SYSTEM-CLARITY-AUDIT.md)  
> **一键接手：** [AGENT-TAKEOVER.md](./AGENT-TAKEOVER.md) · [HANDOFF-MD-MANIFEST.md](./HANDOFF-MD-MANIFEST.md)

---

## 1. 是否达到 Owner 要求？

| Owner 要求 | 现状 | 边界 |
|------------|------|------|
| 数据驱动分析 → 选题 → **写出成稿** | ✅ [XHS-CONTENT-INTAKE-STACK.md](./XHS-CONTENT-INTAKE-STACK.md)（Excel+PDF 叠加）→ 04 成稿 → [CONTENT-DELIVERY-FOR-OWNER.md](../content/xiaohongshu/CONTENT-DELIVERY-FOR-OWNER.md) | 成稿在 Git；**Owner 确认后** App 发帖 |
| Agent 环环相扣 | ✅ 00 指挥链 + autopilot + ceo-dispatch | Task/CLI/Launcher **按需**，不替代 00 步序 |
| 新机 / 新 Agent 能接手 | ✅ 本文 + MANIFEST + verify-handoff | 换机须 **clone + 拷贝 raw/** 或重导 xlsx |
| 完善 verify / 6 case / 函数壳 | ✅ M4 goals + 10×6 矩阵 + kernel 6 case（05/02/03） | Release 档 verify-all **不**默认每日烧 Gemini |

**结论：** 对「分析 + 写帖 + 验收闭环」**已达到**；对「零人工发布 + 自动拉私信」**刻意未做**（平台与隐私）。

---

## 2. 是否有「总 CEO + 部门 Manager」？

**有。**  metaphor 与实现如下：

| 公司角色 | 本仓实现 | 汇总给 Owner 的界面 |
|----------|----------|---------------------|
| **CEO** | **00 Manager**（Cursor 规则自动激活） | `ceo-dispatch-latest.md` · `manager-dashboard-*.md` |
| **部门 Manager** | **01–09** 各 Agent（读 `INTEGRATION-PROMPT.md`） | 步内 PASS/FAIL + 产出路径 |
| **质检 / 合规** | 05 kernel · evaluate · verify-goals | `aligned: true` · `RESULT: PASS` |
| **董事会目标** | G-* · `integration/goals/registry.json` | `verify-goals.sh` |

**反馈闭环（CEO 看的三条线）：**

1. 终端 `RESULT: PASS/FAIL`（autopilot / verify）
2. `content/analytics/derived/manager-dashboard-*.md`
3. `content/analytics/derived/ceo-dispatch-latest.md`

Owner **审阅**定稿与发布；CEO **不**代替 Owner 点小红书发布。

---

## 三层 + Sub-agent 位置

### Layer 0 · Owner

- 目标、审阅、App 发帖、（可选）CSV/xlsx 导入、Drive 权限

### Layer 1 · CEO（单点汇总）

| 路径 | 作用 |
|------|------|
| `agents/00-manager/AUTO-WORKFLOW.md` | 指挥链表 |
| `.cursor/rules/danying-manager-auto.mdc` | 有目标任务即进 00 |
| `scripts/manager-autopilot.sh` | 一键 CEO 链 |
| `scripts/manager-dashboard.sh` | 仪表盘 |
| `content/analytics/derived/ceo-dispatch-latest.md` | 派活块 |

### Layer 2 · 部门（01–09）

| ID | 目录 | 产出目录 | 函数壳 |
|----|------|----------|--------|
| 01 | `agents/01-personal-ip/` | `content/personal-ip/` | `scripts/agent-shells/01-*.sh` |
| 02 | `agents/02-business-brand/` | `content/business-brand/` | `02-*.sh` |
| 03 | `agents/03-marketing-strategy/` | `content/marketing/` | `03-*.sh` |
| 04 | `agents/04-xhs-topic-manager/` | `content/xiaohongshu/*-brief.md` | `04-*.sh` + `evaluate-xhs-topic.py` |
| 05 | `agents/05-xhs-kernel/` | `kernels/xiaohongshu/` | `verify-xhs-topic.sh`（**6 case**） |
| 06 | `agents/06-xhs-content-pipeline/` | Brief 批量 verify | `verify-xhs-content-dir.sh` |
| 07 | `agents/07-brand-visual/` | `content/visual/` | Canva MCP / skill |
| 08 | `agents/08-platform-integration/` | gdocs/Drive | `verify-integration.sh` |
| 09 | `agents/09-data-analytics/` | `content/analytics/` | `analytics-pipeline.sh` |

集成 glue（每 Agent **6 case**）：`integration/agents/a*.py` · 总矩阵 `scripts/verify-agent-matrix.sh`

### Layer 3 · 机制（Skills / Vendor / 扩展）

| 路径 | 作用 |
|------|------|
| `rules/skills/` · `.cursor/skills/` | 路由与领域 skill |
| `vendor/*` | gdocs、process-launcher、ai-agent-cli 等 |
| `integration/EXTENSION-POINTS.md` | 新能力接哪里 |
| `integration/parallel-subagents-adoption.md` | Cursor **Task** 并行 vs 00 步序 |
| `tmp/parallel/` · `tmp/survey/` | Sub-agent scratch（gitignore） |

**Sub-agent 规则：** 宽调研可用 Task；**Brief 写稿 + evaluate 必须 04 单线程**（见 AUTO-WORKFLOW）。

---

## 一步骤 → 一文件（常用）

| 步骤 | 命令 / 动作 | 读/写文件 |
|------|-------------|-----------|
| 接手 | `danying-brand-agent` | [HANDOFF-MD-MANIFEST.md](./HANDOFF-MD-MANIFEST.md) |
| CEO 一键 | `bash scripts/manager-autopilot.sh` | derived/* · goals verify |
| 数据刷新 | analytics-fetch + pipeline | [XHS-DATA-LAYER.md](./XHS-DATA-LAYER.md) |
| 写 Brief | 04 模板 | `kernels/templates/xhs-content-brief.template.md` |
| 对齐 IP | evaluate | `scripts/evaluate-xhs-topic.py --brief …` |
| Manager 验收 | workflow verify | `scripts/manager-workflow-verify.sh content/xiaohongshu/….md` |
| 直发成稿 | Owner 复制 | `2026-10-20-publish-ready-queue.md` |
| 发帖后 | 回填 | Brief `## 发布状态` |

---

## 新机一键（Agent Must）

```bash
cd ~/Desktop/danying-brand-agent   # 或你的 clone 路径
bash scripts/ensure-venv-deps.sh
bash scripts/verify-agent-takeover.sh
bash scripts/manager-autopilot.sh
```

然后读：`docs/AGENT-TAKEOVER.md` → `ceo-dispatch-latest.md` → `docs/XHS-DATA-LAYER.md`（有小红书数据时）。
