# Project Status

## Current goal

Goal: Add Weather Oracle page with tarot-based weather interpretation.

Status: Weather Oracle frontend, backend, and tarot assets are implemented and verified.

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
- Generated 78 tarot card PNG assets under `public/tarot/cards/` from the manually exported Figma group images in `docs/images/78 Tarot Cards (Community)`.
- Enabled tarot card image loading in `src/data/tarotCards.ts` and adjusted the card display ratio to match the exported PNGs.
- Verified the Weather Oracle page loads a real tarot PNG at desktop 1440px and mobile 390px without fallback or horizontal overflow.

## In progress

- None.

## Notes

- Figma MCP metadata access now works again for file `Ekroehh3gLkbPnj2raccJH`.
- Figma PNG export through MCP still hits the Starter plan tool-call limit: `You've reached the Figma MCP tool call limit on the Starter plan. Upgrade your plan for more tool calls`.
- This no longer blocks the current implementation because the user manually exported the source images and the local PNG assets were generated from those files.

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
- Verified `public/tarot/cards/` contains exactly 78 PNGs matching the tarot manifest, each at `500x836`.
- Ran `npm run build` after enabling tarot assets.
- Ran `git diff --check` after enabling tarot assets.
- Ran Chrome DevTools layout checks for `/oracle` at 1440x900 and 390x844 with cache disabled; `major-17-star.png` loaded as `image/png` with HTTP 200 and natural size `500x836`.

## Next actions

1. Review `.local/archive/2026-06-06-cleanup/` and delete it later if the archived files are no longer needed.
2. Inspect the app manually at `http://localhost:5173/oracle`.
