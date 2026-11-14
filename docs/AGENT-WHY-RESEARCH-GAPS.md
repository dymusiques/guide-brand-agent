# 为何「全文 / CEO / 6-case / QC」会反复漏跑

## 根因（架构，不是 Owner 漏说口令）

| # | 现象 | 根因 |
|---|------|------|
| 1 | PDF/MD 只读前几行 | **无硬门禁**：hydrate 是可选脚本；Agent 可凭 handoff 文件名下结论；旧路径用 MCP 截断未见 `truncated:false` 仍当全文 |
| 2 | CEO 未自动跑 | **讨论链与战役链分裂**：`content-session` 只调 `brainstorm-preflight`；`run_ceo_full_execution` 要单独 goal；**无单条 FAIL 出口** |
| 3 | 6-case 未对齐目标 | `ceo-six-case-battery` 未绑 brief / 艺术家目标；`prompt-six-case` 与品牌 battery **未串成一层**；four-dimensions 失败被当整链 FAIL 或整链忽略 |
| 4 | Double-Check 未跑 | **QC 在交付里程碑 E3**，讨论型回答无「可交付」触发；`qc handoff` 无 `--c2-log` 即视为草稿 |
| 5 | Drive screen 未读入选全文 | catalog refresh 用错 Python（无 googleapiclient）→ screen 空转；**无 `owner-drive-hydrate` 监督字段** |
| 6 | 版本对比 / baseline 未绑 | `triple-eval` 依赖 brief 路径；已发复盘 **无 brief** → 脚本设计为 skip，Agent 误当「不需要」 |
| 7 | 跨维度对标 / URL 未深读 | `artist-watchlist-screened` 在仓内但未 **Must 刷新+全文**；无 URL fetch 层 |
| 8 | 一次又一次 | **薄规则 + 厚可选**：Cursor Rules 写 Must，但 **无 `agent-owner-research-gate.py` 式 FAIL**；Agent 为省 token 走最短路径 |
| 9 | 已发复盘却 hydrate 错 PDF | **goal 子串「艺术」误命中 z-library 书名**；`direct_hit` 优先于 task bundle；已发/薯条域未加权「小红书」资料夹 |

## 对策（机械真源）

**唯一硬门禁**（已发 / 复盘 / 监督 / 补全）：

```bash
python3 scripts/agent-owner-research-gate.py --goal "<Owner 原话>"
```

或 monorepo：`python3 scripts/agent-workflow.py brand research-gate --goal "..."`

PASS 才允许交付「我已全链路调研」；否则 handoff `status=FAIL` + 逐层 `layers`。

合同：`integration/handoff/agent-owner-research-gate-contract.json`

**C1/C3 强制（monorepo）**：`scripts/owner_research_gate_preflight.py` — 命中 `deep_research_when_any` 时 handoff 非 PASS → preflight **exit 1**；可自动 `brand research-gate`。真源：`~/Desktop/未命名/docs/agent/AGENT-RESEARCH-GATE-PREFLIGHT.json`
