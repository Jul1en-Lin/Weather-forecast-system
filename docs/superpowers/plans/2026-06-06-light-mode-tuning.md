# Light Mode Background Tuning Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Modify the light mode colors so that the base background color is `#fefcf8`, the card panels are `#fdf9f3` (92% transparent), and the background pattern lines are `#efdac9` on a transparent background.

**Architecture:** Use a Python script with Pillow to process the light mode background texture to have transparent background and `#efdac9` color lines, update the theme CSS variables, and increase the layout opacity of the light mode background texture overlay to `0.85` so it is clearly visible.

**Tech Stack:** Vue 3, CSS variables, Python/Pillow.

---

### Task 1: Process Light Mode Background Texture Image

**Files:**
- Modify: `public/mystical_bg_light.png`

- [ ] **Step 1: Write and run a Python script to process the image**
  Run a Python command using the global environment that reads the existing `public/mystical_bg_light.png`, converts it to a transparent PNG where the background is transparent and the lines are colored `#efdac9` (RGB: `239, 218, 201`).
  Run:
  ```bash
  python3 -c "
  from PIL import Image
  import numpy as np
  img = Image.open('public/mystical_bg_light.png').convert('RGBA')
  data = np.array(img)
  r, g, b, a = data[:,:,0], data[:,:,1], data[:,:,2], data[:,:,3]
  gray = 0.299*r + 0.587*g + 0.114*b
  new_alpha = 255 - gray
  # Adjust contrast to make lines cleaner
  new_alpha = np.clip(new_alpha * 1.5, 0, 255).astype(np.uint8)
  # Set the line color to #efdac9 (239, 218, 201)
  data[:,:,0] = 239
  data[:,:,1] = 218
  data[:,:,2] = 201
  data[:,:,3] = new_alpha
  processed_img = Image.fromarray(data)
  # Resize to 512x512 to ensure it is optimized
  processed_img.thumbnail((512, 512))
  processed_img.save('public/mystical_bg_light.png', 'PNG', optimize=True)
  "
  ```
- [ ] **Step 2: Verify the processed image**
  Ensure the image exists, is true PNG, and size is optimized (<400KB).
  Run: `file public/mystical_bg_light.png`
  Expected output: PNG image data...
  Run: `ls -la public/mystical_bg_light.png`
  Expected output: File size is valid.

- [ ] **Step 3: Commit processed asset**
  Run:
  ```bash
  git add public/mystical_bg_light.png
  git commit -m "feat: process light mode background pattern to be transparent #efdac9 lines"
  ```

---

### Task 2: Update Light Theme CSS Variables

**Files:**
- Modify: `src/styles/oracle-theme.css`

- [ ] **Step 1: Modify light theme variables in `src/styles/oracle-theme.css`**
  Modify: `src/styles/oracle-theme.css` (around lines 30-50).
  Replace:
  ```css
  [data-oracle-theme='light'] {
    --oracle-bg: #fdfaf4;
    --oracle-bg-deep: #f5efe3;
    --oracle-panel: rgba(255, 253, 249, 0.9);
    --oracle-panel-soft: rgba(250, 245, 235, 0.82);
    --oracle-panel-solid: #fffdfa;
    --oracle-border: rgba(180, 140, 85, 0.32);
    --oracle-border-soft: rgba(74, 58, 37, 0.08);
    --oracle-gold: #b28542;
    --oracle-gold-strong: #8c6022;
    --oracle-gold-glow: rgba(180, 140, 85, 0.08);
    --oracle-purple: #7457a4;
    --oracle-purple-soft: rgba(116, 87, 164, 0.08);
    --oracle-blue: #3b6ba5;
    --oracle-text: #3c3020;
    --oracle-muted: #8c7b64;
    --oracle-faint: rgba(60, 48, 32, 0.68);
    --oracle-danger: #ad503f;
    --oracle-success: #378a68;
    --oracle-shadow: 0 15px 35px rgba(140, 110, 80, 0.08);
    --oracle-bg-pattern: url('/mystical_bg_light.png');
  }
  ```
  with:
  ```css
  [data-oracle-theme='light'] {
    --oracle-bg: #fefcf8;
    --oracle-bg-deep: #fefcf8;
    --oracle-panel: rgba(253, 249, 243, 0.92);
    --oracle-panel-soft: rgba(253, 249, 243, 0.80);
    --oracle-panel-solid: #fdf9f3;
    --oracle-border: rgba(180, 140, 85, 0.32);
    --oracle-border-soft: rgba(74, 58, 37, 0.08);
    --oracle-gold: #b28542;
    --oracle-gold-strong: #8c6022;
    --oracle-gold-glow: rgba(180, 140, 85, 0.08);
    --oracle-purple: #7457a4;
    --oracle-purple-soft: rgba(116, 87, 164, 0.08);
    --oracle-blue: #3b6ba5;
    --oracle-text: #3c3020;
    --oracle-muted: #8c7b64;
    --oracle-faint: rgba(60, 48, 32, 0.68);
    --oracle-danger: #ad503f;
    --oracle-success: #378a68;
    --oracle-shadow: 0 15px 35px rgba(140, 110, 80, 0.08);
    --oracle-bg-pattern: url('/mystical_bg_light.png');
  }
  ```

- [ ] **Step 2: Commit CSS changes**
  Run:
  ```bash
  git add src/styles/oracle-theme.css
  git commit -m "style: update light mode theme colors and panel opacity"
  ```

---

### Task 3: Modify Layout Opacity for Light Mode Pattern

**Files:**
- Modify: `src/layouts/OracleLayout.vue`

- [ ] **Step 1: Update opacity of light mode pattern in `src/layouts/OracleLayout.vue`**
  Modify: `src/layouts/OracleLayout.vue` styles to change the light mode pattern opacity from `0.08` to `0.85`.
  Replace (around line 203):
  ```css
  .oracle-layout[data-oracle-theme='light']::after {
    opacity: 0.08;
  }
  ```
  with:
  ```css
  .oracle-layout[data-oracle-theme='light']::after {
    opacity: 0.85;
  }
  ```

- [ ] **Step 2: Commit layout changes**
  Run:
  ```bash
  git add src/layouts/OracleLayout.vue
  git commit -m "style: increase light mode background pattern opacity to 0.85"
  ```

---

### Task 4: Build and Verify

**Files:**
- Test: Build validation

- [ ] **Step 1: Run frontend build**
  Verify everything compiles successfully.
  Run: `npm run build`
  Expected output: Build passes successfully.
