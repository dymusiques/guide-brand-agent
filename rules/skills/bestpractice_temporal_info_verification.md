# 时间敏感信息验证

> **上游：** [grapeot/context-infrastructure · bestpractice_temporal_info_verification.md](https://github.com/grapeot/context-infrastructure/blob/main/rules/skills/bestpractice_temporal_info_verification.md)（standalone 拷贝。）  
> **本仓边界：** 认知期 **品牌 Brief** 速查仍见 [content/xiaohongshu/PIPELINE.md](../../content/xiaohongshu/PIPELINE.md#时间敏感表述摘录--temporal)；**听见 Daily**、脚本/model 名、强资讯向内容 **以本文为准**。

## 元数据

- **类型**: BestPractice
- **适用场景**: 日期、档期、版本号、「最新/刚发布」、技术产品功能更新
- **本仓安装**: 2026-10-19

## 背景

AI 模型有 knowledge cutoff，可能错过之后发布的新版本、新功能、新产品。遇到可能是时间敏感的信息时，**不应仅凭训练数据判断**，应主动验证或标注不确定。

## 触发条件

- 模型名称/版本号（Gemini、Claude、GPT 等）
- 软件/框架/库版本
- API 端点或参数
- 已知产品的功能更新
- 演出/展览/发行 **具体日期**、「今日/最新」类表述

## 做法

1. **不要直接否定**：Owner 或代码里的版本号可能确实存在。
2. **验证**：用本仓可用检索（Cursor **WebSearch** / **WebFetch** / Owner 提供的官方链接）；未安装 [tavily-skill](https://github.com/grapeot/tavily-skill) 时 **不要** 假设有 Tavily CLI。
3. **给出准确信息**：完整版本号、发布日期（如有）；无法确认时用 `[待核实]` 或交 Owner 定稿。
4. **写进 Brief 前**：与 [check.md](../../check.md) 及 PIPELINE temporal 表一致。

## 搜索模板

```text
{产品名} {版本号} release date
{产品名} {版本号} official announcement
{艺术家/活动名} {日期} official
```

## 案例（摘要）

代码中出现看似「太新」的 Gemini 模型名时，应先检索是否已发布及 **完整后缀**（如 `-preview`），而非断定用户写错。

## 物理锚点校验

对 **数值、规格、因果** 做常识量级检查（单位、数量级、是否违背基本物理/行业常识）。异常时要求重新检索或标注不确定，**不**硬写进定稿。

## 验收标准

- 定稿中出现的关键日期/版本/「最新」主张，均有 **来源** 或 **`[待核实]`**。
- 未把 cutoff 时代的猜测写成事实。
- 听见 Daily / 资讯向稿件在发布前至少核对 **1 个** 可引用来源（或 Owner 明示免核）。
