<template>
  <OracleLayout>
    <div class="admin-users-page">
      <div class="content-wrapper">
        <div class="settings-form oracle-surface oracle-gold-corners">
          <div class="section-header flex-between">
            <div class="flex-align-center">
              <svg class="section-icon-svg" viewBox="0 0 24 24" width="20" height="20" style="fill: currentColor; color: var(--oracle-gold); margin-right: 6px; vertical-align: middle;">
                <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>
              </svg>
              <span>用户管理</span>
            </div>
            <!-- 批量全选 -->
            <div v-if="users.length > 1 && !loading" class="flex-align-center batch-select-all-wrapper">
              <label class="select-all-label">
                <input 
                  type="checkbox" 
                  :checked="isAllSelected" 
                  @change="toggleSelectAll" 
                  class="user-select-checkbox"
                />
                <span>全选</span>
              </label>
            </div>
          </div>

          <!-- 加载状态 -->
          <div v-if="loading" class="loading-container">
            <div class="spinner"></div>
            <p>加载中...</p>
          </div>

          <!-- 错误信息 -->
          <div v-else-if="error" class="error-message animate-slide-up">{{ error }}</div>

          <!-- 用户列表网格 -->
          <div v-else class="users-list-wrapper">
            <div class="users-grid">
              <div v-for="user in users" :key="user.id" class="user-card-item">
                <div class="user-card-header">
                  <div class="user-title-desc">
                    <label v-if="user.username !== 'admin'" class="user-select-checkbox-wrapper">
                      <input 
                        type="checkbox" 
                        :value="user.id" 
                        v-model="selectedUserIds" 
                        class="user-select-checkbox"
                      />
                    </label>
                    <div class="user-avatar">{{ user.username.charAt(0).toUpperCase() }}</div>
                    <div class="user-name-role">
                      <h4 :title="user.username">{{ user.username }}</h4>
                      <span class="badge-pill" :class="user.is_admin ? 'badge-pill-admin' : 'badge-pill-user'">
                        {{ user.is_admin ? '管理员' : '普通用户' }}
                      </span>
                    </div>
                  </div>
                  <div class="user-card-actions">
                    <button
                      v-if="user.username !== 'admin'"
                      @click="toggleAdmin(user)"
                      class="btn-card-action edit-btn"
                    >
                      {{ user.is_admin ? '降级' : '升级' }}
                    </button>
                    <button
                      v-if="user.username !== 'admin'"
                      @click="deleteUser(user)"
                      class="btn-card-action delete-btn"
                    >
                      删除
                    </button>
                  </div>
                </div>
                <div class="user-card-body">
                  <div class="user-meta-info">
                    <div class="meta-row">
                      <span class="meta-label">用户 ID:</span>
                      <code class="meta-value">{{ user.id }}</code>
                    </div>
                    <div class="meta-row">
                      <span class="meta-label">注册时间:</span>
                      <span class="meta-value">{{ formatDate(user.created_at) }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- 批量操作面板 -->
          <transition name="slide-up-fade">
            <div v-if="selectedUserIds.length > 0" class="batch-action-bar oracle-surface">
              <div class="batch-info">
                <span>已选中 <strong class="gold-text">{{ selectedUserIds.length }}</strong> 个用户</span>
              </div>
              <div class="batch-buttons">
                <button @click="batchUpdateAdmin(true)" class="btn-batch-action upgrade-btn">
                  设为管理员
                </button>
                <button @click="batchUpdateAdmin(false)" class="btn-batch-action downgrade-btn">
                  降级用户
                </button>
                <button @click="batchDelete" class="btn-batch-action delete-btn">
                  删除
                </button>
                <button @click="clearSelection" class="btn-batch-action cancel-btn">
                  取消
                </button>
              </div>
            </div>
          </transition>

          <!-- 成功信息 -->
          <div v-if="successMessage" class="success-message animate-slide-up">{{ successMessage }}</div>
        </div>
      </div>
    </div>
  </OracleLayout>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
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
const selectedUserIds = ref<number[]>([])

const selectableUsers = computed(() => users.value.filter(u => u.username !== 'admin'))

const isAllSelected = computed(() => {
  if (selectableUsers.value.length === 0) return false
  return selectableUsers.value.every(u => selectedUserIds.value.includes(u.id))
})

const toggleSelectAll = (e: Event) => {
  const checked = (e.target as HTMLInputElement).checked
  if (checked) {
    selectedUserIds.value = selectableUsers.value.map(u => u.id)
  } else {
    selectedUserIds.value = []
  }
}

const fetchUsers = async () => {
  loading.value = true
  error.value = ''
  try {
    const res = await fetch('/api/v1/users/', { credentials: 'include' })
    if (!res.ok) {
      const data = await res.json()
      throw new Error(data.detail || '获取用户列表失败')
    }
    users.value = await res.json()
    const userIdsList = users.value.map(u => u.id)
    selectedUserIds.value = selectedUserIds.value.filter(id => userIdsList.includes(id))
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

const batchUpdateAdmin = async (isAdmin: boolean) => {
  if (selectedUserIds.value.length === 0) return
  
  const label = isAdmin ? '升级为管理员' : '降级为普通用户'
  if (!confirm(`确定要将选中的 ${selectedUserIds.value.length} 个用户${label}吗？`)) return
  
  loading.value = true
  error.value = ''
  successMessage.value = ''
  try {
    const res = await fetch('/api/v1/users/batch/admin', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({ user_ids: selectedUserIds.value, is_admin: isAdmin }),
    })
    if (!res.ok) {
      const data = await res.json()
      throw new Error(data.detail || '批量操作失败')
    }
    const data = await res.json()
    successMessage.value = data.detail || '操作成功'
    setTimeout(() => { successMessage.value = '' }, 3000)
    selectedUserIds.value = []
    await fetchUsers()
  } catch (e: any) {
    error.value = e.message
    setTimeout(() => { error.value = '' }, 3000)
  } finally {
    loading.value = false
  }
}

const batchDelete = async () => {
  if (selectedUserIds.value.length === 0) return
  
  if (!confirm(`确定要删除选中的 ${selectedUserIds.value.length} 个用户吗？此操作不可逆！`)) return
  
  loading.value = true
  error.value = ''
  successMessage.value = ''
  try {
    const res = await fetch('/api/v1/users/batch/delete', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({ user_ids: selectedUserIds.value }),
    })
    if (!res.ok) {
      const data = await res.json()
      throw new Error(data.detail || '批量删除失败')
    }
    const data = await res.json()
    successMessage.value = data.detail || '批量删除成功'
    setTimeout(() => { successMessage.value = '' }, 3000)
    selectedUserIds.value = []
    await fetchUsers()
  } catch (e: any) {
    error.value = e.message
    setTimeout(() => { error.value = '' }, 3000)
  } finally {
    loading.value = false
  }
}

const clearSelection = () => {
  selectedUserIds.value = []
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

/* Container */
.settings-form {
  border-radius: 20px;
  padding: 40px;
}

.section-header {
  display: flex;
  align-items: center;
  font-size: 22px;
  font-weight: 600;
  color: var(--oracle-text);
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 1px solid var(--oracle-border-soft);
}

.flex-between {
  justify-content: space-between;
}

.flex-align-center {
  display: flex;
  align-items: center;
  gap: 12px;
}

/* Grid Layout */
.users-list-wrapper {
  margin-top: 10px;
}

.users-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
  gap: 24px;
}

/* User Card */
.user-card-item {
  background: rgba(0, 0, 0, 0.12);
  border-radius: 18px;
  border: 1px solid var(--oracle-border-soft);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}

[data-oracle-theme='light'] .user-card-item {
  background: rgba(255, 255, 255, 0.35);
}

.user-card-item:hover {
  transform: translateY(-4px);
  border-color: var(--oracle-gold);
  box-shadow: 0 12px 30px var(--oracle-gold-glow);
}

.user-card-header {
  padding: 20px 24px;
  border-bottom: 1px solid var(--oracle-border-soft);
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.user-title-desc {
  display: flex;
  align-items: center;
  gap: 12px;
  min-width: 0;
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--oracle-gold) 0%, var(--oracle-purple) 100%);
  color: #fdf9f3;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  font-weight: 600;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
  border: 1px solid var(--oracle-border-soft);
  flex-shrink: 0;
}

.user-name-role {
  min-width: 0;
  display: flex;
  flex-direction: column;
}

.user-name-role h4 {
  font-size: 16px;
  font-weight: 600;
  color: var(--oracle-text);
  margin: 0 0 4px 0;
  font-family: var(--oracle-font-serif);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* Badges */
.badge-pill {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 99px;
  font-size: 11px;
  font-weight: 600;
  border: 1px solid transparent;
}

.badge-pill-admin {
  border-color: rgba(var(--oracle-gold-rgb), 0.25);
  background: rgba(var(--oracle-gold-rgb), 0.08);
  color: var(--oracle-gold);
}

.badge-pill-user {
  border-color: var(--oracle-border-soft);
  background: rgba(255, 255, 255, 0.02);
  color: var(--oracle-muted);
}

[data-oracle-theme='light'] .badge-pill-user {
  background: rgba(0, 0, 0, 0.02);
}

/* Action Buttons */
.user-card-actions {
  display: flex;
  gap: 8px;
  flex-shrink: 0;
}

.btn-card-action {
  font-size: 13px;
  padding: 6px 12px;
  border-radius: 8px;
  font-weight: 500;
  border: 1px solid var(--oracle-border-soft);
  background: rgba(255, 255, 255, 0.02);
  color: var(--oracle-text);
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-card-action.edit-btn:hover {
  border-color: var(--oracle-gold);
  background: rgba(var(--oracle-gold-rgb), 0.08);
  color: var(--oracle-gold);
}

.btn-card-action.delete-btn {
  border-color: rgba(var(--oracle-danger-rgb), 0.25);
  background: rgba(var(--oracle-danger-rgb), 0.05);
  color: var(--oracle-danger);
}

.btn-card-action.delete-btn:hover {
  background: rgba(var(--oracle-danger-rgb), 0.15);
  border-color: var(--oracle-danger);
}

/* Card Body */
.user-card-body {
  padding: 24px;
  display: flex;
  flex-direction: column;
  flex: 1;
}

.user-meta-info {
  background: rgba(0, 0, 0, 0.15);
  border-radius: 12px;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  border: 1px solid var(--oracle-border-soft);
}

[data-oracle-theme='light'] .user-meta-info {
  background: rgba(0, 0, 0, 0.03);
}

.meta-row {
  display: flex;
  font-size: 13px;
  line-height: 1.4;
  justify-content: space-between;
}

.meta-label {
  color: var(--oracle-muted);
  font-weight: 500;
  flex-shrink: 0;
}

.meta-value {
  color: var(--oracle-text);
  word-break: break-all;
  text-align: right;
}

code.meta-value {
  font-family: SFMono-Regular, Consolas, monospace;
  background: rgba(255, 255, 255, 0.05);
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 12px;
}

[data-oracle-theme='light'] code.meta-value {
  background: rgba(0, 0, 0, 0.05);
}

/* Feedback Messages */
.success-message {
  margin: 24px 0 0 0;
  padding: 14px 20px;
  background: rgba(var(--oracle-success-rgb), 0.12);
  color: var(--oracle-success);
  border-radius: 10px;
  font-size: 14px;
  text-align: center;
  font-weight: 500;
  border: 1px solid rgba(var(--oracle-success-rgb), 0.2);
}

.error-message {
  margin: 24px 0 0 0;
  padding: 14px 20px;
  background: rgba(var(--oracle-danger-rgb), 0.12);
  color: var(--oracle-danger);
  border-radius: 10px;
  font-size: 14px;
  text-align: center;
  font-weight: 500;
  border: 1px solid rgba(var(--oracle-danger-rgb), 0.2);
}

/* Spinner */
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 0;
  color: var(--oracle-muted);
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid var(--oracle-border-soft);
  border-top-color: var(--oracle-gold);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin-bottom: 16px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.animate-slide-up {
  animation: slideUp 0.3s ease-out forwards;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(12px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Batch Action Bar floating panel */
.batch-action-bar {
  position: fixed;
  bottom: 30px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 100;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
  padding: 14px 28px;
  border-radius: 16px;
  border: 1px solid var(--oracle-gold);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4), 0 0 15px var(--oracle-gold-glow);
  background: rgba(30, 26, 20, 0.85);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  width: max-content;
  max-width: 90%;
}

[data-oracle-theme='light'] .batch-action-bar {
  background: rgba(253, 249, 243, 0.9);
  border-color: var(--oracle-gold);
  box-shadow: 0 10px 30px rgba(178, 133, 66, 0.2), 0 0 15px var(--oracle-gold-glow);
}

.batch-info {
  font-size: 14px;
  color: var(--oracle-text);
  font-weight: 500;
  white-space: nowrap;
}

.gold-text {
  color: var(--oracle-gold);
  font-weight: 700;
  font-size: 16px;
}

.batch-buttons {
  display: flex;
  gap: 10px;
  align-items: center;
}

.btn-batch-action {
  font-size: 13px;
  padding: 8px 14px;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.25s cubic-bezier(0.25, 0.8, 0.25, 1);
  border: 1px solid var(--oracle-border-soft);
  background: rgba(255, 255, 255, 0.02);
  color: var(--oracle-text);
}

[data-oracle-theme='light'] .btn-batch-action {
  background: rgba(0, 0, 0, 0.02);
}

.btn-batch-action.upgrade-btn:hover {
  border-color: var(--oracle-gold);
  background: rgba(var(--oracle-gold-rgb), 0.08);
  color: var(--oracle-gold);
  box-shadow: 0 0 10px var(--oracle-gold-glow);
}

.btn-batch-action.downgrade-btn:hover {
  border-color: var(--oracle-purple);
  background: rgba(var(--oracle-purple-rgb), 0.08);
  color: var(--oracle-purple);
  box-shadow: 0 0 10px rgba(var(--oracle-purple-rgb), 0.15);
}

.btn-batch-action.delete-btn {
  border-color: rgba(var(--oracle-danger-rgb), 0.25);
  background: rgba(var(--oracle-danger-rgb), 0.05);
  color: var(--oracle-danger);
}

.btn-batch-action.delete-btn:hover {
  background: rgba(var(--oracle-danger-rgb), 0.15);
  border-color: var(--oracle-danger);
  box-shadow: 0 0 10px rgba(var(--oracle-danger-rgb), 0.2);
}

.btn-batch-action.cancel-btn {
  border-color: var(--oracle-border-soft);
  color: var(--oracle-muted);
}

.btn-batch-action.cancel-btn:hover {
  background: rgba(255, 255, 255, 0.08);
  color: var(--oracle-text);
}

[data-oracle-theme='light'] .btn-batch-action.cancel-btn:hover {
  background: rgba(0, 0, 0, 0.08);
}

/* Checkbox styling */
.batch-select-all-wrapper {
  font-size: 14px;
  color: var(--oracle-muted);
}

.select-all-label {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  font-weight: 500;
  user-select: none;
}

.user-select-checkbox-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 4px;
  flex-shrink: 0;
}

.user-select-checkbox {
  width: 18px;
  height: 18px;
  cursor: pointer;
  accent-color: var(--oracle-gold);
  border-radius: 4px;
  border: 1px solid var(--oracle-border-soft);
  background: rgba(0, 0, 0, 0.2);
  transition: all 0.2s ease;
}

[data-oracle-theme='light'] .user-select-checkbox {
  background: rgba(255, 255, 255, 0.5);
  border-color: var(--oracle-border);
}

.user-select-checkbox:focus {
  outline: none;
  box-shadow: 0 0 6px var(--oracle-gold-glow);
}

/* Transition for Batch Action Bar */
.slide-up-fade-enter-active,
.slide-up-fade-leave-active {
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.slide-up-fade-enter-from,
.slide-up-fade-leave-to {
  opacity: 0;
  transform: translate(-50%, 40px);
}

/* Responsive Design */
@media (max-width: 768px) {
  .content-wrapper {
    padding: 20px;
  }

  .settings-form {
    padding: 20px;
  }

  .users-grid {
    grid-template-columns: 1fr;
  }

  .batch-action-bar {
    flex-direction: column;
    gap: 12px;
    width: 90%;
    bottom: 20px;
    padding: 16px;
  }

  .batch-buttons {
    flex-wrap: wrap;
    justify-content: center;
    width: 100%;
  }

  .btn-batch-action {
    flex-grow: 1;
    text-align: center;
  }
}
</style>
