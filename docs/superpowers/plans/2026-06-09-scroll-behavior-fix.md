# Scroll Behavior Restoration Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Modify the Vue Router configuration in `src/router/index.ts` to automatically scroll to the top of the page when navigating between routes, ensuring that clicking "进入知识库" from the bottom of the home page loads the Knowledge Base view at the top scroll position.

**Architecture:** Edit `src/router/index.ts` to add the `scrollBehavior` handler option in the `createRouter` config.

**Tech Stack:** Vue Router 4, TypeScript

---

### Task 1: Add scrollBehavior to Router Configuration

**Files:**
- Modify: `src/router/index.ts`

- [ ] **Step 1: Update createRouter config in src/router/index.ts**
  - Add the `scrollBehavior` method definition to `createRouter`:

```typescript
const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(_to, _from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0 }
    }
  }
})
```

---

### Task 2: Verify & Build

- [ ] **Step 1: Check Vite Compilation**
  - Run: `npm run build`
  - Expected: Clean build with zero errors.

- [ ] **Step 2: Check Backend Tests**
  - Run: `PYTHONPATH=. venv/bin/pytest tests -q` inside `backend/`
  - Expected: All tests pass.

- [ ] **Step 3: Commit changes**
  - Run:
  ```bash
  git add src/router/index.ts docs/project_status.md
  git commit -m "feat: add scrollBehavior to vue router for top scroll restoration on route changes"
  ```
