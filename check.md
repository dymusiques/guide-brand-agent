---
context_version: "2026-10-30-l012"
repo_path: "check.md"
goal: "check · 验收"
openwebui_route: "rag_l2"
cursor_route: "read"
content_sha256: "5466df4c41e7a039"
---

# check · 验收

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** 做完自己复查 — **canonical 总则**在 hub：
- **Path:** `check.md`
- **Open WebUI:** `rag_l2`
- **Cursor:** `read`

## 章节锚点
- **Agent 交付前（Owner 不必记）**: 1. 先跑 `bash scripts/verify-handoff.sh`


---

## L2 正文

# check · 验收

做完自己复查 — **canonical 总则**在 hub：

**[danying-apps/rules/check/check.md](https://github.com/dymusiques/danying-apps/blob/main/rules/check/check.md)**

**各仓 verify 形态对照**（防查错仓 · Module 3 的 6 test 不在本仓）：

**[danying-apps/rules/check/VERIFY-MAP.md](https://github.com/dymusiques/danying-apps/blob/main/rules/check/VERIFY-MAP.md)**


## Agent 交付前（Owner 不必记）

1. 先跑 `bash scripts/verify-handoff.sh`
2. 再跑 `bash scripts/verify-integration.sh`（有 OAuth 时应 6/6 PASS）
3. 可选 Owner 要求：Drive 写入后 MCP `read_file` 读回（不占必须；Git 已定稿即可）

需代理访问 Google 时：`export HTTPS_PROXY=…` 后再跑集成脚本。