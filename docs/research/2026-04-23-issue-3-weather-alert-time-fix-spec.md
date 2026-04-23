# Issue #3 修复规范：天气/预警查询工具时间准确性

> 对应 GitHub Issue: #3 — 天气/预警查询工具返回过时或不准确的时间信息
> 日期: 2026-04-23

---

## 1. 问题概述

用户询问"今天天气"时，LLM 返回的时间信息不正确（如返回 2025 年 11 月的历史数据）。核心根因：
- 系统提示词缺少当前日期上下文
- TavilySearch 查询词未限定日期与地点
- `alert_query` 工具仅查询静态 DB，无实时预警数据
- 搜索结果未做结构化后处理

---

## 2. 修复目标

| 编号 | 目标 | 优先级 |
|------|------|--------|
| T1 | 系统提示词动态注入当前日期 | P0 |
| T2 | TavilySearch 查询词强制拼接日期+地点 | P0 |
| T3 | `alert_query` 接入实时预警数据源 | P1 |
| T4 | 搜索结果结构化后处理（带时间标注） | P1 |
| T5 | 增加工具调用日志记录 | P2 |

---

## 3. 详细规范

### 3.1 系统提示词注入当前日期 (T1)

**文件**: `backend/app/routers/assistant.py`

- 在构建 `system_parts` 后，使用 `datetime.now()` 获取当前日期时间
- 格式: `今天是 {year} 年 {month} 月 {day} 日，{weekday}。`
- 星期映射: Monday→星期一, ..., Sunday→星期日
- 将该字符串追加到 `system_parts` 列表
- 最终 prompt (`final_prompt_parts`) 中也包含该日期信息

### 3.2 TavilySearch 查询词优化 (T2)

**文件**: `backend/app/services/weather_tool.py`, `backend/app/routers/assistant.py`

- 调用 `tavily_search` 时，构造增强查询词: `{原始查询} {当前日期} 天气`
- 当前日期格式: `YYYY年M月D日`
- 增强后查询词传给 `tool_service.ainvoke({"query": enhanced_query})`

### 3.3 alert_query 实时预警实现 (T3)

**文件**: `backend/app/services/weather_tool.py`

- 保留现有 `_query_alerts` 作为 fallback（防御指南查询）
- 新增 `_fetch_realtime_alerts(location: str = "") -> str` 函数
- 实时预警数据源：优先使用 QWeather 预警 API，fallback 到现有 DB 查询
- 新增可选配置项 `QWEATHER_API_KEY` 到 `config.py`
- 返回格式化字符串，包含：预警类型、级别、发布时间、影响区域、防御建议
- 无 API key 或 API 失败时，返回 DB 定义信息并附注"（以上为预警信号标准定义，非实时预警）"

### 3.4 搜索结果后处理 (T4)

**文件**: `backend/app/services/weather_tool.py`

- 新增 `format_search_results(result) -> str` 替代 `format_tool_result`
- 解析 Tavily 返回列表，提取 `title`, `url`, `content`, `published_date`
- 输出格式：
```
【天气搜索结果】
1. {title}（{published_date or '时间未知'}）
   来源：{url}
   摘要：{content[:500]}
```
- 限制每条内容长度 <= 500 字符

### 3.5 工具调用日志 (T5)

**文件**: `backend/app/routers/assistant.py`

- 引入 `import logging` 和 `logger = logging.getLogger(__name__)`
- 记录工具调用: `logger.info("Tool call: %s, args: %s", tool_name, tool_args)`
- 记录工具结果: `logger.info("Tool result: %s...", result_text[:200])`
- 异常时: `logger.exception("Tool execution failed: %s", tool_name)`

---

## 4. 代码变更文件清单

| 文件 | 变更类型 | 说明 |
|------|---------|------|
| `backend/app/routers/assistant.py` | 修改 | 日期注入、查询词增强、日志、alert_query 调用 |
| `backend/app/services/weather_tool.py` | 修改 | 实时预警、搜索结果后处理 |
| `backend/app/config.py` | 修改 | 新增可选 `qweather_api_key` |
| `docs/project_spec.md` | 更新 | FR-005 补充时间上下文注入规范 |

---

## 5. 验证标准

1. 系统提示词包含当前日期
2. TavilySearch 查询词包含当前日期
3. `alert_query` 被勾选时后端实际调用工具
4. 搜索结果返回结构化文本
5. 用户询问"今天天气"时返回与当前日期匹配的信息
