<template>
  <div class="login-container" :class="theme">
    <div class="login-card oracle-gold-corners">
      <!-- Logo and Brand Header -->
      <div class="login-header">
        <div class="logo">
          <svg class="logo-svg" viewBox="0 0 24 24" width="48" height="48">
            <path fill="currentColor" d="M12 2s.07.01.07.07l1.78 3.61 3.98.58c.06.01.08.08.04.12l-2.88 2.81.68 3.97c.01.06-.05.1-.1.07l-3.57-1.87-3.57 1.87c-.05.03-.11-.01-.1-.07l.68-3.97-2.88-2.81c-.04-.04-.02-.11.04-.12l3.98-.58 1.78-3.61c.01-.06.07-.07.07-.07z" />
            <path fill="currentColor" opacity="0.4" d="M12 22c5.52 0 10-4.48 10-10S17.52 2 12 2 2 6.48 2 12s4.48 10 10 10zm0-1c-4.97 0-9-4.03-9-9s4.03-9 9-9 9 4.03 9 9-4.03 9-9 9z" />
            <circle cx="12" cy="12" r="3" fill="currentColor" />
          </svg>
        </div>
        <h1 class="brand-title">Weather Oracle</h1>
      </div>

      <!-- Welcome Banner -->
      <div class="welcome-banner">
        <h2 class="welcome-title"><span class="star-gold">✦</span> 欢迎回来 <span class="star-gold">✦</span></h2>
      </div>
      
      <form @submit.prevent="handleLogin" class="login-form">
        <div class="form-group">
          <label for="username">用户名/邮箱</label>
          <div class="input-wrapper">
            <span class="input-icon-span">
              <svg viewBox="0 0 24 24" width="18" height="18">
                <path fill="currentColor" d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z" />
              </svg>
            </span>
            <input
              id="username"
              v-model="formData.username"
              type="text"
              placeholder="请输入用户名"
              required
              class="input-field"
            />
          </div>
        </div>
        
        <div class="form-group">
          <label for="password">密码</label>
          <div class="input-wrapper">
            <span class="input-icon-span">
              <svg viewBox="0 0 24 24" width="18" height="18">
                <path fill="currentColor" d="M18 8h-1V6c0-2.76-2.24-5-5-5S7 3.24 7 6v2H6c-1.1 0-2 .9-2 2v10c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V10c0-1.1-.9-2-2-2zm-6 9c-1.1 0-2-.9-2-2s.9-2 2-2 2 .9 2 2-.9 2-2 2zm3.1-9H8.9V6c0-1.71 1.39-3.1 3.1-3.1 1.71 0 3.1 1.39 3.1 3.1v2z" />
              </svg>
            </span>
            <input
              id="password"
              v-model="formData.password"
              type="password"
              placeholder="请输入密码"
              required
              class="input-field"
            />
          </div>
        </div>

        <div class="login-options">
          <label class="remember-me">
            <input type="checkbox" v-model="rememberMe" />
            <span>记住我</span>
          </label>
          <a href="#" class="forgot-password" @click.prevent="handleForgotPassword">忘记密码？</a>
        </div>
        
        <button type="submit" class="login-button" :disabled="isLoading">
          <span v-if="isLoading" class="loading-spinner"></span>
          <span v-else>登 录</span>
        </button>
        
        <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
      </form>

      <div class="login-footer">
        <p class="footer-text">
          没有账号？<router-link to="/register" class="register-link">注册账号</router-link>
        </p>
        <p class="footer-policy">继续即表示你同意我们的服务条款和隐私政策</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const formData = ref({
  username: '',
  password: ''
})

const isLoading = ref(false)
const errorMessage = ref('')
const rememberMe = ref(false)

const theme = ref<'dark' | 'light'>('dark')

onMounted(() => {
  const savedTheme = localStorage.getItem('weather_oracle:theme')
  if (savedTheme === 'light' || savedTheme === 'dark') {
    theme.value = savedTheme
  } else {
    theme.value = 'dark'
  }
  document.documentElement.setAttribute('data-oracle-theme', theme.value)
})

const handleLogin = async () => {
  errorMessage.value = ''
  isLoading.value = true

  try {
    const ok = await authStore.login(formData.value.username, formData.value.password)
    if (ok) {
      router.push('/oracle')
    } else {
      errorMessage.value = '用户名或密码错误'
    }
  } catch {
    errorMessage.value = '登录失败，请检查网络连接'
  } finally {
    isLoading.value = false
  }
}

const handleForgotPassword = () => {
  alert('请联系管理员重置密码')
}
</script>

<style scoped>
.login-container.dark {
  --bg-image: url('/login-dark-background.png');
  --bg-overlay: rgba(10, 15, 30, 0.45);
  --card-bg: rgba(8, 16, 29, 0.65);
  --card-border: rgba(215, 174, 105, 0.25);
  --text-color: #f5ebd9;
  --text-muted: #af9f87;
  --text-faint: rgba(245, 235, 217, 0.65);
  --input-bg: rgba(14, 25, 43, 0.5);
  --input-border: rgba(215, 174, 105, 0.15);
  --input-focus-border: #d7ae69;
  --input-focus-shadow: rgba(215, 174, 105, 0.2);
  --btn-bg: linear-gradient(135deg, #d7ae69 0%, #b28542 100%);
  --btn-hover-shadow: rgba(215, 174, 105, 0.3);
  --btn-text: #120e0a;
  --gold-color: #d7ae69;
  --gold-glow: rgba(215, 174, 105, 0.15);
}

.login-container.light {
  --bg-image: url('/login-background.png');
  --bg-overlay: rgba(255, 255, 255, 0.35);
  --card-bg: rgba(253, 249, 243, 0.65);
  --card-border: rgba(180, 140, 85, 0.3);
  --text-color: #3c3020;
  --text-muted: #8c7b64;
  --text-faint: rgba(60, 48, 32, 0.68);
  --input-bg: rgba(253, 249, 243, 0.7);
  --input-border: rgba(180, 140, 85, 0.2);
  --input-focus-border: #b28542;
  --input-focus-shadow: rgba(180, 140, 85, 0.15);
  --btn-bg: linear-gradient(135deg, #b28542 0%, #8c6022 100%);
  --btn-hover-shadow: rgba(180, 140, 85, 0.25);
  --btn-text: #ffffff;
  --gold-color: #b28542;
  --gold-glow: rgba(180, 140, 85, 0.08);
}

.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background-image: var(--bg-image);
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  padding: 20px;
  position: relative;
  transition: background-image 0.5s ease;
  overflow: hidden;
}

.login-container::before {
  content: '';
  position: absolute;
  inset: 0;
  background: var(--bg-overlay);
  backdrop-filter: blur(4px);
  z-index: 0;
  transition: background 0.5s ease, backdrop-filter 0.5s ease;
}



.login-card {
  background: var(--card-bg);
  backdrop-filter: blur(20px);
  border-radius: 16px;
  border: 1px solid var(--card-border);
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.3);
  padding: 40px 36px;
  width: 100%;
  max-width: 420px;
  animation: slideUp 0.6s cubic-bezier(0.16, 1, 0.3, 1);
  position: relative;
  z-index: 1;
  color: var(--text-color);
  transition: all 0.5s ease;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(40px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.oracle-gold-corners::before,
.oracle-gold-corners::after {
  content: '';
  position: absolute;
  width: 12px;
  height: 12px;
  border: 1.5px solid var(--gold-color);
  pointer-events: none;
  z-index: 2;
  opacity: 0.85;
  transition: all 0.5s ease;
}

.oracle-gold-corners::before {
  top: 8px;
  left: 8px;
  border-right: none;
  border-bottom: none;
}

.oracle-gold-corners::after {
  bottom: 8px;
  right: 8px;
  border-left: none;
  border-top: none;
}

.login-header {
  text-align: center;
  margin-bottom: 24px;
}

.logo {
  margin-bottom: 12px;
  display: inline-block;
}

.logo-svg {
  color: var(--gold-color);
  filter: drop-shadow(0 0 4px var(--gold-glow));
  animation: pulse-mystical 3s ease-in-out infinite;
}

@keyframes pulse-mystical {
  0%, 100% {
    opacity: 0.8;
    transform: scale(1);
  }
  50% {
    opacity: 1;
    transform: scale(1.05);
  }
}

.brand-title {
  font-family: 'Cinzel', serif, var(--oracle-font-display);
  font-size: 24px;
  font-weight: 700;
  letter-spacing: 0.08em;
  margin: 0;
  color: var(--text-color);
}

.welcome-banner {
  text-align: center;
  margin-bottom: 24px;
  border-bottom: 1px solid var(--input-border);
  padding-bottom: 16px;
}

.welcome-title {
  font-size: 18px;
  font-weight: 600;
  margin: 0;
  letter-spacing: 0.05em;
}

.star-gold {
  color: var(--gold-color);
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group label {
  font-size: 13px;
  font-weight: 500;
  color: var(--text-muted);
  letter-spacing: 0.02em;
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.input-icon-span {
  position: absolute;
  left: 14px;
  color: var(--text-muted);
  pointer-events: none;
  display: flex;
  align-items: center;
}

.input-field {
  width: 100%;
  padding: 12px 16px 12px 42px;
  background: var(--input-bg);
  border: 1px solid var(--input-border);
  border-radius: 8px;
  font-size: 14px;
  color: var(--text-color);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  outline: none;
}

.input-field::placeholder {
  color: var(--text-muted);
  opacity: 0.6;
}

.input-field:focus {
  border-color: var(--input-focus-border);
  background: var(--card-bg);
  box-shadow: 0 0 10px var(--input-focus-shadow);
}

.login-options {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 13px;
  margin-top: 2px;
}

.remember-me {
  display: flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
  color: var(--text-muted);
  user-select: none;
}

.remember-me input[type="checkbox"] {
  accent-color: var(--gold-color);
  cursor: pointer;
}

.forgot-password {
  color: var(--gold-color);
  text-decoration: none;
  transition: color 0.3s ease;
}

.forgot-password:hover {
  color: var(--text-color);
  text-decoration: underline;
}

.login-button {
  margin-top: 8px;
  padding: 12px;
  background: var(--btn-bg);
  color: var(--btn-text);
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  box-shadow: 0 4px 15px rgba(0,0,0,0.15);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.login-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px var(--btn-hover-shadow);
  filter: brightness(1.05);
}

.login-button:active:not(:disabled) {
  transform: translateY(0);
}

.login-button:disabled {
  opacity: 0.65;
  cursor: not-allowed;
}

.loading-spinner {
  width: 20px;
  height: 20px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: var(--btn-text);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.error-message {
  color: #ff6b6b;
  font-size: 13px;
  text-align: center;
  margin: 4px 0 0 0;
  padding: 10px;
  background: rgba(255, 107, 107, 0.12);
  border-radius: 6px;
  border: 1px solid rgba(255, 107, 107, 0.2);
  animation: shake 0.4s ease-in-out;
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-6px); }
  75% { transform: translateX(6px); }
}

.login-footer {
  margin-top: 24px;
  text-align: center;
}

.footer-text {
  font-size: 13px;
  color: var(--text-muted);
  margin: 0;
}

.register-link {
  color: var(--gold-color);
  text-decoration: none;
  font-weight: 600;
}

.register-link:hover {
  text-decoration: underline;
}

.footer-policy {
  font-size: 11px;
  color: var(--text-faint);
  margin: 12px 0 0 0;
  opacity: 0.8;
}

@media (max-width: 480px) {
  .login-card {
    padding: 32px 24px;
  }
  .brand-title {
    font-size: 20px;
  }
}
</style>
