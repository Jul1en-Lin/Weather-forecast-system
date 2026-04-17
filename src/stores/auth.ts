import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

const API_BASE = 'http://localhost:8000'

export const useAuthStore = defineStore('auth', () => {
  const isAuthenticated = ref(false)
  const user = ref<{ username: string } | null>(null)

  const isLoggedIn = computed(() => isAuthenticated.value)
  const username = computed(() => user.value?.username || '')

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
    user.value = { username: data.username }
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
        user.value = { username: data.username }
        return true
      }
    } catch {
      // network error, ignore
    }
    isAuthenticated.value = false
    user.value = null
    return false
  }

  return {
    isAuthenticated,
    user,
    isLoggedIn,
    username,
    login,
    logout,
    checkAuth,
  }
})
