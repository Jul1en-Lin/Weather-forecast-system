# Project Status

## Current goal

Goal: Remove divination-related text from Login and Register pages.

Status: Completed Task 1 (Modify Login Page Template and Styles).

## Done

- Completed Task 1 (Modify Login Page Template and Styles):
  - Removed brand subtitle (`✦ 气象占卜台 ✦`) and welcome subtitle (`✦ 登录以继续你的天气占卜之旅 ✦`) from [Login.vue](file:///Users/lien/GitRepo/Weather-forecast-system/src/views/Login.vue).
  - Updated the welcome title to `✦ 欢迎回来 ✦` in [Login.vue](file:///Users/lien/GitRepo/Weather-forecast-system/src/views/Login.vue).
  - Cleaned up unused scoped CSS classes `.brand-subtitle` and `.welcome-subtitle` in [Login.vue](file:///Users/lien/GitRepo/Weather-forecast-system/src/views/Login.vue).
- Verified successful Vite compilation of the frontend after changes.

- Implemented Batch User Management features in both backend and frontend:
  - **Backend**: Added batch admin status update (`POST /api/v1/users/batch/admin`) and batch deletion (`POST /api/v1/users/batch/delete`) endpoints, protected by the `require_admin` dependency. Written comprehensive unit tests in `backend/tests/test_batch_users.py`.
  - **Frontend**: Added a custom styled "Select All" checkbox in the User Management header, checkboxes on individual user cards, and a glassmorphic floating action bar showing selected count with buttons for batch upgrade, batch downgrade, batch delete, and deselect.
  - **Responsive Design**: Ensured the floating batch action bar folds into a neat vertical stack on screens below 768px.
  - **Verification**: Verified that Vite frontend builds successfully and backend tests pass.

- Fixed layout overflow in [AdminUsers.vue](file:///Users/lien/GitRepo/Weather-forecast-system/src/views/AdminUsers.vue):
  - Added `:title` tooltip on hover for user names.
  - Set `.user-title-desc` and `.user-name-role` to `min-width: 0` and enabled `text-overflow: ellipsis` to cleanly truncate long usernames.
  - Configured `.user-card-actions` with `flex-shrink: 0` to prevent upgrade and delete action buttons from being squeezed or pushed out of view.
  - Verified that it compiles cleanly with `npm run build`.

- Redesigned the CSS Stylesheet block in [AdminUsers.vue](file:///Users/lien/GitRepo/Weather-forecast-system/src/views/AdminUsers.vue) (Task 1):
  - Replaced hardcoded RGBA colors in `.badge-pill-admin`, `.btn-card-action.edit-btn:hover`, `.btn-card-action.delete-btn`, `.success-message`, and `.error-message` with theme-aware RGB variables (`var(--oracle-gold-rgb)`, `var(--oracle-danger-rgb)`, and `var(--oracle-success-rgb)`).
  - Verified compilation of Vue templates and styles via `npm run build`.

- Pruned dead CSS styles from [Settings.vue](file:///Users/lien/GitRepo/Weather-forecast-system/src/views/Settings.vue), deleting unused selectors `.config-section`, `.config-grid`, and `.config-card` (along with all nested/theme rules).
- Added light mode adaptability CSS overrides using the `[data-oracle-theme='light']` class selector in [Settings.vue](file:///Users/lien/GitRepo/Weather-forecast-system/src/views/Settings.vue).
- Verified successful Vite compilation via `npm run build`.

- Fixed [AdminUsers.vue](file:///Users/lien/GitRepo/Weather-forecast-system/src/views/AdminUsers.vue) so `fetchUsers()` requests `/api/v1/users/` instead of `/api/v1/users`, avoiding FastAPI's 307 redirect from the Vite proxy origin to the backend origin.
- Redesigned the UI template elements in [Settings.vue](file:///Users/lien/GitRepo/Weather-forecast-system/src/views/Settings.vue) (Task 1):
  - Added `.oracle-surface` class to model and tools tab panel container forms.
  - Replaced `.model-badge` / `.local-badge` classes with `.badge-pill` / `.badge-pill-local`.
  - Replaced status emojis with the `.status-indicator` dot and text element.
  - Replaced system built-in status badge with `.badge-pill.badge-pill-builtin`.
  - Verified compilation of Vue templates via `npm run build`.
- Redesigned the CSS Stylesheet block in [Settings.vue](file:///Users/lien/GitRepo/Weather-forecast-system/src/views/Settings.vue) (Task 2):
  - Replaced original scoped styles with gold-accented, glassmorphic layout rules.
  - Custom styled tabs, loading animations, input fields, badges, forms, and layout grids.
  - Verified compilation of Vue templates and styles via `npm run build`.
- Redesigned the Intelligent Assistant page ([IntelligentAssistant.vue](file:///Users/lien/GitRepo/Weather-forecast-system/src/views/IntelligentAssistant.vue)):
  - Replaced cheap, cartoonish emojis (🤖, 🗑️, ✏️, 📋) with clean, professional SVG vector icons.
  - Aligned colors, backgrounds, borders, and input focus states with the gold-accented glassmorphic theme via CSS variables from `oracle-theme.css`.
  - Updated assistant name to "气象智能助手" and headings typography to match the serif styles.
- Generated and updated new page screenshot mockups matching the glassmorphic theme under `docs/images/`, and updated `README.md` to reference the correct image names and show the updated frontend/backend directory tree structure.
- Implemented the Frontend Redesign Implementation Plan to prioritize weather services over fortune-telling/divination:
  - [OracleLayout.vue](file:///Users/lien/GitRepo/Weather-forecast-system/src/layouts/OracleLayout.vue): Changed "气象占卜台" to "智能气象助手", updated moon phases symbol decor to weather icons (☀ ⛅ 🌤 ⛈ ❄), updated dropdown subtitle user roles to "系统管理员" / "气象助手用户", and renamed footer description.
  - [TarotCardDisplay.vue](file:///Users/lien/GitRepo/Weather-forecast-system/src/components/oracle/TarotCardDisplay.vue): Changed titles to "Weather Intelligence" and "今日天气概览", renamed label values like "幸运色" to "今日色彩", "幸运数字" to "今日数字", "宜" / "忌" to "适宜" / "注意", and updated fallback card text.
  - [WeatherMetricGrid.vue](file:///Users/lien/GitRepo/Weather-forecast-system/src/components/oracle/WeatherMetricGrid.vue): Renamed eyebrow to "Real-time Weather Data" and updated mapping titles and descriptions.
  - [OracleLeftSidebar.vue](file:///Users/lien/GitRepo/Weather-forecast-system/src/components/oracle/OracleLeftSidebar.vue): Replaced today's astrology card headers and zodiac signs array data with daily weather tips, renamed computations, and replaced the moon graphic with a weather graphic.
  - [OracleBottomCards.vue](file:///Users/lien/GitRepo/Weather-forecast-system/src/components/oracle/OracleBottomCards.vue): Replaced daily ratings with Life Weather Index ("穿衣指数"/"运动指数"/"紫外线指数"), travel advisor content, and renamed recommended knowledge base articles to weather-related topics.
  - [OracleChatPanel.vue](file:///Users/lien/GitRepo/Weather-forecast-system/src/components/oracle/OracleChatPanel.vue): Renamed "天气占卜师" to "天气助手", updated suggestions, input placeholders, welcome greetings, and createContextualPrompt chat context prompt formatting.
  - [MoodGuidePanel.vue](file:///Users/lien/GitRepo/Weather-forecast-system/src/components/oracle/MoodGuidePanel.vue): Changed titles to "Weather Life Guide" and "今日天气生活指南".
  - [WeatherOracle.vue](file:///Users/lien/GitRepo/Weather-forecast-system/src/views/WeatherOracle.vue): Changed page placeholder texts from tarot card summoning to weather report query.
  - [index.html](file:///Users/lien/GitRepo/Weather-forecast-system/index.html): Updated title tag content to "Weather Oracle - 智能气象助手".
- Redesigned the login page (`src/views/Login.vue`) using a fullscreen glassmorphic container, theme switcher, custom star logo, inputs with prefix icons, and direct redirection to `/oracle` route upon successful login. Removed GitHub login button.
- Redirected `/home` to `/oracle` in `src/router/index.ts` and deleted the unused `src/views/Home.vue` page.
- Polished IntelligentAssistant interactive elements: optimized transitions, focus states, active click scaling, and hover media query gating for new-chat-btn, chip, chat-input, and send-button in IntelligentAssistant.vue.
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
- Implemented Task 6: Stagger enter animations for weather metrics cards, and progress bar load animations in WeatherMetricGrid.vue.
- Replaced the WeatherMetricGrid fake "带走烦恼百分比" wind footer with model-backed daily travel and clothing advice from the Weather Oracle weather-card response.
- Adjusted the WeatherMetricGrid daily advice footer into a two-line layout and rewrote fallback travel/clothing copy to sound more direct and practical.
- Redesigned the register page (`src/views/Register.vue`) completely to match the exact visual style, background, glassmorphism, theme toggle, and fonts as the redesigned `Login.vue`, but with registration form fields (Username, Password, Confirm Password, Register button, Switch link, and Footer policy text).
- Added backend Weather Oracle tarot metadata for all 78 cards, including names, keywords, core meaning, shadow meaning, mood angle, weather-oracle hint, and response style guidance.
- Updated `/api/v1/assistant/weather-card` prompt input so the model receives the selected card's full meaning data instead of only the card id and generic keywords.
- Added regression tests proving the backend tarot metadata contains real card meanings and the weather-card prompt includes selected-card meaning fields.
- Shortened the Weather Oracle model prompt to only request `fortune` and `mood_guide` from a compact selected-card/weather payload; `daily_advice` and `weather_mappings` continue to use backend fallback unless the model returns them.
- Changed the weather-card LLM call to `temperature=0.3`, `timeout=20.0`, `max_retries=0`, and `use_env_proxy=False`.
- Added an LLM regression test proving `get_llm(..., use_env_proxy=False)` creates an `httpx.Client(trust_env=False)`.

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
- Kimi should not be used for live checks because the current account is out of balance; use `mimo-v2.5` for Weather Oracle runtime tests.
- Live `mimo-v2.5` checks with environment proxy disabled confirmed small JSON prompts can return in about 2 seconds, but Weather Oracle prompt calls still timed out at 20 seconds in two local endpoint checks and returned fallback.

## Checkpoints

- Reproduced the failing path with `curl http://localhost:5174/api/v1/users`, which returned `307` and redirected to `http://localhost:8000/api/v1/users/`.
- Verified `curl http://localhost:5174/api/v1/users/` returns directly without redirect (`401` when unauthenticated, as expected).
- Ran `npm run build` successfully and removed the generated `dist/`.
- Verified the existing Chrome page at `http://localhost:5174/admin/users` now shows the user list instead of `Failed to fetch`.
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
- Ran `npm run build` successfully after removing Tarot card flip and fortune blur from city switches.
- Ran `npm run build` successfully after implementing stagger enter animations for weather metrics cards and progress bar load animations (Task 6).
- Ran `python3 -m py_compile backend/app/routers/assistant.py backend/app/schemas/assistant.py`.
- Ran `PYTHONPATH=. venv/bin/python -m pytest tests/test_weather_card.py -q` (`12 passed, 4 warnings`).
- Ran `PYTHONPATH=. venv/bin/python -m pytest tests -q` (`30 passed, 4 warnings`).
- Ran `npm run build` successfully after adding daily travel and clothing advice to WeatherMetricGrid.
- Ran `PYTHONPATH=. venv/bin/python -m pytest tests/test_weather_card.py -q` (`12 passed, 4 warnings`) after the two-line advice footer and copy update.
- Ran `PYTHONPATH=. venv/bin/python -m pytest tests -q` (`30 passed, 4 warnings`) after the two-line advice footer and copy update.
- Ran `npm run build` successfully after the WeatherMetricGrid footer layout update.
- Ran `npm run build` successfully after redesigning the Login page UI.
- Ran `npm run build` successfully after redesigning the Register page UI.
- Ran focused Weather Oracle metadata regression tests after adding backend tarot meanings.
- Ran `PYTHONPATH=. venv/bin/python -m pytest tests/test_weather_card.py -q` (`13 passed, 4 warnings`).
- Ran `PYTHONPATH=. venv/bin/python -m pytest tests -q` (`31 passed, 4 warnings`).
- Ran `npm run build` successfully after backend tarot prompt updates.
- Ran `git diff --check` successfully.
- Ran focused no-proxy and compact-prompt regression tests after changing Weather Oracle model call settings.
- Ran live authenticated `/api/v1/assistant/weather-card` checks with `model_id=mimo-v2.5`; response stayed HTTP 200 but used fallback after 20-second model read timeout.
- Ran `PYTHONPATH=. venv/bin/python -m pytest tests -q` (`33 passed, 4 warnings`) after no-proxy, 20-second timeout, and compact prompt updates.
- Ran `npm run build` successfully after the final Weather Oracle model-call updates.
- Ran `git diff --check` successfully after the final Weather Oracle model-call updates.

## Next actions

- Decide whether Weather Oracle should show a separate "model summary timed out" notice or skip the model summary during city switches when `mimo-v2.5` is slow.
- Decide whether the Oracle chat panel should expose a model selector or prefer `mimo-v2.5` / `MiniMax-M2.5` while Kimi and DeepSeek are unavailable.
