import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../views/Register.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/home',
    name: 'Home',
    component: () => import('../views/Home.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/intelligent-assistant',
    name: 'IntelligentAssistant',
    component: () => import('../views/IntelligentAssistant.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/admin/users',
    name: 'AdminUsers',
    component: () => import('../views/AdminUsers.vue'),
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/settings',
    name: 'Settings',
    component: () => import('../views/Settings.vue'),
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 导航守卫
router.beforeEach(async (to, _from, next) => {
  const authStore = useAuthStore()

  const isAuthenticated = await authStore.checkAuth()

  if (to.meta.requiresAuth) {
    if (!isAuthenticated) {
      next('/login')
    } else if (to.meta.requiresAdmin && !authStore.isAdmin) {
      next('/home')
    } else {
      next()
    }
  } else {
    if (to.path === '/login' && isAuthenticated) {
      next('/home')
    } else if (to.path === '/register' && isAuthenticated) {
      next('/home')
    } else {
      next()
    }
  }
})

export default router
