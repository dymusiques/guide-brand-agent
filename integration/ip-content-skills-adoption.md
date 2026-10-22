# 集成 · IP 内容工具链（grapeot skills · Owner 2026-10-22 全装）

> **纪律：** 本仓 **已 vendor** 下列 submodule；**默认不跑 CLI**（不替代 00 Manager 小红书主链）。  
> **触发条件表 = 何时才值得动用**；「已安装 ≠ 每次会话都要用」。  
> **真相源：** 小红书 Brief / 口播 → `content/xiaohongshu/` · `VOICE-ANCHOR.md` · `owner-source-*`。

---

## 0. 「anchor 满 10 再 ASR」是什么意思？

**Anchor（声音锚）** 在本仓指 [`content/xiaohongshu/voice-anchor-sources.json`](../content/xiaohongshu/voice-anchor-sources.json) 里登记的 **已发或定稿故事帖**，每条至少含：

- **标题**（你账号验证过的语气）
- **口播开头 ~80 字** 和/或 **全文**（见 `voice-anchor-transcripts-*.md`）

**「满 10」** = JSON 里 `anchor_count` **≥ 10**，且多数条目为 `caption_status: owner_transcript`（有可靠口播文本，不是 Agent 猜的）。

**为什么和 ASR 绑在一起：**

- 你小红书 **描述区常空**，历史口播不在 App 正文里；ASR 用来 **从视频/录音反推文稿**，补 anchor、做检索、对齐 L2 禁词。
- 锚点 **少**（例如现在 **5 条**）时：仍可对 **单条新片** 跑 ASR（Insta360、一条待发稿）；**不建议** 批量爬全账号做 embedding/训练——样本太少、性价比低。
- 锚点 **≥10** 后：值得 **批量 ASR + 写入 transcripts**、开 **semantic-search 索引**、用 **voice-lora-detect** 做全库 AI 腔扫描。

**当前计数（机器可读）：** `voice-anchor-sources.json` → `anchor_count`（2026-10-21 为 **5**）。

---

## 1. 触发条件总表

| Skill | Vendor | 何时启用（触发） | 何时 **不要** 用 | 本仓 overlay |
|-------|--------|------------------|------------------|--------------|
| **semantic-search** | `vendor/semantic-search-skill/` | 写 Round 2+ 前要在 **自己的** anchor/transcripts/packages 里找相似原话；或 anchor ≥10 后建索引 | 只有 1–2 篇稿、还没落盘 owner-source | `semantic-search.local.md`（endpoint、index 路径） |
| **voice-lora-detect** | `vendor/voice-lora/` | 非 Brief 长文 / B 站简介 / 外稿定稿前 **扫 AI 腔**；与 `verify-xhs-voice-qa.sh` 互补 | **小红书 Brief 正文/evaluate 输出**（仍用 L2 lint + Owner 选稿） | `voice-lora.local.md` |
| **voice-lora-rewrite** | 同上 | Owner 明确「润色这篇外稿、保事实」 | Brief、Pitch、aligned 定稿 | 同上 |
| **bilibili-upload** | `vendor/bilibili-upload-skill/` | 有 **导出成片** + B 站文案/封面 ready；Owner 在场 **dry-run → execute 到投稿前** | 只有小红书标题、无视频文件；无人值守发布 | `bilibili-upload.local.md` |
| **asr** | `vendor/asr-skill/` | **单条** 新视频/录音要文稿；或 anchor≥10 后 **批量** 补历史口播 | macOS/MLX 前置未满足；无 Owner 复核的「自动改 Brief」 | `asr-skill.local.md` |
| **online-media** | `vendor/online-media-skill/` | 听见 Daily / 外链媒体 **下载+转写+双语 SRT**（非 XHS Brief） | 纯小红书口播包（无 URL 源） | `online-media.local.md` |
| **voice-memos** | `vendor/voice-memos-skill/` | 从 **Apple 语音备忘录** 导出 m4a → intake/ASR | 已用小红书 App 直录、无 Voice Memos | — |
| **intake** | `vendor/intake-skill/` | Owner 口述故事 **进 Git**：`content/xiaohongshu/owner-source-*.md` | 已有结构化 owner-source，只需改 Brief | `intake-skill.local.md` |
| **ai_session_export** | `vendor/ai_session_export/` | 复盘 **哪种派活/迭代有效**；归档 Cursor 会话 | 日常写 Brief（不必每轮 export） | `ai-session-export.local.md` |
| **vlog** | `vendor/vlog-skill/` | HeyGen 数字人 + 地图字幕 **重讲解片**（≥8min 规划） | 手机/Insta360 **真人一条过** 主路径 | `vlog-skill.local.md` |
| **opus-video-audio** | `vendor/opus-video-audio-skill/` | Insta360 实拍需要 **片头/B-roll/动效包装** | 替代口播内容或小红书 Round1 写稿 | — |
| **playwright-test** | `vendor/playwright-test-skill/` | 调试 **bilibili fill** / XHS Playwright 脚本 step-by-step | 一般内容写作 | — |
| **typefully-twitter** | `vendor/typefully-twitter-skill/` | IG/X 与听见 **英文帖** 走 Typefully 排期 | 小红书 | `typefully-twitter.local.md` |
| **dataforseo** | `vendor/dataforseo-skill/` | **关键词/SERP** 调研补充 Drive PDF | 替代 Owner Excel 选题表 | `dataforseo.local.md` |

---

## 2. 推荐启用顺序（时间线）

1. **现在（anchor=5）：** semantic-search **手工 grep + transcripts** 即可；voice-lora-**detect** 试跑外稿/B站简介；intake + voice-memos 随时收 **新故事**；单条 ASR 按需。  
2. **A→B→C→E 连发后：** 每发一条 **更新 anchor JSON + transcripts**；到 **10 条** 再 **批量 ASR + semantic index**。  
3. **第一条 Insta360 + B 站：** bilibili dry-run fill；仍 **Owner 点投稿**。  
4. **重制作：** vlog/opus **二选一试点**，scratch 在 `content/video/` 或 `tmp/video/`。

---

## 3. 与 00 Manager 分工

| 步 | 仍走原链 | 可加工具链 |
|----|----------|------------|
| 2a 视频迭代 / Round1–3 | `XHS-VIDEO-ITERATION.md` | semantic-search 查 anchor |
| Brief 定稿 / evaluate | 04 + kernel | **不用** voice-lora-rewrite 盖 Brief |
| B 站 / Insta360 | 本文件 §1 | bilibili · asr · opus/vlog |
| 听见 / 外链 | `danying-tingjian-daily` | online-media |

---

## 4. 安装与 pip（已完成 submodule）

```bash
git submodule update --init --recursive
# 按需（见各 vendor README / SETUP.md §2 optional）：
# pip install -e vendor/semantic-search-skill
# pip install -e vendor/bilibili-upload-skill
# …
```

**验收（装完 submodule 后）：**

```bash
bash scripts/verify-handoff.sh
# 首次 bilibili：dry-run only，见 integration/bilibili-inst360-channel-adoption.md
```

---

## 5. Discovery 入口

每个 repo **一个** router：`rules/skills/skill_<name>.md` → vendor root skill（见 [WORKSPACE.md](../rules/WORKSPACE.md) 表）。
