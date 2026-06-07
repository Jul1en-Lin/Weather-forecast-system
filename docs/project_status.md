# Project Status

## Current goal

Goal: Keep Weather Oracle daily tarot fixed while city changes update weather data.

Status: Daily tarot now stays fixed per user and Shanghai date; city switching returns weather data without the request-failed banner, even when the model returns a non-schema JSON shape or times out.

## Done

- Polished notice/error banner slide-fade transitions in WeatherOracle.vue to add slide up/down motion using a premium ease-out bezier.
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
- Generated, optimized (resized to 512x512, converted to true PNG, compressed to ~456KB), and saved the dark mode background texture asset under `public/mystical_bg_dark.png`.
- Generated, optimized (resized to 512x512, converted to true PNG, compressed to ~405KB), and saved the light mode background texture asset under `public/mystical_bg_light.png`.
- Integrated tarot background patterns (`mystical_bg_dark.png` and `mystical_bg_light.png`) as smooth-transitioning pseudo-element overlays under default (dark) and light themes in the Oracle layout.
- Removed the old grid background pattern from `OracleLayout.vue` to allow mystical tarot backgrounds to stand out cleanly.
- Verified frontend build and layout compilation, and checked branch changes against `ab970dc` (Task 4).
- Processed light mode background pattern image `public/mystical_bg_light.png` to be a transparent PNG with `#efdac9` color lines, resizing it to 512x512 and optimizing file size (~208KB).
- Updated light theme variables (off-white base `#fefcf8` and semi-transparent `#fdf9f3` card backgrounds) in `src/styles/oracle-theme.css`.
- Updated opacity of light mode pattern in `src/layouts/OracleLayout.vue` to 0.85.
- Ran frontend build and backend tests verifying that everything compiles successfully and passes with no regressions.
- Found that `Invalid port: ':1'` came from httpx parsing `NO_PROXY` entries containing raw IPv6 loopback values (`::1`, `::1/128`) while creating the LangChain/OpenAI-compatible client.
- Added an LLM-service compatibility wrapper that temporarily removes httpx-incompatible `NO_PROXY` entries only during ChatOpenAI client creation, then restores the original environment.
- Added a backend regression test covering `NO_PROXY=127.0.0.1,localhost,::1,127.0.0.0/8,::1/128`.
- Removed trailing whitespace from the frontend files changed by the recent UI pass.
- Found the Weather Oracle city picker failure had the same root cause as the chat bug: QWeather requests created `httpx.Client()` while `NO_PROXY` contained raw IPv6 loopback entries (`::1`, `::1/128`), so the weather call failed before reaching QWeather and `/weather-card` returned the city weather error.
- Extracted shared `httpx_compatible_proxy_env()` helper under `backend/app/services/httpx_compat.py` and used it from both LLM and weather HTTP client creation paths.
- Added a weather-tool regression test proving realtime weather lookup still works when `NO_PROXY` contains `::1`.
- Removed the custom `frame-label-banner` overlay from `TarotCardDisplay.vue`; the card image now renders without the dark bottom label box.
- Removed the now-unused `romanNumeral` computed value and the overlay CSS classes.
- Changed Weather Oracle tarot selection so the backend chooses the daily card from `user_id + Shanghai date`, not city or weather fingerprint.
- When switching cities on the Weather Oracle page, the frontend sends the existing tarot card id and preserves the current day's tarot card and fortune guidance while replacing city weather, mood guide, and weather mappings from the new response.
- Weather-card model selection now prefers `mimo-v2.5`, then `MiniMax-M2.5`, then the first configured model when no `model_id` is provided.
- Added backend regression tests covering same-day tarot stability across city changes and preferred weather-card model selection.
- Found the new city-switch failure came from the model returning `fortune` and `mood_guide` as strings and `weather_mappings` as an object; the route wrote that invalid payload before schema validation, so fallback validation reused bad data and returned HTTP 500.
- Normalized common model summary shapes into the weather-card schema before validation, and only returns model data after `WeatherCardResponse` accepts it.
- Added a 10-second timeout and zero retries for Weather Oracle model summary calls so city weather data can still return if the model is slow.
- Updated the city picker trigger to show `查询中` while a city request is running.
- Polished QuickCityPicker dropdown & inputs: optimized transitions, focus states, click active animations, and hover media queries according to the design specification.
- Polished OracleChatPanel suggestion chips, inputs, and submit button: optimized transitions, focus states, active click animations, and hover media queries according to the design specification.

## In progress

- None.

## Notes

- Figma MCP metadata access now works again for file `Ekroehh3gLkbPnj2raccJH`.
- Figma PNG export through MCP still hits the Starter plan tool-call limit: `You've reached the Figma MCP tool call limit on the Starter plan. Upgrade your plan for more tool calls`.
- This no longer blocks the current implementation because the user manually exported the source images and the local PNG assets were generated from those files.
- Current `/api/v1/assistant/models` returns Kimi, MiniMax, DeepSeek, and `mimo-v2.5`; the Oracle chat panel currently selects the first returned model, so it will default to Kimi unless the backend order changes or the frontend gets a selector/preference rule.
- Real HTTP stream check: `mimo-v2.5` returned streamed text successfully. `MiniMax-M2.5` no longer returns `Invalid port: ':1'`, but the provider returned `429 usage limit exceeded (2056)`.
- Direct weather check after the fix: Shanghai, Wuhan, Beijing, and Hangzhou all returned structured QWeather realtime data.
- Authenticated `/api/v1/assistant/weather-card` check for Wuhan returned HTTP 200 with weather fields populated.
- Browser automation tools were not available in this turn; visual verification should be done by refreshing `/oracle` in the existing Chrome page.
- Authenticated `/api/v1/assistant/weather-card` check for Shanghai and Jiangmen returned the same tarot id (`swords-06-six`) and different weather temperatures, confirming card stability and city data refresh.
- Authenticated `/api/v1/assistant/weather-card` check for Jiangmen without `model_id` now returns HTTP 200 in about 10.9s with weather values and four mappings; `mimo-v2.5` did not respond before the 10s weather-card timeout in that check, so fallback copy was used for readings.

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
- Ran `npm run build` successfully to verify Vite compilation for Task 4.
- Checked git status and styling rules since `ab970dc` to verify style/asset integration.
- Ran backend pytest suite ensuring all 22 tests pass with zero regressions.
- Ran `npm run build` successfully after removing the old grid background pattern from `OracleLayout.vue`.
- Processed light mode background pattern image `public/mystical_bg_light.png` to be transparent with `#efdac9` lines.
- Verified `public/mystical_bg_light.png` is an optimized PNG image (512x512, ~208KB, <400KB).
- Ran `npm run build` and `pytest` verifying zero regressions.
- Updated light theme variables (off-white base `#fefcf8` and semi-transparent `#fdf9f3` card backgrounds) in `src/styles/oracle-theme.css`.
- Updated opacity of light mode pattern in `src/layouts/OracleLayout.vue` to 0.85.
- Ran frontend build (`npm run build`) and backend regression tests successfully to verify Task 4.
- Verified the new LLM regression test fails before the fix with `httpx.InvalidURL: Invalid port: ':1'`.
- Ran `PYTHONPATH=. venv/bin/python -m pytest tests/test_llm_config.py::LLMConfigTests::test_get_llm_ignores_invalid_ipv6_no_proxy_entry -q` successfully after the fix.
- Ran direct backend cwd checks for `get_llm()` with `kimi-k2.5`, `MiniMax-M2.5`, and `mimo-v2.5`; all clients construct without the port error.
- Ran authenticated HTTP stream checks for `MiniMax-M2.5` and `mimo-v2.5`; MiniMax returned provider 429, mimo streamed text.
- Ran `PYTHONPATH=. venv/bin/python -m pytest tests -q` (`23 passed, 4 warnings`).
- Ran `npm run build` successfully.
- Ran `git diff --check` successfully after whitespace cleanup.
- Verified the new weather regression test fails before the fix because `NO_PROXY` still contains `::1`.
- Ran `PYTHONPATH=. venv/bin/python -m pytest tests/test_weather_tool.py::StructuredWeatherNowTests::test_fetch_realtime_weather_ignores_invalid_ipv6_no_proxy_entry tests/test_llm_config.py::LLMConfigTests::test_get_llm_ignores_invalid_ipv6_no_proxy_entry -q` successfully.
- Ran direct backend cwd checks for `WeatherToolService.fetch_realtime_weather()` with Shanghai, Wuhan, Beijing, and Hangzhou; all returned data.
- Ran authenticated HTTP check for `/api/v1/assistant/weather-card` with `city=武汉`; returned HTTP 200.
- Ran `PYTHONPATH=. venv/bin/python -m pytest tests -q` (`24 passed, 4 warnings`).
- Ran `npm run build` successfully.
- Ran `git diff --check` successfully.
- Ran `npm run build` successfully after removing the tarot overlay.
- Ran `git diff --check` successfully after removing the tarot overlay.
- Confirmed `frame-label-banner`, `card-roman-num`, `card-zh-name`, and `romanNumeral` no longer appear in `TarotCardDisplay.vue`.
- Verified new weather-card tests fail before the implementation because tarot selection still depends on city/weather and preferred model helper is missing.
- Ran focused weather-card tests successfully after the implementation.
- Ran `PYTHONPATH=. venv/bin/python -m pytest tests -q` (`27 passed, 4 warnings`).
- Ran `npm run build` successfully.
- Ran `git diff --check` successfully.
- Ran authenticated HTTP checks for Shanghai and Jiangmen weather-card responses; both returned HTTP 200 with the same tarot id and different weather values.
- Verified the new LLM-shape regression test fails before the fix with `ValidationError` on `fortune`, `mood_guide`, and `weather_mappings`.
- Ran `PYTHONPATH=. venv/bin/python -m pytest tests/test_weather_card.py::WeatherCardEndpointTests::test_weather_card_coerces_common_llm_summary_shape tests/test_llm_config.py::LLMConfigTests::test_get_llm_passes_optional_timeout_and_retry_config -q` successfully.
- Ran `PYTHONPATH=. venv/bin/python -m pytest tests/test_weather_card.py tests/test_llm_config.py -q` (`15 passed, 4 warnings`).
- Ran authenticated HTTP check for `/api/v1/assistant/weather-card` with Jiangmen and no `model_id`; returned HTTP 200 after the 10s model timeout with weather values populated.
- Ran `PYTHONPATH=. venv/bin/python -m pytest tests -q` (`29 passed, 4 warnings`).
- Ran `npm run build` successfully and removed generated `dist/`.
- Ran `git diff --check` successfully.
- Polished QuickCityPicker transitions & animations and verified frontend compilation successfully via `npm run build`.
- Polished notice/error banner slide-fade transitions in WeatherOracle.vue.

## Next actions

- Decide whether Weather Oracle should show a separate "model summary timed out" notice or skip the model summary during city switches when `mimo-v2.5` is slow.
- Decide whether the Oracle chat panel should expose a model selector or prefer `mimo-v2.5` / `MiniMax-M2.5` while Kimi and DeepSeek are unavailable.
