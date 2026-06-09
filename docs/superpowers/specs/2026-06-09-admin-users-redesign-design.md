# User Management Page Redesign Specification

This design document outlines the theme-alignment and visual adjustments for the User Management page (`src/views/AdminUsers.vue`).

## Goals
1. Align the User Management page with the gold-accented, glassmorphic dark/light theme (`oracle-theme.css`) and support full theme adaptability.
2. Replace hardcoded RGBA colors with theme-defined variables (`var(--oracle-xxx-rgb)`), eliminating visual bugs when switching to the light theme.
3. Clean up the stylesheet and improve consistency across the settings and administration pages.

---

## Design Details

### 1. Theme-Aware Colors
Replace all hardcoded RGBA values with variables:
- **Admin Pill Badge (`.badge-pill-admin`)**:
  - Border: `rgba(var(--oracle-gold-rgb), 0.25)`
  - Background: `rgba(var(--oracle-gold-rgb), 0.08)`
- **Upgrade/Downgrade Button Hover (`.btn-card-action.edit-btn:hover`)**:
  - Background: `rgba(var(--oracle-gold-rgb), 0.08)`
- **Delete Button (`.btn-card-action.delete-btn`)**:
  - Border: `rgba(var(--oracle-danger-rgb), 0.25)`
  - Background: `rgba(var(--oracle-danger-rgb), 0.05)`
  - Hover background: `rgba(var(--oracle-danger-rgb), 0.15)`
- **Feedback Messages**:
  - Success message background/border: `rgba(var(--oracle-success-rgb), 0.12)` / `rgba(var(--oracle-success-rgb), 0.2)`
  - Error message background/border: `rgba(var(--oracle-danger-rgb), 0.12)` / `rgba(var(--oracle-danger-rgb), 0.2)`

### 2. Consistency Enhancements
- All margins, paddings, and borders will remain identical to the original layout, but use variables where applicable to keep the UI clean and robust.

---

## Verification Plan
1. **Compilation Check**: Run `npm run build` to verify Vite bundle correctness.
2. **Regression Check**: Run backend tests to ensure user updates, upgrades, and deletions still function as expected.
