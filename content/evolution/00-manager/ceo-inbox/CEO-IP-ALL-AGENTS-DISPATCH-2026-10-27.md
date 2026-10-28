# CEO · 全 Agent 协同派活 · IP 认知期 + Artist + HTML

**截止：** 2026-10-27 24:00 北京时间  
**Owner 原话摘要：** 今晚 12 点前交付小红书认知期队列 + Artist 四指标 + Discovery 对抗复查（HTML）；**01–12 全员**须被 CEO 派活并跑实 verify。  
**Campaign：** `bash scripts/run-ceo-ip-all-agents-campaign.sh`  
**深交付（Gemini 重轮）：** `bash scripts/run-ceo-deep-delivery-cycle.sh`（与 campaign **协调**；二者并行时 campaign 设 `SKIP_GEMINI=1`）

## 交付锚点（Owner 打开）

| 产物 | 路径 |
|------|------|
| 认知期 + 筛选 **Owner HTML** | `content/evolution/00-manager/ceo-inbox/OWNER-XHS-FILTER-DELIVERABLE-2026-10-27.html` |
| Discovery 对抗 challenge HTML | `content/evolution/00-manager/ceo-inbox/challenge-html/` |
| Artist 对标（GM10） | `content/evolution/10-artist-intel/2026-10-27/` |
| IP 日评（GM11） | `content/evolution/11-ip-daily-eval/2026-10-27/` |
| Owner daily brief（GM12） | `content/daily-brief/2026-10-27-owner-daily-brief.md` |
| 本派活 + campaign 日志 | `content/evolution/00-manager/ceo-inbox/ceo-ip-all-agents-campaign-*.log` |

**G-* 总绑：** G-STRONG-LINK · G-NOT-SINGLE-VERTICAL-LOCK · G-BRIEF-ALIGNED-GATE · G-ANALYTICS-EVIDENCE

---

## 00 · CEO / Manager（本文件 + 收汇报）

- 解析截止交付；启动 **campaign**（01–12 顺序 verify）与/或 **deep-delivery**（多轮 gate + HTML）。
- 读 `agents/00-manager/AUTO-WORKFLOW.md`；FAIL → `CEO-REROUTE` → 同会话改稿（≤3 轮）。
- 验收：`bash scripts/manager-workflow-verify.sh` · `bash scripts/manager-dashboard.sh`
- **交 Owner 前：** 任 Brief 须 `manager-ceo-owner-gate.sh` PASS；HTML 须存在且日期为今日。

---

## 01 · personal-ip · IP 战略

**目标：** 认知期叙事与 CAPSTONE 一致；Discovery 四篇不绑垂直、不单品类。

| 任务 | 产出/动作 |
|------|-----------|
| 复核 playbook §4 认知期 vs Discovery Brief 支柱 | `content/personal-ip/2026-10-18-key-person-of-influence-capstone-playbook.md` |
| 确认 ip-positioning 三支柱 + 品牌合作范围 | `content/personal-ip/ip-positioning-brief-2026-10-05.md` |
| 对抗 drill 结论进 CEO 决策 | `content/personal-ip/2026-10-27-ip-adversarial-FULL-DRILL-REPORT.md` |

**验收：** `bash scripts/agent-shells/01-personal-ip.sh --check` · `bash scripts/verify-agent-fused.sh --agent 01`

---

## 02 · business-brand · 商业侧

**目标：** SWOT/定位不 contradict 全品类 open；认知期勿硬推产品生态。

| 任务 | 产出/动作 |
|------|-----------|
| README + SWOT 块与 01 IP 边界对齐 | `content/business-brand/` |
| campaign 级文档若有则 lint | 最新 SWOT/定位 md |

**验收：** `bash scripts/agent-shells/02-business-brand.sh --verify` · `verify-agent-fused --agent 02`

---

## 03 · marketing-strategy · 触达 / 认知期 program

**目标：** 认知期 operating plan 与 Discovery 队列节奏一致。

| 任务 | 产出/动作 |
|------|-----------|
| 读 discovery-phase OPERATING-PLAN | `content/marketing/discovery-phase-OPERATING-PLAN.md` |
| 触达计划不越级强转化 | `content/marketing/` |

**验收：** `bash scripts/agent-shells/03-marketing.sh --verify` · `verify-agent-fused --agent 03`

---

## 04 · xhs-topic-manager · 小红书写稿 / Brief

**目标：** Discovery 01–04 + 认知期 #1–4 对抗复查；moment/标签/强链接 hygiene。

| 任务 | 产出/动作 |
|------|-----------|
| Intake 栈叠加 Excel+PDF | `docs/XHS-CONTENT-INTAKE-STACK.md` |
| 四篇 Discovery Brief + challenge 对齐 | `content/xiaohongshu/2026-10-17-discovery-0*-brief.md` · `content/xiaohongshu/challenge/` |
| 读 09 派活块下一 Brief | `content/analytics/derived/ceo-dispatch-latest.md` |
| redteam-pre 补齐 | `ensure-redteam-pre.py --brief …` |

**验收：** `verify-agent-fused --agent 04`（深交付在跑时 B 层 Gemini 由 deep cycle 负责）· discovery brief evaluate（gate loop 内）

---

## 05 · xhs-kernel · 对齐判定

**目标：** classifier / Gemini 6 case 与 IP Brief 一致；不写入 vanity KPI。

| 任务 | 产出/动作 |
|------|-----------|
| 仅集成层触达；**不改** kernel 除非 Owner 专项 | `kernels/xiaohongshu/line2/` |

**验收：** `bash scripts/agent-shells/05-xhs-kernel.sh`（与 deep-delivery 并行时 campaign 仅 `--check`）· `verify-agent-fused --agent 05`

---

## 06 · xhs-content-pipeline · Brief 批量

**目标：** 全 Brief 目录 SEO + 结构 PASS。

| 任务 | 产出/动作 |
|------|-----------|
| 批量 verify 全 `content/xiaohongshu/*-brief.md` | pipeline hygiene |

**验收：** `bash scripts/agent-shells/06-xhs-pipeline.sh` · `verify-agent-fused --agent 06`

---

## 07 · brand-visual · 封面 / kit

**目标：** Discovery 待发 Brief 封面块就绪（Owner 要图时 Canva）。

| 任务 | 产出/动作 |
|------|-----------|
| 视觉 README + brand-visual skill 路径 | `content/visual/README.md` |
| Brief 内封面块检查（discovery-01 优先） | 各 Brief `## 封面` |

**验收：** `bash scripts/agent-shells/07-brand-visual.sh --check` · `verify-agent-fused --agent 07`

---

## 08 · platform-integration · gdocs/Drive

**目标：** 集成 6 case 可读；Owner 未要求则不 sync Drive。

| 任务 | 产出/动作 |
|------|-----------|
| verify-integration 干跑 | OAuth 可选 |

**验收：** `bash scripts/agent-shells/08-platform.sh --check`（campaign 全量时 `--verify` 若未 SKIP）· `verify-agent-fused --agent 08`

---

## 09 · data-analytics · CSV → 策略

**目标：** 认知期队列证据 + ceo-dispatch → 04；Artist watchlist 输入 GM10。

| 任务 | 产出/动作 |
|------|-----------|
| pipeline → next-topics + dispatch 刷新 | `bash scripts/analytics-pipeline.sh --demo`（有 inbox 则 live） |
| screen artist watchlist | `scripts/screen-artist-watchlist.py` |
| 仪表盘 | `content/analytics/derived/manager-dashboard-2026-10-27.md` |

**验收：** `bash scripts/agent-shells/09-analytics.sh --demo` · `verify-agent-fused --agent 09` · `ceo-dispatch-refresh.py`

---

## 10 · artist-benchmark · 日更对标

**目标：** Artist 四指标 + timeline；thatviolakid 等 watchlist 条目进 catalog。

| 任务 | 产出/动作 |
|------|-----------|
| 当日 v0-benchmark.json + challenge 链 | `content/evolution/10-artist-intel/2026-10-27/` |
| merge catalog | `merge-artist-intel-catalog.py` |

**验收：** `verify-agent-fused --agent 10 --with-artifacts`（Gemini 由 daily/deep 跑过时 campaign 仅 L1+artifacts）

---

## 11 · ip-daily-evaluator · IP challenge

**目标：** rollups 筛选 + challenge-log + gold 与 Discovery 对抗一致。

| 任务 | 产出/动作 |
|------|-----------|
| v0-eval.json · challenge-log.md · reference/gold.md | `content/evolution/11-ip-daily-eval/2026-10-27/` |

**验收：** `verify-agent-fused --agent 11 --with-artifacts`

---

## 12 · owner-daily-brief · Owner 汇总

**目标：** 一页纸：认知期优先级 + Artist 要点 + HTML 链接 + 待 Owner 动作（发帖/CSV）。

| 任务 | 产出/动作 |
|------|-----------|
| 刷新 daily brief 含 ceo-dispatch + HTML 路径 | `content/daily-brief/2026-10-27-owner-daily-brief.md` |

**验收：** `verify-agent-fused --agent 12 --with-artifacts`

---

## Manager 派活记录（模板 · campaign 结束后填）

```markdown
## Manager 派活记录 · 2026-10-27 全 Agent
- 目标：认知期 + Artist + HTML · 24:00 前
- Campaign：ceo-ip-all-agents-campaign · deep-delivery：（并行/否）
- 01–12 终端：见 campaign log
- Owner Gate：PASS/FAIL · 打回轮次 n/3 · 交 Owner：是/否
- Owner HTML：`OWNER-XHS-FILTER-DELIVERABLE-2026-10-27.html`
```

---

*CEO 签发 · 2026-10-27 · 勿把未 gate PASS 的 Brief 当终稿交 Owner。*
