#!/usr/bin/env python3
"""Run Open WebUI RAG / Pipe and write Desktop outbox + integration/handoff job JSON."""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAG_SCRIPTS = ROOT / "integration/openwebui-rag/scripts"
sys.path.insert(0, str(RAG_SCRIPTS))

from openwebui_sync_lib import OpenWebUIClient, cfg, load_env  # noqa: E402

DEFAULT_ENV = RAG_SCRIPTS / "brand-drive-sync.env"
OUTBOX_IP = Path.home() / "Desktop/Open WebUI Personal IP/outbox"
OUTBOX_WEB = Path.home() / "Desktop/Open WebUI Fluid Body/outbox"
JOBS_DIR = ROOT / "integration/handoff/openwebui-jobs"

PIPE_MODELS = {
    "PIPE_COT": "yage_cot.yage/yage-outline",
    "PIPE_DILIGENT": "yage_long_context.yage/yage-long-context",
    "HYBRID": "yage_cot.yage/yage-outline",
}


def chat(
    client: OpenWebUIClient,
    *,
    model: str,
    user_content: str,
    knowledge_id: str | None,
) -> str:
    body = {
        "model": model,
        "messages": [{"role": "user", "content": user_content}],
        "stream": False,
    }
    if knowledge_id:
        body["metadata"] = {"files": [{"type": "collection", "id": knowledge_id}]}
    res = client._request("POST", "/api/chat/completions", data=body)
    try:
        return res["choices"][0]["message"]["content"] or ""
    except (KeyError, IndexError, TypeError) as e:
        raise RuntimeError(f"Unexpected chat response: {res!r}") from e


def read_intake(path: str | None) -> tuple[str | None, str | None]:
    if not path:
        return None, None
    p = Path(path).expanduser()
    if not p.is_file():
        raise FileNotFoundError(f"intake not found: {p}")
    text = p.read_text(encoding="utf-8").strip()
    rel = str(p) if not p.is_absolute() else str(p)
    try:
        rel = str(p.relative_to(ROOT))
    except ValueError:
        pass
    return rel, text


def build_user_prompt(
    goal: str,
    route: str,
    *,
    intake_rel: str | None = None,
    intake_body: str | None = None,
    rag_context: str | None = None,
) -> str:
    disambig = (
        "术语（Must）：\n"
        "- `personal-ip` = Owner 个人 IP 品牌项目（法派长笛 × 跨界策划），**不是** intellectual property 知识产权。\n"
        "- 句中「E2E workflow test」= 本次 CEO→Open WebUI 流程测试任务名，**不是** 软件 QA 的端到端测试科普。\n"
        "- 受众：LinkedIn / 系列深度口播；语气：专业、具体、可拍可发；**先观点后产品**。\n\n"
    )
    base = f"Owner/CEO 目标：\n{goal.strip()}\n\n{disambig}"
    if intake_body:
        base += f"## Intake 源稿（Must 遵循，勿忽略）\n路径：`{intake_rel}`\n\n{intake_body}\n\n"
    if rag_context:
        base += f"## 品牌库 RAG 事实要点（Must 引用或对齐）\n{rag_context.strip()}\n\n"
    if route in ("PIPE_COT", "HYBRID"):
        return (
            base
            + "请用中文：先给出 **LinkedIn 系列深度口播** 的 Markdown 分节提纲（含每节 hook），"
            + "再按提纲分节深入写作，最后合并为完整文稿。"
            + "必须体现法派长笛 × 跨界品牌策划；不要写泛化的 KPI/知识产权/软件测试说明。"
            + "不要省略例子；若某节过长可分段但不可跳过章节。"
        )
    if route == "PIPE_DILIGENT":
        return (
            base
            + "内容可能很长：请采用分而治之，逐段处理，完整输出，不要跳过段落或只写摘要。"
        )
    return base + goal


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--route", required=True, choices=["RAG_ONLY", "PIPE_COT", "PIPE_DILIGENT", "HYBRID", "SKIP"])
    parser.add_argument("--goal", "-g", required=True)
    parser.add_argument("--slug", required=True)
    parser.add_argument("--platform", default="personal_ip", choices=["personal_ip", "website"])
    parser.add_argument("--env", type=Path, default=DEFAULT_ENV)
    parser.add_argument("--brief", default="")
    parser.add_argument("--intake", type=Path, default=None, help="Markdown intake to inject into prompt")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if args.route == "SKIP":
        print("SKIP: nothing to run")
        return 0

    outbox_root = OUTBOX_WEB if args.platform == "website" else OUTBOX_IP
    outbox_root.mkdir(parents=True, exist_ok=True)
    JOBS_DIR.mkdir(parents=True, exist_ok=True)

    job_path = JOBS_DIR / f"{args.slug}.json"
    md_path = outbox_root / f"{args.slug}.md"

    job = {
        "version": 1,
        "slug": args.slug,
        "route": args.route,
        "platform": args.platform,
        "goal": args.goal,
        "brief_path": args.brief or None,
        "intake_path": str(args.intake) if args.intake else None,
        "outbox_md": str(md_path),
        "status": "pending",
        "updated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }

    if args.dry_run:
        job["status"] = "dry_run"
        job_path.write_text(json.dumps(job, ensure_ascii=False, indent=2), encoding="utf-8")
        print(json.dumps(job, ensure_ascii=False, indent=2))
        return 0

    env = load_env(args.env)
    client = OpenWebUIClient.from_env(env)
    kb_name = cfg(env, "KNOWLEDGE_NAME", "brand-ip-knowledge")
    kb_id = client.knowledge_id_by_name(kb_name)
    rag_model = (
        cfg(env, "OPENWEBUI_RAG_MODEL", "")
        or cfg(env, "OPENWEBUI_PIPE_MODEL", "")
        or "deepseek/deepseek-v4.1-flash-1017"
    )

    intake_rel, intake_body = read_intake(str(args.intake) if args.intake else None)

    try:
        if args.route == "RAG_ONLY":
            if not rag_model:
                raise RuntimeError("Set OPENWEBUI_RAG_MODEL in brand-drive-sync.env")
            model = rag_model
            prompt = build_user_prompt(
                args.goal, "RAG_ONLY", intake_rel=intake_rel, intake_body=intake_body
            )
            content = chat(client, model=model, user_content=prompt, knowledge_id=kb_id)
        else:
            model = PIPE_MODELS[args.route]
            rag_context = None
            if args.route == "HYBRID":
                rag_q = (
                    f"{args.goal}\n\n"
                    "请仅从知识库列出与上述目标相关的可引用事实要点（bullet，中文，≤12 条）。"
                )
                rag_context = chat(
                    client, model=rag_model, user_content=rag_q, knowledge_id=kb_id
                )
                job["rag_prefetch"] = True
            pipe_route = "PIPE_COT" if args.route == "HYBRID" else args.route
            prompt = build_user_prompt(
                args.goal,
                pipe_route,
                intake_rel=intake_rel,
                intake_body=intake_body,
                rag_context=rag_context,
            )
            content = chat(client, model=model, user_content=prompt, knowledge_id=kb_id)

        header = (
            f"---\n"
            f"slug: {args.slug}\n"
            f"route: {args.route}\n"
            f"model: {model}\n"
            f"knowledge: {kb_name}\n"
            f"generated_at: {job['updated_at']}\n"
            f"---\n\n"
        )
        md_path.write_text(header + content.strip() + "\n", encoding="utf-8")
        job["status"] = "done"
        job["model"] = model
        job["knowledge"] = kb_name
        job_path.write_text(json.dumps(job, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Wrote {md_path}")
        print(f"Job {job_path}")
        return 0
    except urllib.error.HTTPError as e:
        job["status"] = "failed"
        job["error"] = e.read().decode()[:2000]
        job_path.write_text(json.dumps(job, ensure_ascii=False, indent=2), encoding="utf-8")
        print(job["error"], file=sys.stderr)
        return 1
    except Exception as e:
        job["status"] = "failed"
        job["error"] = str(e)[:2000]
        job_path.write_text(json.dumps(job, ensure_ascii=False, indent=2), encoding="utf-8")
        print(str(e), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
