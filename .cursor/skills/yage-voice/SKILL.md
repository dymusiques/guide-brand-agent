---
context_version: "2026-11-14"
repo_path: ".cursor/skills/yage-voice/SKILL.md"
goal: "yage-voice · Danying 去 AI（锚点优先）"
openwebui_route: "rag_l2"
cursor_route: "read"
content_sha256: "0d14bc2603667768"
---

# yage-voice（Danying · 去 AI 腔）

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** **Must read in order:** [`VOICE-ANCHOR.md`](../../../content/xiaohongshu/VOICE-ANCHOR.md) → [`skill_yage_voice.md`](../../../rules/skills/skill_yage_voice.md) → [`skill_yage_voice-danying.overlay.md`](../../../rules/skills/overlays/skill_yage_voice-danying.overlay.md)
- **Path:** `.cursor/skills/yage-voice/SKILL.md`
- **Open WebUI:** `rag_l2`
- **Cursor:** `read`

---

## L2 正文

# yage-voice（Danying · 去 AI 腔）

**Must read in order:**

1. [`content/xiaohongshu/VOICE-ANCHOR.md`](../../../content/xiaohongshu/VOICE-ANCHOR.md) — **张丹瀛** 真人口吻（标题模式 · 会说/不会说 · 口播原话）  
2. [`rules/skills/skill_yage_voice.md`](../../../rules/skills/skill_yage_voice.md) — 去 AI 句式卫生  
3. [`rules/skills/overlays/skill_yage_voice-danying.overlay.md`](../../../rules/skills/overlays/skill_yage_voice-danying.overlay.md) — 体裁表 · North Star · 平台分工

**Do not** apply鸭哥/工程师人格 to any `content/xiaohongshu/*-brief.md` classifier bodies or CAPSTONE Pitch 定稿.

**Must apply** (with anchor) to:

- 口播文案 · Owner 长稿 `content/xiaohongshu/drafts/*-longform.md` — [`OWNER-LONGFORM-DE-AI-VOICE.md`](../../../docs/OWNER-LONGFORM-DE-AI-VOICE.md) + [`VOICE-ANCHOR.md`](../../../content/xiaohongshu/VOICE-ANCHOR.md)  
- 多通道草稿 — 按 overlay 体裁表 + platform-voice handoff

**Clever 反方席：** ≥4 个 `**反方·…**` → [`OWNER-LONGFORM-CLEVER-ADVOCATE.md`](../../../docs/OWNER-LONGFORM-CLEVER-ADVOCATE.md) · `verify-xhs-clever-advocate.sh`.