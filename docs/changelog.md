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
| 2026-05-25 | — | docs: 更新 README 页面截图，新增系统设置与用户管理界面，并将本地截图改为 GitHub 兼容的 Markdown 图片语法 | Codex | — |
| 2026-05-25 | — | fix: 补充 README 引用的截图资源入库，修复 GitHub 图片无法展示问题 | Codex | — |
| 2026-05-25 | — | docs: 更新 README 系统设置、用户管理与智能助手截图，首页部分改用最新智能助手截图 | Codex | — |
| 2026-05-25 | — | docs: 使用用户提供的截图文件替换 README 展示图片 | Codex | — |
| 2026-05-30 | — | feat: LLM 模型配置动态化，支持用户在系统设置中添加新模型、修改接口地址/名称，智能助手模型列表动态渲染 | Antigravity | — |
| 2026-05-30 | — | feat: 天气服务（Tavily/和风天气）API 密钥及 Host 字段移至数据库（`tool_configs`），移除全局冗余配置表单 | Antigravity | — |
| 2026-05-30 | — | refactor: 重构系统设置，取消独立全局配置，API 继承进具体模型/工具编辑；支持动态渲染真实生效的掩码 API Key；修复侧边栏切换导致会话模型重置回 Kimi 的 Bug 并跑通单元测试；支持对话栏标题在第一条消息后通过 AI 自动总结重命名，并支持手动修改；修复对话模型切换状态无法被持久化和前端缓存导致的重置 Bug | Antigravity | — |
| 2026-05-30 | — | fix: 天气查询工具优先使用 QWeather 结构化多日预报，Tavily 仅作为 fallback，避免“未来七天”只返回单日网页摘要 | Codex | — |
| 2026-05-30 | — | fix: Session 改为数据库持久化并修正前端 401 提示，避免后端热重载后误显示“服务暂时不可用” | Codex | — |

---

## 变更类型说明

- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档更新
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建/工具变更
