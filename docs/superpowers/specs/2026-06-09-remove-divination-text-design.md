# Design: Remove Divination-Related Text from Login and Register Pages

This design document specifies the removal of divination-related terms ("占卜") from the user authentication interfaces to make the application branding cleaner and more standard.

## 1. Problem Statement
The current login and registration pages contain subtitles and brand subtitles referencing "气象占卜台" (Meteorological Divination Platform) and "天气占卜之旅" (weather divination journey). The user requested to remove these references entirely to simplify the text and keep the interface clean.

## 2. Solution Summary
We will directly delete the subtitle `<p>` elements containing these phrases from the Vue components for both the Login page and the Register page.

## 3. Detailed Changes

### 3.1 Login Page
In `src/views/Login.vue`:
- Remove the line:
  ```html
  <p class="brand-subtitle">✦ 气象占卜台 ✦</p>
  ```
- Remove the line:
  ```html
  <p class="welcome-subtitle">✦ 登录以继续你的天气占卜之旅 ✦</p>
  ```

### 3.2 Register Page
In `src/views/Register.vue`:
- Remove the line:
  ```html
  <p class="brand-subtitle">✦ 气象占卜台 ✦</p>
  ```
- Remove the line:
  ```html
  <p class="welcome-subtitle">✦ 开启你的天气占卜之旅 ✦</p>
  ```

## 4. Verification Plan
- Verify that `Login.vue` and `Register.vue` compile successfully using `npm run build` or Vite type checks.
- Visually verify that the pages no longer display these subtitles.
