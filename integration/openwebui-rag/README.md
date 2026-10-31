# Open WebUI ↔ Drive RAG sync（随仓分发）

**Canonical 路径：** `integration/openwebui-rag/scripts/`（与 GitHub / Cursor Origin 同步）

## 配置

1. 复制 `scripts/brand-drive-sync.env.example` → `scripts/brand-drive-sync.env`（含 `OPENWEBUI_API_KEY`，**勿 commit**）
2. 可选：`export BRAND_KNOWLEDGE_MIRROR=/path/to/brand-knowledge-mirror`  
   默认：若存在 legacy `~/Desktop/未命名/LLM-Ollama/RAG/RAG/brand-knowledge-mirror` 则沿用，否则 `var/brand-knowledge-mirror/`（gitignore）

## 常用命令（在仓库根目录）

```bash
bash scripts/run-context-reorg-pipeline.sh
bash scripts/deploy-learning-stack.sh
python3 integration/openwebui-rag/scripts/verify_openwebui_knowledge_status.py
```
