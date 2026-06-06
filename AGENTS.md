# AGENTS.md

## Project overview

- Purpose: 大语言模型气象业务应用平台，前端提供登录、设置、用户管理和智能气象问答界面，后端提供认证、配置、对话、知识库和天气工具 API。
- Tech stack: Vue 3 + Vite + TypeScript + Pinia + Vue Router on the frontend; FastAPI + SQLAlchemy + SQLite + LangChain on the backend.
- Main entry points: `src/main.ts`, `src/router/index.ts`, `src/views/IntelligentAssistant.vue`, `backend/app/main.py`.
- Key directories: `src/` frontend source, `backend/app/` API source, `backend/tests/` backend regression tests, `docs/` project docs, `scripts/` utility scripts.
- External services: Kimi, DeepSeek, MiniMax, Tavily, QWeather, optional Ollama-compatible local endpoint.

## Setup commands

- Install frontend dependencies: `npm install`.
- Install backend dependencies: `cd backend && python3 -m pip install -r requirements.txt`.
- Run locally: `npm run dev` starts Vite on `http://localhost:5173` and FastAPI on `http://localhost:8000`.
- Run frontend only: `npm run dev:frontend`.
- Run backend only: `npm run dev:backend`.
- Run backend tests: `cd backend && python3 -m pytest`.
- Build frontend: `npm run build`.
- API docs: start backend, then open `http://localhost:8000/docs`.

## Project map

- `src/views/`: page-level Vue views for login, registration, home, settings, user admin, and assistant chat.
- `src/stores/auth.ts`: Pinia auth state and session-aware user loading.
- `backend/app/routers/`: FastAPI route modules for auth, assistant, users, config, model config, and tool config.
- `backend/app/services/`: LLM, conversation, knowledge base, and weather-tool service logic.
- `backend/app/models/` and `backend/app/schemas/`: SQLAlchemy models and Pydantic request/response schemas.
- `backend/tests/`: pytest coverage for assistant defaults, LLM config, weather tool, and security regressions.
- `docs/`: tracked agent workflow/status docs plus README screenshots; generated PDFs belong under `docs/manuals/` and are ignored.
- `scripts/`: PPT generation/checking helpers and Markdown-to-HTML conversion utility.

## Agent notes

- Code style: follow the existing Vue single-file component style and FastAPI service/router split. Keep frontend API calls aligned with the Vite `/api` proxy.
- Security / secrets: never commit `backend/.env`, SQLite files, API keys, cookies, or local logs. Use `backend/.env.example` for variable names.
- Files or directories to avoid: do not edit `node_modules/`, `dist/`, `backend/venv/`, SQLite database files, or generated logs unless explicitly asked.
- Test note: `package.json` has no frontend test script right now; use `npm run build` for frontend type/build validation and `pytest` for backend tests.

<!-- BEGIN: setup-long-term-docs -->

## Lightweight agent workflow

This repository uses a small project memory setup for short-lived projects, scripts, demos, and experiments. Keep the project overview, commands, and directory map above this managed block current.

### Documentation sources of truth

- `docs/project_status.md`: current goal, progress, blockers, checks, and next actions.
- `docs/agent_workflow.md`: lightweight status, commit, and handoff workflow.

### Required rules

- Read the project overview and setup commands in `AGENTS.md` before making changes.
- Read `docs/project_status.md` before making changes when it exists.
- Update `docs/project_status.md` when meaningful progress is made, a blocker appears or is resolved, the next action changes, or work should be resumable later.
- Keep updates short. Do not create extra planning documents unless the user asks.
- Before any git commit, check whether `docs/project_status.md` should be updated.
- Commit only files related to the current work. Do not sweep unrelated files into commits.
- Do not push unless the user explicitly asks or the current task grants push/publish authorization.
- Summarize changed files, checks run, and remaining risks.

### Detailed workflows

For status, commit, and handoff details, read `docs/agent_workflow.md`.

<!-- END: setup-long-term-docs -->
