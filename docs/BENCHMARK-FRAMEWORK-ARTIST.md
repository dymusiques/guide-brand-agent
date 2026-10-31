---
context_version: "2026-10-30-l012"
repo_path: "docs/BENCHMARK-FRAMEWORK-ARTIST.md"
goal: "Artist 对标四指标 · DB / PLD / APO / CTD"
openwebui_route: "rag_l1"
cursor_route: "read"
content_sha256: "2435f89e3c369a9b"
---

# Artist 对标四指标 · DB / PLD / APO / CTD

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** > **取代 SWOT** 作为 GM10 与 watchlist 筛查的统一框架。实现：`kernels/daily-gm/benchmark_framework.py`
- **Path:** `docs/BENCHMARK-FRAMEWORK-ARTIST.md`
- **Open WebUI:** `rag_l1`
- **Cursor:** `read`

## 章节锚点
- **指标定义（相对 Owner · 张丹瀛 IP）**: | 缩写 | 全称 | 含义 |
- **命令**: ```bash
- **JSON 契约（v0-benchmark.json）**: ```json


---

## L2 正文

# Artist 对标四指标 · DB / PLD / APO / CTD

> **取代 SWOT** 作为 GM10 与 watchlist 筛查的统一框架。实现：`kernels/daily-gm/benchmark_framework.py`

## 指标定义（相对 Owner · 张丹瀛 IP）

| 缩写 | 全称 | 含义 |
|------|------|------|
| **DB** | Directional Benchmarking | 对标对象的战略方向是否与 Owner（法派×跨界×强链接×不绑单品类×AI 可选）**同向** |
| **PLD** | Pixel-Level Deconstruction | 内容 **像素级** 可拆解性：封面、标题、钩子、栏目、CTA、日/周更结构能否迁移执行 |
| **APO** | Audience Persona Overlap | 受众 persona 与 Owner（品牌/艺术/教育/AI）**重叠度**；惩罚纯 vanity |
| **CTD** | Core Topic Density | 核心题 **密度**：专业+跨界+叙事是否集中，而非垂直锁号/跑题 |

**borrow_score** = 加权合成（DB 30% · PLD 25% · APO 25% · CTD 20%）。**P1/P2/P3** = composite ≥72 / ≥58 / 其余。

## 命令

```bash
python scripts/screen-artist-watchlist.py          # 全 watchlist 启发式筛查
python scripts/daily-gm-10-artist-benchmark.py     # 日更 1 人 · Gemini 填四指标
python scripts/merge-artist-intel-catalog.py       # 合并 catalog
```

验收：`kernels/daily-gm/tests/test_benchmark_framework.py` · `test_artist_benchmark_6.py`

## JSON 契约（v0-benchmark.json）

```json
"benchmark_metrics": {
  "directional_benchmarking": {"score": 0, "rationale": "..."},
  "pixel_level_deconstruction": {"score": 0, "rationale": "..."},
  "audience_persona_overlap": {"score": 0, "rationale": "..."},
  "core_topic_density": {"score": 0, "rationale": "..."}
}
```