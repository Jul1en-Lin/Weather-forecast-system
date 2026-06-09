# Logo Glow Style Fix Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Remove the rectangular box shadow (border glow box) from the logo SVG in `OracleLayout.vue` and replace the animation with a clean, path-based drop shadow animation.

**Architecture:** Edit `OracleLayout.vue` to add a scoped keyframe animation `pulse-logo-glow` that uses `opacity` and SVG `filter: drop-shadow` instead of DOM `box-shadow`, and apply it to `.oracle-header-logo-svg`.

**Tech Stack:** Vue 3, CSS

---

### Task 1: Modify CSS in OracleLayout.vue

**Files:**
- Modify: `src/layouts/OracleLayout.vue`

- [ ] **Step 1: Replace logo animation and add custom keyframe animation in `<style scoped>`**
  - In `OracleLayout.vue`, locate `.oracle-header-logo-svg` style and replace `animation: pulse-mystical ...` with `animation: pulse-logo-glow ...`.
  - Add the `@keyframes pulse-logo-glow` definition at the bottom of the `<style scoped>` block.

```css
.oracle-header-logo-svg {
  color: var(--oracle-gold);
  filter: drop-shadow(0 0 4px var(--oracle-gold-glow));
  animation: pulse-logo-glow 3s ease-in-out infinite;
}

@keyframes pulse-logo-glow {
  0%, 100% {
    opacity: 0.85;
    filter: drop-shadow(0 0 2px var(--oracle-gold-glow));
  }
  50% {
    opacity: 1;
    filter: drop-shadow(0 0 6px var(--oracle-gold));
  }
}
```

---

### Task 2: Verify & Build

- [ ] **Step 1: Check Vite Compilation**
  - Run: `npm run build`
  - Expected: Build succeeds without errors.

- [ ] **Step 2: Check Backend Tests**
  - Run: `PYTHONPATH=. venv/bin/pytest tests -q` inside `backend/`
  - Expected: All tests pass.

- [ ] **Step 3: Commit changes**
  - Run:
  ```bash
  git add src/layouts/OracleLayout.vue docs/project_status.md
  git commit -m "style: replace logo box-shadow animation with path-based drop-shadow animation"
  ```
