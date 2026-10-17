# 接手 MD 清单 · 新机「植入」读序

> Owner 在新会话说 **`danying-brand-agent`** → Agent 按本清单 **Read 文件**（不依赖旧对话）。  
> 总入口：[AGENT-TAKEOVER.md](AGENT-TAKEOVER.md) · 规则：`.cursor/rules/danying-brand-agent-bootstrap.mdc`

## 1 · 指挥与架构（Must）

| # | 路径 |
|---|------|
| 1 | [AGENT-TAKEOVER.md](AGENT-TAKEOVER.md) |
| 2 | [../AGENTS.md](../AGENTS.md) |
| 3 | [../agents/00-manager/AUTO-WORKFLOW.md](../agents/00-manager/AUTO-WORKFLOW.md) |
| 4 | [AUTOPILOT.md](AUTOPILOT.md) |
| 5 | [DANYING-BRAND-AGENT-INTEGRATION.md](DANYING-BRAND-AGENT-INTEGRATION.md) |
| 6 | [HANDOFF-SOP.md](HANDOFF-SOP.md) |

## 2 · Owner / IP / 红线（Must）

| # | 路径 |
|---|------|
| 7 | [../rules/SOUL.md](../rules/SOUL.md) |
| 8 | [../rules/USER.md](../rules/USER.md) |
| 9 | [../content/personal-ip/ip-positioning-brief-2026-10-05.md](../content/personal-ip/ip-positioning-brief-2026-10-05.md) |
| 10 | [../integration/IMPORTANT.md](../integration/IMPORTANT.md) |
| 11 | [../integration/GOALS-REGISTRY.md](../integration/GOALS-REGISTRY.md) |

## 3 · 认知期触达 + 商业（当前 program · Must）

| # | 路径 |
|---|------|
| 12 | [../content/marketing/2026-10-brand-discovery-phase.md](../content/marketing/2026-10-brand-discovery-phase.md) |
| 13 | [../content/marketing/discovery-phase-OPERATING-PLAN.md](../content/marketing/discovery-phase-OPERATING-PLAN.md) |
| 14 | [../content/marketing/discovery-phase-note-queue.md](../content/marketing/discovery-phase-note-queue.md) |
| 15 | [../content/business-brand/2026-10-17-brand-positioning-swot.md](../content/business-brand/2026-10-17-brand-positioning-swot.md) |
| 16 | [../content/xiaohongshu/PUBLISH-AND-DATA-CHECKLIST.md](../content/xiaohongshu/PUBLISH-AND-DATA-CHECKLIST.md) |

## 4 · 小红书 Brief 队列（Must · 当前 4+1）

| # | 路径 |
|---|------|
| 17–20 | `content/xiaohongshu/2026-10-17-discovery-0{1,2,3,4}-*-brief.md` |
| 21 | [../content/xiaohongshu/PIPELINE.md](../content/xiaohongshu/PIPELINE.md) |

## 5 · 路由与验收（Should）

| # | 路径 |
|---|------|
| 22 | [../integrations/index.md](../integrations/index.md) |
| 23 | [../rules/WORKSPACE.md](../rules/WORKSPACE.md) |
| 24 | [VERIFY-TIERS.md](VERIFY-TIERS.md) |
| 25 | [../check.md](../check.md) |

## 6 · 终端（Must · 植入后跑）

```bash
bash scripts/ensure-venv-deps.sh
bash scripts/verify-agent-takeover.sh
bash scripts/manager-autopilot.sh
```

然后读生成文件：`content/analytics/derived/ceo-dispatch-latest.md`（若不存在则 autopilot 已创建）。

## 不读旧对话

Chat 历史 **不在** Git；真相源仅为上表 **L0 路径** + derived 刷新结果。
