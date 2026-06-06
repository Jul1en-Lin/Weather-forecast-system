<template>
  <div class="oracle-layout">
    <aside class="oracle-sidebar">
      <div class="oracle-brand">
        <span class="oracle-brand-icon">☁</span>
        <div>
          <strong>Weather Oracle</strong>
          <span>气象平台</span>
        </div>
      </div>

      <nav class="oracle-nav">
        <router-link to="/oracle" class="oracle-nav-item" active-class="active">
          <span class="oracle-nav-icon">⌂</span>
          <span class="oracle-nav-text">首页</span>
        </router-link>
        <router-link to="/intelligent-assistant" class="oracle-nav-item" active-class="active">
          <span class="oracle-nav-icon">✦</span>
          <span class="oracle-nav-text">智能对话</span>
        </router-link>
        <router-link v-if="isAdmin" to="/settings" class="oracle-nav-item" active-class="active">
          <span class="oracle-nav-icon">⚙</span>
          <span class="oracle-nav-text">系统设置</span>
        </router-link>
        <router-link v-if="isAdmin" to="/admin/users" class="oracle-nav-item" active-class="active">
          <span class="oracle-nav-icon">👥</span>
          <span class="oracle-nav-text">用户管理</span>
        </router-link>
      </nav>

      <div class="oracle-user">
        <div class="oracle-avatar">{{ userInitial }}</div>
        <div class="oracle-user-copy">
          <strong>{{ username }}</strong>
          <span>{{ isAdmin ? '管理员' : '普通用户' }}</span>
        </div>
        <button type="button" @click="handleLogout">退出</button>
      </div>
    </aside>

    <main class="oracle-main">
      <slot />
    </main>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const username = computed(() => authStore.username)
const isAdmin = computed(() => authStore.isAdmin)
const userInitial = computed(() => username.value ? username.value.charAt(0).toUpperCase() : 'U')

async function handleLogout() {
  await authStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.oracle-layout {
  min-height: 100vh;
  background-image: url('/background.jpg');
  background-position: center;
  background-repeat: no-repeat;
  background-size: cover;
  color: #1d1d1f;
  position: relative;
}

.oracle-layout::before {
  content: '';
  position: fixed;
  inset: 0;
  background: rgba(255, 255, 255, 0.3);
  backdrop-filter: blur(2px);
  z-index: 0;
}

.oracle-sidebar {
  position: fixed;
  inset: 0 auto 0 0;
  z-index: 2;
  width: 260px;
  box-sizing: border-box;
  min-height: 100vh;
  padding: 24px 20px;
  background: rgba(255, 255, 255, 0.42);
  backdrop-filter: blur(15px);
  border-right: 1px solid rgba(255, 255, 255, 0.22);
  box-shadow: 2px 0 15px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
}

.oracle-brand {
  display: flex;
  align-items: center;
  gap: 12px;
  padding-bottom: 24px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}

.oracle-brand-icon {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: linear-gradient(135deg, #007aff 0%, #10a37f 100%);
  color: white;
  display: grid;
  place-items: center;
  font-size: 26px;
}

.oracle-brand strong,
.oracle-user-copy strong {
  display: block;
  font-size: 15px;
  font-weight: 600;
}

.oracle-brand span,
.oracle-user-copy span {
  display: block;
  font-size: 12px;
  color: #86868b;
  margin-top: 2px;
}

.oracle-nav {
  flex: 1;
  display: grid;
  align-content: start;
  gap: 4px;
  padding: 24px 0;
}

.oracle-nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 16px;
  border-radius: 12px;
  color: #1d1d1f;
  font-size: 15px;
  font-weight: 500;
  text-decoration: none;
  transition: all 0.2s ease;
}

.oracle-nav-item:hover {
  background: rgba(0, 0, 0, 0.05);
}

.oracle-nav-item.active {
  background: #007aff;
  color: white;
}

.oracle-nav-icon {
  width: 20px;
  text-align: center;
  font-size: 18px;
}

.oracle-user {
  display: grid;
  grid-template-columns: 40px 1fr;
  gap: 12px;
  padding-top: 20px;
  border-top: 1px solid rgba(0, 0, 0, 0.05);
}

.oracle-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  display: grid;
  place-items: center;
  font-size: 18px;
  font-weight: 600;
}

.oracle-user button {
  grid-column: 1 / -1;
  width: 100%;
  padding: 12px;
  border: 0;
  border-radius: 10px;
  background: #f5f5f7;
  color: #1d1d1f;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
}

.oracle-user button:hover {
  background: #e8e8ed;
}

.oracle-main {
  min-height: 100vh;
  margin-left: 260px;
  position: relative;
  z-index: 1;
}

@media (max-width: 768px) {
  .oracle-sidebar {
    width: 80px;
    padding: 20px 10px;
  }

  .oracle-brand {
    justify-content: center;
  }

  .oracle-brand div,
  .oracle-nav-text,
  .oracle-user-copy {
    display: none;
  }

  .oracle-nav-item {
    justify-content: center;
    padding: 14px;
  }

  .oracle-user {
    grid-template-columns: 1fr;
    justify-items: center;
  }

  .oracle-user button {
    padding: 10px 4px;
    font-size: 12px;
  }

  .oracle-main {
    margin-left: 80px;
  }
}
</style>
