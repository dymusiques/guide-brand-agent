---
context_version: "2026-10-30-l012"
repo_path: "content/personal-ip/2026-10-27-ip-adversarial-red-team.md"
goal: "IP 对抗性红队 · 全 Agent 动员（2026-10-27）"
openwebui_route: "intake_l2"
cursor_route: "read"
content_sha256: "81dc422e40a2fc39"
---

# IP 对抗性红队 · 全 Agent 动员（2026-10-27）

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** > **用途：** Owner 要求「先定正确方向，再用行业常见坑 + 本仓 SOP/函数壳做**高挑战对抗**」——让 00–09、kernel、verify **都有明确攻击面**，而不是只写鸡汤 checklist。  
> **真相源：** [ip-positioning-brief-2026-10-05.md](./ip-positioning-b
- **Path:** `content/personal-ip/2026-10-27-ip-adversarial-red-team.md`
- **Open WebUI:** `intake_l2`
- **Cursor:** `read`

## 章节锚点
- **B. 错误分级 · 为何「很难被自动纠正」**: | 级别 | 含义 | 本仓谁管 | 典型例子 |
- **D. 分 Agent 红队攻击（每个 Agent「动起来」干什么）**
- **F. Owner 启动（口语即可 · 不必复制口令）**: **任一句即可触发 CEO 链：**
- **H. 与 verify / 函数壳映射（SOP 不是摆设）**: | 程序 | 红队测的层 |
- **J. CEO + Evaluator + 全员 Sub-agent 动员 SOP**: ```text
- **L. Owner 固定 · Brief 前红队 2 条/篇（2026-10-27）**: **Owner 确认：要固定。** 每篇 Brief 动笔前内部 2 条攻击（X1–X12 或 §D），落盘 `content/xiaohongshu/redteam/<slug>-pre.md`；O…


---

## L2 正文

# IP 对抗性红队 · 全 Agent 动员（2026-10-27）

> **用途：** Owner 要求「先定正确方向，再用行业常见坑 + 本仓 SOP/函数壳做**高挑战对抗**」——让 00–09、kernel、verify **都有明确攻击面**，而不是只写鸡汤 checklist。  
> **真相源：** [ip-positioning-brief-2026-10-05.md](./ip-positioning-brief-2026-10-05.md) · [integration/IMPORTANT.md](../../integration/IMPORTANT.md) · [GOALS-REGISTRY.md](../../integration/GOALS-REGISTRY.md)  
> **外部参考（非 Tier-1 事实）：** 人人都是产品经理 IP 误区文 · 杨天真「定位+内容+产业」· PBL/Forbes 一致性论述 · 见文末链接。


## B. 错误分级 · 为何「很难被自动纠正」

| 级别 | 含义 | 本仓谁管 | 典型例子 |
|------|------|----------|----------|
| **L1** | 脚本/规则能拦 | 05 kernel · L2 lint · evaluate | consultant 腔、单品类 Brief 句 |
| **L2** | verify PASS 仍跑偏 | 09 口径 · 01 战略 · Owner 眼 | aligned 但标题筛错人；约课填进 dm_count |
| **L3** | 人性/时间/环境 | **仅 Owner** | 审美要慢、怕争议、多平台分散、AI 浅用 |

**红队原则：** 专门打 **L2–L3**；L1 交给现有 `evaluate` + Manager's Loop。


## D. 分 Agent 红队攻击（每个 Agent「动起来」干什么）

> **用法：** 每月或每轮大选题前，让 Cursor 会话 **顺序扮演** 下列角色，对 **下一篇 Brief / 下一月计划** 念出「攻击句」；Owner 必须 **逐条驳或改稿**。  
> **验收挂钩：** 见 `G-*` 与 `bash scripts/verify-agent-matrix.sh --agent NN`。

### 00 · CEO / Manager

| 攻击（挑战性） | 在测什么 | 对抗动作 / SOP |
|----------------|----------|----------------|
| 「派活记录很漂亮，但 **没有任何一步强制 Owner 发帖** — 你是不是在用 verify 代替生意？」 | 编制 enforcement | 每轮必写 **Manager 派活记录**；未 aligned **禁止**称定稿；[AUTO-WORKFLOW](../../agents/00-manager/AUTO-WORKFLOW.md) |
| 「Goal 表上 G-QUALITY-GROWTH，你却 **从不导入 CSV** — 1700→5000 是幻想还是策略？」 | 数据飞轮 idle | `bash scripts/manager-autopilot.sh` · inbox CSV |
| 「EXTENSION 工具箱全开着，**主链 1→6 谁走了？**」 | 第二 CEO | [EXTENSION-POINTS](../../integration/EXTENSION-POINTS.md) §0 只认 Manager 链 |

### 01 · personal-ip（0b / 1）

| 攻击 | 测什么 | 对抗 |
|------|--------|------|
| 「四维受众平铺 — **卖课、卖策划还是卖藏品？** 电梯 8 秒对方记什么？」 | Pitch 失焦 | [CAPSTONE playbook](./2026-10-18-key-person-of-influence-capstone-playbook.md) §3.2–3.3 · **先观点后产品** |
| 「师承+三语+跨界 **形容词堆满**，**签单理由一句没有**。」 | 履历 IP | cv-source + **一个可验证 moment** |
| 「pivot 审美线 vs 旧 ✅技巧 — **你在 rebranding 第几次？**」 | 定位漂移 | 改频 **弧线叙事**（A→B→C→E），人设层一句不变 |
| 「**工作=IP** — 听见 Daily 日更把 **人即品牌** 冲淡了？」 | 栏目吞噬 IP | Daily ≠ 认知期 depth；[OPERATING-PLAN](../marketing/discovery-phase-OPERATING-PLAN.md) |

### 02 · business-brand

| 攻击 | G-* |
|------|-----|
| SWOT 写完 **零取舍** — 战略文档是安慰剂？ | G-BUSINESS-BRAND |
| 案例层家居/某行业 **出现 3 次** — 跨行业 open 死了？ | G-NOT-SINGLE-VERTICAL-LOCK |
| 把涨粉写进 **商业计划 KPI** — 强链接呢？ | G-STRONG-LINK |

**验收：** `evaluate-business-brand` / M4 lint（见 GOALS-REGISTRY）

### 03 · marketing-strategy

| 攻击 | G-* |
|------|-----|
| 认知期 **上 W1–W4 体验季大表** — 还没被看见就要大单？ | G-MARKETING-CAMPAIGN |
| 正文 **70% 招标 CTA** — 市场人为何收藏？ | G-STRONG-LINK |
| 标题钩子塞满 **「合作/品牌」** — 销售线索帖？ | G-STRONG-LINK |
| Daily 也要 **每条私信聊聊**？ | G-MARKETING-CAMPAIGN |

**验收：** `evaluate-marketing-campaign` · [discovery-phase](../marketing/2026-10-brand-discovery-phase.md)

### 04 · xhs-topic-manager（+ 2a 视频）

| 攻击 | 对抗 |
|------|------|
| 「**evaluate 过了** — 但口播像 consultant，**像本人吗？**」 | 2a Round1 + [VOICE-ANCHOR](../xiaohongshu/VOICE-ANCHOR.md) · `verify-xhs-voice-qa.sh` |
| 「追 **故事+冲突帖** 数据，认知期 **名片帖** 永远不发。」 | Intake + discovery 队列，不唯 Top 收藏 |
| 「**AI 写稿爽** — 审美/慢思考全没了。」 | Owner 原话进 owner-source；禁 L2 词 |
| 「Brief 工厂：**aligned 堆叠，App 零发布**。」 | [PUBLISH-AND-DATA-CHECKLIST](../xiaohongshu/PUBLISH-AND-DATA-CHECKLIST.md) |

### 05 · xhs-kernel（函数壳 / 6 case）

| aligned 仍失败 | Gemini 盲点 |
|----------------|-------------|
| 标题筛错人（猎奇 CTR、低完播） | 不读 CSV / dm 口径 |
| 连续垂类案例标签 | 不读系列级人设 |
| 约课向过密仍 yes | 不区分约课 vs 品牌 CTA |
| 口播/封面与 Brief 不一致 | 只读 subject+body JSON |
| 空泛「私信合作」无 moment | 不判完播与信任 |

**对抗：** 05 改规则 **仅 Owner 专项**；集成层改 Brief/Skill · [Manager's Loop](../../agents/00-manager/AUTO-WORKFLOW.md)

**验收：** `bash scripts/verify-xhs-topic.sh`（6 Gemini case）

### 06 · content-pipeline

| 攻击 | 对抗 |
|------|------|
| 「`verify-xhs-content-dir.sh` **全绿** — 账号在路人眼里是谁？」 | 绿 ≠ 战略；CEO 看 **发布状态** 非 verify |
| 「批量改 Brief **git add .** — Dry Run 呢？」 | [IMPORTANT Dry Run](../../integration/IMPORTANT.md) |

### 07 · brand-visual

| 攻击 | 对抗 |
|------|------|
| 「封面 **网红滤镜/错字体** — 法派专业高度在封面就塌。」 | brand-visual / Canva brand-check |
| 「标题讲审美，封面 **纯炫技大字** — 信号分裂。」 | 封面字块与 Brief 一致 |

### 08 · platform-integration

| 攻击 | 对抗 |
|------|------|
| 「Drive 同步了 — **Git 真相源还 care 吗？**」 | 未 aligned 不 Drive；定稿 **Must commit** |
| 「gdocs 当写稿入口 — **Vendor 绕开 04**。」 | Brief 只走 `content/xiaohongshu/` |

### 09 · data-analytics

| 攻击 | 对抗 |
|------|------|
| 「**约课私信填 dm_count** — pipeline 强链接造假。」 | [signal-baseline](../marketing/discovery-phase-signal-baseline.md) |
| 「无 CSV 仍 **next-topics 斩钉截铁**。」 | 标「未验证」· 不编造阅读/转化 |
| 「Top 帖全是 **泰斗发火体** — discovery 队列饿死。」 | 数据 **校准** 不 **覆盖** 认知期 program |
| 「用爆款压 05 **改 kernel**。」 | IMPORTANT：集成层不改 classifier |

**验收：** `bash scripts/analytics-pipeline.sh` · `ceo-dispatch-latest.md`


## F. Owner 启动（口语即可 · 不必复制口令）

**任一句即可触发 CEO 链：**

- 「**按 FULL-DRILL 再打一轮毒计划**」→ [FULL-DRILL-REPORT](./2026-10-27-ip-adversarial-FULL-DRILL-REPORT.md) · §3 毒计划 · 9 GM 评分 · 内部 Gate  
- 「**红队 §F**」或「**全员红队**」→ 本文件 §A North Star + §D 各 2 条攻击（轻量，不出完整 REPORT 除非你要）

Agent 内化：CEO→9 GM→内部 Gate；**不要求** Owner 公式化 prompt。见 [OWNER-INPUT-PRINCIPLES.md](../../docs/OWNER-INPUT-PRINCIPLES.md)。

<details><summary>可选 · 结构化口令（Agent 自用）</summary>

```text
1) CEO 复述 North Star §A
2) 顺序 01→09 各用 §D 对「下一篇/下一月计划」念 2 条攻击
3) 驳完后 04 才写 Brief（且仍须步 1c redteam-pre）
4) Manager 派活记录 + L2/L3 清单
```

</details>


## H. 与 verify / 函数壳映射（SOP 不是摆设）

| 程序 | 红队测的层 |
|------|------------|
| `evaluate-xhs-topic.py` | 单篇 Brief 内容 gate（L1） |
| `verify-xhs-topic.sh` | kernel 6 case 回归 |
| `verify-xhs-content-dir.sh` | 目录卫生（非战略） |
| `verify-agent-matrix.sh --agent NN` | 各部门函数壳 6 case |
| `verify-goals.sh` | G-* 钩子 |
| `manager-autopilot.sh` | CEO 链 + 09 派活 |
| `verify-xhs-voice-qa.sh` | 2a 声音 L2 |

**结论：** 自动程序 **擅长 L1**；本文件强迫 **L2–L3** 进入 Owner 对话 —— 这才是「打造 IP」真正难的部分。


## J. CEO + Evaluator + 全员 Sub-agent 动员 SOP

```text
1) Collector：Owner 口语指令 → collector-intake（slug ip-adversarial-drill-YYYY-MM-DD）
2) gold = reference/gold.md（North Star 不可删节对抗）
3) CEO 注入 §3 毒计划 v0 → 01–09 各 GM 驳斥 + SOP（§4 评分表）
4) CEO 出 v1 反击计划 → evaluate-edit-distance → metrics 均值应↓
5) 内部 manager-ceo-owner-gate（Brief 任务再加 --brief）
6) 交付 FULL-DRILL-REPORT；Owner 只勾确认项，不手跑 verify
```

**本轮执行报告：** [2026-10-27-ip-adversarial-FULL-DRILL-REPORT.md](./2026-10-27-ip-adversarial-FULL-DRILL-REPORT.md)  
**进化目录：** `content/evolution/00-manager/ip-adversarial-drill-2026-10-27/`


## L. Owner 固定 · Brief 前红队 2 条/篇（2026-10-27）

**Owner 确认：要固定。** 每篇 Brief 动笔前内部 2 条攻击（X1–X12 或 §D），落盘 `content/xiaohongshu/redteam/<slug>-pre.md`；Owner 不参与。  
**SOP：** [BRIEF-REDTEAM-PRE.md](../xiaohongshu/BRIEF-REDTEAM-PRE.md) · [AUTO-WORKFLOW 步 1c](../../agents/00-manager/AUTO-WORKFLOW.md)