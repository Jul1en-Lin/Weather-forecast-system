<template>
  <div class="register-container">
    <div class="register-card">
      <div class="register-header">
        <div class="logo">
          <span class="logo-icon">🌤️</span>
        </div>
        <h1 class="title">用户注册</h1>
        <p class="subtitle">创建您的账户</p>
      </div>

      <form @submit.prevent="handleRegister" class="register-form">
        <div class="form-group">
          <label for="username">用户名</label>
          <input
            id="username"
            v-model="formData.username"
            type="text"
            placeholder="请输入用户名（3-64个字符）"
            required
            minlength="3"
            maxlength="64"
            class="input-field"
          />
        </div>

        <div class="form-group">
          <label for="password">密码</label>
          <input
            id="password"
            v-model="formData.password"
            type="password"
            placeholder="请输入密码（6-128个字符）"
            required
            minlength="6"
            maxlength="128"
            class="input-field"
          />
        </div>

        <div class="form-group">
          <label for="confirmPassword">确认密码</label>
          <input
            id="confirmPassword"
            v-model="formData.confirmPassword"
            type="password"
            placeholder="请再次输入密码"
            required
            class="input-field"
          />
        </div>

        <button type="submit" class="register-button" :disabled="isLoading">
          <span v-if="isLoading" class="loading-spinner"></span>
          <span v-else>注 册</span>
        </button>

        <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
        <p v-if="successMessage" class="success-message">{{ successMessage }}</p>
      </form>

      <div class="register-footer">
        <p class="footer-text">
          已有账号？<router-link to="/login" class="login-link">立即登录</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const formData = ref({
  username: '',
  password: '',
  confirmPassword: ''
})

const isLoading = ref(false)
const errorMessage = ref('')
const successMessage = ref('')

const handleRegister = async () => {
  errorMessage.value = ''
  successMessage.value = ''

  if (formData.value.password !== formData.value.confirmPassword) {
    errorMessage.value = '两次输入的密码不一致'
    return
  }

  isLoading.value = true

  try {
    const result = await authStore.register(formData.value.username, formData.value.password)
    if (result.success) {
      successMessage.value = '注册成功！即将跳转到登录页面...'
      setTimeout(() => {
        router.push('/login')
      }, 1500)
    } else {
      errorMessage.value = result.error || '注册失败'
    }
  } catch {
    errorMessage.value = '注册失败，请检查网络连接'
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.register-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background-image: url('/background.jpg');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  padding: 20px;
  position: relative;
}

.register-container::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.4);
  backdrop-filter: blur(5px);
}

.register-card {
  background: rgba(255, 255, 255, 0.4);
  backdrop-filter: blur(20px);
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.5);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.15);
  padding: 48px 40px;
  width: 100%;
  max-width: 420px;
  animation: slideUp 0.6s ease-out;
  position: relative;
  z-index: 1;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.register-header {
  text-align: center;
  margin-bottom: 40px;
}

.logo {
  margin-bottom: 20px;
}

.logo-icon {
  font-size: 64px;
  display: inline-block;
  animation: float 3s ease-in-out infinite;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
}

.title {
  font-size: 24px;
  font-weight: 600;
  color: #1d1d1f;
  margin: 0 0 8px 0;
  letter-spacing: -0.5px;
}

.subtitle {
  font-size: 14px;
  color: #1d1d1f;
  margin: 0;
  text-shadow: 0 1px 2px rgba(255, 255, 255, 0.5);
}

.register-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group label {
  font-size: 14px;
  font-weight: 500;
  color: #1d1d1f;
}

.input-field {
  padding: 12px 16px;
  border: 1px solid rgba(255, 255, 255, 0.4);
  border-radius: 12px;
  font-size: 16px;
  transition: all 0.3s ease;
  outline: none;
  background: rgba(255, 255, 255, 0.3);
  backdrop-filter: blur(10px);
  color: #1d1d1f;
}

.input-field:focus {
  border-color: #007aff;
  background: rgba(255, 255, 255, 0.5);
  box-shadow: 0 0 0 3px rgba(0, 122, 255, 0.1);
}

.input-field::placeholder {
  color: #86868b;
}

.register-button {
  margin-top: 10px;
  padding: 14px;
  background: linear-gradient(135deg, #007aff 0%, #0056cc 100%);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 17px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.register-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(0, 122, 255, 0.4);
}

.register-button:active:not(:disabled) {
  transform: translateY(0);
}

.register-button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.loading-spinner {
  width: 20px;
  height: 20px;
  border: 3px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.error-message {
  color: #ff3b30;
  font-size: 14px;
  text-align: center;
  margin: 0;
  padding: 10px;
  background: rgba(255, 59, 48, 0.15);
  backdrop-filter: blur(10px);
  border-radius: 8px;
  border: 1px solid rgba(255, 59, 48, 0.3);
  animation: shake 0.5s ease-in-out;
}

.success-message {
  color: #34c759;
  font-size: 14px;
  text-align: center;
  margin: 0;
  padding: 10px;
  background: rgba(52, 199, 89, 0.15);
  backdrop-filter: blur(10px);
  border-radius: 8px;
  border: 1px solid rgba(52, 199, 89, 0.3);
}

@keyframes shake {
  0%, 100% {
    transform: translateX(0);
  }
  25% {
    transform: translateX(-5px);
  }
  75% {
    transform: translateX(5px);
  }
}

.register-footer {
  margin-top: 30px;
  text-align: center;
}

.footer-text {
  font-size: 14px;
  color: #1d1d1f;
  margin: 0;
  text-shadow: 0 1px 2px rgba(255, 255, 255, 0.5);
}

.login-link {
  color: #007aff;
  text-decoration: none;
  font-weight: 500;
}

.login-link:hover {
  text-decoration: underline;
}

@media (max-width: 480px) {
  .register-card {
    padding: 32px 24px;
  }

  .title {
    font-size: 20px;
  }
}
</style>