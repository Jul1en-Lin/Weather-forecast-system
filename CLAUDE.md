# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

大语言模型气象业务应用平台前端——基于 Vue 3 + Vite + TypeScript 的单页应用，提供气象智能助手对话界面。

## 常用命令

```bash
# 开发服务器
npm run dev

# 生产构建
npm run build

# 预览构建产物
npm run preview
```

本项目未配置 lint 或 test 脚本。TypeScript 检查内置于构建流程：`vue-tsc -b && vite build`。

## 技术栈

- Vue 3（Composition API + `<script setup>`）
- Vue Router（history 模式）
- Pinia（状态管理）
- Vite（构建工具）
- TypeScript（严格模式，启用 `noUnusedLocals` 和 `noUnusedParameters`）

## 架构要点

### 路由与认证

- `src/router/index.ts`：定义了 `/login`、`/home`、`/intelligent-assistant` 三条主路由，根路径重定向到 `/login`。
- 导航守卫 `beforeEach` 检查 `meta.requiresAuth`，未认证用户重定向到登录页，已认证用户访问登录页则重定向到首页。
- 认证状态通过 Pinia `auth` store 管理，并持久化到 `localStorage`。

### 状态管理

- `src/stores/auth.ts`：使用 Pinia Setup Store 管理登录状态。`login()` 写入 `localStorage`，`checkAuth()` 从 `localStorage` 恢复状态。当前为模拟登录（用户名密码非空即可）。

### 智能助手对话

- `src/views/IntelligentAssistant.vue` 是核心功能页面，包含：
  - 历史对话侧边栏（创建、切换、删除对话）
  - 模型选择（deepseek-32b / qwen-32b）
  - 知识库与工具多选
  - 流式消息展示（当前为 `mockStreamReply` 模拟，待后端接入）
- 对话数据全部持久化到 `localStorage`（`assistant_conversations`、`assistant_currentConvId`）。
- 后端 API 契约定义在 `openapi.yaml` 中，路径前缀 `/api/v1/assistant`，包含模型列表、知识库、工具、流式对话 `/chat/stream`（SSE）等端点。

### 样式体系

- `src/style.css` 定义全局 Apple 风格设计令牌：CSS 变量（`--apple-blue`、`--apple-gray` 等）、圆角、阴影、滚动条、工具类。
- 各视图组件使用大量 `scoped` CSS，导航栏样式在 `Home.vue` 和 `IntelligentAssistant.vue` 中分别维护（存在重复）。

## 重要文件

| 文件 | 说明 |
|------|------|
| `src/main.ts` | 应用入口，挂载 Vue + Pinia + Router |
| `src/router/index.ts` | 路由定义与导航守卫 |
| `src/stores/auth.ts` | 认证状态管理 |
| `src/views/IntelligentAssistant.vue` | 智能助手主页面（核心功能） |
| `openapi.yaml` | 后端 API 规格说明（OpenAPI 3.0） |
| `.env` | 环境变量模板（含数据库、AI API、天气 API 配置），实际值需本地填写 |

## 注意事项

- 当前无真实后端对接，LLM 回复由 `mockStreamReply` 模拟生成。接入后端后需替换为调用 `openapi.yaml` 中定义的 `/chat/stream` SSE 接口。
- `tsconfig.app.json` 启用 `strict` 与 `noUnusedLocals`/`noUnusedParameters`，未使用的变量会导致构建失败。
- 项目未配置 ESLint / Prettier / 测试框架。

## 开发核心准则 (Development Core Guidelines)

1. **文档更新义务**：在项目完成里程碑或主要新增内容后，更新 `docs/project_spec.md` 文件，确保规格说明与实现保持同步。

2. **提交规范**：在 git 进行提交时使用 `/update-docs-and-commit` 命令，自动将变更摘要记录到文档并生成规范的 commit message。

3. **规格溯源原则**：所有的逻辑实现必须溯源至 `docs/project_spec.md`。若代码实现与规格说明不符，以规格说明为准；若需要修改规格，必须先询问用户是否要更新文档，获得确认后再修改代码。

## Project Rules

### 文档更新规则

1. **架构对齐**：每当引入新的第三方库、修改核心类交互或调整数据库模式时，必须同步更新 `docs/architecture.md`。

2. **变更溯源**：每次 Git 提交前，需在 `docs/changelog.md` 中追加一条简要变更记录。

3. **进度锚定**：在每个任务（Issue）开始前，先读取 `docs/project_status.md` 确认当前里程碑；任务完成后，更新该文件的"已完成工作"与"待办与后续计划"部分。
