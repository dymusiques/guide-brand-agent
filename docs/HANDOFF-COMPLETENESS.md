---
context_version: "2026-10-30-l012"
repo_path: "docs/HANDOFF-COMPLETENESS.md"
goal: "接手完整性 · Handoff Completeness"
openwebui_route: "rag_l1"
cursor_route: "read"
content_sha256: "67506a29d4551ef2"
---

# 接手完整性 · Handoff Completeness

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** *最后更新：2026-10-05*
- **Path:** `docs/HANDOFF-COMPLETENESS.md`
- **Open WebUI:** `rag_l1`
- **Cursor:** `read`

## 章节锚点
- **L1 任务（压缩 · Open WebUI / Cursor 顶栏）**: - **Goal:** > **目标：** 尽量少占 Google Drive，同时让 **全新 AI clone 后能完整接手、顺利运行**。
- **章节锚点**: - **2. 四层存储（从低到高）**: | 层 | 名称 | 放什么 | 新 Agent clone 后 | Drive 占用 |


---

## L2 正文

# 接手完整性 · Handoff Completeness

> **目标：** 尽量少占 Google Drive，同时让 **全新 AI clone 后能完整接手、顺利运行**。  
> **验证：** 运行 `bash scripts/verify-handoff.sh`（Agent 在交班前 / 全部克隆后 Must 跑）。  
> **新 Agent 指挥手册（Must）：** [AGENT-TAKEOVER.md](AGENT-TAKEOVER.md)  
> **一页纸 SOP（M5）：** [HANDOFF-SOP.md](HANDOFF-SOP.md) · 全自动链 [AUTOPILOT.md](AUTOPILOT.md)


## 2. 四层存储（从低到高）

| 层 | 名称 | 放什么 | 新 Agent clone 后 | Drive 占用 |
|----|------|--------|-------------------|------------|
| **L0** | Git 真相源 | 规则、USER、稳定 Brief、路由、Skills、Kernels、已定稿 `content/` | ✅ 必有 | 无 |
| **L1** | 本地私有 | OAuth、`*.local.md` overlay | ⚠️ 需备份或重新授权 | 无 |
| **L2** | 工作草稿 | 未 commit 的 `content/` | ❌ 新机没有 | 无 |
| **L3** | Drive 定稿 | Owner 说「同步 Drive」或要分享的 Google Doc | ⚠️ 需 MCP/OAuth | 小（Doc 文本） |
| **L4** | Canva | 视觉成品 | 链接写在 Git/Drive 即可 | 无（在 Canva） |

**原则：** L0 决定 Agent 能否接手；L3/L4 是加分项，不是阻塞项。


## 4. L1 本地私有（不进 Git · 新机需恢复）

| 路径 | 作用 | 新机怎么办 |
|------|------|------------|
| `vendor/gdocs-skill/secrets/credentials.json` | OAuth 客户端 | 从安全备份恢复或 Console 重下 |
| `vendor/gdocs-skill/secrets/token.json` | 已授权 token | 恢复或重新跑 smoke test |
| `rules/skills/overlays/gdocs-skill.local.md` | Drive folder ID 等 | 从 example 复制 + 填 ID |

**无 L1：** Agent 仍可读 Git、写本地 `content/`；**不能**自动 sync Google Doc，直到 Owner 授权。

**新机网络：** `vendor/gdocs-skill` 是 GitHub submodule；若 `git submodule update` 失败，需能访问 `github.com` 或临时设置 `HTTPS_PROXY` 后重试（见 `SETUP.md` §1）。


## 6. 与 Hub / 全部克隆 的关系

| 场景 | 读什么 |
|------|--------|
| 新机 | Hub `全部克隆.md` → 本仓 `SETUP.md` → **`verify-handoff.sh`** → **`verify-integration.sh`** |
| 日常任务 | `integrations/index.md` → 领域 Skill |
| 交班前 | 本文件 + `verify-handoff.sh` 全绿（WARN 可接受并报告） |


## 8. 文字规则 vs 验证脚本（互补，不是二选一）

| | Skill 里的存储默认规则 | `verify-handoff.sh` |
|--|------------------------|---------------------|
| **作用** | 指导 Agent **每次任务怎么做** | 交班前 **检查是否做到** |
| **何时用** | 写产出、定稿、同步 Drive 时 | 全部克隆后、交班前、Owner 问「能接手吗」 |
| **检查什么** | 行为约定（content → commit → 可选 Drive） | L0 文件是否在 Git、USER/IP Brief 是否齐全 |
| **不检查什么** | — | Drive 是否满、Canva 里有多少设计 |

**为什么两层都有：** 文字规则防止 Agent 做错；脚本防止「以为交班了其实 Git 里缺东西」。你不需要记细节，跑脚本即可得到 PASS / WARN / FAIL。

---

*最后更新：2026-10-05*