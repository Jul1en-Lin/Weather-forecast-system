# Project Status

## Current goal

Goal: Add Weather Oracle page with tarot-based weather interpretation.

Status: Weather Oracle frontend and backend code is implemented. Figma tarot asset export is blocked by the Figma MCP Starter plan tool-call limit.

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
- Wrote implementation plan at `docs/superpowers/plans/2026-06-06-weather-oracle.md`.
- Confirmed Figma tarot source file `Ekroehh3gLkbPnj2raccJH` contains 78 card nodes under `All Cards`.
- Added Weather Oracle page and compact oracle components for city draw, tarot display, metric cards, mood guide, and contextual chat.
- Weather Oracle page now restores same-day localStorage readings per username and drops stale readings by Shanghai date.
- Added `/oracle` route and Weather Oracle navigation shell.
- Added dark/light Weather Oracle theme variables and a theme toggle in the Oracle layout.
- Restyled the Weather Oracle page into a dense dashboard with tarot, fortune, metric, mood, and right-side chat areas.
- Added a temporary `tarotAssetsReady = false` guard so missing tarot PNGs do not create broken image requests before real Figma assets are exported.
- Verified the Weather Oracle page at desktop 1440px and mobile 390px with a same-day cached reading: dashboard renders, mobile nav text is hidden, mobile theme toggle is visible, mobile phase icons are hidden, no horizontal overflow appears, and no `/tarot/cards/` requests are made while assets are unavailable.

## In progress

- Figma tarot asset export follow-up.

## Blocked / Questions

- Figma MCP metadata access now works again for file `Ekroehh3gLkbPnj2raccJH`.
- Figma PNG export is blocked by the Figma MCP Starter plan tool-call limit: `You've reached the Figma MCP tool call limit on the Starter plan. Upgrade your plan for more tool calls`.

## Checkpoints

- Ran setup-light initialization script.
- Preserved archived local files instead of deleting them.
- Confirmed the remaining root `index.html`, `package*.json`, and `tsconfig*.json` files are standard Vite/TypeScript project files.
- Verified edited cleanup files with `git diff --check -- .gitignore README.md AGENTS.md CLAUDE.md docs/project_status.md docs/agent_workflow.md scripts/md-to-html.py`.
- Ran `python3 -m py_compile scripts/md-to-html.py scripts/check-ppt.py`.
- Ran `npm run build`.
- Ran `npm run build` after Task 7 page/component implementation.
- Ran `npm run build` after Task 9 theme implementation.
- Ran `git diff --check -- src/styles/oracle-theme.css src/style.css src/layouts/OracleLayout.vue src/views/WeatherOracle.vue src/components/oracle`.
- Ran `npm run build` after Task 9 review fixes.
- Ran `git diff --check`.
- Ran `PYTHONPATH=backend backend/venv/bin/python -m pytest backend/tests -q` (`22 passed, 4 warnings`).
- Ran Chrome DevTools layout checks for `/oracle` at 1440x900 and 390x844 after logging in as `admin` and loading a same-day cached reading.

## Next actions

1. Review `.local/archive/2026-06-06-cleanup/` and delete it later if the archived files are no longer needed.
2. Retry Figma export for 78 tarot PNG assets from file `Ekroehh3gLkbPnj2raccJH` after MCP quota is available, then place them under `public/tarot/cards/`.
3. Flip `tarotAssetsReady` to `true` in `src/data/tarotCards.ts` after the real PNGs exist and rerun `npm run build` plus the `/oracle` browser checks.
