# 多平台发帖飞轮（小红书 + LinkedIn + Medium）

真源：`integration/handoff/owner-multichannel-post-flywheel.json`

## 哲学

**你发帖** → **等窗口** → **把数据交给仓库** → **Agent ingest/sync** → **复盘/选题** → 再发帖。  
全自动的终点是 **你不用记命令**，不是不用导表。

## 小红书（主力 · Drive）

| 步 | Owner | 机器 |
|----|-------|------|
| 发帖 | 平台点发送 | — |
| 等 | 见下「导表节奏」 | — |
| 导表 | 后台 xlsx → Drive「我的小红书数据」 | `sync-owner-xhs-data-from-drive.sh` |
| 验 | — | `verify-xhs-analytics-freshness.py` |

### 导表节奏（每周 2–3 条视频/笔记）

| 方案 | 建议 |
|------|------|
| **默认（推荐）** | **周三 21:00 + 周日 21:00** 各导一次 **近 7 日** + 列表/全量（按你平时用的表） |
| 为何 | 覆盖首波（约 48–72h）和周末长尾，**不必每篇 24h 导** |
| 爆款单条 | 可选发帖 **第 2 天中午** 多导一次 |
| 月度复盘 | 每月初可加一次 **近 30 日** |

提醒：`docs/OWNER-XHS-EXPORT-REMINDER-AUTOMATION-INSTRUCTIONS.md` · 脚本 `owner-xhs-export-reminder.py`（周三/日）。

## LinkedIn / Medium（轻量 intake）

**不**并进 `notes.csv`。

1. 复制模板填数：`content/analytics/linkedin/inbox/TEMPLATE-post-metrics.md` · `medium/.../TEMPLATE-post-metrics.md`
2. 或 chat 贴同结构 / JSON / CSV
3. Agent：

```bash
python3 scripts/ingest-owner-linkedin-metrics.py --file content/analytics/linkedin/inbox/<file>
python3 scripts/ingest-owner-medium-metrics.py --file content/analytics/medium/inbox/<file>
```

LinkedIn/Medium 建议 **发帖后 48–72h** 或 **跟小红书同日晚上** 填一次即可（阅读长尾比短视频慢）。

## Drive 变更检测

见 `docs/OWNER-XHS-DRIVE-WATCH-ARCHITECTURE.md` · `compare-owner-xhs-drive-listing.py`

## Gate · evaluate · baseline（与小红书同合同）

`agent-owner-research-gate.py` 层 **`multichannel_post_gate`**：

| 状态 | 行为 |
|------|------|
| inbox 空 | **PASS**（架构就绪，不阻塞） |
| 有 `inbox/*` 文件 | ingest → `agent-multichannel-eval-baseline-loop.py` |
| goal 含 LinkedIn/Medium/领英/复盘/多平台 | 强制跑（见 contract `triggers_any`） |

满链写稿仍：`派活给 CEO` → six-case · triple-eval（有 Brief 时）。本层管 **发帖数据** 的 evaluate + baseline 滚动。

Handoff：`integration/handoff/owner-multichannel-post-gate-latest.json` · `owner-multichannel-post-eval-*.json`

## 阶段（Owner 不必背术语）

| 阶段 | 做什么 |
|------|--------|
| **0 · 积攒**（现在） | 小红书 Drive + LinkedIn/Medium inbox 数据；**不要求** 三平台 SEO 互链 |
| **1 · 写稿战役** | `派活给 CEO` + goal → **各平台交付包**满链（见 [OWNER-DELIVERABLE-PACK-PLATFORMS.md](./OWNER-DELIVERABLE-PACK-PLATFORMS.md)） |
| **2 · 跨平台互链**（以后） | 交付包/HTML 里 Medium↔LinkedIn↔小红书链接；Agent 在交付时 **会主动问** 是否上互链，你现在不用提前做 |

「埋链」若指 **架构接线**：已接 gate，你 **贴文件 / 丢 inbox** 即可，**不必**说固定口令。若指 **SEO 互链**：积攒阶段 **可以只做 LinkedIn + Medium 数据**，小红书仍走 Drive。