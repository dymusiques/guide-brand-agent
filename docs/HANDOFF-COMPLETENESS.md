# 接手完整性 · Handoff Completeness

> **目标：** 尽量少占 Google Drive，同时让 **全新 AI clone 后能完整接手、顺利运行**。  
> **验证：** 运行 `bash scripts/verify-handoff.sh`（Agent 在交班前 / 全部克隆后 Must 跑）。

---

## 1. 什么算「完整」？

完整 = **Git 里的真相源齐全** + **本地 secrets/overlay 可恢复** + **Drive 只承担定稿/协作（可选）**。

新 Agent **不依赖** Drive 里每一份草稿；**依赖** Git 里已 commit 的品牌事实与稳定产出。

---

## 2. 四层存储（从低到高）

| 层 | 名称 | 放什么 | 新 Agent clone 后 | Drive 占用 |
|----|------|--------|-------------------|------------|
| **L0** | Git 真相源 | 规则、USER、稳定 Brief、路由、Skills、Kernels、已定稿 `content/` | ✅ 必有 | 无 |
| **L1** | 本地私有 | OAuth、`*.local.md` overlay | ⚠️ 需备份或重新授权 | 无 |
| **L2** | 工作草稿 | 未 commit 的 `content/` | ❌ 新机没有 | 无 |
| **L3** | Drive 定稿 | Owner 说「同步 Drive」或要分享的 Google Doc | ⚠️ 需 MCP/OAuth | 小（Doc 文本） |
| **L4** | Canva | 视觉成品 | 链接写在 Git/Drive 即可 | 无（在 Canva） |

**原则：** L0 决定 Agent 能否接手；L3/L4 是加分项，不是阻塞项。

---

## 3. L0 必填清单（必须在 Git · main）

### 3.1 仓库骨架（缺一 = 不能接手）

| 路径 | 用途 |
|------|------|
| `AGENTS.md` | Agent 入口 |
| `INDEX.md` | 本仓索引 |
| `integrations/index.md` | 任务路由 |
| `rules/SOUL.md` | 品牌边界 |
| `rules/USER.md` | Owner + 一句话 IP + 受众 |
| `rules/WORKSPACE.md` | 路径路由 |
| `.cursor/skills/guide-core/` | 总控 |
| `.gitmodules` + `vendor/gdocs-skill` | Google CLI |

### 3.2 品牌事实（缺一 = 会编造）

| 路径 | 最低要求 |
|------|----------|
| `rules/USER.md` | 含「一句话定位」「目标受众」且非空 |
| `content/personal-ip/*.md` | 至少 1 份 IP Brief（与 USER 一致或更完整） |

### 3.3 稳定产出（按领域 · 任务相关则应有）

| 领域 | Git 路径（定稿后 commit） | Drive（仅定稿可选） |
|------|---------------------------|---------------------|
| 个人 IP | `content/personal-ip/` | `02-personal-ip/` |
| 商业品牌 | `content/business-brand/` | `03-business-brand/` |
| 营销 | `content/marketing/` | `04-marketing/` |
| 小红书 | `content/xiaohongshu/` | `05-xiaohongshu/` |
| 视觉 | `content/visual/`（Brief + Canva 链接） | `06-visual/` |

---

## 4. L1 本地私有（不进 Git · 新机需恢复）

| 路径 | 作用 | 新机怎么办 |
|------|------|------------|
| `vendor/gdocs-skill/secrets/credentials.json` | OAuth 客户端 | 从安全备份恢复或 Console 重下 |
| `vendor/gdocs-skill/secrets/token.json` | 已授权 token | 恢复或重新跑 smoke test |
| `rules/skills/overlays/gdocs-skill.local.md` | Drive folder ID 等 | 从 example 复制 + 填 ID |

**无 L1：** Agent 仍可读 Git、写本地 `content/`；**不能**自动 sync Google Doc，直到 Owner 授权。

---

## 5. 产出工作流（Agent 必须遵守）

```
① 草稿 → 写 content/<domain>/（本地）
② 稳定 → git add + commit（L0 真相源）← Owner 说「定稿」或任务段落完成时
③ 可选 → Owner 说「同步 Drive」→ MCP/gdocs 写入 L3 对应文件夹
④ 视觉 → Canva 成品；Git 只存 Brief + 设计链接（L4）
```

**禁止：** 仅写 Drive 不 commit Git；仅留本地不 commit 就称「已完成交班」。

---

## 6. 与 Hub / 全部克隆 的关系

| 场景 | 读什么 |
|------|--------|
| 新机 | Hub `全部克隆.md` → 本仓 `SETUP.md` → **`bash scripts/verify-handoff.sh`** |
| 日常任务 | `integrations/index.md` → 领域 Skill |
| 交班前 | 本文件 + `verify-handoff.sh` 全绿（WARN 可接受并报告） |

---

## 7. 验收标准（verify-handoff.sh）

| 级别 | 含义 |
|------|------|
| **PASS** | L0 齐全；新 Agent 可独立做品牌/营销/小红书任务 |
| **WARN** | L0 齐但 L1 缺（OAuth/overlay）；可接手，Google 相关需 Owner |
| **FAIL** | L0 缺项；必须先补 commit 或补文件 |

---

*最后更新：2026-10-05*
