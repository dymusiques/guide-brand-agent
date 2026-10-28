# CEO · 全员派活（晚间战役）· 90 天 IP 筛选漏斗

**签发：** 2026-10-27 晚（北京）· 00 Manager 代 CEO  
**战役题目：** 「**90 天 IP 筛选漏斗：从 Discovery 01 定稿到 Artist 强链接**」  
**Owner 原话：** 「动用所有的 Sub Agent，CEO，动用所有的 Sub Agent。以打造我的 IP 为目标，让他们所有人都动起来……只要这个题目能让所有的 Agent 动起来就可以」  
**North star：** Danying 长笛 / 教育 / 咨询 IP — 小红书 Discovery 系列 + Artist Watchlist + 听见 Daily 同一叙事轴；每 Agent 产出可验收结果，不是空聊。  
**关联日间派活：** [CEO-IP-ALL-AGENTS-DISPATCH-2026-10-27.md](CEO-IP-ALL-AGENTS-DISPATCH-2026-10-27.md)  
**Campaign 命令：** `VERIFY_GOALS_SKIP_PLATFORM=0 bash scripts/run-ceo-ip-all-agents-campaign.sh`  
**G-* 总绑：** G-STRONG-LINK · G-NOT-SINGLE-VERTICAL-LOCK · G-BRIEF-ALIGNED-GATE · G-ANALYTICS-EVIDENCE

## 漏斗三段（叙事轴）

| 段 | 0–30 天 | 31–60 天 | 61–90 天 |
|----|---------|----------|----------|
| 筛选 | Discovery 01–04 定稿发布（认知期） | 数据回流 → 筛哪类读者互动最强 | 强链接名单：品牌 / 艺术家 / 教育 |
| 内容 | 不可替代性 · 叙事非硬广 · 专业信任 | Artist Watchlist 对标（thatviolakid 等） | 听见 Daily 与 Discovery 互链 |
| 红线 | 不单品类绑定；先观点后产品 | 不编造数据（无 CSV 标未验证） | 发布/私信/Drive 仅 Owner 授权 |

## Per-agent 任务与验收

| Agent | 任务 | 验收（终端） |
|-------|------|--------------|
| 00 Manager | 派活记录 · auto-gate 政策 · 收汇报 | `manager-dashboard.sh` · `manager-workflow-verify.sh` |
| 01 personal-ip | 三支柱 + 人设对齐漏斗；Pitch 先观点后产品 | `agent-shells/01-personal-ip.sh --check` · `verify-agent-fused --agent 01` |
| 02 business-brand | 筛选漏斗定位 / SWOT 不 contradict 全品类 open | `02-business-brand.sh` · `fused 02` |
| 03 marketing | 90 天 campaign beat + 渠道（小红书主 + Daily） | `03-marketing.sh` · `fused 03` |
| 04 xhs topic | Discovery 01 v1.1（moment + 10 标签）工作项；Brief/challenge 对齐 | `fused 04` · auto-gate-loop |
| 05 xhs growth | 钩子 / CTA 强链接；kernel 不改 | `05-xhs-kernel.sh` · `fused 05` |
| 06 pipeline | 全 Brief 目录结构 + SEO | `06-xhs-pipeline.sh` · `fused 06` |
| 07 brand visual | 封面块 / 视觉一致性 | `07-brand-visual.sh --check` · `fused 07` |
| 08 platform | integration / verify-goals（平台含 Drive） | `08-platform.sh` · `fused 08` |
| 09 analytics | pipeline 证据 + ceo-dispatch + watchlist 筛 | `09-analytics.sh` · `screen-artist-watchlist.py` · `fused 09` |
| 10 artist-benchmark | Artist 四指标 · catalog | `fused 10 --with-artifacts` |
| 11 ip-daily-evaluator | rollups · challenge hygiene | `fused 11 --with-artifacts` |
| 12 owner-daily-brief | Owner 一页汇总（07 语气，非 Brief 正文） | `fused 12 --with-artifacts` |

## Manager 派活记录（执行后回填见本文件末「结果」）

- **Campaign：** `ceo-ip-all-agents-campaign-20261027-182723` · **18:27–18:30** · `VERIFY_GOALS_SKIP_PLATFORM=0` · `SKIP_GEMINI=0`
- **结果：** **RESULT: PASS** · failures **0** · 01–12 verify 链完成（含 02/03 Gemini 6）
- **Owner Gate：** **PASS** · 打回轮次 **n/a** · **交 Owner：是**
- **报告 / 日志：** `ceo-ip-all-agents-campaign-20261027-182723.md` · `.log`
- **HTML：** `OWNER-XHS-FILTER-DELIVERABLE-2026-10-27.html`（campaign 后 + **follow-up** `build-owner-xhs-report-html.py` 含 Discovery 01 v1.1 / ThatViolaKid 标题）

---

## 结果 · 2026-10-27 18:27–18:35（北京）

- **Campaign：** `VERIFY_GOALS_SKIP_PLATFORM=0` · `SKIP_GEMINI=0`（预检无 deep-delivery 在跑）· **RESULT: PASS ceo-ip-all-agents-campaign**
  - 报告：`content/evolution/00-manager/ceo-inbox/ceo-ip-all-agents-campaign-20261027-182723.md`
  - 日志：`content/evolution/00-manager/ceo-inbox/ceo-ip-all-agents-campaign-20261027-182723.log`
- **事故：** 首次启动（18:21:51，`…-182151.log`）在 03 Gemini 阶段进程被工具会话回收；`ceo-auto-recover-blocked.sh` 清锁后重跑成功。recover 顺带拉起的 deep-delivery 同样被回收，已清 stale lock（`ceo-deep-delivery-20261027-182650.log` 为半截日志，无 PASS 标记，勿当交付）。

### 01–12 终端矩阵

| Agent | 命令 | 结果 |
|-------|------|------|
| 00 | manager-dashboard + ceo-dispatch-refresh | PASS |
| 01 | 01-personal-ip --check + fused 01 | PASS |
| 02 | verify-business-brand（Gemini 6）+ fused 02 | PASS |
| 03 | verify-marketing-campaign（Gemini 6）+ fused 03 | PASS |
| 04 | fused 04（A + B kernel 6） | PASS |
| 05 | 05-xhs-kernel（Gemini 6）+ fused 05 | PASS |
| 06 | 06-xhs-pipeline + fused 06 | PASS |
| 07 | 07-brand-visual --check + fused 07 | PASS |
| 08 | 08-platform verify + fused 08（platform 未跳过） | PASS |
| 09 | 09-analytics --live + screen-artist-watchlist + fused 09 | PASS |
| 10 | fused 10 --with-artifacts | PASS |
| 11 | fused 11 --with-artifacts | PASS |
| 12 | fused 12 --with-artifacts | PASS |

### 04 工作项 · Discovery 01 v1.1（已落地）

- 改动：开头加匿名 moment（「你一定见过这一幕：快闪现场人人举手机拍装置，音乐响起，手机慢慢放下。」——泛场景，**非**声称真实亲历）· 标签补满 10 个 · 封面定为文字海报。
- 文件：`content/xiaohongshu/2026-10-17-discovery-01-irreplaceability-brief.md` · `content/xiaohongshu/2026-10-20-publish-ready-queue.md`（篇 1 正文 + 标签）。
- 验收：`manager-ceo-auto-gate-loop.sh --brief …` **PASS（round 1/3）** · `manager-ceo-owner-gate.sh` **PASS** · `manager-workflow-verify.sh` PASS。

### 06 卫生项

- `verify-xhs-content-dir.sh` 曾报 `2026-10-27-artist-benchmark-thatviolakid-brief.md` H1 > 40 字；已缩短 H1，复跑 **6/6 PASS**。

### Manager 派活记录 · 晚间终版

- 目标：90 天 IP 筛选漏斗 · 01–12 全员动起来
- 终端：Campaign PASS（0 failures）· Discovery 01 v1.1 gate PASS · 06 SEO 6/6 PASS
- **Owner Gate：PASS · 打回轮次 0/3（round 1/3 即过）· 交 Owner：是（仅限：Discovery 01 v1.1 发布裁决 / 发帖 / CSV 导出）**
- 未做：未 commit · 未 sync Drive · 未发帖 · 09 inbox 仍 0 CSV → 数据类结论标「未验证」
