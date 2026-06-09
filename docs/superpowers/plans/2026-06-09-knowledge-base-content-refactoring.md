# Knowledge Base Content Refactoring Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Clean up the Knowledge Base content to remove tarot/fun mappings, model reference footers, and built-in badges. Restructure humidity, pressure, wind speed, solstices, and weather science content into bulleted list layouts matching the temperature article style.

**Architecture:** Remove the tarot field from the `Article` interface and data. Remove the model-builtin badge and footer from the article template. Restructure the article HTML contents into uniform `<ul>` structures.

**Tech Stack:** Vue 3, HTML, CSS

---

### Task 1: Refactor Template & Content in KnowledgeBase.vue

**Files:**
- Modify: `src/views/KnowledgeBase.vue`

- [ ] **Step 1: Update the Article interface and remove the tarot field from articles data**
  - Modify the `Article` TypeScript interface to remove `tarot: string`.
  - Remove the `tarot` property from all objects in the `articles` array.
  - Reformat all articles' `content` using `<ul><li><strong>...</strong>：...</li></ul>` structure, removing tarot/mystical mapping references.

- [ ] **Step 2: Update the template block**
  - Remove the `<span class="article-builtin-badge">模型内置</span>` tag from `<div class="article-badges">`.
  - Remove the `<footer class="article-footer">` element displaying the model reference and tarot info.

- [ ] **Step 3: Remove unused CSS classes in `<style scoped>`**
  - Delete `.article-builtin-badge` styles.
  - Delete `.article-footer` and `.article-footer strong` styles.

---

### Task 2: Verify the Changes & Compilation

- [ ] **Step 1: Check Vite Compilation**
  - Run: `npm run build`
  - Expected: Clean compilation with zero type errors.

- [ ] **Step 2: Check Backend Tests**
  - Run: `PYTHONPATH=. venv/bin/pytest tests -q` inside `backend/` directory
  - Expected: All backend tests pass successfully.

- [ ] **Step 3: Commit Changes**
  - Run:
  ```bash
  git add src/views/KnowledgeBase.vue docs/project_status.md
  git commit -m "style: clean up tarot metadata, remove builtin tags/footers, and format all articles as lists"
  ```
