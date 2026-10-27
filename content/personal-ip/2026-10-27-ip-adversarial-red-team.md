# IP 对抗性红队 · 全 Agent 动员（2026-10-27）

> **用途：** Owner 要求「先定正确方向，再用行业常见坑 + 本仓 SOP/函数壳做**高挑战对抗**」——让 00–09、kernel、verify **都有明确攻击面**，而不是只写鸡汤 checklist。  
> **真相源：** [ip-positioning-brief-2026-10-05.md](./ip-positioning-brief-2026-10-05.md) · [integration/IMPORTANT.md](../../integration/IMPORTANT.md) · [GOALS-REGISTRY.md](../../integration/GOALS-REGISTRY.md)  
> **外部参考（非 Tier-1 事实）：** 人人都是产品经理 IP 误区文 · 杨天真「定位+内容+产业」· PBL/Forbes 一致性论述 · 见文末链接。

---

## A. 正确方向（North Star · CEO 锁定 · 对抗的靶心）

**一句话（不可删改对抗）：**  
法派长笛传承 × 跨界品牌策划 —— 帮 **跨行业** 品牌/艺术家/教育/AI 创新者，把 **不可替代的古典审美与叙事** 变成 **可合作、可传播、可沉淀** 的语言；**人即品牌**，不是单栏目。

**认知期（2026 Q4）当前战役，不是终身定位：**

| 维度 | 对 | 错（红队最爱打你这里） |
|------|----|------------------------|
| 受众 | 品牌市场/文化合作岗（多行业） | 把约课私信当 KPI 胜利 |
| 内容 | 每周 1 深度：你是谁、能帮品牌什么；Daily 分层 | 每条都要转化、每条都 Pitch |
| 信号 | 品牌向私信「聊聊/合作/品牌」；收藏 + 判断帖 | 粉丝数、爆款、✅技巧流量 |
| 边界 | 案例可写具体行业；**人设层**不绑垂直 | 系列默认家居/建材/某品类 |
| 产品 | 先信任与强链接；CAPSTONE 产品 **后** | 体验季、大单、campaign 表 |

**三支柱（内容分配对抗尺）：** ① 艺术专业高度 ② 跨界品牌策划 ③ AI×数字藏品（文案禁 Web3/NFT 字样）

---

## B. 错误分级 · 为何「很难被自动纠正」

| 级别 | 含义 | 本仓谁管 | 典型例子 |
|------|------|----------|----------|
| **L1** | 脚本/规则能拦 | 05 kernel · L2 lint · evaluate | consultant 腔、单品类 Brief 句 |
| **L2** | verify PASS 仍跑偏 | 09 口径 · 01 战略 · Owner 眼 | aligned 但标题筛错人；约课填进 dm_count |
| **L3** | 人性/时间/环境 | **仅 Owner** | 审美要慢、怕争议、多平台分散、AI 浅用 |

**红队原则：** 专门打 **L2–L3**；L1 交给现有 `evaluate` + Manager's Loop。

---

## C. 行业常见坑（浓缩 · 用来武装各 Agent）

1. **账号 ≠ IP**（有号、有爆款 ≠ 被需要 5–10 年）  
2. **日更勤奋 ≠ 被看见**（无结构、无定位）  
3. **教导感 / 成功人士口吻**（杨天真：受众有压力）  
4. **定位+内容 无产业/交付支点**（只有流量变现）  
5. **贪多求全、追热点**（支柱失焦）  
6. **AI 代写 / 代经营**（判力下降、假事实）  
7. **从他人心中出发**（讨好算法而非真我）  
8. **工具先行无策略**（Drive/多平台/verify 绿但无人记得你是谁）  
9. **定位漂移 / 年度 rebranding**（12–18 个月无法建立「推荐你解决 X」）  
10. ** vanity 粉丝 ≠ 商业强链接**

---

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

---

## E. 十项「高难度对抗演练」（Owner 每月可选 2 项）

| # | 演练名 | 红队出招 | 你必须交付的反击 |
|---|--------|----------|------------------|
| 1 | **电梯 Pitch 劫机** | 01+02：8 秒内只能讲 **一个** 受众 + **一个** 结果 | 录音 30s，写入 ip-positioning-brief 脚注 |
| 2 | **约课陷阱** | 09：用约课私信证明强链接 | 按 signal-baseline 重填 CSV 口径说明 |
| 3 | **aligned 幻觉** | 05+04：故意写一篇「对齐但无聊」Brief | 人审 + 2a 口播，否者重写 |
| 4 | **垂类绑定** | 01+03：连发 3 篇都带同一行业案例 | 第三篇必须 **纯方法论零行业名** |
| 5 | **教导感刑场** | 03：杨天真式 — 「成功人士教训我」 | 改第一人称故事 + 判断，删「你应该」 |
| 6 | **AI 浅层镜像** | 01+04：把 Brief 改得像豆包教程体 | 对照篇 E「浅层使用」自删 30% |
| 7 | **工具箱越狱** | 00+08：不走 04 直接用 writing-skill 出 Brief | 必须走 evaluate；writing 只 memo |
| 8 | **数据绑架** | 09：用一条 23 年旧帖否定 pivot | 写 3 行「历史帖 vs 当前战役」 |
| 9 | **视觉分裂** | 07：封面与口播主题不一致 | brand-check 或人工对照表 |
| 10 | **发布幽灵** | CEO：aligned  Brief >4 篇 **发布状态仍待发** | 选 1 篇发布或删队列 |

---

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

---

## G. 外部链接（调研 · 非自动真理）

- [打造个人IP的8大误区](https://www.woshipm.com/share/6174332.html)  
- [行走的解决方案 · 定位精准](https://www.woshipm.com/share/6202672.html)  
- [杨天真 · 定位+内容+产业](https://news.qq.com/rain/a/20250421A05WSV00)  
- [个人品牌10误解 · 真诚/AI](https://www.ipibresume.com/blog/blog/8-most-misunderstood-concept-on-personal-branding/)  
- [PBL · 10 mistakes foundation](https://resources.personalbrandlab.co/resource/blog/personal-branding-mistakes)  
- [Forbes · rebranding too much](https://www.forbes.com/sites/rhettpower/2025/03/09/how-much-personal-rebranding-is-too-much-the-case-for-consistency/)

---

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

---

## I. 极高隐蔽坑 · X1–X12（2026-10-27 外部补强）

与 [FULL-DRILL-REPORT §2](./2026-10-27-ip-adversarial-FULL-DRILL-REPORT.md#2--高挑战错误库本轮新增--含外部调研) 同步：活动先于目标、头衔当定位、证据错配、跨信号分裂、借 visible 口吻、AI 代写、季度换 niche、平台即全部、attention 无 recognition、弱 claim、aligned 幻觉、CEO 发布 ghost。

**对抗原则：** 这些 **不** 要求 Owner 公式化输入；CEO 派 GM 内化，**内部 Gate + 红队** 拦截。

---

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

---

## K. 与 Owner 输入原则

红队/对抗 **不提高** Owner 门槛：[OWNER-INPUT-PRINCIPLES.md](../../docs/OWNER-INPUT-PRINCIPLES.md) — 你说「全员对抗测一遍」即可，CEO 内化 §F/J。

---

## L. Owner 固定 · Brief 前红队 2 条/篇（2026-10-27）

**Owner 确认：要固定。** 每篇 Brief 动笔前内部 2 条攻击（X1–X12 或 §D），落盘 `content/xiaohongshu/redteam/<slug>-pre.md`；Owner 不参与。  
**SOP：** [BRIEF-REDTEAM-PRE.md](../xiaohongshu/BRIEF-REDTEAM-PRE.md) · [AUTO-WORKFLOW 步 1c](../../agents/00-manager/AUTO-WORKFLOW.md)
