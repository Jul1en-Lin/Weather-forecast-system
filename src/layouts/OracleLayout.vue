<template>
  <div class="oracle-layout" :data-oracle-theme="theme">
    <aside class="oracle-sidebar">
      <div class="oracle-brand">
        <span class="oracle-brand-icon">☁</span>
        <div>
          <strong>Weather Oracle</strong>
          <span>气象平台</span>
        </div>
      </div>

      <nav class="oracle-nav">
        <router-link to="/oracle" class="oracle-nav-item" active-class="active" aria-label="首页">
          <span class="oracle-nav-icon">⌂</span>
          <span class="oracle-nav-text">首页</span>
        </router-link>
        <router-link to="/intelligent-assistant" class="oracle-nav-item" active-class="active" aria-label="智能对话">
          <span class="oracle-nav-icon">✦</span>
          <span class="oracle-nav-text">智能对话</span>
        </router-link>
        <router-link v-if="isAdmin" to="/settings" class="oracle-nav-item" active-class="active" aria-label="系统设置">
          <span class="oracle-nav-icon">⚙</span>
          <span class="oracle-nav-text">系统设置</span>
        </router-link>
        <router-link v-if="isAdmin" to="/admin/users" class="oracle-nav-item" active-class="active" aria-label="用户管理">
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
        <div class="oracle-user-actions">
          <button type="button" class="oracle-theme-toggle" @click="toggleTheme">
            {{ isLightTheme ? '夜间' : '日间' }}
          </button>
          <button type="button" @click="handleLogout">退出</button>
        </div>
      </div>
    </aside>

    <main class="oracle-main">
      <header class="oracle-topbar">
        <div class="oracle-topbar-title">
          <span class="oracle-eyebrow">Weather Oracle</span>
          <strong>气象占卜台</strong>
        </div>
        <div class="oracle-topbar-actions">
          <div class="oracle-phase">
            <span>☾</span>
            <span>◐</span>
            <span>☀</span>
            <span>◑</span>
            <span>☽</span>
          </div>
          <button type="button" class="oracle-topbar-theme" @click="toggleTheme">
            {{ isLightTheme ? '夜间' : '日间' }}
          </button>
        </div>
      </header>
      <slot />
    </main>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()
const theme = ref<'dark' | 'light'>(
  localStorage.getItem('weather_oracle:theme') === 'light' ? 'light' : 'dark',
)

const username = computed(() => authStore.username)
const isAdmin = computed(() => authStore.isAdmin)
const userInitial = computed(() => username.value ? username.value.charAt(0).toUpperCase() : 'U')
const isLightTheme = computed(() => theme.value === 'light')

watch(theme, value => {
  localStorage.setItem('weather_oracle:theme', value)
})

function toggleTheme() {
  theme.value = theme.value === 'light' ? 'dark' : 'light'
}

async function handleLogout() {
  await authStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.oracle-layout {
  min-height: 100vh;
  color: var(--oracle-text);
  position: relative;
  isolation: isolate;
  background:
    linear-gradient(115deg, rgba(215, 174, 105, 0.08), transparent 28%),
    linear-gradient(245deg, rgba(168, 138, 223, 0.08), transparent 34%),
    linear-gradient(135deg, var(--oracle-bg-deep), var(--oracle-bg) 42%, var(--oracle-panel-solid));
}

.oracle-layout::before {
  content: '';
  position: fixed;
  inset: 0;
  z-index: -1;
  pointer-events: none;
  background-image:
    linear-gradient(var(--oracle-border-soft) 1px, transparent 1px),
    linear-gradient(90deg, var(--oracle-border-soft) 1px, transparent 1px);
  background-size: 72px 72px, 72px 72px;
  mask-image: linear-gradient(180deg, #000 0%, rgba(0, 0, 0, 0.72) 54%, rgba(0, 0, 0, 0.22) 100%);
}

.oracle-sidebar {
  position: fixed;
  inset: 0 auto 0 0;
  z-index: 2;
  width: var(--oracle-sidebar-width);
  box-sizing: border-box;
  min-height: 100vh;
  padding: 24px 20px;
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.055), transparent 46%), var(--oracle-panel);
  backdrop-filter: blur(18px);
  border-right: 1px solid var(--oracle-border);
  box-shadow: 18px 0 42px rgba(0, 0, 0, 0.22);
  display: flex;
  flex-direction: column;
}

.oracle-brand {
  display: flex;
  align-items: center;
  gap: 12px;
  padding-bottom: 24px;
  border-bottom: 1px solid var(--oracle-border-soft);
}

.oracle-brand-icon {
  width: 44px;
  height: 44px;
  border: 1px solid var(--oracle-border);
  border-radius: 8px;
  background: linear-gradient(145deg, rgba(215, 174, 105, 0.24), rgba(168, 138, 223, 0.12)), var(--oracle-panel-soft);
  color: var(--oracle-gold);
  display: grid;
  place-items: center;
  font-size: 26px;
}

.oracle-brand strong,
.oracle-user-copy strong {
  display: block;
  font-size: 15px;
  font-weight: 700;
  color: var(--oracle-text);
}

.oracle-brand span,
.oracle-user-copy span {
  display: block;
  font-size: 12px;
  color: var(--oracle-muted);
  margin-top: 2px;
}

.oracle-brand strong {
  color: var(--oracle-text);
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
  border: 1px solid transparent;
  border-radius: 8px;
  color: var(--oracle-faint);
  font-size: 15px;
  font-weight: 700;
  text-decoration: none;
  transition: border-color 0.2s ease, background-color 0.2s ease, color 0.2s ease;
}

.oracle-nav-item:hover {
  border-color: var(--oracle-border-soft);
  background: var(--oracle-panel-soft);
  color: var(--oracle-text);
}

.oracle-nav-item.active {
  border-color: var(--oracle-border);
  background: linear-gradient(135deg, rgba(215, 174, 105, 0.18), rgba(168, 138, 223, 0.14));
  color: var(--oracle-gold-strong);
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
  border-top: 1px solid var(--oracle-border-soft);
}

.oracle-avatar {
  width: 40px;
  height: 40px;
  border: 1px solid var(--oracle-border);
  border-radius: 8px;
  background: linear-gradient(135deg, rgba(168, 138, 223, 0.32), rgba(215, 174, 105, 0.18));
  color: var(--oracle-text);
  display: grid;
  place-items: center;
  font-size: 18px;
  font-weight: 800;
}

.oracle-user-actions {
  grid-column: 1 / -1;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
}

.oracle-user button {
  width: 100%;
  padding: 12px;
  border: 1px solid var(--oracle-border-soft);
  border-radius: 8px;
  background: var(--oracle-panel-soft);
  color: var(--oracle-text);
  cursor: pointer;
  font-size: 14px;
  font-weight: 700;
  transition: border-color 0.2s ease, background-color 0.2s ease;
}

.oracle-user button:hover {
  border-color: var(--oracle-border);
}

.oracle-theme-toggle {
  color: var(--oracle-gold-strong);
}

.oracle-main {
  min-height: 100vh;
  margin-left: var(--oracle-sidebar-width);
  padding: 18px 20px 28px;
  position: relative;
  z-index: 1;
}

.oracle-topbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  min-height: 58px;
  padding: 0 16px 18px;
  color: var(--oracle-text);
}

.oracle-topbar-title {
  display: grid;
  gap: 3px;
}

.oracle-topbar strong {
  color: var(--oracle-text);
  font-size: 20px;
}

.oracle-phase {
  display: flex;
  align-items: center;
  gap: 13px;
  color: var(--oracle-gold);
}

.oracle-topbar-actions {
  display: flex;
  align-items: center;
  gap: 16px;
}

.oracle-topbar-theme {
  display: none;
  padding: 9px 12px;
  border: 1px solid var(--oracle-border);
  border-radius: 8px;
  background: var(--oracle-panel-soft);
  color: var(--oracle-gold-strong);
  font-weight: 700;
}

@media (max-width: 900px) {
  .oracle-sidebar {
    inset: auto 12px 12px;
    width: auto;
    min-height: 0;
    padding: 8px;
    border: 1px solid var(--oracle-border);
    border-radius: 8px;
    flex-direction: row;
    align-items: center;
  }

  .oracle-brand,
  .oracle-user {
    display: none;
  }

  .oracle-nav {
    flex: 1;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 6px;
    padding: 0;
  }

  .oracle-nav-item {
    justify-content: center;
    gap: 6px;
    padding: 10px 8px;
    min-width: 0;
    font-size: 12px;
  }

  .oracle-nav-icon {
    width: auto;
    font-size: 16px;
  }

  .oracle-nav-text {
    display: none;
  }

  .oracle-main {
    margin-left: 0;
    padding: 14px 12px 92px;
  }

  .oracle-topbar {
    padding: 0 4px 12px;
  }

  .oracle-phase {
    display: none;
  }

  .oracle-topbar-theme {
    display: inline-flex;
  }
}

@media (max-width: 560px) {
  .oracle-nav-item {
    gap: 0;
    padding: 11px 6px;
  }

  .oracle-nav-icon {
    font-size: 18px;
  }
}
</style>
