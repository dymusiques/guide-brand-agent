---
context_version: "2026-11-14"
repo_path: "rules/skills/skill_yage_voice.md"
goal: "Danying · 去 AI 腔（人格=VOICE-ANCHOR · 方法源自 yage 句式）"
openwebui_route: "rag_l1"
cursor_route: "read"
content_sha256: "eeaa25390cc03cff"
---

# Skill · Danying 去 AI 腔（叠加 VOICE-ANCHOR）

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** **人格真源 = 张丹瀛 VOICE-ANCHOR**；本 skill = **句式卫生**（短句、有判断、去 AI 套话）。方法参考鸭哥/yage.ai · [voice-lora](https://github.com/grapeot/voice-lora)。**Owner overlay Must：** [`overlays/skill_yage_voice-danying.overlay.md`](./overlays/skill_yage_voice-danying.overlay.md)
- **Path:** `rules/skills/skill_yage_voice.md`
- **Open WebUI:** `rag_l1`
- **Cursor:** `read`

## 章节锚点
- **何时用**: | 场景 | 读本 skill？ |
- **叠用顺序**: overlay 表 · 先锚点后去 AI
- **口吻要点（Agent 直接写时）**: 短句、有判断；少综述腔
- **若本机已装 voice-lora（可选）**
- **路由**

---

## L2 正文

# Skill · Danying 去 AI 腔（叠加 VOICE-ANCHOR）

> **人格真源（Must 先读）：** [`content/xiaohongshu/VOICE-ANCHOR.md`](../../content/xiaohongshu/VOICE-ANCHOR.md)  
> **Owner 体裁 / North Star / 平台表：** [`overlays/skill_yage_voice-danying.overlay.md`](./overlays/skill_yage_voice-danying.overlay.md)  
> **方法来源（footnote）：** 鸭哥 / yage.ai 中文工程博客 · voice-lora — **仅** 去 AI，**不** 默认工程师人格。  
> **边界：** 小红书 **Brief / classifier JSON / Pitch 定稿** = **张丹瀛 IP + CAPSTONE + evaluate**；本 skill **不** 覆盖 Brief 正文气质。

## 何时用

| 场景 | 读本 skill + overlay？ |
|------|------------------------|
| 小红书 **口播文案**、**Owner 长稿** `drafts/*-longform.md` | ✅ **Must**（先 VOICE-ANCHOR，再本 skill，见 overlay 叠用顺序） |
| LinkedIn / Medium（多通道） | ✅ Must 去 AI；人设仍 VOICE-ANCHOR；节奏见 platform-voice handoff |
| 向 Owner **解释** 选题、workflow、测试结果 | ✅ |
| 小红书 **Brief 正文**、**evaluate 用的 body** | ❌（保持 Danying 品牌 + CAPSTONE；仅可删套话） |
| 实验稿 / memo / 内部说明 | ✅ 可选 |
| 已装 **voice-lora-rewrite** CLI | ✅ 对 **非 Brief** 段落；未安装 **禁止** 假装跑过 |

## 叠用顺序（摘要 · 全文在 overlay）

1. **VOICE-ANCHOR** + `voice-anchor-sources.json`（口播开头勿润色）  
2. **本 skill** 口吻要点  
3. 长稿：**OWNER-LONGFORM-DE-AI-VOICE**（感想≥60%）  
4. 三平台：**owner-platform-voice-benchmark-latest.json**（只学笔触，不抄人设）

## 口吻要点（Agent 直接写时）

- **短句、有判断**：可「经历→判断」或「判断→一句为什么」；少「首先其次此外综上所述」。  
- **少空洞形容词**：不用「赋能、抓手、闭环、深度洞察」堆满屏。  
- **像跟人说话**：可用「你」「我们」；避免公文腔和营销腔。  
- **专业场域说人话**：法派、台下、标准、家长在场 — 术语该用则用。  
- **不像 AI**：禁止一段内连续括号出处；报告事实进 Brief `## 依据与引用`。

## 若本机已装 voice-lora（可选）

```bash
voice-lora-detect path/to.md
voice-lora-rewrite path/to.md -o path/to.out.md
```

未安装时 **不要** 假装跑过 rewrite；按口吻要点 + overlay 自检即可。

## 路由

| 任务 | 读什么 |
|------|--------|
| Owner overlay（体裁·North Star） | `rules/skills/overlays/skill_yage_voice-danying.overlay.md` |
| 长稿 SOP | `docs/OWNER-LONGFORM-DE-AI-VOICE.md` · `content/xiaohongshu/OWNER-LONGFORM-XHS-SPEC.md` |
| 写作总规范（非 Brief） | `rules/skills/skill_writing.md` |
| 小红书定稿 / evaluate | `agents/04-xhs-topic-manager/` · **不用** 本 skill 覆盖 Brief |
| 平台大V对标 | `integration/handoff/platform-voice-benchmark-roster.json` |