---
context_version: "2026-11-14"
repo_path: "rules/skills/overlays/skill_yage_voice-danying.overlay.md"
goal: "Danying · 去 AI 腔与人格叠加（真源 VOICE-ANCHOR · 非鸭哥人格）"
openwebui_route: "rag_l1"
cursor_route: "read"
---

# Danying overlay · 去 AI 腔 × 张丹瀛 IP

> **人格真源（禁止本 overlay 覆盖）：** [`content/xiaohongshu/VOICE-ANCHOR.md`](../../../content/xiaohongshu/VOICE-ANCHOR.md) · [`voice-anchor-sources.json`](../../../content/xiaohongshu/voice-anchor-sources.json) · [`voice-anchor-transcripts-2026-10-21.md`](../../../content/xiaohongshu/voice-anchor-transcripts-2026-10-21.md)  
> **本文件管什么：** 叠用顺序、体裁表、North Star、禁词与平台分工。  
> **方法来源（footnote）：** grapeot [voice-lora](https://github.com/grapeot/voice-lora) · 鸭哥 / yage.ai **句式卫生** — **不是** 默认口吻。

## North Star（与 IP Brief 对齐 · 写稿自检一句）

帮**家长与孩子**在「走不走专业」之外，仍看见**标准长什么样、会不会照镜子、家长能不能在场**；祛魅大师与赛道 myth，**张丹瀛本人即品牌**（`G-PERSON-IS-BRAND`）。  
每篇口播/长文至少有一句判断与此 **不冲突**。详见 [`content/personal-ip/ip-positioning-brief-2026-10-05.md`](../../../content/personal-ip/ip-positioning-brief-2026-10-05.md)。

## 叠用顺序（Agent Must · 写/改 Owner 对外正文前）

| 步 | 读什么 | 目的 |
|----|--------|------|
| 1 | **VOICE-ANCHOR** + 锚点 JSON 里 1–2 条 `first_80_chars` | 像不像**你** |
| 2 | [`skill_yage_voice.md`](../skill_yage_voice.md) 口吻要点 | 去 AI / 少套话 |
| 3 | 若已定选题：[`OWNER-LONGFORM-DE-AI-VOICE.md`](../../../docs/OWNER-LONGFORM-DE-AI-VOICE.md) 比例 | 长稿感想≥60% |
| 4 | 若三平台：handoff `owner-platform-voice-benchmark-latest.json` | **只学节奏**，不学 KOL 人设 |
| 5 | Brief / evaluate classifier body | **只用 1–2** · 不用鸭哥工程师体 |

## 体裁表（篇幅 · 锚点 · 对标）

| 体裁 | VOICE-ANCHOR | 去 AI（yage 要点） | 大V笔触 | 篇幅真源 |
|------|:------------:|:------------------:|:-------:|----------|
| 小红书口播 60–90s | **Must** | Must | 小红书轴（问句封面·一条一判断） | Brief / 视频轨 · 无 yage 字数 |
| 小红书长稿 `drafts/*-longform.md` | **Must** | Must | 可选 | **3000–5000 字** · `OWNER-LONGFORM-XHS-SPEC.md` |
| LinkedIn 帖 | 语气 Must | Must | stakes + 短行 · 禁海报体 | `OWNER-MULTICHANNEL-LINKEDIN-IMAGE-DELIVERABLE.md` |
| Medium 长文 | 场景 Must | Must | process / 场景开场 | 约 800–1200 词（英文主）或多通道 MD |
| Brief / Pitch / aligned 定稿 | IP + CAPSTONE | 仅删套话 | ❌ | evaluate 规范 |
| Agent 给 Owner 解释 workflow | 可弱化 | ✅ 最适合 yage 句式 | ❌ | 无 |

## 张丹瀛 · 我会说 / 叠加（摘自 VOICE-ANCHOR · Agent 可复用）

| ✅ 优先 | ❌ 避免 |
|---------|---------|
| 祛魅、契约式、光环、真实经历、「我跟大家分享」 | 装饰型艺术、赋能闭环、深度洞察、首先其次此外综上所述 |
| 法派、台下、标准、照镜子、家长在场 | 虚构「上周有人问我」访谈开场 |
| 事件+情绪标题弧（泰斗发火 / 原来也有剧本） | 把鸭哥工程博客腔当整篇人设 |
| 直接、不藏着掖着 | 论文综述 · 一段三括号出处 |

**口播开头：** 优先对齐锚点里 **Owner 原话** 结构；Agent **不得**润色 transcript 存档字段。

## 不要从鸭哥默认学来的东西

- 冷淡工程师独白 → 你有高互动**情绪与现场**  
- 结论先行到底 → 你可先**经历后判断**（见锚点口播）  
- 长论证体 → 口播是**短段+判断**  
- 用本 overlay 覆盖 Brief classifier 正文 → **禁止**

## 验收（CEO 长稿轨 · Cursor 写稿后）

| 脚本 / 文档 | 何时 |
|-------------|------|
| `verify-xhs-voice-qa.sh` | 小红书声音 QA |
| `verify-xhs-clever-advocate.sh` | 长稿 ≥4 反方 |
| `OWNER-LONGFORM-DE-AI-VOICE.md` 比例自检 | 长稿定稿前 |
| `verify-owner-copy-v-tier-attestation.py` | brief 绑 V-Tier 时 |

## 路由

| 键 | 路径 |
|----|------|
| 主 skill | `rules/skills/skill_yage_voice.md` |
| 平台对标 roster | `integration/handoff/platform-voice-benchmark-roster.json` |
| research-gate 写稿链 | monorepo `AGENT-OWNER-COPY-PIPELINE-GATE.json` |
| CEO 新篇 autopilot | `docs/CEO-XHS-NEW-BRIEF-AUTOPILOT.md` |