---
context_version: "2026-11-03-xhs-corpus"
repo_path: "content/personal-ip/intake/2026-11-03-xhs-drive-corpus-L1.md"
goal: "新 Agent：小红书 IP 资料库入口（只读本页再按需下钻）"
openwebui_route: "rag_l1"
cursor_route: "read"
---

# L1 · 小红书 IP 资料库（Drive 文件夹）

## 裁定（2026-11-03 · Owner 重开对话后）

- **这份资料库由 Cursor 管。** 记忆 = 本页 + 清单 JSON + 按需打开的原件。Open WebUI 只处理「这一篇输出很长、要防中途丢段」（CoT / Diligent），不把 215 份资料整库 RAG 当成已经读过。
- **卡片是地址，不是正文。** 引用前打开 mirror 或按 Drive file id 打开原件。禁止用总摘要 MASTER 代替原件。
- **筛选是脚本，不靠记得读本页。** `python3 scripts/screen-xhs-drive-corpus.py --goal "<原话>"` 会扫 live JSON 的全部文件名，写出 `content/evolution/00-manager/ceo-inbox/xhs-drive-screen-latest.md`。CEO 全量与 Router 会调用它。
- **完整文件名在** `_raw/xhs-ip-2026-11-03/drive-listing-2026-11-03-live.json`（2026-11-03 当场从 Drive 翻页拉全，380 个，无子文件夹）。旧 dry-run（215）已过期。OUTLINE 会截断，以这份 live JSON 为准。
- 裁定全文：[`2026-11-03-context-cursor-vs-openwebui.md`](./2026-11-03-context-cursor-vs-openwebui.md)

## 新 Agent Must（30 秒）

- **Goal：** 做法派长笛 / Personal IP 的小红书内容与 Brief 时，用本库**背书**（平台规则、内容心法、投放逻辑）；**禁止**把全库或长 chat 塞进 prompt。
- **无损原件：** Drive 文件夹是真相；本地 mirror 只是缓存。路径 `content/personal-ip/intake/_raw/xhs-ip-2026-11-03/drive-mirror/小红书/`
- **知识地图：** [`2026-11-03-xhs-drive-corpus-OUTLINE.md`](./2026-11-03-xhs-drive-corpus-OUTLINE.md)（分桶会截断，只作提示）
- **清单：** [`2026-11-03-xhs-drive-corpus-MANIFEST.md`](./2026-11-03-xhs-drive-corpus-MANIFEST.md)
- **Drive：** [文件夹 `1SrD2n_zXN2HjhH_YPbQa-_54YakKXbzZ`](https://drive.google.com/drive/folders/1SrD2n_zXN2HjhH_YPbQa-_54YakKXbzZ)

## 读序（防偷懒、防混乱）

1. 本 L1。要找某一个文件名 → `drive-manifest-dry-run.json`，不要停在 OUTLINE 的「另有 N 个」。
2. 写某主题 Brief → 只打开 **1–3 个**相关原件（优先已镜像的 `.md`，其次 `pdf-text/*.txt` 或 Drive file id）。
3. 需要数据背书 → 摘录进 Brief 并写 **来源文件名**。摘录不能代替原件。
4. 只有「这一篇输出本身很长」才用 CoT / Diligent 分段写、再合并，并抽查开头、中间、结尾。见 [`PROMPT-CONTEXT-STANDARD.md`](../../docs/PROMPT-CONTEXT-STANDARD.md)。

## 整理状态（2026-11-03）

| 项 | 状态 |
|----|------|
| Drive 当场清点 | **380 个文件 · 约 1.77 GiB · 无子文件夹**。比旧清单多 165，删除 0。见 live JSON |
| 类型 | PDF 253 · Markdown 94 · PPTX 14 · DOCX 12 · 表格 6 |
| 本地镜像 | 仍只有先前约 19 个。未打开正文的文件不算已读 |
| 总摘要 MASTER | **不要做。** 总摘录会变成新 Agent 误以为的全文 |

## 已有人工摘录（可先用于 Brief）

- [`2026-11-03-xhs-corpus-extract-seed.md`](./2026-11-03-xhs-corpus-extract-seed.md) — 只覆盖 2 个文件（50 条心得、教培合规导流）。其余文件仍须打开原件。
