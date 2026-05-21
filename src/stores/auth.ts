import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

const API_BASE = ''  // 使用相对路径，通过 Vite 代理转发到后端

export const useAuthStore = defineStore('auth', () => {
  const isAuthenticated = ref(false)
  const user = ref<{ username: string; is_admin: boolean } | null>(null)

  const isLoggedIn = computed(() => isAuthenticated.value)
  const username = computed(() => user.value?.username || '')
  const isAdmin = computed(() => user.value?.is_admin || false)

  const login = async (uname: string, password: string): Promise<boolean> => {
    const res = await fetch(`${API_BASE}/api/v1/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({ username: uname, password }),
    })
    if (!res.ok) return false
    const data = await res.json()
    isAuthenticated.value = true
    user.value = { username: data.username, is_admin: data.is_admin }
    return true
  }

  const logout = async () => {
    await fetch(`${API_BASE}/api/v1/auth/logout`, {
      method: 'POST',
      credentials: 'include',
    })
    isAuthenticated.value = false
    user.value = null
  }

  const checkAuth = async (): Promise<boolean> => {
    if (isAuthenticated.value) return true
    try {
      const res = await fetch(`${API_BASE}/api/v1/auth/me`, {
        credentials: 'include',
      })
      if (res.ok) {
        const data = await res.json()
        isAuthenticated.value = true
        user.value = { username: data.username, is_admin: data.is_admin }
        return true
      }
    } catch {
      // network error, ignore
    }
    isAuthenticated.value = false
    user.value = null
    return false
  }

  const register = async (username: string, password: string): Promise<{ success: boolean; error?: string }> => {
    const res = await fetch(`${API_BASE}/api/v1/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({ username, password }),
    })
    const data = await res.json()
    if (!res.ok) {
      return { success: false, error: data.detail || '注册失败' }
    }
    return { success: true }
  }

  return {
    isAuthenticated,
    user,
    isLoggedIn,
    username,
    isAdmin,
    login,
    logout,
    checkAuth,
    register,
  }
})
