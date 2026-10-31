---
context_version: "2026-10-30-l012"
repo_path: "docs/OWNER-LONGFORM-DE-AI-VOICE.md"
goal: "Owner 长稿 · 去 AI 味 · 网红感 · 感想优先（Must · 2026-10-30）"
openwebui_route: "rag_l1"
cursor_route: "read"
content_sha256: "98b3580ca3c7af82"
---

# Owner 长稿 · 去 AI 味 · 网红感 · 感想优先（Must · 2026-10-30）

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** > **长稿**（`drafts/*-longform.md`）= Owner 要读要发的正文，**不是** classifier JSON。  
> **Must** 在定稿前走本 SOP + [`rules/skills/skill_yage_voice.md`](../rules/skills/skill_yage_voice.md) + [`cont
- **Path:** `docs/OWNER-LONGFORM-DE-AI-VOICE.md`
- **Open WebUI:** `rag_l1`
- **Cursor:** `read`

## 章节锚点
- **1. 比例（硬规则）**: | 类型 | 上限 |
- **2. 语气（网红感 · 张丹瀛 IP · 去 AI）**: - 读 [`VOICE-ANCHOR.md`](../content/xiaohongshu/VOICE-ANCHOR.md) 标题模式：**事件+情绪 · 原来… · 被…后我… · A但不B**
- **3. Agent 流程（写/改长稿 Must）**: 1. 初稿（感想为主）
- **4. 规则锚点**: - [`.cursor/rules/danying-manager-auto.mdc`](../.cursor/rules/danying-manager-auto.mdc) · 1b 长稿


---

## L2 正文

# Owner 长稿 · 去 AI 味 · 网红感 · 感想优先（Must · 2026-10-30）

> **长稿**（`drafts/*-longform.md`）= Owner 要读要发的正文，**不是** classifier JSON。  
> **Must** 在定稿前走本 SOP + [`rules/skills/skill_yage_voice.md`](../rules/skills/skill_yage_voice.md) + [`content/xiaohongshu/VOICE-ANCHOR.md`](../content/xiaohongshu/VOICE-ANCHOR.md)。

## 1. 比例（硬规则）

| 类型 | 上限 |
|------|------|
| **第一人称感想 / 现场 / 情绪 / 判断** | **≥60%** 篇幅 |
| **引用、报告、链接、案例「事实锚点」** | **≤15%** · **全部挪到 Brief `## 依据与引用`**，正文最多 **口语提一嘴**（如「郎朗接 Dior 那事」） |
| **清单/表格/小标题堆叠** | 能省则省；表格 **≤1 个** |

## 2. 语气（网红感 · 张丹瀛 IP · 去 AI）

- 读 [`VOICE-ANCHOR.md`](../content/xiaohongshu/VOICE-ANCHOR.md) 标题模式：**事件+情绪 · 原来… · 被…后我… · A但不B**  
- 读 **鸭哥去 AI**：[`skill_yage_voice.md`](../rules/skills/skill_yage_voice.md) — 短句、先结论、少「首先/此外/综上所述」、禁赋能闭环体  
- **像刷到的一个真人**：可以吐槽、可以自黑、可以「我当时愣了」— **禁止** 论文综述腔  
- **禁：** 一段里连续 3 个括号出处 · 英文术语堆叠 · 「据 XX 报告」开头段落

## 3. Agent 流程（写/改长稿 Must）

1. 初稿（感想为主）  
2. **Clever 反方席：** ≥4 个 `**反方·网红人设**` 杠主观点 → 「收进包里」收束 — [OWNER-LONGFORM-CLEVER-ADVOCATE.md](./OWNER-LONGFORM-CLEVER-ADVOCATE.md)  
3. **自检 AI 腔：** 删引用块 → 改口语 → 加 2–3 处 **只有你能写的细节**（场子、气、人）  
4. 可选：`voice-lora-detect` / `voice-lora-rewrite`（非 Brief · 见 skill_yage_voice）  
5. `verify-xhs-voice-qa.sh` · **`verify-xhs-clever-advocate.sh --brief …`**  
6. 再跑 evolution / multichannel HTML

## 4. 规则锚点

- [`.cursor/rules/danying-manager-auto.mdc`](../.cursor/rules/danying-manager-auto.mdc) · 1b 长稿  
- [`OWNER-LONGFORM-XHS-SPEC.md`](../content/xiaohongshu/OWNER-LONGFORM-XHS-SPEC.md)  
- [`agents/04-xhs-topic-manager/INTEGRATION-PROMPT.md`](../agents/04-xhs-topic-manager/INTEGRATION-PROMPT.md)