<template>
  <div class="home-container">
    <!-- 左侧导航栏 -->
    <aside class="sidebar">
      <div class="sidebar-header">
        <div class="logo">
          <span class="logo-icon">🌤️</span>
        </div>
        <h2 class="platform-name">气象平台</h2>
      </div>

      <nav class="nav-menu">
        <router-link to="/home" class="nav-item" active-class="active">
          <span class="nav-icon">🏠</span>
          <span class="nav-text">首页</span>
        </router-link>

        <router-link to="/intelligent-assistant" class="nav-item" active-class="active">
          <span class="nav-icon">🤖</span>
          <span class="nav-text">智能助手</span>
        </router-link>

        <router-link to="/settings" class="nav-item active" active-class="active">
          <span class="nav-icon">⚙️</span>
          <span class="nav-text">系统设置</span>
        </router-link>

        <router-link v-if="isAdmin" to="/admin/users" class="nav-item" active-class="active">
          <span class="nav-icon">👥</span>
          <span class="nav-text">用户管理</span>
        </router-link>
      </nav>

      <div class="sidebar-footer">
        <div class="user-info">
          <div class="user-avatar">
            {{ userInitial }}
          </div>
          <div class="user-details">
            <p class="username">{{ username }}</p>
            <p class="user-role">{{ isAdmin ? '管理员' : '普通用户' }}</p>
          </div>
        </div>
        <button @click="handleLogout" class="logout-button">
          退出登录
        </button>
      </div>
    </aside>

    <!-- 右侧主内容区 -->
    <main class="main-content">
      <div class="content-wrapper">
        <!-- 标签页切换 -->
        <div class="tab-nav">
          <button
            v-for="tab in tabs"
            :key="tab.id"
            :class="['tab-btn', { active: activeTab === tab.id }]"
            @click="activeTab = tab.id"
          >
            <span class="tab-icon">{{ tab.icon }}</span>
            <span class="tab-text">{{ tab.label }}</span>
          </button>
        </div>

        <!-- 加载状态 -->
        <div v-if="loading" class="loading-container">
          <div class="spinner"></div>
          <p>加载配置中...</p>
        </div>

        <!-- 配置内容 -->
        <form v-else @submit.prevent="handleSave" class="settings-form">
          <!-- LLM 模型配置 -->
          <div v-show="activeTab === 'llm'" class="config-section">
            <div class="section-header">
              <span class="section-icon">🤖</span>
              <span>LLM 模型配置</span>
            </div>

            <div class="config-grid">
              <div class="config-card">
                <label>Kimi API Key</label>
                <input
                  v-model="formData.kimi_api_key"
                  type="password"
                  placeholder="sk-xxxxxxxx"
                  autocomplete="off"
                />
                <span v-if="maskedConfig.kimi_api_key" class="current-value">
                  当前值: {{ maskedConfig.kimi_api_key }}
                </span>
              </div>

              <div class="config-card">
                <label>DeepSeek API Key</label>
                <input
                  v-model="formData.deepseek_api_key"
                  type="password"
                  placeholder="sk-xxxxxxxx"
                  autocomplete="off"
                />
                <span v-if="maskedConfig.deepseek_api_key" class="current-value">
                  当前值: {{ maskedConfig.deepseek_api_key }}
                </span>
              </div>

              <div class="config-card">
                <label>MiniMax API Key</label>
                <input
                  v-model="formData.minimax_api_key"
                  type="password"
                  placeholder="sk-xxxxxxxx"
                  autocomplete="off"
                />
                <span v-if="maskedConfig.minimax_api_key" class="current-value">
                  当前值: {{ maskedConfig.minimax_api_key }}
                </span>
              </div>

              <div class="config-card">
                <label>Ollama 本地地址</label>
                <input
                  v-model="formData.ollama_base_url"
                  type="text"
                  placeholder="http://localhost:11434/v1"
                />
                <span v-if="maskedConfig.ollama_base_url" class="current-value">
                  当前值: {{ maskedConfig.ollama_base_url }}
                </span>
              </div>
            </div>
          </div>

          <!-- 天气服务配置 -->
          <div v-show="activeTab === 'weather'" class="config-section">
            <div class="section-header">
              <span class="section-icon">🌤️</span>
              <span>天气服务配置</span>
            </div>

            <div class="config-grid">
              <div class="config-card">
                <label>Tavily API Key</label>
                <input
                  v-model="formData.tavily_api_key"
                  type="password"
                  placeholder="tvly-xxxxxxxx"
                  autocomplete="off"
                />
                <span v-if="maskedConfig.tavily_api_key" class="current-value">
                  当前值: {{ maskedConfig.tavily_api_key }}
                </span>
              </div>

              <div class="config-card">
                <label>和风天气 API Key</label>
                <input
                  v-model="formData.qweather_api_key"
                  type="password"
                  placeholder="xxxxxxxx"
                  autocomplete="off"
                />
                <span v-if="maskedConfig.qweather_api_key" class="current-value">
                  当前值: {{ maskedConfig.qweather_api_key }}
                </span>
              </div>

              <div class="config-card">
                <label>和风天气 API Host</label>
                <input
                  v-model="formData.qweather_api_host"
                  type="text"
                  placeholder="devapi.qweather.com"
                />
                <span v-if="maskedConfig.qweather_api_host" class="current-value">
                  当前值: {{ maskedConfig.qweather_api_host }}
                </span>
              </div>
            </div>
          </div>

          <!-- 操作按钮 -->
          <div class="form-actions">
            <button type="button" @click="handleReset" class="btn-reset">
              重置
            </button>
            <button type="submit" class="btn-save" :disabled="saving">
              <span v-if="saving" class="btn-spinner"></span>
              <span v-else>保存配置</span>
            </button>
          </div>

          <!-- 消息提示 -->
          <transition name="fade">
            <p v-if="successMessage" class="success-message">{{ successMessage }}</p>
          </transition>
          <transition name="fade">
            <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
          </transition>
        </form>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const username = computed(() => authStore.username)
const isAdmin = computed(() => authStore.isAdmin)

const userInitial = computed(() => {
  const name = username.value
  return name ? name.charAt(0).toUpperCase() : 'U'
})

const tabs = [
  { id: 'llm', label: 'LLM 模型', icon: '🤖' },
  { id: 'weather', label: '天气服务', icon: '🌤️' },
]

const activeTab = ref('llm')

const formData = ref({
  kimi_api_key: '',
  deepseek_api_key: '',
  minimax_api_key: '',
  ollama_base_url: '',
  tavily_api_key: '',
  qweather_api_key: '',
  qweather_api_host: '',
})

const maskedConfig = ref<Record<string, string>>({})
const loading = ref(false)
const saving = ref(false)
const successMessage = ref('')
const errorMessage = ref('')

const fetchConfig = async () => {
  loading.value = true
  try {
    const res = await fetch('/api/v1/config', { credentials: 'include' })
    if (res.ok) {
      const data = await res.json()
      maskedConfig.value = data
    }
  } catch {
    errorMessage.value = '获取配置失败'
  } finally {
    loading.value = false
  }
}

const handleSave = async () => {
  successMessage.value = ''
  errorMessage.value = ''
  saving.value = true

  try {
    const updateData: Record<string, string> = {}
    for (const [key, value] of Object.entries(formData.value)) {
      if (value.trim() !== '') {
        updateData[key] = value.trim()
      }
    }

    const res = await fetch('/api/v1/config', {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify(updateData),
    })

    if (res.ok) {
      const data = await res.json()
      maskedConfig.value = data
      successMessage.value = '配置已保存'
      setTimeout(() => { successMessage.value = '' }, 3000)
      formData.value = {
        kimi_api_key: '',
        deepseek_api_key: '',
        minimax_api_key: '',
        ollama_base_url: '',
        tavily_api_key: '',
        qweather_api_key: '',
        qweather_api_host: '',
      }
    } else {
      const data = await res.json()
      errorMessage.value = data.detail || '保存失败'
    }
  } catch {
    errorMessage.value = '保存失败，请检查网络连接'
  } finally {
    saving.value = false
  }
}

const handleReset = () => {
  formData.value = {
    kimi_api_key: '',
    deepseek_api_key: '',
    minimax_api_key: '',
    ollama_base_url: '',
    tavily_api_key: '',
    qweather_api_key: '',
    qweather_api_host: '',
  }
}

const handleLogout = async () => {
  await authStore.logout()
  router.push('/login')
}

onMounted(fetchConfig)
</script>

<style scoped>
/* ===== 沿用 Home.vue 的框架样式 ===== */
.home-container {
  display: flex;
  min-height: 100vh;
  background-image: url('/background.jpg');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  position: relative;
}

.home-container::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.3);
  backdrop-filter: blur(2px);
  z-index: 0;
}

.sidebar {
  width: 260px;
  background: rgba(255, 255, 255, 0.4);
  backdrop-filter: blur(15px);
  border-right: 1px solid rgba(255, 255, 255, 0.2);
  display: flex;
  flex-direction: column;
  box-shadow: 2px 0 15px rgba(0, 0, 0, 0.1);
  position: fixed;
  height: 100vh;
  left: 0;
  top: 0;
  z-index: 10;
}

.sidebar-header {
  padding: 30px 20px;
  border-bottom: 1px solid #f0f0f0;
}

.logo {
  display: flex;
  justify-content: center;
  margin-bottom: 12px;
}

.logo-icon {
  font-size: 40px;
}

.platform-name {
  font-size: 18px;
  font-weight: 600;
  color: #1d1d1f;
  margin: 0;
  text-align: center;
}

.nav-menu {
  flex: 1;
  padding: 20px 12px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 16px;
  border-radius: 12px;
  text-decoration: none;
  color: #1d1d1f;
  font-size: 15px;
  font-weight: 500;
  transition: all 0.3s ease;
  cursor: pointer;
}

.nav-item:hover {
  background: #f5f5f7;
}

.nav-item.active {
  background: #007aff;
  color: white;
}

.nav-icon {
  font-size: 20px;
}

.nav-text {
  flex: 1;
}

.sidebar-footer {
  padding: 20px;
  border-top: 1px solid #f0f0f0;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  font-weight: 600;
}

.user-details {
  flex: 1;
}

.username {
  margin: 0;
  font-size: 14px;
  font-weight: 600;
  color: #1d1d1f;
}

.user-role {
  margin: 0;
  font-size: 12px;
  color: #86868b;
}

.logout-button {
  width: 100%;
  padding: 12px;
  background: #f5f5f7;
  border: none;
  border-radius: 10px;
  color: #1d1d1f;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.logout-button:hover {
  background: #e8e8ed;
}

.main-content {
  flex: 1;
  margin-left: 260px;
  min-height: 100vh;
  background-image: url('/background.jpg');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  position: relative;
}

.main-content::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.3);
  backdrop-filter: blur(2px);
  z-index: 0;
}

.content-wrapper {
  padding: 40px;
  max-width: 1400px;
  margin: 0 auto;
  position: relative;
  z-index: 1;
}

/* ===== 设置页面特有样式 ===== */

/* 标签页切换 */
.tab-nav {
  display: flex;
  justify-content: center;
  gap: 16px;
  margin-bottom: 32px;
}

.tab-btn {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 14px 28px;
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(15px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 12px;
  font-size: 16px;
  font-weight: 500;
  color: #1d1d1f;
  cursor: pointer;
  transition: all 0.3s ease;
}

.tab-btn:hover {
  background: rgba(255, 255, 255, 0.35);
  transform: translateY(-2px);
}

.tab-btn.active {
  background: #007aff;
  border-color: #007aff;
  color: white;
}

.tab-icon {
  font-size: 22px;
}

/* 加载状态 */
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 0;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid rgba(255, 255, 255, 0.3);
  border-top-color: #007aff;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin-bottom: 16px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* 配置表单 */
.settings-form {
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(15px);
  border-radius: 20px;
  padding: 40px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.config-section {
  margin-bottom: 32px;
}

.section-header {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 22px;
  font-weight: 600;
  color: #1d1d1f;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 2px solid rgba(0, 0, 0, 0.05);
}

.section-icon {
  font-size: 28px;
}

.config-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
}

.config-card {
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(15px);
  border-radius: 16px;
  padding: 24px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
}

.config-card:hover {
  background: rgba(255, 255, 255, 0.35);
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.12);
}

.config-card label {
  display: block;
  font-size: 14px;
  font-weight: 600;
  color: #1d1d1f;
  margin-bottom: 12px;
}

.config-card input {
  width: 100%;
  padding: 14px 16px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 12px;
  font-size: 15px;
  background: rgba(255, 255, 255, 0.3);
  backdrop-filter: blur(10px);
  transition: all 0.3s ease;
  box-sizing: border-box;
}

.config-card input:focus {
  outline: none;
  border-color: #007aff;
  box-shadow: 0 0 0 3px rgba(0, 122, 255, 0.1);
}

.config-card input::placeholder {
  color: #86868b;
}

.current-value {
  display: block;
  margin-top: 10px;
  font-size: 12px;
  color: #86868b;
}

.current-value code {
  background: rgba(0, 0, 0, 0.05);
  padding: 3px 8px;
  border-radius: 4px;
  font-family: 'SF Mono', Monaco, monospace;
}

/* 操作按钮 */
.form-actions {
  display: flex;
  justify-content: center;
  gap: 16px;
  margin-top: 32px;
  padding-top: 24px;
  border-top: 1px solid rgba(0, 0, 0, 0.05);
}

.btn-reset {
  padding: 14px 36px;
  background: white;
  border: 1px solid #d2d2d7;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 500;
  color: #1d1d1f;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-reset:hover {
  background: #f5f5f7;
}

.btn-save {
  padding: 14px 40px;
  background: linear-gradient(135deg, #007aff 0%, #0056cc 100%);
  border: none;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  color: white;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(0, 122, 255, 0.3);
  display: flex;
  align-items: center;
  gap: 8px;
}

.btn-save:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 122, 255, 0.4);
}

.btn-save:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-spinner {
  width: 18px;
  height: 18px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

/* 消息提示 */
.success-message {
  margin: 24px 0 0 0;
  padding: 16px 24px;
  background: rgba(52, 199, 89, 0.15);
  color: #34c759;
  border-radius: 12px;
  font-size: 15px;
  text-align: center;
}

.error-message {
  margin: 24px 0 0 0;
  padding: 16px 24px;
  background: rgba(255, 59, 48, 0.15);
  color: #ff3b30;
  border-radius: 12px;
  font-size: 15px;
  text-align: center;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* 响应式 */
@media (max-width: 768px) {
  .sidebar {
    width: 80px;
  }

  .sidebar-header {
    padding: 20px 10px;
  }

  .platform-name {
    display: none;
  }

  .nav-text {
    display: none;
  }

  .nav-item {
    justify-content: center;
    padding: 14px;
  }

  .user-details {
    display: none;
  }

  .main-content {
    margin-left: 80px;
  }

  .content-wrapper {
    padding: 20px;
  }

  .hero-section {
    padding: 40px 20px;
  }

  .main-title {
    font-size: 28px;
  }

  .tab-nav {
    flex-direction: column;
  }

  .tab-btn {
    justify-content: center;
  }

  .config-grid {
    grid-template-columns: 1fr;
  }
}
</style>