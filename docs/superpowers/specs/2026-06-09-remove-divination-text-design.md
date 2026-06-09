# Design: Remove Divination-Related Text from Login and Register Pages

This design document specifies the removal of divination-related terms ("占卜") from the user authentication interfaces and styling adjustments.

## 1. Problem Statement
The current login and registration pages contain subtitles and brand subtitles referencing "气象占卜台" (Meteorological Divination Platform) and "天气占卜之旅" (weather divination journey). The user requested to remove these references entirely, while keeping the star motifs (✦) around the welcome text.

## 2. Solution Summary
- **Brand Subtitle**: Completely delete `<p class="brand-subtitle">✦ 气象占卜台 ✦</p>` from both Login and Register pages.
- **Welcome Section**:
  - In `Login.vue`: Replace `<h2 class="welcome-title">欢迎回来</h2>` with `<h2 class="welcome-title">✦ 欢迎回来 ✦</h2>`, and remove the welcome subtitle `<p class="welcome-subtitle">✦ 登录以继续你的天气占卜之旅 ✦</p>`.
  - In `Register.vue`: Replace `<h2 class="welcome-title">创建您的账户</h2>` with `<h2 class="welcome-title">✦ 创建您的账户 ✦</h2>`, and remove the welcome subtitle `<p class="welcome-subtitle">✦ 开启你的天气占卜之旅 ✦</p>`.

## 3. Detailed Changes

### 3.1 Login Page
In `src/views/Login.vue`:
- Remove:
  ```html
  <p class="brand-subtitle">✦ 气象占卜台 ✦</p>
  ```
- Change:
  ```html
  <h2 class="welcome-title">欢迎回来</h2>
  ```
  to:
  ```html
  <h2 class="welcome-title">✦ 欢迎回来 ✦</h2>
  ```
- Remove:
  ```html
  <p class="welcome-subtitle">✦ 登录以继续你的天气占卜之旅 ✦</p>
  ```

### 3.2 Register Page
In `src/views/Register.vue`:
- Remove:
  ```html
  <p class="brand-subtitle">✦ 气象占卜台 ✦</p>
  ```
- Change:
  ```html
  <h2 class="welcome-title">创建您的账户</h2>
  ```
  to:
  ```html
  <h2 class="welcome-title">✦ 创建您的账户 ✦</h2>
  ```
- Remove:
  ```html
  <p class="welcome-subtitle">✦ 开启你的天气占卜之旅 ✦</p>
  ```

## 4. Verification Plan
- Verify that `Login.vue` and `Register.vue` compile successfully using `npm run build` or Vite type checks.
- Visually verify that the pages display `✦ 欢迎回来 ✦` and `✦ 创建您的账户 ✦` with no subtitles.
