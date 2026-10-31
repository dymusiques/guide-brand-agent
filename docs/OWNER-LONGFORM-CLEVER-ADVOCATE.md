---
context_version: "2026-10-30-l012"
repo_path: "docs/OWNER-LONGFORM-CLEVER-ADVOCATE.md"
goal: "Owner 长稿 · Clever 多立场反驳（Must · 2026-10-30）"
openwebui_route: "rag_l1"
cursor_route: "read"
content_sha256: "255da7f2fc5cc329"
---

# Owner 长稿 · Clever 多立场反驳（Must · 2026-10-30）

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** > **Clever** = 刁钻、有趣、像不同网红在评论区杠你——不是论文反证，是**有脸有立场**的 against。  
> 与 [OWNER-LONGFORM-DE-AI-VOICE.md](./OWNER-LONGFORM-DE-AI-VOICE.md)（感想 + 鸭哥去 AI）**叠加 Must**。
- **Path:** `docs/OWNER-LONGFORM-CLEVER-ADVOCATE.md`
- **Open WebUI:** `rag_l1`
- **Cursor:** `read`

## 章节锚点
- **1. 写什么**: | 块 | Must |
- **2. 反方怎么找（Agent Must · 写 v0 前）**: 1. WebSearch / 评论区常见话术（活动拆解博主、音乐学院劝退帖、「我就赚个出场费」乐手、旺场 BGM 派）
- **3. CEO evaluate · 三重 evaluate · 压测（Must 顺序）**: 有 `--brief` 且存在长稿时：
- **4. 规则锚点**: - [CEO-SIX-CASE-GM-TO-CEO-WORKFLOW.md](./CEO-SIX-CASE-GM-TO-CEO-WORKFLOW.md) §3–4
- **5. 脚本**: - `scripts/xhs_clever_advocate.py` · `scripts/verify-xhs-clever-advocate.sh`


---

## L2 正文

# Owner 长稿 · Clever 多立场反驳（Must · 2026-10-30）

> **Clever** = 刁钻、有趣、像不同网红在评论区杠你——不是论文反证，是**有脸有立场**的 against。  
> 与 [OWNER-LONGFORM-DE-AI-VOICE.md](./OWNER-LONGFORM-DE-AI-VOICE.md)（感想 + 鸭哥去 AI）**叠加 Must**。

## 1. 写什么

| 块 | Must |
|----|------|
| **主观点** | 1 个可杠的核心判断（本篇如「不需要那么多音乐家 / wallpaper」） |
| **反方席** | **≥4 个不同立场** · 每人 **2–4 句** · 标签 `**反方·<网红人设>**` 或 `**@<类型>**` |
| **立场差异** | 采购 / 学生保就业 / 接活乐手 / 玄学旺场 / 纯爱党 / 机构拆解号 / 同行 PR … **至少 4 类** |
| **作者收束** | 小节「**我把杠收进包里**」或「**杠完仍坚持**」——**逐条回嘴**，留 trade-off，不和稀泥 |
| **语气** | 网红口语 + [skill_yage_voice.md](../rules/skills/skill_yage_voice.md)（短句、有判断、禁综述腔） |

## 2. 反方怎么找（Agent Must · 写 v0 前）

1. WebSearch / 评论区常见话术（活动拆解博主、音乐学院劝退帖、「我就赚个出场费」乐手、旺场 BGM 派）  
2. 每反方 **只杠一个角度**——要刁钻，不要四个反方说同一句  
3. 写完后 **自检**：删掉任何一个反方，文章是否少一层张力？是则合格  

## 3. CEO evaluate · 三重 evaluate · 压测（Must 顺序）

有 `--brief` 且存在长稿时：

```bash
# 1) 写/改长稿含 Clever 反方席
# 2) L1 + Gemini
.venv/bin/python scripts/evaluate-xhs-brief-complete.py --brief content/xiaohongshu/<file>-brief.md
# 3) Clever 结构门（FAIL → 同会话补反方再跑）
bash scripts/verify-xhs-clever-advocate.sh --brief content/xiaohongshu/<file>-brief.md
# 4) gap + gold distance
python scripts/analyze-brief-evolution-gap.py --brief …
# 5) triple-eval / double-stress 已编排上述步骤（见 ceo-triple-eval-baseline-loop.sh · ceo-double-stress.sh）
```

**READY 条件（gap）：** Clever 门 **PASS** 与 longform 字数、verify gate 等并列（见 `analyze-brief-evolution-gap.py`）。

## 4. 规则锚点

- [CEO-SIX-CASE-GM-TO-CEO-WORKFLOW.md](./CEO-SIX-CASE-GM-TO-CEO-WORKFLOW.md) §3–4  
- [CEO-FULL-EXECUTION-MANDATE.md](./CEO-FULL-EXECUTION-MANDATE.md) · `run_ceo_full_execution.py`  
- [`OWNER-LONGFORM-XHS-SPEC.md`](../content/xiaohongshu/OWNER-LONGFORM-XHS-SPEC.md)  
- [`.cursor/rules/danying-manager-auto.mdc`](../.cursor/rules/danying-manager-auto.mdc) §1b  

## 5. 脚本

- `scripts/xhs_clever_advocate.py` · `scripts/verify-xhs-clever-advocate.sh`  
- 对抗 MD 附录：`run-xhs-brief-adversarial-challenge.py` → `## Clever · 长稿反方席`