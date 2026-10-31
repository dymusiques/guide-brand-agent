---
context_version: "2026-10-30-l012"
repo_path: "content/xiaohongshu/BRIEF-THREE-LENS-SOP.md"
goal: "小红书 Brief · 三镜头 SOP（Owner · 必写进正文 · 2026-10-28）"
openwebui_route: "intake_l2"
cursor_route: "read"
content_sha256: "3f12538b90a41f5a"
---

# 小红书 Brief · 三镜头 SOP（Owner · 必写进正文 · 2026-10-28）

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** > **总纲：** [OWNER-XHS-ADVERSARIAL-AND-EVOLUTION-MANDATE.md](../../docs/OWNER-XHS-ADVERSARIAL-AND-EVOLUTION-MANDATE.md) · 写前先 [BRIEF-PITFALLS-RESEARCH-SOP.md](./BRIEF-PITFALLS-RESEAR
- **Path:** `content/xiaohongshu/BRIEF-THREE-LENS-SOP.md`
- **Open WebUI:** `intake_l2`
- **Cursor:** `read`

## 章节锚点
- **三镜头（每篇 Must）**: | 镜头 | 写什么 | 失败信号 |
- **专业人士嵌入（策展/线下）**: Must 回答：**艺术家如何进展览动线**，既 **大众可进入** 又 **传导品牌**——不是「请音乐家来」。
- **对抗来源**: - X1–X12：[2026-10-27-ip-adversarial-FULL-DRILL-REPORT.md](../personal-ip/2026-10-27-ip-adversarial-F…
- **禁止**: - 命题式标题全文无案例（「什么是 X 的艺术」）
- **验收**: - `manager-brief-evolution-until-gap.sh` · `analyze-brief-evolution-gap.py` → **READY**


---

## L2 正文

# 小红书 Brief · 三镜头 SOP（Owner · 必写进正文 · 2026-10-28）

> **总纲：** [OWNER-XHS-ADVERSARIAL-AND-EVOLUTION-MANDATE.md](../../docs/OWNER-XHS-ADVERSARIAL-AND-EVOLUTION-MANDATE.md) · 写前先 [BRIEF-PITFALLS-RESEARCH-SOP.md](./BRIEF-PITFALLS-RESEARCH-SOP.md)  
> **不是**写在「程序里」就算完成——**Must 出现在 `*-brief.md` 正文 + classifier body**，且 fusion **三镜头 · 可辨认案例** 须 ✅。

## 三镜头（每篇 Must）

| 镜头 | 写什么 | 失败信号 |
|------|--------|----------|
| **1 · 谁怎么做** | ≥2 个可辨认案例（品牌/馆/项目/人；可 1 匿名但要有城市·环节·细节） | 只有「很多品牌」「有人」 |
| **2 · 忽略了什么** | 声学/动线/测量/伦理/礼仪里 **被跳过** 的具体项 | 只写「没做好」 |
| **3 · 反常规** | 有个性的做法 + **trade-off**（会丢什么、换来什么） | 只有正确 checklist |

## 专业人士嵌入（策展/线下）

Must 回答：**艺术家如何进展览动线**，既 **大众可进入** 又 **传导品牌**——不是「请音乐家来」。

## 对抗来源

- X1–X12：[2026-10-27-ip-adversarial-FULL-DRILL-REPORT.md](../personal-ip/2026-10-27-ip-adversarial-FULL-DRILL-REPORT.md)  
- 写前 redteam-pre · 写后 [BRIEF-ADVERSARIAL-CHALLENGE.md](../agents/_shared/BRIEF-ADVERSARIAL-CHALLENGE.md)

## 禁止

- 命题式标题全文无案例（「什么是 X 的艺术」）  
- Tier/声压/六维 **清单体** 当正文  
- evaluate **aligned** 但读者划走（L2 · X2/X11）

## 验收

- `manager-brief-evolution-until-gap.sh` · `analyze-brief-evolution-gap.py` → **READY**  
- `run-xhs-brief-adversarial-challenge.py` · `evaluate-xhs-brief-complete.py`  
- 有 gold：`evaluate-edit-distance.py` vs `reference/gold.md`