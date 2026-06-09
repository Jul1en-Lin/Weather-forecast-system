# Navigation and Logo Refactoring Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Modify the header navigation and logo brand in `OracleLayout.vue`. Replace the astrological logo with a clean, professional weather + AI logo, and delete the redundant "天气查询" (Weather Search) navigation link and its associated handler.

**Architecture:** Edit `OracleLayout.vue` to update the SVG path of the logo, remove the `router-link` for Weather Search, and clean up the unused `handleWeatherSearchClick` handler.

**Tech Stack:** Vue 3, SVG, CSS

---

### Task 1: Refactor Template & Script in OracleLayout.vue

**Files:**
- Modify: `src/layouts/OracleLayout.vue`

- [ ] **Step 1: Replace Logo SVG in template**
  - In `OracleLayout.vue`, replace the current `<svg class="oracle-header-logo-svg" ...>` with the new weather-and-AI logo:

```html
          <svg class="oracle-header-logo-svg" viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <!-- Sun behind cloud -->
            <path d="M12 2v2M4.93 4.93l1.41 1.41M20.66 17H22M19.07 4.93l-1.41 1.41M15.5 8.5a3 3 0 1 0-6 0c0 .35.06.68.17 1H6.5a3.5 3.5 0 0 0 0 7h11a3.5 3.5 0 0 0 0-7H16.83a2.97 2.97 0 0 0-.17-1c0-.33-.05-.66-.16-1z" fill="currentColor" fill-opacity="0.2"/>
            <!-- Sparkle for AI in upper right -->
            <path d="M19 12l.5 1.5.5-1.5 1.5-.5-1.5-.5-.5-1.5-.5 1.5-1.5.5 1.5.5z" fill="var(--oracle-gold)"/>
          </svg>
```
  Wait, let's make sure the SVG paths are standard, valid and look great.
  Let's refine the SVG to be very beautiful and clean:
```html
          <svg class="oracle-header-logo-svg" viewBox="0 0 24 24" width="28" height="28">
            <!-- Sun (Backdrop) -->
            <circle cx="8" cy="9" r="4" fill="currentColor" opacity="0.4" />
            <!-- Sun rays -->
            <path d="M8 3v2M4.46 5.46l1.42 1.42M2 9h2M4.46 12.54l1.42-1.42" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" />
            <!-- Cloud (Foreground) -->
            <path d="M17.5 12.5a2.5 2.5 0 0 0-2.5-2.5c-.32 0-.62.06-.9.17a3.5 3.5 0 0 0-6.6 1.83 2.5 2.5 0 0 0 .5 4.5h9a2.5 2.5 0 0 0 .5-4z" fill="currentColor" />
            <!-- AI Sparkle (Top-Right Accent) -->
            <path d="M19 2l.75 1.75L21.5 4.5 19.75 5.25 19 7l-.75-1.75L16.5 4.5l1.75-.75L19 2z" fill="var(--oracle-gold)" />
          </svg>
```
  This is extremely clean and doesn't rely on external stroke settings that could look weird depending on CSS rules. It has a beautiful semi-transparent sun backdrop, cloud foreground, and a gold AI sparkle.

- [ ] **Step 2: Remove the "天气查询" nav link**
  - In `OracleLayout.vue`, delete the following lines:
```html
          <router-link to="/oracle" class="oracle-header-nav-item" active-class="active" @click="handleWeatherSearchClick">
            <span class="nav-dot"></span> 天气查询
          </router-link>
```

- [ ] **Step 3: Remove `handleWeatherSearchClick` from `<script setup>`**
  - Delete the `handleWeatherSearchClick` function definition.

---

### Task 2: Verify & Build

- [ ] **Step 1: Check Vite Compilation**
  - Run: `npm run build`
  - Expected: Build succeeds with no warnings or errors.

- [ ] **Step 2: Check Backend Tests**
  - Run: `PYTHONPATH=. venv/bin/pytest tests -q` inside `backend/`
  - Expected: All tests pass.

- [ ] **Step 3: Commit changes**
  - Run:
  ```bash
  git add src/layouts/OracleLayout.vue docs/project_status.md
  git commit -m "style: replace logo with weather-AI logo and remove redundant weather search link"
  ```
