---
context_version: "2026-10-30-l012"
repo_path: "docs/CEO-MANAGER-OPERATING-PRINCIPLES.md"
goal: "CEO / Manager 运营五原则 · SOP"
openwebui_route: "rag_l1"
cursor_route: "read"
content_sha256: "b644a83b092aecca"
---

# CEO / Manager 运营五原则 · SOP

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** - [ ] dispatch md 已落盘，每个 Agent 有验收命令
- [ ] 终端有 PASS 输出（非口头）
- [ ] Brief 已过 auto-gate（Owner Gate PASS）
- [ ] 无数据处已标「未验证」
- [ ] FAIL / 中断已 recover，非半截日志
- [ ] 洞见已落盘（本仓文件），待 commit 项已
- **Path:** `docs/CEO-MANAGER-OPERATING-PRINCIPLES.md`
- **Open WebUI:** `rag_l1`
- **Cursor:** `read`

## 章节锚点
- **L1 任务（压缩 · Open WebUI / Cursor 顶栏）**: - **Goal:** > **定位：** 原则 → **脚本映射** + **晚间派活 8 步**（偏执行清单）。
- **章节锚点**: - **1. 清晰的委派**: **做法**
- **8. 自检清单（CEO 每次交付前）**: - [ ] dispatch md 已落盘，每个 Agent 有验收命令


---

## L2 正文

# CEO / Manager 运营五原则 · SOP

> **定位：** 原则 → **脚本映射** + **晚间派活 8 步**（偏执行清单）。  
> **详述与案例：** [CEO-MANAGER-OPERATING-STANDARDS.md](./CEO-MANAGER-OPERATING-STANDARDS.md) · **GM 五 step 环对照：** [MANAGER-EVAL-IMPROVEMENT-LOOP.md](./MANAGER-EVAL-IMPROVEMENT-LOOP.md) · **派活模板：** [CEO-DISPATCH-SOP.md](../agents/00-manager/CEO-DISPATCH-SOP.md)  
> **主框架：** Owner 三支柱 → [MANAGER-THREE-PILLARS.md](./MANAGER-THREE-PILLARS.md)；**CEO 双轮迭代（consult SOP）：** [CEO-DOUBLE-ITERATION-SOP.md](../agents/00-manager/CEO-DOUBLE-ITERATION-SOP.md) · [CEO-SENIOR-MANAGER-IMPROVEMENT-LOOP.md](./CEO-SENIOR-MANAGER-IMPROVEMENT-LOOP.md)；本文五原则为落地清单。  
> **范围：** 不改 kernel、不新增第二套 CEO 体系（见 [integration/IMPORTANT.md](../integration/IMPORTANT.md)）。  
> **首次落盘：** 2026-10-27 晚（北京）· Owner 确认五原则 + 目标「打造个人 IP」。


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
4. **Routine Gate PASS：** 交 Owner **否** · 通知 **HTML**（[OWNER-DELIVERY-NOTIFY-DEFAULT.md](./OWNER-DELIVERY-NOTIFY-DEFAULT.md)）。**交 Owner：是** 仅 gold / 战略 / 不可逆 / 3 轮仍 FAIL。

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


## 3. 数据驱动改进

1. **FAIL 先分类**：集成路径 / Brief 内容 / kernel（`IMPORTANT.md`）。
2. **自动改稿环（≤3 轮）**：FAIL → 写 `CEO-REROUTE.md` → 同会话改稿 → 再 `auto-gate-loop`。**勿**等 Owner 说「evaluate / challenge」。
3. **重对抗**：`run-xhs-brief-adversarial-challenge.py`（规范：[BRIEF-ADVERSARIAL-CHALLENGE.md](../agents/_shared/BRIEF-ADVERSARIAL-CHALLENGE.md)）；产物 `content/xiaohongshu/challenge/*-challenge.md`。
4. **中断/阻塞/跑错**：`bash scripts/ceo-auto-recover-blocked.sh` → 读 `ceo-inbox/ceo-auto-recover-latest.md` → 按需 nohup 重跑（[CEO-AUTO-RECOVER-AND-RETRY.md](CEO-AUTO-RECOVER-AND-RETRY.md)）。
5. **数据诚实**：09 无 CSV（`content/analytics/inbox/`）时，阅读/转化结论一律标 **「未验证」**，不编造。
6. **深交付**：Owner 给截止时用 `run-ceo-deep-delivery-cycle.sh`（多轮 pipeline + gate + adversarial 刷新），不以单轮 `ceo-xhs-ip-filter-batch.py` 应付（[CEO-OWNER-DEADLINE-DELIVERY.md](CEO-OWNER-DEADLINE-DELIVERY.md)）。


## 5. 个人 + AI 洞见 → 持久团队资产

| 洞见来源 | 落盘位置 | 要求 |
|----------|----------|------|
| Owner 口语判断/裁决 | dispatch md「Owner 原话」· `rules/USER.md` · `content/personal-ip/` | 原话保留，摘要不改义 |
| Agent 分析 / 对标 | `content/ip-research/artist-intel-catalog.*` · `content/xiaohongshu/*-brief.md` · `challenge/` | 会话开头一次性列全未审条目（[OWNER-ARTIST-CATALOG-ON-OPEN.md](OWNER-ARTIST-CATALOG-ON-OPEN.md)） |
| 战役结果 | `ceo-inbox/ceo-ip-all-agents-campaign-<ts>.md/.log` · Owner HTML | 报告 + 日志成对保留 |
| 流程经验 | 本文件 · `docs/*.md` · `agents/_shared/` | 新目录同步 `rules/WORKSPACE.md` |
| 交班 | `verify-handoff.sh` · [AGENT-TAKEOVER.md](AGENT-TAKEOVER.md) | **定稿产出 commit 进 Git**；Drive 仅 Owner 要求时 sync |

红线：未 `aligned: true` 不称定稿、不 sync Drive；发布/私信/Drive 覆盖仅 Owner 授权。


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