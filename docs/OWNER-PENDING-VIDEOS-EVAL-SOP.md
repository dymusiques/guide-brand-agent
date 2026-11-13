---
context_version: "2026-11-08"
repo_path: "docs/OWNER-PENDING-VIDEOS-EVAL-SOP.md"
goal: "待发口播 MD+Python 混合流水线 · Owner / 新 Agent 唯一入口"
openwebui_route: "rag_l1"
cursor_route: "read"
---

# 待发口播评估 · SOP（MD 流程 + Python 打分）

## L1（30 秒）

| 项 | 值 |
|----|-----|
| **你放口播** | `content/xiaohongshu/inbox/pending-videos/*.md`（条数不限） |
| **你说话触发** | 「评估待发口播」 / `CEO 开始执行 · 评估待发口播` |
| **一条命令** | `bash scripts/run-owner-pending-videos-eval.sh` |
| **你看结果** | `content/evolution/00-manager/ceo-inbox/OWNER-PENDING-VIDEOS-EVAL-latest.html` |
| **机器真源（分数）** | `integration/handoff/owner-pending-videos-eval-latest.json` |
| **机器真源（事实·Agent 必引）** | `integration/handoff/owner-pending-videos-facts-latest.json` → `decision_summary` |
| **建议硬门禁** | `python3 scripts/agent-gate-pending-videos-advice.py`（PASS 后才能给薯条/标题/选题） |
| **分层 ID** | `L2d_PENDING_VIDEOS_EVAL`（见 workflow-automation-manifest） |

**MD 与 Python 分工：** 本文 = 流程与路径；`scripts/evaluate-owner-pending-videos.py` = 每次一致的分数/排序/薯条档；`build-owner-pending-videos-eval-html.py` = 表格可视化。

---

## L2 正文

### 1. 在 CEO 栈中的位置

```text
Owner 口播 / 剪映字幕 / ASR
        │
        ▼
┌─────────────────────────────────────────────────┐
│ L1 · Collector（MD 文件 intake）                  │
│ content/xiaohongshu/inbox/pending-videos/*.md     │
│ 模板：…/pending-videos/TEMPLATE.md               │
└─────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────┐
│ L2d · 本流水线（Python · 可重复）                 │
│ run-owner-pending-videos-eval.sh                  │
│   → evaluate → facts manifest → advice gate PASS │
│   → build-owner-pending-videos-eval-html.py      │
└─────────────────────────────────────────────────┘
        │
        ├──────────────► HTML + JSON（Owner 决策）
        │
        ▼
Owner 周三/五/日晚发布 → Drive 数据 → analytics 同步
        │
        ▼
┌─────────────────────────────────────────────────┐
│ L3 · Brief 进化 / aligned（另链 · 勿混）          │
│ manager-brief-evolution-until-gap.sh 等           │
└─────────────────────────────────────────────────┘
```

**本层不做：** 改 Brief、发帖、聚光/薯条下单。

### Agent 口播建议 · 硬门禁（2026-11-13 · 全文机械真源）

**原则：** `.md` 全文是唯一事实源；Agent **不得**凭 `body_preview` / `human_glance_only` / 口播开头下结论。  
机器用 Python **通读全文** 生成 `decision_summary`；你只要给建议前跑 gate，就不会漏读文末（如「法国」「不是发生在我身上」）。

| 步 | 命令（品牌仓根） | 含义 |
|----|------------------|------|
| G0 | `bash scripts/run-owner-pending-videos-eval.sh --no-open` | inbox 变更后刷新 eval + facts + gate |
| G1 | `python3 scripts/agent-gate-pending-videos-advice.py` | **PASS** → 允许谈薯条/标题/选题；**exit 1** → 禁止交付 |
| G2 | 引用 stdout 的 `decision_summary` 或读 `owner-pending-videos-facts-latest.json` | 地点 / 目击者 / 标题一致性 |
| G3（可选） | `python3 scripts/read-pending-video-for-agent.py 01-法国大师课迟到与教养.md` | 单条核对 |

| 禁止 | 必须 |
|------|------|
| 用 eval JSON 的 `human_glance_only` 当证据 | 用 `integration/handoff/owner-pending-videos-facts-latest.json` 的 `decision_summary` |
| gate 未 PASS 就写薯条/标题/地点/视角建议 | 交付话术里带上 gate 引用的 `decision_summary`（至少涉及条目） |
| 把「意大利」文件名当实景 | 全文解析 + 元数据 **地点** / **叙事视角** |

**本层做：** 扫描 inbox **全部** `.md`（全文）→ 匹配度 + 完播风险 + 薯条 A/B/C + facts manifest。

### 2. 文件地图（新 Agent 按路径找）

| 用途 | 路径 |
|------|------|
| **操作说明（本文件）** | `docs/OWNER-PENDING-VIDEOS-EVAL-SOP.md` |
| **机器流水线注册** | `integration/handoff/owner-pending-videos-pipeline.json` |
| **自动化层注册** | `integration/handoff/workflow-automation-manifest.json` → `L2d` |
| **Owner 口播 inbox** | `content/xiaohongshu/inbox/pending-videos/` |
| **口播模板** | `content/xiaohongshu/inbox/pending-videos/TEMPLATE.md` |
| **inbox 说明** | `content/xiaohongshu/inbox/pending-videos/README.md` |
| **评估脚本** | `scripts/evaluate-owner-pending-videos.py` |
| **全文事实 manifest** | `scripts/build-owner-pending-videos-facts-manifest.py` |
| **建议硬门禁** | `scripts/agent-gate-pending-videos-advice.py` |
| **事实 JSON** | `integration/handoff/owner-pending-videos-facts-latest.json` |
| **gate handoff** | `integration/handoff/owner-pending-videos-advice-gate-latest.json` |
| **HTML 构建** | `scripts/build-owner-pending-videos-eval-html.py` |
| **一键入口** | `scripts/run-owner-pending-videos-eval.sh` |
| **仅弹 HTML** | `scripts/open-owner-pending-videos-eval-html.sh` |
| **验收** | `bash scripts/verify-owner-pending-videos-pipeline.sh` |
| **最新 JSON** | `integration/handoff/owner-pending-videos-eval-latest.json` |
| **最新 HTML** | `content/evolution/00-manager/ceo-inbox/OWNER-PENDING-VIDEOS-EVAL-latest.html` |
| **薯条背书（Drive 已缓存）** | `content/personal-ip/intake/_cache/drive-ref/如何投放好小红书薯条.md` |
| **你的历史数据** | `content/analytics/xiaohongshu/DATA-MANIFEST.json` |
| **CEO 口语触发** | `docs/CEO-OWNER-ONE-LINE-TRIGGERS.md` |
| **Collector 总览** | `docs/COLLECTOR-EVALUATOR-PIPELINE.md` § L2d |

### 3. Owner 操作（排版步骤）

**步骤 A · 写入口播（MD）**

1. 复制 `TEMPLATE.md` → `01-短标题.md`（序号仅作排序，可 05、06…）。
2. 填：发布标题、轨（IP/FB）、计划发（周三/五/日）、时长、口播全文。
3. 保存到 `pending-videos/`（**一篇一个文件**）。

**步骤 B · 跑评估（Python）**

```bash
bash scripts/run-owner-pending-videos-eval.sh
```

或 chat：**「评估待发口播」**（Agent 跑同上；CEO 全量 goal 含触发词且 inbox 有 `.md` 时会附带本步）。

**步骤 C · 看表决策**

- 打开 HTML：综合匹配、故事/数据/钩子/完播风险、薯条 **A/B/C**。
- **A**：自然发 72h 后可小额薯条试播放；**B**：先自然流；**C**：先改 hook 再发。

**步骤 D · 发完闭环**

- 按 `docs/XHS-DATA-LAYER.md` 更新 Drive「我的小红书数据」→ `bash scripts/sync-owner-xhs-data-from-drive.sh`。

### 4. 评分列含义（HTML 表头）

| 列 | 含义 |
|----|------|
| **综合匹配** | 35% 故事像 + 35% 数据像 + 15% 好拍 + 15% 提量（规则层 v1） |
| **故事** | 与泰斗/考场/判断类结构接近度 |
| **数据像** | 对照你 23 篇「故事涨粉、技巧不主引擎」 |
| **钩子** | 前 120 字反常识/问句信号 |
| **完播风险** | 争议/嘲讽类偏高 → 发前检查第 4 秒价值 |
| **投流 A/B/C** | 参考 Drive 薯条 SOP：内容为 1，薯条为 0 |

### 5. 与 CEO 全量连接

```bash
bash scripts/ceo-full-execution-pipeline.sh --goal "评估待发口播"
```

`run_ceo_full_execution.py` 在 **inbox 有 `.md`** 且 goal 含 `评估待发|待发口播|口播评估|pending-videos` 时执行：

`bash scripts/run-owner-pending-videos-eval.sh --no-open`

**不替代** `evolve-platform-hits` / Brief gate。

### 6. 口播转文字（Collector 上游）

| 方式 | 推荐 |
|------|------|
| 剪映/CapCut 导出字幕 → 贴进 MD | ✅ 首选 |
| `vendor/asr-skill` 本地转写 → 你改一遍 → MD | ✅ 无字幕时 |
| 边听边 dictate | 仅应急 |

见 `rules/skills/skill_asr.md`。

### 7. 新 Agent 读序

1. 本 SOP  
2. `owner-pending-videos-pipeline.json`  
3. `owner-pending-videos-eval-latest.json` + HTML（若有）  
4. 勿与 `L3_BRIEF_GATE` 混为一步
