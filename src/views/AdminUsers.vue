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

        <router-link to="/settings" class="nav-item" active-class="active">
          <span class="nav-icon">⚙️</span>
          <span class="nav-text">系统设置</span>
        </router-link>

        <router-link to="/admin/users" class="nav-item active" active-class="active">
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
        <!-- 用户列表 -->
        <div v-if="loading" class="loading-state">
          <div class="spinner"></div>
          <p>加载中...</p>
        </div>

        <div v-else-if="error" class="error-msg">{{ error }}</div>

        <div v-else class="users-container">
          <div class="users-header">
            <h2>用户管理</h2>
            <p>管理所有用户账户</p>
          </div>

          <div class="users-list">
            <div v-for="user in users" :key="user.id" class="user-card">
              <div class="user-info">
                <div class="user-avatar">{{ user.username.charAt(0).toUpperCase() }}</div>
                <div class="user-details">
                  <p class="username">{{ user.username }}</p>
                  <p class="user-meta">注册时间：{{ formatDate(user.created_at) }}</p>
                </div>
              </div>

              <div class="user-actions">
                <span class="role-badge" :class="{ 'is-admin': user.is_admin }">
                  {{ user.is_admin ? '管理员' : '普通用户' }}
                </span>

                <button
                  v-if="user.username !== 'admin'"
                  @click="toggleAdmin(user)"
                  class="action-btn"
                  :class="{ 'promote': !user.is_admin }"
                >
                  {{ user.is_admin ? '降级' : '升级' }}
                </button>

                <button
                  v-if="user.username !== 'admin'"
                  @click="deleteUser(user)"
                  class="action-btn delete"
                >
                  删除
                </button>
              </div>
            </div>
          </div>
        </div>

        <div v-if="successMessage" class="success-msg">{{ successMessage }}</div>
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

interface User {
  id: number
  username: string
  is_admin: boolean
  created_at: string
}

const users = ref<User[]>([])
const loading = ref(false)
const error = ref('')
const successMessage = ref('')

const fetchUsers = async () => {
  loading.value = true
  error.value = ''
  try {
    const res = await fetch('/api/v1/users', { credentials: 'include' })
    if (!res.ok) {
      const data = await res.json()
      throw new Error(data.detail || '获取用户列表失败')
    }
    users.value = await res.json()
  } catch (e: any) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}

const toggleAdmin = async (user: User) => {
  try {
    const res = await fetch(`/api/v1/users/${user.id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({ is_admin: !user.is_admin }),
    })
    if (!res.ok) {
      const data = await res.json()
      throw new Error(data.detail || '更新失败')
    }
    successMessage.value = user.is_admin ? '已降级为普通用户' : '已升级为管理员'
    setTimeout(() => { successMessage.value = '' }, 3000)
    await fetchUsers()
  } catch (e: any) {
    error.value = e.message
    setTimeout(() => { error.value = '' }, 3000)
  }
}

const deleteUser = async (user: User) => {
  if (!confirm(`确定要删除用户 "${user.username}" 吗？`)) return

  try {
    const res = await fetch(`/api/v1/users/${user.id}`, {
      method: 'DELETE',
      credentials: 'include',
    })
    if (!res.ok) {
      const data = await res.json()
      throw new Error(data.detail || '删除失败')
    }
    successMessage.value = '用户已删除'
    setTimeout(() => { successMessage.value = '' }, 3000)
    await fetchUsers()
  } catch (e: any) {
    error.value = e.message
    setTimeout(() => { error.value = '' }, 3000)
  }
}

const formatDate = (dateStr: string) => {
  const date = new Date(dateStr)
  return date.toLocaleString('zh-CN')
}

const handleLogout = async () => {
  await authStore.logout()
  router.push('/login')
}

onMounted(fetchUsers)
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

.user-info-sidebar {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
}

.user-avatar-sidebar {
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

.user-details-sidebar {
  flex: 1;
}

.username-sidebar {
  margin: 0;
  font-size: 14px;
  font-weight: 600;
  color: #1d1d1f;
}

.user-role-sidebar {
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

/* ===== 用户管理特有样式 ===== */
.users-container {
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(15px);
  border-radius: 20px;
  padding: 40px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.users-header {
  margin-bottom: 32px;
}

.users-header h2 {
  font-size: 28px;
  font-weight: 600;
  color: #1d1d1f;
  margin: 0 0 8px 0;
}

.users-header p {
  font-size: 15px;
  color: #86868b;
  margin: 0;
}

.loading-state {
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

.error-msg {
  padding: 16px 24px;
  background: rgba(255, 59, 48, 0.15);
  color: #ff3b30;
  border-radius: 12px;
  font-size: 15px;
  margin-bottom: 20px;
}

.success-msg {
  padding: 16px 24px;
  background: rgba(52, 199, 89, 0.15);
  color: #34c759;
  border-radius: 12px;
  font-size: 15px;
  margin-top: 20px;
}

.users-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.user-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px;
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(15px);
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
}

.user-card:hover {
  background: rgba(255, 255, 255, 0.35);
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.12);
}

.user-info {
  display: flex;
  align-items: center;
  gap: 16px;
}

.user-avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 22px;
  font-weight: 600;
}

.user-details .username {
  font-size: 17px;
  font-weight: 600;
  color: #1d1d1f;
  margin: 0 0 6px 0;
}

.user-meta {
  font-size: 13px;
  color: #86868b;
  margin: 0;
}

.user-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.role-badge {
  padding: 8px 16px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 500;
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  color: #86868b;
}

.role-badge.is-admin {
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  color: #007aff;
}

.action-btn {
  padding: 10px 20px;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  border: 1px solid rgba(255, 255, 255, 0.3);
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  color: #1d1d1f;
  transition: all 0.3s ease;
}

.action-btn:hover {
  background: rgba(255, 255, 255, 0.35);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.action-btn.promote {
  border-color: #007aff;
  color: #007aff;
}

.action-btn.promote:hover {
  background: rgba(0, 122, 255, 0.1);
}

.action-btn.delete {
  border-color: #ff3b30;
  color: #ff3b30;
}

.action-btn.delete:hover {
  background: rgba(255, 59, 48, 0.1);
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

  .user-details-sidebar {
    display: none;
  }

  .main-content {
    margin-left: 80px;
  }

  .content-wrapper {
    padding: 20px;
  }

  .user-card {
    flex-direction: column;
    gap: 16px;
  }

  .user-actions {
    flex-wrap: wrap;
    justify-content: center;
  }
}
</style>