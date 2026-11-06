# CEO · Owner HTML 该弹什么

## 问题（Owner 反馈 2026-11-05）

跑 **FluteBuddy / 产品战略 / 无 Brief** 的 CEO pipeline 时，浏览器仍打开 `OWNER-XHS-FILTER-DELIVERABLE-<date>.html`，里面是 **Discovery 认知期 01–04 + 工作流测试稿**，与当轮任务无关；且 `#owner-latest` 曾自动弹出 **含 YAML/锚点** 的正文，不像人话。

## 规则

| 当轮任务 | 应打开的交付 | 不应做 |
|----------|--------------|--------|
| 小红书 **Brief** Gate / owner-delivery | `OWNER-XHS-FILTER-DELIVERABLE-<date>.html`（可选 `#owner-latest`） | — |
| **无 Brief** · FluteBuddy 产品轨 | `OWNER-FLUTEBUDDY-DELIVERABLE-<date>.html` | `open-owner-flutebuddy-deliverable-html.sh` |
| **无 Brief** · 个人 IP / 生态链轨 | `OWNER-IP-ECOSYSTEM-DELIVERABLE-<date>.html` | `open-owner-ip-ecosystem-deliverable-html.sh` |
| 三平台 **evolve-platform-hits** | `platform-hits/<slug>/linkedin.html` 等 | 不替代 FILTER，但也不是 FluteBuddy 战略 |

## 环境变量

- `CEO_OWNER_HTML_REFRESH=0` — 不重建 FILTER HTML（`run_ceo_full_execution.py` 在无 Brief 且 goal 不含小红书关键词时 **自动设置**）。
- `CEO_OWNER_HTML_OPEN=0` — 不 `open` 浏览器。
- `CEO_OWNER_DELIVERABLE_PATH` — 写入 manifest 的 **本轮主交付**（Markdown）。
- `CEO_OWNER_HTML_AUTO_MODAL=1` — 仅当 **明确绑 Brief**（`CEO_OWNER_EXTRA_BRIEF`）时，FILTER 页才用 hash 自动弹层；默认 **0**。

## 弹层内容

- **发布正文** = `extract_longform_text(brief)` → 只取 `## L2 正文`，不含 frontmatter。
- Brief 元数据收进 `<details>`，标题 **Agent Brief 元数据**，不是「Brief 全文」首屏。

## 文案过关

- Owner 线：**2000+** 互动范文 → `integration/handoff/owner-copy-benchmarks-tier2.json`
- 顶线对抗 → `docs/angle-benchmarks.json` + `scripts/evolve-platform-hits.py`
- 人话门禁 → `scripts/verify-owner-copy-human-readable.py`

## Cursor Agent（Must）

**FluteBuddy：** `bash scripts/open-owner-flutebuddy-deliverable-html.sh`

**个人 IP / 生态链 / 张丹瀛多维度：** `bash scripts/open-owner-ip-ecosystem-deliverable-html.sh`

双线说明：[CEO-DUAL-TRACK-WORKFLOWS.md](./CEO-DUAL-TRACK-WORKFLOWS.md) · **不要**弹 FILTER。

## 相关

- [OWNER-DELIVERY-NOTIFY-DEFAULT.md](./OWNER-DELIVERY-NOTIFY-DEFAULT.md)
- [OWNER-COPY-BENCHMARKS-TIER2.md](./OWNER-COPY-BENCHMARKS-TIER2.md)
