# 变更日志 (Changelog)

本文档记录项目的所有重要变更。

## 版本记录

| 日期 | 版本 | 变更项 | 作者 | 关联 Issue |
|-----|-----|-------|-----|-----------|
| 2026-04-17 | — | feat: 完整后端实现（FastAPI + SQLAlchemy + LangChain + SSE 流式对话） | Claude | — |
| 2026-04-18 | — | fix: 修复 MiniMax 天气工具调用报 400（chat content is empty）；feat: 实现预警查询工具并补充示例数据 | Claude | #2 |
| 2026-04-19 | — | fix: 过滤 MiniMax SSE 流式回复中的 `<think>` 思维链标签；新增 `ThinkingFilter` 流式过滤器与 `strip_thinking_tags` 工具函数 | Claude | #1 |

---

## 变更类型说明

- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档更新
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建/工具变更
