# CEO / Manager 运营五原则 · SOP

> **定位：** 原则 → **脚本映射** + **晚间派活 8 步**（偏执行清单）。  
> **详述与案例：** [CEO-MANAGER-OPERATING-STANDARDS.md](./CEO-MANAGER-OPERATING-STANDARDS.md) · **GM 五 step 环对照：** [MANAGER-EVAL-IMPROVEMENT-LOOP.md](./MANAGER-EVAL-IMPROVEMENT-LOOP.md) · **派活模板：** [CEO-DISPATCH-SOP.md](../agents/00-manager/CEO-DISPATCH-SOP.md)  
> **主框架：** Owner 三支柱 → [MANAGER-THREE-PILLARS.md](./MANAGER-THREE-PILLARS.md)；**CEO 双轮迭代（consult SOP）：** [CEO-DOUBLE-ITERATION-SOP.md](../agents/00-manager/CEO-DOUBLE-ITERATION-SOP.md) · [CEO-SENIOR-MANAGER-IMPROVEMENT-LOOP.md](./CEO-SENIOR-MANAGER-IMPROVEMENT-LOOP.md)；本文五原则为落地清单。  
> **范围：** 不改 kernel、不新增第二套 CEO 体系（见 [integration/IMPORTANT.md](../integration/IMPORTANT.md)）。  
> **首次落盘：** 2026-10-27 晚（北京）· Owner 确认五原则 + 目标「打造个人 IP」。

---

## 0. 五原则一页纸

| # | 原则 | 一句话 | 仓库里的落点 |
|---|------|--------|--------------|
| 1 | **清晰的委派** | 谁、做什么、验收什么、红线是什么，写进 dispatch md | `ceo-inbox/CEO-IP-ALL-AGENTS-DISPATCH-*.md` · [AUTO-WORKFLOW](../agents/00-manager/AUTO-WORKFLOW.md) |
| 2 | **有把握的评估** | 进展必须可衡量：终端 PASS/FAIL + 日志，不凭感觉 | `verify-goals` · `verify-agent-fused` · auto-gate · 6 test |
| 3 | **数据驱动改进** | 失败 → 分类 → 改稿/改集成 → 复测；无数据标「未验证」 | adversarial · CEO-REROUTE · 09 analytics · auto-recover |
| 4 | **教练式引导促成长** | 给 GM 具体 REROUTE 与评分理由，让其改稿，不替 Owner 兜底 | `CEO-REROUTE.md` · GM-REPORT · Manager's Loop |
| 5 | **个人+AI 洞见 → 持久团队资产** | Owner 的口语判断 + Agent 的分析 → 落盘 md/HTML/catalog，并 commit | `docs/` · `content/` · `artist-intel-catalog` · handoff |

---

## 1. 清晰的委派

**做法**

1. Owner 口语目标 → 00 Manager **自动接手**（无需口令，见 `danying-manager-auto.mdc`）。
2. 凡「多 Agent / 有截止」任务：**先落盘 dispatch md**，再跑脚本。至少含：
   - 签发时间、战役题目、Owner 原话、North star
   - 叙事轴（例：0–30 / 31–60 / 61–90 天）
   - **Per-agent 表：任务 + 终端验收命令**（01–12）
   - 红线（不编造数据、不单品类绑定、发布/Drive 仅 Owner）
   - 回填区：Manager 派活记录 + 结果
3. 每步派活前读 `agents/<nn>-*/INTEGRATION-PROMPT.md`；单会话内顺序扮演各 Agent。
4. 交 Owner 的只有：gold / 发布 / 裁决 / 3 轮仍 FAIL 的升级项。

**Dispatch md 模板（复制改日期即可）**

```markdown
# CEO · 全员派活（<日间|晚间>）· <战役题目>
**签发：** YYYY-MM-DD <时段>（北京）· 00 Manager 代 CEO
**战役题目：** 「…」
**Owner 原话：** 「…」
**North star：** …
**Campaign 命令：** `VERIFY_GOALS_SKIP_PLATFORM=0 bash scripts/run-ceo-ip-all-agents-campaign.sh`
**G-* 总绑：** G-STRONG-LINK · G-NOT-SINGLE-VERTICAL-LOCK · G-BRIEF-ALIGNED-GATE · G-ANALYTICS-EVIDENCE

## 叙事轴（漏斗/阶段表）
## Per-agent 任务与验收（01–12 · 每行必须有终端命令）
## Manager 派活记录（目标 · 终端 · Owner Gate PASS/FAIL · 打回轮次 n/3 · 交 Owner：是/否）
## 结果（campaign 报告路径 · 事故与 recover · 未做事项）
```

参考实例：[CEO-IP-ALL-AGENTS-DISPATCH-2026-10-27-evening.md](../content/evolution/00-manager/ceo-inbox/CEO-IP-ALL-AGENTS-DISPATCH-2026-10-27-evening.md)（日间版：同目录 `…-2026-10-27.md`）。

---

## 2. 有把握的评估（可衡量进展）

**规则：** 没有命令输出 / 日志 / JSON，就不叫「完成」。

| 度量层 | 命令 / 产物 | 回答的问题 |
|--------|-------------|------------|
| 目标钩子 | `bash scripts/verify-goals.sh`（`VERIFY_GOALS_SKIP_PLATFORM=0` 含 Drive 平台） | G-* 总目标是否仍成立 |
| 单 Agent 融合 | `bash scripts/verify-agent-fused.sh --agent <nn> [--with-artifacts]` · `scripts/agent-shells/<nn>-*.sh` | 该 Agent 的 verify + 产物是否达标 |
| Brief Owner Gate | `manager-ceo-auto-gate-loop.sh --brief …`（内嵌 redteam + adversarial + complete）· `manager-ceo-owner-gate.sh` | 稿能否交 Owner |
| 全仓 Brief | `manager-xhs-briefs-auto-pipeline.sh` | 全部 Brief 是否对齐 |
| 6 test（Gemini） | `bash scripts/verify-xhs-topic.sh`（04/05 kernel 6 case）；02/03 另有各自 Gemini 6 | 小红书涨粉/强链接/IP 对齐判定是否稳定。**Module 3 课纲 6 test 不在本仓**，见 [check.md](../check.md) |
| 小红书目录卫生 | `bash scripts/verify-xhs-content-dir.sh`（SEO：H1≤40 字等 6 项） | 标题/结构/SEO |
| 集成 / 交班 | `verify-integration.sh`（6 case）· `verify-handoff.sh` | 工具链与接手完整性 |
| Manager 总验 | `bash scripts/manager-workflow-verify.sh [brief]` | 指挥链是否闭环 |

**派活记录固定格式（每轮必出）：** `Owner Gate PASS/FAIL · 打回轮次 n/3 · 交 Owner：是/否`。

---

## 3. 数据驱动改进

1. **FAIL 先分类**：集成路径 / Brief 内容 / kernel（`IMPORTANT.md`）。
2. **自动改稿环（≤3 轮）**：FAIL → 写 `CEO-REROUTE.md` → 同会话改稿 → 再 `auto-gate-loop`。**勿**等 Owner 说「evaluate / challenge」。
3. **重对抗**：`run-xhs-brief-adversarial-challenge.py`（规范：[BRIEF-ADVERSARIAL-CHALLENGE.md](../agents/_shared/BRIEF-ADVERSARIAL-CHALLENGE.md)）；产物 `content/xiaohongshu/challenge/*-challenge.md`。
4. **中断/阻塞/跑错**：`bash scripts/ceo-auto-recover-blocked.sh` → 读 `ceo-inbox/ceo-auto-recover-latest.md` → 按需 nohup 重跑（[CEO-AUTO-RECOVER-AND-RETRY.md](CEO-AUTO-RECOVER-AND-RETRY.md)）。
5. **数据诚实**：09 无 CSV（`content/analytics/inbox/`）时，阅读/转化结论一律标 **「未验证」**，不编造。
6. **深交付**：Owner 给截止时用 `run-ceo-deep-delivery-cycle.sh`（多轮 pipeline + gate + adversarial 刷新），不以单轮 `ceo-xhs-ip-filter-batch.py` 应付（[CEO-OWNER-DEADLINE-DELIVERY.md](CEO-OWNER-DEADLINE-DELIVERY.md)）。

---

## 4. 教练式引导促成长

- **REROUTE 不是判决书**：写清「哪条红线/哪条 challenge 没过 → 建议怎么改 → 复测命令」，让 GM（04/01/09/11…）在同会话自己改到 PASS。
- **GM-REPORT**：每个 GM 先自跑本部门 evaluate/verify，再汇报；CEO 只在 gate 层抽检。
- **Manager's Loop**（`AUTO-WORKFLOW.md`）：`Analyze Failures → Manual Analysis → Propose Prompt Change → Observe Score → Re-run`——改的是集成/Brief/Skill，**不碰 kernel**（除非 05 专项）。
- **每轮复盘一句话**：本轮学到什么（例：开头加匿名 moment 可过 gate；H1 超 40 字会挂 06 SEO），写进 dispatch md「结果」或相关 SOP，下一轮默认应用。
- **对 Owner**：只升级需要其判断的事；不要求 Owner 学公式化 prompt（[OWNER-INPUT-PRINCIPLES.md](OWNER-INPUT-PRINCIPLES.md)）。

---

## 5. 个人 + AI 洞见 → 持久团队资产

| 洞见来源 | 落盘位置 | 要求 |
|----------|----------|------|
| Owner 口语判断/裁决 | dispatch md「Owner 原话」· `rules/USER.md` · `content/personal-ip/` | 原话保留，摘要不改义 |
| Agent 分析 / 对标 | `content/ip-research/artist-intel-catalog.*` · `content/xiaohongshu/*-brief.md` · `challenge/` | 会话开头一次性列全未审条目（[OWNER-ARTIST-CATALOG-ON-OPEN.md](OWNER-ARTIST-CATALOG-ON-OPEN.md)） |
| 战役结果 | `ceo-inbox/ceo-ip-all-agents-campaign-<ts>.md/.log` · Owner HTML | 报告 + 日志成对保留 |
| 流程经验 | 本文件 · `docs/*.md` · `agents/_shared/` | 新目录同步 `rules/WORKSPACE.md` |
| 交班 | `verify-handoff.sh` · [AGENT-TAKEOVER.md](AGENT-TAKEOVER.md) | **定稿产出 commit 进 Git**；Drive 仅 Owner 要求时 sync |

红线：未 `aligned: true` 不称定稿、不 sync Drive；发布/私信/Drive 覆盖仅 Owner 授权。

---

## 6. 原则 → 脚本映射总表

| 脚本 / 机制 | 对应原则 | 作用 |
|-------------|----------|------|
| dispatch md（`ceo-inbox/CEO-IP-ALL-AGENTS-DISPATCH-*.md`） | 1 | 委派契约：任务 + 验收 + 红线 |
| `run-ceo-ip-all-agents-campaign.sh` | 1·2 | 01–12 顺序 verify + shell，出 campaign 报告 |
| `verify-agent-fused.sh` / `agent-shells/*.sh` | 2 | 每 Agent 可测的进展 |
| `verify-goals.sh` | 2 | G-* 目标钩子 |
| `manager-ceo-auto-gate-loop.sh` · `manager-ceo-owner-gate.sh` | 2·3·4 | Owner Gate + ≤3 轮改稿 |
| `run-xhs-brief-adversarial-challenge.py` | 3 | 对抗找漏洞 |
| `verify-xhs-topic.sh`（6 test）· `verify-xhs-content-dir.sh` | 2·3 | kernel 判定 + SEO/目录卫生 |
| `ceo-auto-recover-blocked.sh` | 3 | 中断自愈，不打扰 Owner |
| `run-ceo-deep-delivery-cycle.sh` | 2·3 | 截止前多轮深筛 |
| `build-owner-xhs-report-html.py` | 5 | 交 Owner 的 HTML 资产 |
| `manager-workflow-verify.sh` | 2 | 指挥链总验 |
| `ceo-dispatch-refresh.py` / 09→04 派活块 | 3·5 | 数据 → 下一轮派活 |

---

## 7. 晚间派活套路（Evening Dispatch Pattern）

适用：Owner 晚间一句话「动用所有 Sub Agent，以 X 为目标」。

1. **落盘** `CEO-IP-ALL-AGENTS-DISPATCH-<date>-evening.md`（题目 + 叙事轴 + 01–12 验收表 + 红线）。
2. **预检**：无 deep-delivery 在跑（`/tmp/ceo-deep-delivery.lock` 或进程检测）；有则 `SKIP_GEMINI=1`，避免重复 heavy Gemini。
3. **跑 campaign**：`VERIFY_GOALS_SKIP_PLATFORM=0 bash scripts/run-ceo-ip-all-agents-campaign.sh`（`nohup` 后台 + 读 log）。
4. **逐 Agent**：verify / fused；04 同步做具体工作项（改 Brief）→ `manager-ceo-auto-gate-loop.sh --brief …` → `manager-ceo-owner-gate.sh`。
5. **中断**：`ceo-auto-recover-blocked.sh` → 清锁 → 重跑；半截日志（无 PASS 标记）**不当交付**。
6. **收尾**：`build-owner-xhs-report-html.py` 出 Owner HTML；`manager-workflow-verify.sh`。
7. **回填 dispatch md**：Manager 派活记录（`Owner Gate · 打回轮次 n/3 · 交 Owner`）+ 事故 + 未做项（未 commit / 未 sync Drive / 未发帖 / 无 CSV）。
8. **只交 Owner 裁决项**（发布、CSV 导出、gold）。

**2026-10-27 实例**：见 [dispatch evening](../content/evolution/00-manager/ceo-inbox/CEO-IP-ALL-AGENTS-DISPATCH-2026-10-27-evening.md) · campaign `ceo-ip-all-agents-campaign-20261027-182723`（PASS，0 failures）。

---

## 8. 自检清单（CEO 每次交付前）

- [ ] dispatch md 已落盘，每个 Agent 有验收命令
- [ ] 终端有 PASS 输出（非口头）
- [ ] Brief 已过 auto-gate（Owner Gate PASS）
- [ ] 无数据处已标「未验证」
- [ ] FAIL / 中断已 recover，非半截日志
- [ ] 洞见已落盘（本仓文件），待 commit 项已列给 Owner
- [ ] Manager 派活记录含 `Owner Gate · n/3 · 交 Owner`
