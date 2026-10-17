# Strategic docs kernel (Agents 02 / 03)

Separate from `kernels/xiaohongshu/line2` (Agent 05 · 小红书笔记).

- Classifier: `line2/is_strategic_doc_aligned.py`
- Verify: `bash scripts/verify-business-brand.sh` · `bash scripts/verify-marketing-campaign.sh`
- Single doc: `python scripts/evaluate-business-brand.py --file …`

Gemini config reuses `kernels/xiaohongshu/config/gemini_config.py` (`.env`).
