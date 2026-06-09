# 登录与注册页面重构设计文档

## 1. 背景与目标
当前系统的登录与注册页面为旧版本（Apple简约亮色风），不符合现有的 **Weather Oracle 气象占卜台** 的高感官神密星象风格。此外，用户登录成功后会被引导至旧中转页（`/home`，即“大语言模型气象业务应用平台”），产生了多余的页面层级。

本设计的目标是：
1. 重构 `src/views/Login.vue` 和 `src/views/Register.vue`，采用以选项 A（现代磨砂玻璃态）为主、辅以选项 B（占卜台金色角折线）的磨砂玻璃化视觉风格。
2. 登录与注册功能只保留用户名与密码方式，不显示或屏蔽 GitHub 第三方登录，且无任何塔罗牌、预测等重度占卜元素。
3. 登录成功后直接跳转至 Weather Oracle 气象占卜台主页（`/oracle`）。
4. 修改路由将 `/home` 重定向至 `/oracle`，并安全删除不再使用的 `src/views/Home.vue`。

---

## 2. 视觉设计细节
重构页面将根据用户的亮暗主题偏好自适应调整背景与卡片配色，并支持右上角悬浮的手动切换：

### 2.1 全屏玻璃模糊背景
* **亮色模式**：
  * 背景图片：`login-background.png`
  * 遮罩层：`background: rgba(255, 255, 255, 0.35); backdrop-filter: blur(8px);`
* **暗色模式**：
  * 背景图片：`login-dark-background.png`
  * 遮罩层：`background: rgba(10, 15, 30, 0.45); backdrop-filter: blur(8px);`

### 2.2 磨砂玻璃态卡片 (Frosted Glassmorphic Card)
* **卡片背景**：
  * 亮色：`rgba(253, 249, 243, 0.65)`（复用 Oracle 亮色面板基色）
  * 暗色：`rgba(8, 16, 29, 0.65)`（复用 Oracle 暗色面板基色）
  * 模糊度：`backdrop-filter: blur(20px)`
  * 阴影：`box-shadow: 0 20px 50px rgba(0, 0, 0, 0.3)`
* **卡片边框与金角装饰**：
  * 亮色：`1px solid rgba(180, 140, 85, 0.3)`
  * 暗色：`1px solid rgba(215, 174, 105, 0.25)`
  * 金角装饰：在卡片四角增加极简的折线金色边角修饰（亮色 `b28542`，暗色 `d7ae69`），提供古典气象占卜台的轻微点缀。

---

## 3. 页面内容与组件结构

### 3.1 登录页 (`Login.vue`)
* **头部品牌 (Logo Brand)**：
  * 精致的星象 Logo SVG（复用 `OracleLayout.vue` 中的金色星芒图标）。
  * 标题：`Weather Oracle` (Cinzel/serif 字体)
  * 副标题：`气象占卜台` (Marcellus/serif 字体，亮金色)
* **主迎宾语 (Welcome Banner)**：
  * 标题：`✦ 欢迎回来 ✦`
  * 引导语：`登录以继续你的天气占卜之旅` (小字，柔和金沙色)
* **表单控件 (Inputs)**：
  * 👤 用户名/邮箱输入框（带 `user` 矢量图标前缀，聚焦时外发光）。
  * 🔒 密码输入框（带 `lock` 矢量图标前缀，聚焦时外发光）。
  * “记住我”复选框 & “忘记密码？”链接（复选框与文字颜色适配亮暗模式）。
* **操作区域 (CTAs)**：
  * 登录主按钮：磨砂金色渐变背景，聚焦与悬浮有呼吸发光及轻微上浮缩放动效。
  * 注册账号链接：跳转至 `/register`。
  * 页脚服务条款声明：“继续即表示你同意我们的服务条款和隐私政策”。

### 3.2 注册页 (`Register.vue`)
* 结构同登录页，表单包含：
  * 用户名
  * 密码
  * 确认密码
* 注册主按钮及返回登录链接（`已有账号？立即登录`）。

---

## 4. 逻辑与路由变更
1. **成功登录跳转**：
   * 在 `Login.vue` 的 `handleLogin` 成功后，执行 `router.push('/oracle')`。
2. **路由定义重置**：
   * 修改 `src/router/index.ts`：
     ```typescript
     {
       path: '/home',
       redirect: '/oracle'
     }
     ```
3. **文件删除**：
   * 物理删除 `src/views/Home.vue`。
