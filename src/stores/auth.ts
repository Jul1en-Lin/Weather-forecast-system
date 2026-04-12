import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  // 状态
  const isAuthenticated = ref(false)
  const user = ref<{ username: string } | null>(null)
  
  // 计算属性
  const isLoggedIn = computed(() => isAuthenticated.value)
  const username = computed(() => user.value?.username || '')
  
  // 方法
  const login = (userData: string) => {
    isAuthenticated.value = true
    user.value = { username: userData }
    // 保存到 localStorage
    localStorage.setItem('isAuthenticated', 'true')
    localStorage.setItem('user', JSON.stringify({ username: userData }))
  }
  
  const logout = () => {
    isAuthenticated.value = false
    user.value = null
    // 清除 localStorage
    localStorage.removeItem('isAuthenticated')
    localStorage.removeItem('user')
  }
  
  const checkAuth = () => {
    // 从 localStorage 恢复状态
    const storedAuth = localStorage.getItem('isAuthenticated')
    const storedUser = localStorage.getItem('user')
    
    if (storedAuth === 'true' && storedUser) {
      isAuthenticated.value = true
      user.value = JSON.parse(storedUser)
      return true
    }
    return false
  }
  
  return {
    isAuthenticated,
    user,
    isLoggedIn,
    username,
    login,
    logout,
    checkAuth
  }
})
