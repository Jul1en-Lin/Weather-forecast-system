# User Management Page Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Redesign the User Management view (`src/views/AdminUsers.vue`) to align with the theme variables, replacing hardcoded RGBA colors with theme-aware RGB variables.

**Architecture:** Modify `src/views/AdminUsers.vue`'s scoped stylesheet. Update colors in `.badge-pill-admin`, `.btn-card-action.edit-btn:hover`, `.btn-card-action.delete-btn`, `.success-message`, and `.error-message` to use CSS custom properties from `oracle-theme.css`.

**Tech Stack:** Vue 3, Vite, TypeScript, CSS Variables.

---

### Task 1: Redesign CSS Stylesheet in AdminUsers.vue

**Files:**
- Modify: `src/views/AdminUsers.vue`
- Verify: `npm run build`

- [ ] **Step 1: Replace hardcoded RGBA colors in scoped styles**

  In `src/views/AdminUsers.vue` starting around line 269:
  - Replace `rgba(215, 174, 105, ...)` with `rgba(var(--oracle-gold-rgb), ...)`.
  - Replace `rgba(207, 110, 91, ...)` with `rgba(var(--oracle-danger-rgb), ...)`.
  - Replace `rgba(84, 191, 163, ...)` with `rgba(var(--oracle-success-rgb), ...)`.

  *Exact target CSS block to modify:*
  ```css
  /* Badges */
  .badge-pill {
    display: inline-block;
    padding: 2px 8px;
    border-radius: 99px;
    font-size: 11px;
    font-weight: 600;
    border: 1px solid transparent;
  }

  .badge-pill-admin {
    border-color: rgba(215, 174, 105, 0.25);
    background: rgba(215, 174, 105, 0.08);
    color: var(--oracle-gold);
  }

  .badge-pill-user {
    border-color: var(--oracle-border-soft);
    background: rgba(255, 255, 255, 0.02);
    color: var(--oracle-muted);
  }

  [data-oracle-theme='light'] .badge-pill-user {
    background: rgba(0, 0, 0, 0.02);
  }

  /* Action Buttons */
  .user-card-actions {
    display: flex;
    gap: 8px;
  }

  .btn-card-action {
    font-size: 13px;
    padding: 6px 12px;
    border-radius: 8px;
    font-weight: 500;
    border: 1px solid var(--oracle-border-soft);
    background: rgba(255, 255, 255, 0.02);
    color: var(--oracle-text);
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .btn-card-action.edit-btn:hover {
    border-color: var(--oracle-gold);
    background: rgba(215, 174, 105, 0.08);
    color: var(--oracle-gold);
  }

  .btn-card-action.delete-btn {
    border-color: rgba(207, 110, 91, 0.25);
    background: rgba(207, 110, 91, 0.05);
    color: var(--oracle-danger);
  }

  .btn-card-action.delete-btn:hover {
    background: rgba(207, 110, 91, 0.15);
    border-color: var(--oracle-danger);
  }

  /* Card Body */
  .user-card-body {
    padding: 24px;
    display: flex;
    flex-direction: column;
    flex: 1;
  }

  .user-meta-info {
    background: rgba(0, 0, 0, 0.15);
    border-radius: 12px;
    padding: 16px;
    display: flex;
    flex-direction: column;
    gap: 10px;
    border: 1px solid var(--oracle-border-soft);
  }

  [data-oracle-theme='light'] .user-meta-info {
    background: rgba(0, 0, 0, 0.03);
  }

  .meta-row {
    display: flex;
    font-size: 13px;
    line-height: 1.4;
    justify-content: space-between;
  }

  .meta-label {
    color: var(--oracle-muted);
    font-weight: 500;
    flex-shrink: 0;
  }

  .meta-value {
    color: var(--oracle-text);
    word-break: break-all;
    text-align: right;
  }

  code.meta-value {
    font-family: SFMono-Regular, Consolas, monospace;
    background: rgba(255, 255, 255, 0.05);
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 12px;
  }

  [data-oracle-theme='light'] code.meta-value {
    background: rgba(0, 0, 0, 0.05);
  }

  /* Feedback Messages */
  .success-message {
    margin: 24px 0 0 0;
    padding: 14px 20px;
    background: rgba(84, 191, 163, 0.15);
    color: var(--oracle-success);
    border-radius: 10px;
    font-size: 14px;
    text-align: center;
    font-weight: 500;
    border: 1px solid rgba(84, 191, 163, 0.2);
  }

  .error-message {
    margin: 24px 0 0 0;
    padding: 14px 20px;
    background: rgba(207, 110, 91, 0.15);
    color: var(--oracle-danger);
    border-radius: 10px;
    font-size: 14px;
    text-align: center;
    font-weight: 500;
    border: 1px solid rgba(207, 110, 91, 0.2);
  }
  ```

  *Exact replacement CSS block:*
  ```css
  /* Badges */
  .badge-pill {
    display: inline-block;
    padding: 2px 8px;
    border-radius: 99px;
    font-size: 11px;
    font-weight: 600;
    border: 1px solid transparent;
  }

  .badge-pill-admin {
    border-color: rgba(var(--oracle-gold-rgb), 0.25);
    background: rgba(var(--oracle-gold-rgb), 0.08);
    color: var(--oracle-gold);
  }

  .badge-pill-user {
    border-color: var(--oracle-border-soft);
    background: rgba(255, 255, 255, 0.02);
    color: var(--oracle-muted);
  }

  [data-oracle-theme='light'] .badge-pill-user {
    background: rgba(0, 0, 0, 0.02);
  }

  /* Action Buttons */
  .user-card-actions {
    display: flex;
    gap: 8px;
  }

  .btn-card-action {
    font-size: 13px;
    padding: 6px 12px;
    border-radius: 8px;
    font-weight: 500;
    border: 1px solid var(--oracle-border-soft);
    background: rgba(255, 255, 255, 0.02);
    color: var(--oracle-text);
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .btn-card-action.edit-btn:hover {
    border-color: var(--oracle-gold);
    background: rgba(var(--oracle-gold-rgb), 0.08);
    color: var(--oracle-gold);
  }

  .btn-card-action.delete-btn {
    border-color: rgba(var(--oracle-danger-rgb), 0.25);
    background: rgba(var(--oracle-danger-rgb), 0.05);
    color: var(--oracle-danger);
  }

  .btn-card-action.delete-btn:hover {
    background: rgba(var(--oracle-danger-rgb), 0.15);
    border-color: var(--oracle-danger);
  }

  /* Card Body */
  .user-card-body {
    padding: 24px;
    display: flex;
    flex-direction: column;
    flex: 1;
  }

  .user-meta-info {
    background: rgba(0, 0, 0, 0.15);
    border-radius: 12px;
    padding: 16px;
    display: flex;
    flex-direction: column;
    gap: 10px;
    border: 1px solid var(--oracle-border-soft);
  }

  [data-oracle-theme='light'] .user-meta-info {
    background: rgba(0, 0, 0, 0.03);
  }

  .meta-row {
    display: flex;
    font-size: 13px;
    line-height: 1.4;
    justify-content: space-between;
  }

  .meta-label {
    color: var(--oracle-muted);
    font-weight: 500;
    flex-shrink: 0;
  }

  .meta-value {
    color: var(--oracle-text);
    word-break: break-all;
    text-align: right;
  }

  code.meta-value {
    font-family: SFMono-Regular, Consolas, monospace;
    background: rgba(255, 255, 255, 0.05);
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 12px;
  }

  [data-oracle-theme='light'] code.meta-value {
    background: rgba(0, 0, 0, 0.05);
  }

  /* Feedback Messages */
  .success-message {
    margin: 24px 0 0 0;
    padding: 14px 20px;
    background: rgba(var(--oracle-success-rgb), 0.12);
    color: var(--oracle-success);
    border-radius: 10px;
    font-size: 14px;
    text-align: center;
    font-weight: 500;
    border: 1px solid rgba(var(--oracle-success-rgb), 0.2);
  }

  .error-message {
    margin: 24px 0 0 0;
    padding: 14px 20px;
    background: rgba(var(--oracle-danger-rgb), 0.12);
    color: var(--oracle-danger);
    border-radius: 10px;
    font-size: 14px;
    text-align: center;
    font-weight: 500;
    border: 1px solid rgba(var(--oracle-danger-rgb), 0.2);
  }
  ```

- [ ] **Step 2: Verify Vite build compilation**

  Run: `npm run build`
  Expected: Command succeeds with zero compiler/Vite bundle errors.

- [ ] **Step 3: Commit changes**

  ```bash
  git add src/views/AdminUsers.vue
  git commit -m "style(admin): align user management page styles with oracle theme using RGB variables"
  ```
