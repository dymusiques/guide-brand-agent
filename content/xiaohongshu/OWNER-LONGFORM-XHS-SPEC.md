---
context_version: "2026-10-30-l012"
repo_path: "content/xiaohongshu/OWNER-LONGFORM-XHS-SPEC.md"
goal: "Owner · 小红书长稿规范（Must · 2026-10-30）"
openwebui_route: "intake_l2"
cursor_route: "read"
content_sha256: "d021f55d435875b0"
---

# Owner · 小红书长稿规范（Must · 2026-10-30）

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** > **适用范围：** Owner 指定的新篇、CEO 派 04 写的 **所有** 待发布小红书文案（Discovery / 测试稿 / 单篇主题）。  
> **短 classifier JSON** 仍供 gate；**Owner 真正要读、要发的**是长稿。
- **Path:** `content/xiaohongshu/OWNER-LONGFORM-XHS-SPEC.md`
- **Open WebUI:** `intake_l2`
- **Cursor:** `read`

## 章节锚点
- **1. 字数与结构**: | 项 | Must |
- **2. 风格（Owner 固定）**: - **吸睛 · 有趣 · 幽默 · 犀利 · 浅显易懂**（大众读得懂，少圈内黑话；必要术语一句人话解释）
- **3. 网络检索（Must · Agent API / WebSearch）**: 写 v0 前 **Must**：
- **4. 进化闭环**: - `analyze-brief-evolution-gap.py` 会检查 **长稿字数**（不足 3000 或超过 5500 → **NEEDS_WORK**）
- **5. Intake（Owner 原话）**: 模板：`content/evolution/_template/intake/OWNER-XHS-TASK-intake.md`


---

## L2 正文

# Owner · 小红书长稿规范（Must · 2026-10-30）

> **适用范围：** Owner 指定的新篇、CEO 派 04 写的 **所有** 待发布小红书文案（Discovery / 测试稿 / 单篇主题）。  
> **短 classifier JSON** 仍供 gate；**Owner 真正要读、要发的**是长稿。

## 1. 字数与结构

| 项 | Must |
|----|------|
| **长稿字数** | **3000–5000 汉字**（含标点；不含标签行）· **Owner 商业深度版** 可至 **7000**（含「商业课 + 可拍案例」节） |
| **落盘位置** | Brief 内 `## 正文（长稿 · Owner 发布版）` **或** `content/xiaohongshu/drafts/<slug>-longform.md` + Brief 内链接 |
| **classifier `body`** | **≤600 字** 摘要：钩子 + 三镜头锚点 + CTA（供 evaluate / 列表预览） |
| **标题** | ≤20 字（见 [OWNER-CONTENT-SPEC.md](./OWNER-CONTENT-SPEC.md)） |
| **标签** | 10 个 `#` |

## 2. 风格（Owner 固定）

- **吸睛 · 有趣 · 幽默 · 犀利 · 浅显易懂**（大众读得懂，少圈内黑话；必要术语一句人话解释）  
- **禁止** 正确但空洞的鸡汤、堆砌「高端/赋能/专业信任」禁词（见 04 INTEGRATION · voice QA）  
- **Must 有三镜头**（谁怎么做 / 被忽略什么 / 反常规 + trade-off）——见 [BRIEF-THREE-LENS-SOP.md](./BRIEF-THREE-LENS-SOP.md)  
- **Must 有具体案例轴**（本 IP 默认：NGV×Cartier×MSO / 百富 Frieze / RCM 等同系列语言可复用）  
- **去 AI 味 · 感想优先（Must · Owner 2026-10-30）：** 全文按 [docs/OWNER-LONGFORM-DE-AI-VOICE.md](../docs/OWNER-LONGFORM-DE-AI-VOICE.md) — **第一人称感想 ≥60%** · 正文 **禁** URL/报告堆砌 · 检索进 Brief `## 依据与引用` · 定稿前读 [`rules/skills/skill_yage_voice.md`](../rules/skills/skill_yage_voice.md) + [VOICE-ANCHOR.md](./VOICE-ANCHOR.md)（网红口语 · 短句 · 有判断）  
- **Clever 多立场反驳（Must）：** [docs/OWNER-LONGFORM-CLEVER-ADVOCATE.md](../docs/OWNER-LONGFORM-CLEVER-ADVOCATE.md) — **≥4 反方人设** 刁钻杠主观点 + 作者收束 · CEO evaluate / triple-eval / double-stress 门：`verify-xhs-clever-advocate.sh`

## 3. 网络检索（Must · Agent API / WebSearch）

写 v0 前 **Must**：

1. 更新 `research/<slug>-pitfalls.md`（≥3 条可核对来源 · 见 [BRIEF-PITFALLS-RESEARCH-SOP.md](./BRIEF-PITFALLS-RESEARCH-SOP.md)）  
2. 长稿 **口语化用** 检索结论（**≥2 处** 观点/事实），**不**在正文贴链接块；URL **只**进 Brief `## 依据与引用`  
3. Brief `## 依据与引用` 列出 URL + **一句** Agent 如何化进正文（感想/案例，非综述）  

## 4. 进化闭环

- `analyze-brief-evolution-gap.py` 会检查 **长稿字数**（不足 3000 或超过 5500 → **NEEDS_WORK**）  
- HTML 弹出层 **优先展示长稿全文**（`build-owner-xhs-report-html.py`）

## 5. Intake（Owner 原话）

模板：`content/evolution/_template/intake/OWNER-XHS-TASK-intake.md`  
每篇 Must 有 `content/evolution/04-xhs-topic-manager/<slug>/intake/` 记录 Owner 主题 + 本规范引用。