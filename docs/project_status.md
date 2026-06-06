# Project Status

## Current goal

Goal: Run the project locally for manual inspection.

Status: In progress: dev server is running.

## Done

- Started the project with `npm run dev`.
- Verified frontend root returns HTTP 200 at `http://localhost:5173/`.
- Verified backend health returns `{"status":"ok"}` at `http://localhost:8000/health`.
- Verified FastAPI docs return HTTP 200 at `http://localhost:8000/docs`.
- Removed generated `dist/` after build verification.
- Refreshed `AGENTS.md` with project overview, setup commands, project map, and agent notes.
- Moved root-level local SQLite files, old dev log, and unreferenced `ask1.png` into `.local/archive/2026-06-06-cleanup/`.
- Renamed `docs/3. 用户使用手册.pdf` to `docs/manuals/user_manual.pdf`.
- Moved `docs/md_to_pdf.py` to `scripts/md-to-html.py` and made it accept input/output arguments.
- Updated `.gitignore` so `docs/project_status.md` and `docs/agent_workflow.md` can be tracked while generated PDFs remain ignored.
- Updated `README.md` to match the current lightweight docs layout.
- Ran frontend build successfully.

## In progress

- User inspection of the running app.

## Blocked / Questions

- Full `git diff --check` currently fails on unrelated whitespace in `backend/app/routers/assistant.py`.
- `backend/app/routers/assistant.py` and `backend/app/schemas/assistant.py` have pre-existing or external edits outside this cleanup.

## Checkpoints

- Ran setup-light initialization script.
- Preserved archived local files instead of deleting them.
- Confirmed the remaining root `index.html`, `package*.json`, and `tsconfig*.json` files are standard Vite/TypeScript project files.
- Verified edited cleanup files with `git diff --check -- .gitignore README.md AGENTS.md CLAUDE.md docs/project_status.md docs/agent_workflow.md scripts/md-to-html.py`.
- Ran `python3 -m py_compile scripts/md-to-html.py scripts/check-ppt.py`.
- Ran `npm run build`.

## Next actions

1. Review `.local/archive/2026-06-06-cleanup/` and delete it later if the archived files are no longer needed.
2. Stop the dev server after inspection.
3. Review the unrelated backend edits before committing.
