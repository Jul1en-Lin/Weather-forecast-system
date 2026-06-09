# Remove Divination-Related Text Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Remove all divination-related text prompts ("气象占卜台", "天气占卜之旅") from the login and register pages.

**Architecture:** We will modify the HTML templates of the Vue single-file components `Login.vue` and `Register.vue` to delete the `<p>` elements containing the divination phrases.

**Tech Stack:** Vue 3, Vite, TypeScript

---

### Task 1: Modify Login Page Template

**Files:**
- Modify: `src/views/Login.vue`

- [ ] **Step 1: Locate and remove the brand subtitle**

Locate the brand subtitle in [Login.vue](file:///Users/lien/GitRepo/Weather-forecast-system/src/views/Login.vue):
```html
        <p class="brand-subtitle">✦ 气象占卜台 ✦</p>
```
and delete it.

- [ ] **Step 2: Locate and remove the welcome subtitle**

Locate the welcome subtitle in [Login.vue](file:///Users/lien/GitRepo/Weather-forecast-system/src/views/Login.vue):
```html
        <p class="welcome-subtitle">✦ 登录以继续你的天气占卜之旅 ✦</p>
```
and delete it.

- [ ] **Step 3: Commit the Login.vue changes**

```bash
git add src/views/Login.vue
git commit -m "style: remove divination subtitles from Login page"
```

---

### Task 2: Modify Register Page Template

**Files:**
- Modify: `src/views/Register.vue`

- [ ] **Step 1: Locate and remove the brand subtitle**

Locate the brand subtitle in [Register.vue](file:///Users/lien/GitRepo/Weather-forecast-system/src/views/Register.vue):
```html
        <p class="brand-subtitle">✦ 气象占卜台 ✦</p>
```
and delete it.

- [ ] **Step 2: Locate and remove the welcome subtitle**

Locate the welcome subtitle in [Register.vue](file:///Users/lien/GitRepo/Weather-forecast-system/src/views/Register.vue):
```html
        <p class="welcome-subtitle">✦ 开启你的天气占卜之旅 ✦</p>
```
and delete it.

- [ ] **Step 3: Commit the Register.vue changes**

```bash
git add src/views/Register.vue
git commit -m "style: remove divination subtitles from Register page"
```

---

### Task 3: Build Verification

**Files:**
- None

- [ ] **Step 1: Run compilation build to verify changes don't break frontend build**

Run: `npm run build`
Expected: Successful compile with no TypeScript or build errors.
