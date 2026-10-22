# 集成 · B 站 + Insta360（Phase 2 渠道 · Owner 定调）

> **与小红书关系：** 小红书仍是 **主渠道 + Manager 步 2a**（标题-only · VOICE-ANCHOR · A/B/C/E 包）。  
> **B 站 / Insta360** = **扩展分发与制作**，不替代 XHS 真相源。  
> **Public skill：** [bilibili-upload-skill](https://github.com/grapeot/bilibili-upload-skill) · 可选 [vlog-skill](https://github.com/grapeot/vlog-skill) · [opus-video-audio-skill](https://github.com/grapeot/opus-video-audio-skill)（见 [SKILL_ECOSYSTEM](https://github.com/grapeot/context-infrastructure/blob/main/docs/SKILL_ECOSYSTEM.md)）

---

## 1. Owner 意图（2026-10-22）

- 已有 **B 站账号**；后续可能 **Insta360 拍摄** → 导出 → **上传 B 站**。  
- **仍可能** 用现有 **手机直录** 发小红书（同一条内容可 **一源多裁**）。  
- `bilibili-upload-skill` **要纳入** 能力规划（非「永远不用」）。

---

## 2. bilibili-upload-skill · 能力边界（来自 ecosystem 说明）

| 项 | 说明 |
|----|------|
| **做什么** | Playwright + **可见 Chrome** + 独立 profile；代填标题、简介、标签、双封面、分区、字幕等；**读回核对** |
| **不做什么** | **不点「立即投稿」**；不批量无人值守；登录 **人扫码**；`fill` 默认 **dry-run** |
| **成熟度** | 各步在真实页验证过；**完整 `--execute` 端到端** 文档称尚未跑通一次 → 首次必须 Owner 在场验收 |

**对 IP 的意义：** 与小红书一样，**Agent 备稿 + 填表，Owner 最终提交**——和 `CONTENT-DELIVERY-FOR-OWNER.md` 同哲学。

---

## 3. Insta360 → 工作流（建议 · 未装 skill 前也可人工）

```text
Insta360 导出（主片 + 可选代理文件）
  → content/video/inst360/<YYYY-MM-DD>-<slug>/  （Git：脚本/清单；大文件 gitignore）
  → 口播/标题/简介：复用 XHS 包（A/B/C/E）或 B 站专用一行简介（可更长）
  → （可选）vlog/opus：精剪、字幕、B-roll — 非默认路径
  → bilibili-upload-skill：dry-run fill → Owner 核对 → execute 到「立即投稿」前停
  → Owner 点击投稿 · 回填链接 → content/bilibili/published-index.md
```

**小红书 vs B 站 同条内容：**

| 字段 | 小红书（现状） | B 站（Phase 2） |
|------|----------------|-----------------|
| 标题 | ≤20 字 · packages | 可略长 · 同义改写 |
| 正文/简介 | 常空 · 口播在片内 | **简介可写** 要点 + 时间戳（可选） |
| 标签 | 10 `#` | B 站 tag 规则按 skill/cli |
| 封面 | Canva 3:4 | skill 支持 **4:3 + 16:9** 双封面 |
| 字幕 | 可选 | 支持 `.srt` |

---

## 4. vlog-skill / opus-video-audio-skill · 何时用

| Skill | 适合 | 与你路径的关系 |
|-------|------|----------------|
| **vlog-skill** | HeyGen 数字人 + 精剪旁白 + 论证地图字幕 | Insta360 **真人出镜** 时 **不必** 上；若以后「讲解+地图」重片可用 |
| **opus-video-audio-skill** | Opus 代码渲染短片、分镜配乐、逐帧 QA | Insta360 **实拍为主** 时作 **后期包装/B-roll/片头片尾** 可选，**不** 替代手机口播主路径 |

**纪律：** submodule 已装；**pip / 首次 fill** 仍按 Owner 在场验收。路由：`rules/skills/skill_bilibili_upload.md` · 总表 [ip-content-skills-adoption.md](./ip-content-skills-adoption.md)。

---

## 5. 安装协议（已完成 · 首次用 B 站 CLI 时）

1. ~~submodule~~ → `vendor/bilibili-upload-skill/` ✅  
2. Router → `rules/skills/skill_bilibili_upload.md` ✅  
3. 私有：`rules/skills/overlays/bilibili-upload.local.md`（profile 路径、默认分区、是否 execute）  
4. 产出目录：`content/bilibili/` · 链接表 `content/bilibili/published-index.md`  
5. **首次：** 只跑 **dry-run fill**，Owner 截图确认后再 `--execute`  
6. 验收：填表读回 PASS + Owner 手动投稿成功一条 → 写入 index

**vlog / opus：** 已 vendor；依赖（Apple Silicon、GPU、HeyGen 等）见各 vendor README，**触发条件**见 ip-content-skills-adoption §1。

---

## 6. Manager 路由（不抢 00 主链）

| Owner 说 | 走哪 |
|----------|------|
| 小红书 Round1/2 · A/B/C/E | 现有 **步 2a** + `XHS-VIDEO-ITERATION.md` |
| B 站投稿 · Insta360 素材 | 读本文件 → bilibili skill → **仍 Git 落盘** → Owner 投稿 |
| 重剪辑 / 地图字幕 / 动效 | 可选 vlog/opus skill · scratch 在 `tmp/video/` 或 `content/video/` |

**禁止：** B 站 fill 脚本 **代点发布**；未 Owner 确认称「已发 B 站」。

---

## 7. 与 IP / 声音

- **口播真相源不变：** `VOICE-ANCHOR.md` · `voice-anchor-transcripts-*.md` · `owner-source-pivot-*`  
- B 站简介 **可更长**，但 **语气须 L2 禁词自检**（`verify-xhs-voice-qa.sh` 禁词表可复用到 `content/bilibili/*.md`）  
- Insta360 片 **不必** 为 B 站改 XHS 标题逻辑；可 **同一 slug** 两渠道两标题

---

## 8. 当前状态

| 项 | 状态 |
|----|------|
| bilibili-upload-skill | **vendor ✅** · CLI 首次 **dry-run 待 Owner** |
| vlog / opus | **vendor ✅** · 按触发条件启用 |
| `content/bilibili/` | 见 `content/bilibili/README.md` |

Owner 下一步：**dry-run fill 一条成片** 或 **先写 B 站简介模板（复用 A/B/C/E slug）**。
