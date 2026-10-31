---
context_version: "2026-10-30-l012"
repo_path: "kernels/xiaohongshu/docs/02-gemini-and-functions.md"
goal: "Gemini 调用方式与函数说明"
openwebui_route: "rag_l2"
cursor_route: "read"
content_sha256: "9ef46e23b2a4f2ac"
---

# Gemini 调用方式与函数说明

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** ```bash
pip install -r requirements-gemini.txt
```
- **Path:** `kernels/xiaohongshu/docs/02-gemini-and-functions.md`
- **Open WebUI:** `rag_l2`
- **Cursor:** `read`

## 章节锚点
- **依赖与环境**: ```bash
- **调用逻辑（对齐 demo / 课纲）**: 1. 用 `inspect.getdoc(is_xhs_growth_aligned)` 取得 **分类规则**（与对外文档同源）。
- **命令行 demo**: ```bash
- **函数 API**
- **在 Python 中调用示例**: ```python
- **验收**: ```bash


---

## L2 正文

# Gemini 调用方式与函数说明

## 依赖与环境

```bash
pip install -r requirements-gemini.txt
```

| 变量 | 位置 | 说明 |
|------|------|------|
| `GEMINI_API_KEY` | `Guide/0/.env` | 必填；勿提交 Git |
| `GEMINI_MODEL` | `.env` 可选 | 默认 `gemini-3.5-flash`（`config/gemini_config.py`） |

加载顺序：`.env`（dotenv）→ 可选 `.local-config.json` → 进程环境变量。

## 调用逻辑（对齐 demo / 课纲）

1. 用 `inspect.getdoc(is_xhs_growth_aligned)` 取得 **分类规则**（与对外文档同源）。
2. 拼接 prompt：规则 + 待判定的 `Subject` / `Body` + 「首行仅 yes 或 no」。
3. `genai.Client(api_key=...).models.generate_content(...)`  
   - `temperature=0`  
   - `max_output_tokens=256`（避免空 `response.text`）  
4. `_parse_yes_no(response.text)` → `yes` / `no`；解析失败最多 **3 次**重试。  
5. `yes` → `True`，`no` → `False`。

**边界：** `subject` 与 `body` 均为空时 **不调用 API**，直接返回 `False`。

参考实现：`line2/is_xhs_growth_aligned.py` 中 `_build_gemini_prompt`、`_call_gemini_yes_no`。

## 命令行 demo

```bash
.venv/bin/python kernels/xiaohongshu/examples/demo.py
```

打印 JSON，字段含 `subject`、`body`、`aligned`。

## 函数 API

### `normalize_xhs_content(content: Any) -> dict[str, str]`

- 强制输出 `{"subject": str, "body": str}`。  
- 非 dict 输入按空处理；非 str 字段 `str()` 化。

### `is_xhs_growth_aligned(content: dict) -> bool`

- **参数：** `content` 含 `subject`、`body`（建议先 normalize）。  
- **返回：** 是否对齐 IP / 涨粉 / 强链接目标。  
- **异常：** 缺 Key → `RuntimeError`；多次无法解析 yes/no → `ValueError`。  
- **规则全文：** 见该函数 **docstring**（Personal IP、Audience、Strong link、Growth intent；歧义以 **body** 为准）。

### `evaluate_xhs_growth_content(content: dict) -> dict`

- **返回：**  
  ```python
  {"subject": str, "body": str, "aligned": bool}
  ```  
- 供 Topic Manager 管线统一落盘 / 日志。

## 在 Python 中调用示例

```python
from line2.is_xhs_growth_aligned import evaluate_xhs_growth_content

note = {
    "subject": "标题",
    "body": "正文含专业价值与私信/合作 CTA",
}
print(evaluate_xhs_growth_content(note))
```

（从仓库根跑 demo 时，`examples/demo.py` 已把 `kernels/xiaohongshu` 加入 `sys.path`。）

## 验收

```bash
bash scripts/verify-xhs-topic.sh
```

期望：`cases: 6 passed, 0 failed` 且 `RESULT: PASS`。