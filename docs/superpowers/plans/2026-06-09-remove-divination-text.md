# Remove Divination-Related Text Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Remove all divination-related text prompts ("气象占卜台", "天气占卜之旅") from the login and register pages, and add star decoration to the welcome titles (e.g. "✦ 欢迎回来 ✦").

**Architecture:** We will modify the HTML templates of the Vue single-file components `Login.vue` and `Register.vue` to delete the `<p>` elements containing the divination phrases, update the `welcome-title` texts, and clean up any unused CSS rules.

**Tech Stack:** Vue 3, Vite, TypeScript

---

### Task 1: Modify Login Page Template and Styles

**Files:**
- Modify: `src/views/Login.vue`

- [ ] **Step 1: Remove the brand subtitle**
Locate the brand subtitle in [Login.vue](file:///Users/lien/GitRepo/Weather-forecast-system/src/views/Login.vue):
```html
        <p class="brand-subtitle">✦ 气象占卜台 ✦</p>
```
and delete it.

- [ ] **Step 2: Update the welcome title and remove welcome subtitle**
In [Login.vue](file:///Users/lien/GitRepo/Weather-forecast-system/src/views/Login.vue):
Change:
```html
        <h2 class="welcome-title">欢迎回来</h2>
        <p class="welcome-subtitle">✦ 登录以继续你的天气占卜之旅 ✦</p>
```
to:
```html
        <h2 class="welcome-title">✦ 欢迎回来 ✦</h2>
```

- [ ] **Step 3: Remove unused scoped CSS classes**
In [Login.vue](file:///Users/lien/GitRepo/Weather-forecast-system/src/views/Login.vue) style block:
Find and remove the styles for `.brand-subtitle` and `.welcome-subtitle` to keep the codebase clean.

- [ ] **Step 4: Commit the Login.vue changes**
Run:
```bash
git add src/views/Login.vue
git commit -m "style: remove divination text and add stars to welcome title on Login page"
```

---

### Task 2: Modify Register Page Template and Styles

**Files:**
- Modify: `src/views/Register.vue`

- [ ] **Step 1: Remove the brand subtitle**
Locate the brand subtitle in [Register.vue](file:///Users/lien/GitRepo/Weather-forecast-system/src/views/Register.vue):
```html
        <p class="brand-subtitle">✦ 气象占卜台 ✦</p>
```
and delete it.

- [ ] **Step 2: Update the welcome title and remove welcome subtitle**
In [Register.vue](file:///Users/lien/GitRepo/Weather-forecast-system/src/views/Register.vue):
Change:
```html
        <h2 class="welcome-title">创建您的账户</h2>
        <p class="welcome-subtitle">✦ 开启你的天气占卜之旅 ✦</p>
```
to:
```html
        <h2 class="welcome-title">✦ 创建您的账户 ✦</h2>
```

- [ ] **Step 3: Remove unused scoped CSS classes**
In [Register.vue](file:///Users/lien/GitRepo/Weather-forecast-system/src/views/Register.vue) style block:
Find and remove the styles for `.brand-subtitle` and `.welcome-subtitle`.

- [ ] **Step 4: Commit the Register.vue changes**
Run:
```bash
git add src/views/Register.vue
git commit -m "style: remove divination text and add stars to welcome title on Register page"
```

---

### Task 3: Build Verification

**Files:**
- None

- [ ] **Step 1: Run compilation build to verify changes don't break frontend build**
Run: `npm run build`
Expected: Successful compile with no TypeScript or build errors.
