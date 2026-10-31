---
context_version: "2026-10-30-l012"
repo_path: "content/evolution/00-manager/ceo-inbox/CEO-IP-ALL-AGENTS-DISPATCH-2026-10-27.md"
goal: "CEO · 全 Agent 协同派活 · IP 认知期 + Artist + HTML"
openwebui_route: "intake_l2"
cursor_route: "read"
content_sha256: "4cf6e442297606c5"
---

# CEO · 全 Agent 协同派活 · IP 认知期 + Artist + HTML

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** *CEO 签发 · 2026-10-27 · 勿把未 gate PASS 的 Brief 当终稿交 Owner。*
- **Path:** `content/evolution/00-manager/ceo-inbox/CEO-IP-ALL-AGENTS-DISPATCH-2026-10-27.md`
- **Open WebUI:** `intake_l2`
- **Cursor:** `read`

## 章节锚点
- **L1 任务（压缩 · Open WebUI / Cursor 顶栏）**: - **Goal:** **截止：** 2026-10-27 24:00 北京时间
- **章节锚点**: - **交付锚点（Owner 打开）**: | 产物 | 路径 |


---

## L2 正文

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


## 01 · personal-ip · IP 战略

**目标：** 认知期叙事与 CAPSTONE 一致；Discovery 四篇不绑垂直、不单品类。

| 任务 | 产出/动作 |
|------|-----------|
| 复核 playbook §4 认知期 vs Discovery Brief 支柱 | `content/personal-ip/2026-10-18-key-person-of-influence-capstone-playbook.md` |
| 确认 ip-positioning 三支柱 + 品牌合作范围 | `content/personal-ip/ip-positioning-brief-2026-10-05.md` |
| 对抗 drill 结论进 CEO 决策 | `content/personal-ip/2026-10-27-ip-adversarial-FULL-DRILL-REPORT.md` |

**验收：** `bash scripts/agent-shells/01-personal-ip.sh --check` · `bash scripts/verify-agent-fused.sh --agent 01`


## 03 · marketing-strategy · 触达 / 认知期 program

**目标：** 认知期 operating plan 与 Discovery 队列节奏一致。

| 任务 | 产出/动作 |
|------|-----------|
| 读 discovery-phase OPERATING-PLAN | `content/marketing/discovery-phase-OPERATING-PLAN.md` |
| 触达计划不越级强转化 | `content/marketing/` |

**验收：** `bash scripts/agent-shells/03-marketing.sh --verify` · `verify-agent-fused --agent 03`


## 05 · xhs-kernel · 对齐判定

**目标：** classifier / Gemini 6 case 与 IP Brief 一致；不写入 vanity KPI。

| 任务 | 产出/动作 |
|------|-----------|
| 仅集成层触达；**不改** kernel 除非 Owner 专项 | `kernels/xiaohongshu/line2/` |

**验收：** `bash scripts/agent-shells/05-xhs-kernel.sh`（与 deep-delivery 并行时 campaign 仅 `--check`）· `verify-agent-fused --agent 05`


## 07 · brand-visual · 封面 / kit

**目标：** Discovery 待发 Brief 封面块就绪（Owner 要图时 Canva）。

| 任务 | 产出/动作 |
|------|-----------|
| 视觉 README + brand-visual skill 路径 | `content/visual/README.md` |
| Brief 内封面块检查（discovery-01 优先） | 各 Brief `## 封面` |

**验收：** `bash scripts/agent-shells/07-brand-visual.sh --check` · `verify-agent-fused --agent 07`


## 09 · data-analytics · CSV → 策略

**目标：** 认知期队列证据 + ceo-dispatch → 04；Artist watchlist 输入 GM10。

| 任务 | 产出/动作 |
|------|-----------|
| pipeline → next-topics + dispatch 刷新 | `bash scripts/analytics-pipeline.sh --demo`（有 inbox 则 live） |
| screen artist watchlist | `scripts/screen-artist-watchlist.py` |
| 仪表盘 | `content/analytics/derived/manager-dashboard-2026-10-27.md` |

**验收：** `bash scripts/agent-shells/09-analytics.sh --demo` · `verify-agent-fused --agent 09` · `ceo-dispatch-refresh.py`


## 11 · ip-daily-evaluator · IP challenge

**目标：** rollups 筛选 + challenge-log + gold 与 Discovery 对抗一致。

| 任务 | 产出/动作 |
|------|-----------|
| v0-eval.json · challenge-log.md · reference/gold.md | `content/evolution/11-ip-daily-eval/2026-10-27/` |

**验收：** `verify-agent-fused --agent 11 --with-artifacts`


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