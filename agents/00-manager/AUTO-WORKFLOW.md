# 00 Manager · 自动接手工作流（无需启动口令）

> **何时生效：** Owner 在本仓库给出 **目标任务**（写、做、选题、Brief、IP、小红书、品牌、定稿、campaign、涨粉、强链接等）时，Agent **默认就是 00 Manager**，不要等粘贴口令。  
> **纯问答**（解释概念、历史对话回顾、不用交付文件）可不跑全流程，但仍遵守 `integration/IMPORTANT.md` 红线。

## Manager's Loop（失败时）

`Analyze Failures` → `Manual Analysis` → `Propose Prompt Change`（只改集成/Brief/Skill，**不改** kernel 除非 05 专项）→ `Observe Score` → `Re-run Evaluation`

## 标准指挥链（单会话内顺序执行）

每一步：**读** `agents/<nn>-*/INTEGRATION-PROMPT.md` → **产出** → **终端验收** → 再下一步。

| 步 | Agent | 做什么 | 验收 |
|----|-------|--------|------|
| 0 | **00 Manager** | 解析 Owner 目标，写 3 行计划（受众、支柱、CTA 类型） | 计划与 `content/personal-ip/` 不冲突 |
| 1 | **01 personal-ip** | 若涉及战略/行业边界，核对「品牌合作范围」 | 非家居主攻、跨行业 open |
| 2 | **04 xhs-topic-manager** | 写 `content/xiaohongshu/YYYY-MM-DD-<slug>-brief.md` + classifier JSON | 模板见 `kernels/templates/xhs-content-brief.template.md` |
| 3 | **04 + 核心** | `python scripts/evaluate-xhs-topic.py --brief <file>` | `aligned: true`，exit 0 |
| 4 | **06 pipeline** | `bash scripts/verify-xhs-content-dir.sh` | 全 Brief PASS |
| 5 | **00 Manager** | Owner 未反对则 **git commit** 定稿；**禁止**未 aligned commit | `git status` clean |
| 6 | **07 brand-visual** | Owner 要封面时：Brief 封面块 → Canva / visual skill | 可选 |
| 7 | **08 platform** | 仅 Owner 说「同步 Drive」 | 可选 |
| 8 | **09 data-analytics** | `bash scripts/analytics-pipeline.sh` → 读 `content/analytics/derived/next-topics-*.md` → 派 04 写 Brief | 见 `agents/09-data-analytics/DATA-NEEDS.md` |

**05 xhs-kernel：** 仅当改 `kernels/xiaohongshu/line2/` 或 classifier 规则时介入 → 必跑 `bash scripts/verify-xhs-topic.sh`（Gemini 6）。

**03 / 02：** campaign 级或商业计划时，在步 2 前或并行读 INTEGRATION-PROMPT，产出进 `content/marketing/` 或 `content/business-brand/`。

## 一键验收（Manager 在步 3–4 后必跑）

```bash
# 健康检查（无 Brief）
bash scripts/manager-workflow-verify.sh

# 单条 Brief 定稿前
bash scripts/manager-workflow-verify.sh content/xiaohongshu/<file>.md
```

## 派活记录（Manager 每轮必输出）

```markdown
## Manager 派活记录
- 目标：（Owner 原话摘要）
- 当前步：0x · Agent 名称
- 终端：PASS/FAIL + 命令
- 下一步：…
```

## 红线

- 未 `aligned: true` → 不 Drive、不称定稿
- 集成层不改 classifier docstring（05 专属）
- 不编造阅读/转化数据（09 无 CSV 则标「未验证」）
