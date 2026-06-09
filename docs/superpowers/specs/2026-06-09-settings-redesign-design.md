# System Settings Page Redesign Specification

This design document outlines the visual redesign and theme alignment for the Model Management and Weather Services tabs in the System Settings page (`src/views/Settings.vue`).

## Goals
1. Align the Settings page with the dark/light mystical gold-accented theme (`oracle-theme.css`) used across the application.
2. Remove native iOS/macOS styled primary colors (blue, red, green, gray) and replace them with theme-defined variables.
3. Eliminate cartoon emojis (`✅`, `❌`) and replace them with elegant, premium vector elements and status indicator lights.
4. Enhance interactive elements (buttons, inputs, hover states) with smooth CSS transitions, glowing shadows, and micro-animations.

---

## Design Details

### 1. Tab Navigation & Panels
- **Tab Buttons**: 
  - Passive state: Semi-transparent background using `rgba(255, 255, 255, 0.02)` (dark theme) or `rgba(0, 0, 0, 0.02)` (light theme), bounded by `var(--oracle-border-soft)`.
  - Active state: Background using `rgba(215, 174, 105, 0.08)`, border using `var(--oracle-gold)`, and text color using `var(--oracle-gold)`. Added a subtle glow shadow `0 0 12px var(--oracle-gold-glow)`.
- **Form Panels**:
  - The `.settings-form` container will have `.oracle-surface` and `.oracle-gold-corners` classes applied.

### 2. Config & Model Cards
- **Card Styling**:
  - Transparent glassmorphic cards using `linear-gradient` overlays.
  - Hover effect: Card border shifts to `var(--oracle-gold)`, accompanied by a translation transition `translateY(-3px)` and glow shadow `0 10px 25px var(--oracle-gold-glow)`.
- **Pill Badges (H4 Header Badge)**:
  - Replace `.model-badge` and `.local-badge` with a unified `.badge-pill` class.
  - Custom colors mapping:
    - Cloud API: Gold text, soft gold transparent background, gold border.
    - Ollama Local: Green text (`var(--oracle-success)`), soft green background, green border.
    - System Built-in: Purple text (`var(--oracle-purple)`), soft purple background, purple border.
- **Status Dot Indicators**:
  - Emojis `✅ 支持` and `❌ 不支持` will be replaced by:
    ```html
    <span class="status-indicator" :class="{ active: m.supports_tools }">
      <span class="status-dot"></span>
      <span class="status-text">{{ m.supports_tools ? '支持' : '不支持' }}</span>
    </span>
    ```
  - Active state dot: Glowing green (`var(--oracle-success)`).
  - Inactive state dot: Muted gray/red (`var(--oracle-muted)`).

### 3. Form Input Controls
- **Inputs & Textareas**:
  - Background: `rgba(0, 0, 0, 0.15)` in dark theme, `rgba(255, 255, 255, 0.4)` in light theme.
  - Borders: `var(--oracle-border)`.
  - Focus state: Outline colored with `var(--oracle-gold)` and a box shadow glow `0 0 8px var(--oracle-gold-glow)`.
- **Checkboxes**:
  - Styled custom checkbox to match gold-accent theme, removing native browser blue colors.

### 4. Interactive Buttons
- **Primary Save Button (`.btn-save`)**:
  - Gradient background using gold theme shades: `linear-gradient(135deg, var(--oracle-gold) 0%, #a47631 100%)`.
  - Hover state: Brightened gold gradient, upward translation, and gold shadow glow.
- **Secondary / Cancel Button (`.btn-reset`)**:
  - Transparent/semi-transparent background, subtle border, with gold text hover highlights.
- **Danger Button (`.delete-btn`)**:
  - Border and text colored with `var(--oracle-danger)`. Hover states show a soft background fill.

---

## File Changes

1. **`src/views/Settings.vue`**:
   - Update the template to include the status indicators and badge pills.
   - Completely replace the `<style scoped>` CSS block at the end of the file with the redesigned stylesheet.

---

## Verification Plan
1. **Compilation Check**: Run `npm run build` to verify type checking and Vite build correctness.
2. **Visual Verification**: Check light/dark mode display of the settings view, tab switching, form controls, and card lists.
3. **Integration Check**: Ensure backend settings logic and configuration saving (API calls) continue to function exactly as before.
