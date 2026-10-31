#!/usr/bin/env bash
# Full pipeline: L0/L1/L2 export → Open WebUI Knowledge → HTML handback to Owner.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
RAG="/Users/danying/Desktop/未命名/LLM-Ollama/RAG/RAG/scripts"

python3 "$ROOT/scripts/reorganize-brand-corpus-l012.py" --apply-repo
python3 "$RAG/fix_openwebui_rag_ollama_url.py"
python3 "$RAG/setup_cursor_brand_corpus_knowledge.py"
python3 "$RAG/sync_cursor_brand_corpus_to_openwebui.py" --tier all
python3 "$RAG/sync_agent_prompt_pack_to_openwebui.py"
bash "$ROOT/scripts/export-workflow-automation-pack.sh"
python3 "$RAG/setup_workflow_automation_pack_knowledge.py"
python3 "$RAG/sync_workflow_automation_pack_to_openwebui.py"
python3 "$RAG/verify_openwebui_knowledge_status.py"
bash "$ROOT/scripts/verify-workflow-automation.sh"
python3 "$ROOT/scripts/build-context-reorg-pipeline-html.py"
open -a "Google Chrome" "$ROOT/content/evolution/00-manager/ceo-inbox/CONTEXT-REORG-PIPELINE-LATEST.html"
echo "CONTEXT-REORG-PIPELINE: OK"
