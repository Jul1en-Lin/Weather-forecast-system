<template>
  <OracleLayout>
    <div class="admin-users-page">
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
    </div>
  </OracleLayout>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import OracleLayout from '../layouts/OracleLayout.vue'

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

onMounted(fetchUsers)
</script>

<style scoped>
.admin-users-page {
  min-height: 100vh;
}

.content-wrapper {
  padding: 40px;
  max-width: 1400px;
  margin: 0 auto;
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

.user-card .user-info {
  display: flex;
  align-items: center;
  gap: 16px;
}

.user-card .user-avatar {
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

.user-card .user-details .username {
  font-size: 17px;
  font-weight: 600;
  color: #1d1d1f;
  margin: 0 0 6px 0;
}

.user-card .user-meta {
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
