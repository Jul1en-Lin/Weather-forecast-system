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
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 导航守卫
router.beforeEach((to, _from, next) => {
  const authStore = useAuthStore()
  
  // 检查是否已认证
  const isAuthenticated = authStore.checkAuth()
  
  // 如果路由需要认证
  if (to.meta.requiresAuth) {
    if (!isAuthenticated) {
      // 未登录，重定向到登录页
      next('/login')
    } else {
      // 已登录，允许访问
      next()
    }
  } else {
    // 公开路由
    if (to.path === '/login' && isAuthenticated) {
      // 已登录用户访问登录页，重定向到首页
      next('/home')
    } else {
      next()
    }
  }
})

export default router
