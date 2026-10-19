# 全自动 CEO 编排 · Autopilot

**设计原则：** 会话内仍由 **00 Manager** 扮演 CEO；本脚本把 **可机器化的链** 串成一条命令。**不** 多进程、**不** 代发帖、**不** 爬小红书 API。破坏性/写操作前见 [integration/IMPORTANT.md](../integration/IMPORTANT.md#dry-run破坏性--发布侧--摘录)（`AUTOPILOT_FULL=1` 跑 release verify 前尤其适用）。

## Owner 仅做两件事

| 环节 | 说明 |
|------|------|
| **发帖** | 各平台后台发布；回填 Brief `## 发布状态` |
| **数据** | 导出 CSV → `content/analytics/inbox/` |

## 一条命令（其余全自动）

```bash
bash scripts/manager-autopilot.sh
```

顺序：Goal verify (M4) → CEO 仪表盘 → SEO lint（非阻塞）→ 09 pipeline（有 inbox 用真数据，否则 `--demo`）→ **CEO 派活块** `derived/ceo-dispatch-latest.md` → 可选 `AUTOPILOT_FULL=1` 跑 CI 档 verify-all。

**与 Gemini 6 case 的分工：** M4 验 Owner 目标与当前交付物，**不**跑 05/02/03 的 kernel 6 case 整包；日常 autopilot 也不默认烧 Gemini。分层表见 [VERIFY-TIERS.md · Gemini 6 case 与 M4 分工](VERIFY-TIERS.md#gemini-6-case-与-m4-分工)。交班 / 改 kernel 后请 Owner 或 Agent 单独跑 `VERIFY_TIER=release bash scripts/verify-all.sh`（或对应 `verify-xhs-topic.sh` / `verify-business-brand.sh` / `verify-marketing-campaign.sh`）。

## SEO（小红书可发现性）

`scripts/seo-lint-xhs-briefs.py` 检查 Brief 的 `## 标签`（≥3 个 `#`）、标题长度、软 CTA。autopilot 内 **WARN 不挡跑**；Release 交班可单独跑：

```bash
python scripts/seo-lint-xhs-briefs.py
```

## 09 → 04 半自动派活

- `scripts/analytics-summarize.py` 结束后自动刷新 `ceo-dispatch-latest.md`
- 模板含 **Owner 边界** + **当前待发 Brief** + **next-topics 全文** + 粘贴给 04 的口令

## 相关

- M4：`bash scripts/verify-goals.sh` · `integration/goals/verify_hooks.json` · 与 kernel 6 case 分工：[VERIFY-TIERS.md](VERIFY-TIERS.md#gemini-6-case-与-m4-分工)
- M5：`docs/HANDOFF-SOP.md`
- 15 天定时：`content/marketing/automation/CURSOR-AUTOMATION-15D.md`
