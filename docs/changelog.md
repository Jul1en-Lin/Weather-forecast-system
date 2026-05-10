# 变更日志 (Changelog)

本文档记录项目的所有重要变更。

## 版本记录

| 日期 | 版本 | 变更项 | 作者 | 关联 Issue |
|-----|-----|-------|-----|-----------|
| 2026-04-17 | — | feat: 完整后端实现（FastAPI + SQLAlchemy + LangChain + SSE 流式对话） | Claude | — |
| 2026-04-18 | — | fix: 修复 MiniMax 天气工具调用报 400（chat content is empty）；feat: 实现预警查询工具并补充示例数据 | Claude | #2 |
| 2026-04-19 | — | fix: 过滤 MiniMax SSE 流式回复中的 `<think>` 思维链标签；新增 `ThinkingFilter` 流式过滤器与 `strip_thinking_tags` 工具函数 | Claude | #1 |
| 2026-04-23 | — | fix: 系统提示词注入当前日期；TavilySearch 查询词增强拼接日期地点；alert_query 接入 QWeather 实时预警 API（fallback 到 DB 定义）；搜索结果结构化后处理；增加工具调用日志 | Claude | #3 |
| 2026-04-23 | — | config: 支持 QWeather 私有部署 API Host 配置；修复预警响应字段 `adcode` → `sender`；新增 `QWEATHER_API_HOST` 环境变量 | Claude | — |
| 2026-05-09 | — | refactor: 数据库从 MySQL 迁移到 SQLite（移除 PyMySQL 依赖，SQLAlchemy 自动适配；`Enum` → `String`；手动管理 `updated_at`；添加 PRAGMA foreign_keys/WAL） | Claude | — |
| 2026-05-09 | — | feat: 集成 `concurrently` 实现 `npm run dev` 一键启动前后端；添加 Vite API 代理配置；前端改用相对路径调用后端 API | Claude | — |
| 2026-05-10 | — | feat: 新增用户注册功能（`POST /api/v1/auth/register`）；新增用户管理页面（管理员可查看、修改权限、删除用户）；新增 is_admin 字段到用户表 | Claude | — |
| 2026-05-10 | — | feat: 新增系统设置页面，支持在前端配置 LLM API Keys（Kimi/DeepSeek/MiniMax/Ollama）和天气服务配置（Tavily/和风天气）；所有已登录用户均可修改配置 | Claude | — |
| 2026-05-10 | — | style: 统一所有页面背景样式，使用 `/background.jpg` 图片 + 玻璃模糊效果（`backdrop-filter: blur`）；登录/注册页使用玻璃质感卡片设计；Settings.vue 和 AdminUsers.vue 采用与首页一致的框架布局；卡片透明度调整为 20% 白色 + 模糊效果 | Claude | — |

---

## 变更类型说明

- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档更新
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建/工具变更
