# Tarot Mystical Backgrounds Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement premium mystical tarot background patterns for Light and Dark modes.

**Architecture:** Generate two tileable background images using AI image generation, save them in `public/`, and apply them dynamically via CSS variables using a low-opacity pseudo-element layout layer in the global oracle stylesheet to ensure readability.

**Tech Stack:** Vue 3, CSS variables, HTML/CSS, AI Image Generation.

---

### Task 1: Generate Dark Mode Background Image

**Files:**
- Create: `public/mystical_bg_dark.png`

- [ ] **Step 1: Generate the image using the image generation tool**
  We will generate the dark mode tileable background texture.
  Tool: `generate_image`
  Parameters:
  - ImageName: `mystical_bg_dark`
  - Prompt: `mystical dark celestial tarot card background pattern, seamless tileable, subtle gold stars, constellations, alchemy lines, sacred geometry, low contrast, deep blue and black obsidian, premium clean texture, flat design, no frame, no device mockups`

- [ ] **Step 2: Verify the image file is created successfully**
  Confirm the image is created under `public/mystical_bg_dark.png`.
  Run: `ls -la public/mystical_bg_dark.png`
  Expected output: File exists with non-zero size.

- [ ] **Step 3: Commit the new asset**
  Run:
  ```bash
  git add public/mystical_bg_dark.png
  git commit -m "feat: add dark mode background texture asset"
  ```

---

### Task 2: Generate Light Mode Background Image

**Files:**
- Create: `public/mystical_bg_light.png`

- [ ] **Step 1: Generate the image using the image generation tool**
  We will generate the light mode tileable background texture.
  Tool: `generate_image`
  Parameters:
  - ImageName: `mystical_bg_light`
  - Prompt: `mystical light celestial tarot card background pattern, seamless tileable, subtle sepia stars, constellations, alchemy lines, sacred geometry, low contrast, warm parchment cream color, premium clean texture, flat design, no frame, no device mockups`

- [ ] **Step 2: Verify the image file is created successfully**
  Confirm the image is created under `public/mystical_bg_light.png`.
  Run: `ls -la public/mystical_bg_light.png`
  Expected output: File exists with non-zero size.

- [ ] **Step 3: Commit the new asset**
  Run:
  ```bash
  git add public/mystical_bg_light.png
  git commit -m "feat: add light mode background texture asset"
  ```

---

### Task 3: Update CSS Styling for Oracle Theme and Layout

**Files:**
- Modify: `src/styles/oracle-theme.css`
- Modify: `src/layouts/OracleLayout.vue`

- [ ] **Step 1: Add `--oracle-bg-pattern` variable in `src/styles/oracle-theme.css`**
  Modify: `src/styles/oracle-theme.css` to add the `--oracle-bg-pattern` variable under both default and light themes.

  Add under `:root` (around line 27):
  ```css
  --oracle-bg-pattern: url('/mystical_bg_dark.png');
  ```

  Add under `[data-oracle-theme='light']` (around line 49):
  ```css
  --oracle-bg-pattern: url('/mystical_bg_light.png');
  ```

- [ ] **Step 2: Apply the background pattern pseudo-element in `src/layouts/OracleLayout.vue`**
  Modify: `src/layouts/OracleLayout.vue` styles to append the new background overlay pseudo-element.

  Add to `<style scoped>` (around line 197, right after `.oracle-layout::before`):
  ```css
  .oracle-layout::after {
    content: '';
    position: fixed;
    inset: 0;
    z-index: -1;
    pointer-events: none;
    background-image: var(--oracle-bg-pattern);
    background-repeat: repeat;
    background-size: 360px;
    opacity: 0.12;
    transition: opacity 0.5s ease, background-image 0.5s ease;
  }

  .oracle-layout[data-oracle-theme='light']::after {
    opacity: 0.08;
  }
  ```

- [ ] **Step 3: Remove the old grid background pattern in `src/layouts/OracleLayout.vue`**
  Modify: `src/layouts/OracleLayout.vue` styles to delete the `.oracle-layout::before` CSS block (around lines 184-197).

- [ ] **Step 4: Commit styling modifications**
  Run:
  ```bash
  git add src/styles/oracle-theme.css src/layouts/OracleLayout.vue
  git commit -m "style: integrate tarot background pattern and remove grid background"
  ```

---

### Task 4: Build and Verify Frontend Layout

**Files:**
- Test: Build validation

- [ ] **Step 1: Run frontend build**
  Verify the changes do not break the Vite compilation.
  Run: `npm run build`
  Expected output: Build passes successfully.

- [ ] **Step 2: Inspect application locally**
  Check the rendering of the `/oracle` route at `http://localhost:5173/oracle` under both dark and light modes.
  Verify:
  1. Background pattern is visible but subtle.
  2. Text remains highly readable.
  3. Switching modes (via theme toggle) transitions the background pattern smoothly.
