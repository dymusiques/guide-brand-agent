---
context_version: "2026-10-30-l012"
repo_path: ".cursor/skills/yage-voice/SKILL.md"
goal: "yage-voice"
openwebui_route: "rag_l2"
cursor_route: "read"
content_sha256: "0d14bc2603667768"
---

# yage-voice

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** Read and follow [rules/skills/skill_yage_voice.md](../../../rules/skills/skill_yage_voice.md).
- **Path:** `.cursor/skills/yage-voice/SKILL.md`
- **Open WebUI:** `rag_l2`
- **Cursor:** `read`


---

## L2 正文

# yage-voice

Read and follow [rules/skills/skill_yage_voice.md](../../../rules/skills/skill_yage_voice.md).

**Do not** apply to `content/xiaohongshu/*-brief.md` classifier bodies or CAPSTONE Pitch 定稿.

**Must apply** to Owner 长稿 `content/xiaohongshu/drafts/*-longform.md` per [docs/OWNER-LONGFORM-DE-AI-VOICE.md](../../../docs/OWNER-LONGFORM-DE-AI-VOICE.md) (+ [VOICE-ANCHOR.md](../../../content/xiaohongshu/VOICE-ANCHOR.md) 网红/IP 口语).

**Clever 反方席：** ≥4 个 `**反方·…**` 杠主观点 → 收束 — [docs/OWNER-LONGFORM-CLEVER-ADVOCATE.md](../../../docs/OWNER-LONGFORM-CLEVER-ADVOCATE.md) · CEO evaluate/压测 `verify-xhs-clever-advocate.sh`.