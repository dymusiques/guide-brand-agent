---
context_version: "2026-10-30-l012"
repo_path: "integration/bilibili-inst360-channel-adoption.md"
goal: "集成 · B 站 + Insta360（Phase 2 渠道 · Owner 定调）"
openwebui_route: "rag_l2"
cursor_route: "read"
content_sha256: "de556031a07e57c1"
---

# 集成 · B 站 + Insta360（Phase 2 渠道 · Owner 定调）

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** > **与小红书关系：** 小红书仍是 **主渠道 + Manager 步 2a**（标题-only · VOICE-ANCHOR · A/B/C/E 包）。  
> **B 站 / Insta360** = **扩展分发与制作**，不替代 XHS 真相源。  
> **Public skill：** [bilibili-upload-skill](http
- **Path:** `integration/bilibili-inst360-channel-adoption.md`
- **Open WebUI:** `rag_l2`
- **Cursor:** `read`

## 章节锚点
- **2. bilibili-upload-skill · 能力边界（来自 ecosystem 说明）**: | 项 | 说明 |
- **4. vlog-skill / opus-video-audio-skill · 何时用**: | Skill | 适合 | 与你路径的关系 |
- **6. Manager 路由（不抢 00 主链）**: | Owner 说 | 走哪 |
- **8. 当前状态**: | 项 | 状态 |


---

## L2 正文

# 集成 · B 站 + Insta360（Phase 2 渠道 · Owner 定调）

> **与小红书关系：** 小红书仍是 **主渠道 + Manager 步 2a**（标题-only · VOICE-ANCHOR · A/B/C/E 包）。  
> **B 站 / Insta360** = **扩展分发与制作**，不替代 XHS 真相源。  
> **Public skill：** [bilibili-upload-skill](https://github.com/grapeot/bilibili-upload-skill) · 可选 [vlog-skill](https://github.com/grapeot/vlog-skill) · [opus-video-audio-skill](https://github.com/grapeot/opus-video-audio-skill)（见 [SKILL_ECOSYSTEM](https://github.com/grapeot/context-infrastructure/blob/main/docs/SKILL_ECOSYSTEM.md)）


## 2. bilibili-upload-skill · 能力边界（来自 ecosystem 说明）

| 项 | 说明 |
|----|------|
| **做什么** | Playwright + **可见 Chrome** + 独立 profile；代填标题、简介、标签、双封面、分区、字幕等；**读回核对** |
| **不做什么** | **不点「立即投稿」**；不批量无人值守；登录 **人扫码**；`fill` 默认 **dry-run** |
| **成熟度** | 各步在真实页验证过；**完整 `--execute` 端到端** 文档称尚未跑通一次 → 首次必须 Owner 在场验收 |

**对 IP 的意义：** 与小红书一样，**Agent 备稿 + 填表，Owner 最终提交**——和 `CONTENT-DELIVERY-FOR-OWNER.md` 同哲学。


## 4. vlog-skill / opus-video-audio-skill · 何时用

| Skill | 适合 | 与你路径的关系 |
|-------|------|----------------|
| **vlog-skill** | HeyGen 数字人 + 精剪旁白 + 论证地图字幕 | Insta360 **真人出镜** 时 **不必** 上；若以后「讲解+地图」重片可用 |
| **opus-video-audio-skill** | Opus 代码渲染短片、分镜配乐、逐帧 QA | Insta360 **实拍为主** 时作 **后期包装/B-roll/片头片尾** 可选，**不** 替代手机口播主路径 |

**纪律：** submodule 已装；**pip / 首次 fill** 仍按 Owner 在场验收。路由：`rules/skills/skill_bilibili_upload.md` · 总表 [ip-content-skills-adoption.md](./ip-content-skills-adoption.md)。


## 6. Manager 路由（不抢 00 主链）

| Owner 说 | 走哪 |
|----------|------|
| 小红书 Round1/2 · A/B/C/E | 现有 **步 2a** + `XHS-VIDEO-ITERATION.md` |
| B 站投稿 · Insta360 素材 | 读本文件 → bilibili skill → **仍 Git 落盘** → Owner 投稿 |
| 重剪辑 / 地图字幕 / 动效 | 可选 vlog/opus skill · scratch 在 `tmp/video/` 或 `content/video/` |

**禁止：** B 站 fill 脚本 **代点发布**；未 Owner 确认称「已发 B 站」。


## 8. 当前状态

| 项 | 状态 |
|----|------|
| bilibili-upload-skill | **vendor ✅** · CLI 首次 **dry-run 待 Owner** |
| vlog / opus | **vendor ✅** · 按触发条件启用 |
| `content/bilibili/` | 见 `content/bilibili/README.md` |

Owner 下一步：**dry-run fill 一条成片** 或 **先写 B 站简介模板（复用 A/B/C/E slug）**。