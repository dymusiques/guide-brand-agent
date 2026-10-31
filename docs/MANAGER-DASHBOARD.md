---
context_version: "2026-10-30-l012"
repo_path: "docs/MANAGER-DASHBOARD.md"
goal: "CEO 仪表盘（00 Manager）"
openwebui_route: "rag_l1"
cursor_route: "read"
content_sha256: "2ad8b5c69fdfc9a1"
---

# CEO 仪表盘（00 Manager）

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** **命令：**
- **Path:** `docs/MANAGER-DASHBOARD.md`
- **Open WebUI:** `rag_l1`
- **Cursor:** `read`


---

## L2 正文

# CEO 仪表盘（00 Manager）

**命令：**

```bash
bash scripts/manager-dashboard.sh
```

**输出：**

- 终端打印全文
- 写入 `content/analytics/derived/manager-dashboard-YYYY-MM-DD.md`（gitignore，本地查看）

**汇总内容：**

- 认知期 discovery Brief：evaluate / 发布状态
- 15 天快检提醒（依赖 Brief 内 `发布日期`）
- analytics inbox / derived 是否为空
- Goal Registry 摘要
- 上次 `verify-all` 记录（成功跑过后写入 state）
- 建议下一步派活

**不是全自动：** 不发帖、不拉小红书 API；发布后在 Brief 填 `## 发布状态`。

`verify-all` PASS 后会自动刷新 state 并静默 regenerate 仪表盘。