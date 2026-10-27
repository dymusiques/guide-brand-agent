# 小红书 · 视频选题迭代（流程真相源）

> **能力边界在流程里定义：** 本文件 + [VOICE-ANCHOR.md](./VOICE-ANCHOR.md) + [OWNER-CONTENT-SPEC.md](./OWNER-CONTENT-SPEC.md)  
> **00 Manager 步 2（视频/标题）Must 读本文件** · Intake 栈 #9：[XHS-CONTENT-INTAKE-STACK.md](../../docs/XHS-CONTENT-INTAKE-STACK.md)

---

## 双轨（勿混）

| 轨 | 默认 | 产出 |
|----|------|------|
| **轨 1 · 人/笛/故事** | **视频 Round 1–2 默认** | 像已发爆款标题（泰斗/考场/嘲讽） |
| **轨 2 · 认知期品牌** | Owner 说「品牌向」 | discovery Brief · evaluate · 收藏+聊聊 |

**禁止：** 未过 Round 1 点选就交轨 2 长正文或 discovery 体「装饰型艺术/站得住 moment」堆砌。

---

## 三轮协议

### Round 1（Agent 交付 · Owner 只选题）

**Must 包含：**

- **5 个视频方向**（各 1 句「拍什么」+ 数据/CV 依据 ID）  
- 每方向 **3 个标题**（≤20 字含 emoji/符号 · 人工再数）  
- 每方向 **2 个封面字**（overlay · 短于标题）  
- **1 句口播钩子**（不写长正文）

**Must 不包含：** 完整正文、10 tag、evaluate（除非 Owner 要求提前跑）

**落盘：** `content/xiaohongshu/YYYY-MM-DD-video-round1-*.md`

### Round 2（Owner 点选后）

Owner 回复格式示例：`方向 3 · 标题 3B · 封面 3-2`

Agent 交付：**口播/描述区正文 + 分镜表 + 10 tag** · 仍 **待 Owner 确认**。

### Round 3（语气）

只改措辞；结构不动。对照 [VOICE-ANCHOR.md](./VOICE-ANCHOR.md) + `bash scripts/verify-xhs-voice-qa.sh`。

**Brief 定稿（轨 2 或 Owner 要求 aligned）：** 再跑 `evaluate-xhs-topic.py`（L1）。

---

## 数据与 Drive（写 Round 1 前）

| # | 读什么 |
|---|--------|
| 1 | [voice-anchor-sources.json](./voice-anchor-sources.json) · [VOICE-ANCHOR.md](./VOICE-ANCHOR.md) |
| 2 | [xhs-data-strategy-2026-10-20.md](../analytics/derived/xhs-data-strategy-2026-10-20.md) |
| 3 | [cv-source-2026-09-15.md](../personal-ip/cv-source-2026-09-15.md) |
| 4 | 平台 MD（WILL/Momentum）· **校准结构，不盖过轨 1 语气** |

---

## 声音锚定（标题-only 笔记）

- Owner 账号常见形态：**仅标题 + tag，描述区为空** → 锚定 = **标题 + 口播开头 ~80 字**（见 [VOICE-ANCHOR.md](./VOICE-ANCHOR.md) §如何补口播开头）。  
- Excel / 网页抓取 **拿不到口播**；`xhs_fetch_note_captions.py` 仅在有描述区时有用。  
- Agent：**先** `python scripts/analytics/xhs_build_voice_anchor.py`（标题与数据）。

---

## 验收（分层）

| 层 | 命令 | 含义 |
|----|------|------|
| **L0** | `bash scripts/verify-xhs-content-intake.sh` | 数据栈文件在 |
| **L2 声音 QA** | `bash scripts/verify-xhs-voice-qa.sh [round1.md]` | 流程文件 + 禁词 + Round1 结构 |
| **L1 IP** | `evaluate-xhs-topic.py --brief` | 仅 Brief 定稿 / 轨 2 |

见 [VERIFY-TIERS.md](../../docs/VERIFY-TIERS.md) §小红书声音 L2。
