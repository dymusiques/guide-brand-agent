---
context_version: "2026-10-30-l012"
repo_path: "kernels/strategic_docs/README.md"
goal: "Strategic docs kernel (Agents 02 / 03)"
openwebui_route: "rag_l2"
cursor_route: "read"
content_sha256: "d108fcbf9675d635"
---

# Strategic docs kernel (Agents 02 / 03)

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** Separate from `kernels/xiaohongshu/line2` (Agent 05 · 小红书笔记).
- **Path:** `kernels/strategic_docs/README.md`
- **Open WebUI:** `rag_l2`
- **Cursor:** `read`


---

## L2 正文

# Strategic docs kernel (Agents 02 / 03)

Separate from `kernels/xiaohongshu/line2` (Agent 05 · 小红书笔记).

- Classifier: `line2/is_strategic_doc_aligned.py`
- Verify: `bash scripts/verify-business-brand.sh` · `bash scripts/verify-marketing-campaign.sh`
- Single doc: `python scripts/evaluate-business-brand.py --file …`

Gemini config reuses `kernels/xiaohongshu/config/gemini_config.py` (`.env`).