---
context_version: "2026-10-30-l012"
repo_path: "docs/SOP-ARTIST-BENCHMARK-AND-HANDOFF.md"
goal: "SOP · Artist 四指标对标 + 新机/新 Agent 接手"
openwebui_route: "rag_l1"
cursor_route: "read"
content_sha256: "703a60d0ad7485d1"
---

# SOP · Artist 四指标对标 + 新机/新 Agent 接手

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** > **Owner（2026-10-27）：** 筛选 **其他 artist** 不用 SWOT；用 **DB / PLD / APO / CTD**。  
> **SWOT 保留场景：** 仅 **02 商业品牌** · `content/business-brand/*-swot.md`（个人 IP 战略侧，非 GM10 对人清单）。
- **Path:** `docs/SOP-ARTIST-BENCHMARK-AND-HANDOFF.md`
- **Open WebUI:** `rag_l1`
- **Cursor:** `read`

## 章节锚点
- **B · 新机 / 新 Agent 接手 SOP（Must）**
- **D · 当前 P1 优先（screen 结果 · 可随 Owner 改）**: 1. **ThatViolaKid** — `drew-forde-thatviolakid` · composite 见 `artist-watchlist-screened.json`


---

## L2 正文

# SOP · Artist 四指标对标 + 新机/新 Agent 接手

> **Owner（2026-10-27）：** 筛选 **其他 artist** 不用 SWOT；用 **DB / PLD / APO / CTD**。  
> **SWOT 保留场景：** 仅 **02 商业品牌** · `content/business-brand/*-swot.md`（个人 IP 战略侧，非 GM10 对人清单）。


## B · 新机 / 新 Agent 接手 SOP（Must）

### B1 · Clone 与依赖（一次）

```bash
git clone <remote> danying-brand-agent && cd danying-brand-agent
git submodule update --init --recursive
bash scripts/ensure-venv-deps.sh
# 读 SETUP.md · 配置 .env（Gemini）· gdocs overlay 若用 Google
```

### B2 · 读序（不读旧 chat）

1. [HANDOFF-MD-MANIFEST.md](HANDOFF-MD-MANIFEST.md)  
2. [AGENT-TAKEOVER.md](AGENT-TAKEOVER.md) · [NEW-AGENT-WORKFLOW-SOP.md](NEW-AGENT-WORKFLOW-SOP.md)  
3. 本文 **A 节** + [DAILY-GM-TRIO-SOP.md](DAILY-GM-TRIO-SOP.md) + [VERIFY-AGENT-FUSED.md](VERIFY-AGENT-FUSED.md)

### B3 · 验收（Must）

```bash
bash scripts/verify-handoff.sh
bash scripts/verify-agent-takeover.sh
SKIP_GEMINI=1 bash scripts/verify-agent-fused.sh --agent all-daily --with-artifacts
python scripts/screen-artist-watchlist.py
```

有 Gemini key 交班档：`VERIFY_TIER=release bash scripts/verify-all.sh`

### B4 · 后台 daily（Owner 曾 setup 一次）

```bash
bash scripts/setup-background-goal-evolution.sh
# Process Launcher 见 docs/BACKGROUND-GOAL-EVOLUTION.md · vendor/process-launcher
```

未 setup → 仅 Cursor 内 CEO 链 + 手动 `bash scripts/run-daily-gm-trio.sh`。

### B5 · Git 与 SOP 分工

| 手段 | 作用 |
|------|------|
| **Git push（L0）** | 脚本、watchlist、screened、Brief 定稿、SOP — **新机 pull 即得** |
| **SOP（本文件 + MANIFEST）** | **顺序与红线** — 防止误用 SWOT、误交 Owner 未 Gate 稿 |
| **L1 本地** | `.env`、OAuth、`*.local.md` — 新机 **重新授权**，不进 Git |


## D · 当前 P1 优先（screen 结果 · 可随 Owner 改）

1. **ThatViolaKid** — `drew-forde-thatviolakid` · composite 见 `artist-watchlist-screened.json`  
2. 土豆人 · 小福象（P2）— 见 screened 表  

Owner 裁决后更新 `artist-intel-review-state.json`。