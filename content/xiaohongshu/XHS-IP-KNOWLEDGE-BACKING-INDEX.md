---
context_version: "2026-11-03"
repo_path: "content/xiaohongshu/XHS-IP-KNOWLEDGE-BACKING-INDEX.md"
goal: "小红书 Brief 写稿 · 外部资料背书索引"
openwebui_route: "rag_l1"
cursor_route: "read"
---

# 小红书 IP · 资料背书索引

定稿 Brief 时，行业/平台背书来自 **筛选脚本的入选原件**。不要整库 RAG，不要把提纲当成全文。

| 层级 | 入口 |
|------|------|
| 执行 | `python3 scripts/screen-xhs-drive-corpus.py --goal "<原话>"` → [`../evolution/00-manager/ceo-inbox/xhs-drive-screen-latest.md`](../evolution/00-manager/ceo-inbox/xhs-drive-screen-latest.md) |
| 全库名单 | [`../personal-ip/intake/_raw/xhs-ip-2026-11-03/drive-listing-2026-11-03-live.json`](../personal-ip/intake/_raw/xhs-ip-2026-11-03/drive-listing-2026-11-03-live.json) |
| L1 | [`../personal-ip/intake/2026-11-03-xhs-drive-corpus-L1.md`](../personal-ip/intake/2026-11-03-xhs-drive-corpus-L1.md) |
| Drive | 文件夹 `1SrD2n_zXN2HjhH_YPbQa-_54YakKXbzZ`（原件在 Drive；本地 mirror 不进 Git） |

**04 Topic Manager / CEO：** 流水线已跑筛选。写稿前打开入选文件，再决定 pitfall 调研是否补 WebSearch。
