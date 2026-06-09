<template>
  <div class="oracle-layout" :data-oracle-theme="theme">
    <!-- Top Horizontal Navigation Header -->
    <header class="oracle-header">
      <div class="oracle-header-inner">
        <!-- Logo Brand -->
        <div class="oracle-header-brand" @click="router.push('/oracle')">
          <svg class="oracle-header-logo-svg" viewBox="0 0 24 24" width="28" height="28">
            <!-- Sun (Backdrop) -->
            <circle cx="8" cy="9" r="4" fill="currentColor" opacity="0.4" />
            <!-- Sun rays -->
            <path d="M8 3v2M4.46 5.46l1.42 1.42M2 9h2M4.46 12.54l1.42-1.42" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" />
            <!-- Cloud (Foreground) -->
            <path d="M17.5 12.5a2.5 2.5 0 0 0-2.5-2.5c-.32 0-.62.06-.9.17a3.5 3.5 0 0 0-6.6 1.83 2.5 2.5 0 0 0 .5 4.5h9a2.5 2.5 0 0 0 .5-4z" fill="currentColor" />
            <!-- AI Sparkle (Top-Right Accent) -->
            <path d="M19 2l.75 1.75L21.5 4.5 19.75 5.25 19 7l-.75-1.75L16.5 4.5l1.75-.75L19 2z" fill="var(--oracle-gold)" />
          </svg>
          <div class="oracle-header-brand-text">
            <strong>Weather Oracle</strong>
            <span>智能气象助手</span>
          </div>
        </div>

        <!-- Horizontal Nav Links -->
        <nav class="oracle-header-nav">
          <router-link to="/oracle" class="oracle-header-nav-item" active-class="active">
            <span class="nav-dot"></span> 首页
          </router-link>
          <router-link to="/intelligent-assistant" class="oracle-header-nav-item" active-class="active">
            <span class="nav-dot"></span> 智能对话
          </router-link>
          <router-link to="/knowledge-base" class="oracle-header-nav-item" active-class="active">
            <span class="nav-dot"></span> 知识库
          </router-link>
          <router-link v-if="isAdmin" to="/admin/users" class="oracle-header-nav-item" active-class="active">
            <span class="nav-dot"></span> 用户管理
          </router-link>
        </nav>

        <!-- Right Side Controls & Profile Dropdown -->
        <div class="oracle-header-right">
          <!-- Moon Phase Decoration -->
          <div class="oracle-header-moon-phases">
            <span class="phase-symbol select-none">☀</span>
            <span class="phase-symbol select-none">⛅</span>
            <span class="phase-symbol select-none">🌤</span>
            <span class="phase-symbol select-none">⛈</span>
            <span class="phase-symbol select-none">❄</span>
          </div>

          <!-- User Profile Dropdown -->
          <div class="oracle-header-user-wrapper" ref="dropdownRef">
            <div class="oracle-header-profile-trigger" @click="toggleDropdown">
              <div class="oracle-header-avatar">{{ userInitial }}</div>
              <div class="oracle-header-user-info">
                <span class="user-level-badge">{{ userTitle }}</span>
                <span class="user-trigger-name">{{ username }} ▾</span>
              </div>
            </div>

            <!-- Dropdown Menu -->
            <transition name="fade-slide">
              <div v-if="isDropdownOpen" class="oracle-header-dropdown-menu oracle-surface oracle-gold-corners">
                <div class="dropdown-header">
                  <strong>{{ username }}</strong>
                  <span class="dropdown-subtitle">{{ isAdmin ? '系统管理员' : '气象助手用户' }}</span>
                </div>
                <div class="oracle-divider"></div>
                <ul class="dropdown-list">
                  <li v-if="isAdmin" @click="navigateTo('/settings')">
                    <span class="dropdown-icon">⚙</span> 系统设置
                  </li>
                  <li @click="toggleTheme">
                    <span class="dropdown-icon">{{ isLightTheme ? '🌙' : '☀️' }}</span>
                    {{ isLightTheme ? '夜间模式' : '日间模式' }}
                  </li>
                  <li class="logout-item" @click="handleLogout">
                    <span class="dropdown-icon">🚪</span> 退出登录
                  </li>
                </ul>
              </div>
            </transition>
          </div>
        </div>
      </div>
    </header>

    <!-- Main Content Slot wrapper -->
    <main class="oracle-main">
      <div class="oracle-main-content">
        <slot />
      </div>
    </main>

    <!-- Global Footer -->
    <footer class="oracle-layout-footer">
      <p>© 2026 Weather Oracle 智能气象助手 | 科学预报，智慧服务</p>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, watch, onMounted, onUnmounted } from 'vue'
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

const userTitle = computed(() => {
  return isAdmin.value ? '管理员' : '用户'
})

const isDropdownOpen = ref(false)
const dropdownRef = ref<HTMLElement | null>(null)

watch(theme, value => {
  localStorage.setItem('weather_oracle:theme', value)
})

function toggleTheme() {
  theme.value = theme.value === 'light' ? 'dark' : 'light'
}

function toggleDropdown() {
  isDropdownOpen.value = !isDropdownOpen.value
}

function navigateTo(path: string) {
  isDropdownOpen.value = false
  router.push(path)
}

async function handleLogout() {
  isDropdownOpen.value = false
  await authStore.logout()
  router.push('/login')
}

// Click outside helper to close dropdown
function handleClickOutside(event: MouseEvent) {
  if (dropdownRef.value && !dropdownRef.value.contains(event.target as Node)) {
    isDropdownOpen.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
.oracle-layout {
  min-height: 100vh;
  color: var(--oracle-text);
  position: relative;
  isolation: isolate;
  background:
    linear-gradient(115deg, rgba(215, 174, 105, 0.05), transparent 30%),
    linear-gradient(245deg, rgba(142, 110, 194, 0.05), transparent 35%),
    linear-gradient(135deg, var(--oracle-bg-deep), var(--oracle-bg) 45%, var(--oracle-panel-solid));
  display: flex;
  flex-direction: column;
}

.oracle-layout::after {
  content: '';
  position: fixed;
  inset: 0;
  z-index: -1;
  pointer-events: none;
  background-image: var(--oracle-bg-pattern);
  background-repeat: repeat;
  background-size: 360px;
  opacity: 0.12;
  transition: opacity 0.5s ease, background-image 0.5s ease;
}

.oracle-layout[data-oracle-theme='light']::after {
  opacity: 0.85;
}

/* Header Navbar Styles */
.oracle-header {
  position: sticky;
  top: 0;
  z-index: 100;
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.03), transparent), var(--oracle-panel);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid var(--oracle-border);
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.15);
  width: 100%;
}

.oracle-header-inner {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 24px;
  height: 72px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

/* Logo Brand */
.oracle-header-brand {
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  user-select: none;
}

.oracle-header-logo-svg {
  color: var(--oracle-gold);
  filter: drop-shadow(0 0 4px var(--oracle-gold-glow));
  animation: pulse-mystical 3s ease-in-out infinite;
}

.oracle-header-brand-text strong {
  display: block;
  font-family: var(--oracle-font-display);
  font-size: 16px;
  font-weight: 700;
  color: var(--oracle-text);
  letter-spacing: 0.05em;
}

.oracle-header-brand-text span {
  display: block;
  font-size: 11px;
  color: var(--oracle-gold);
  margin-top: 1px;
  letter-spacing: 0.1em;
}

/* Horizontal Nav */
.oracle-header-nav {
  display: flex;
  align-items: center;
  gap: 8px;
}

.oracle-header-nav-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  border-radius: 20px;
  color: var(--oracle-faint);
  font-size: 14px;
  font-weight: 600;
  text-decoration: none;
  border: 1px solid transparent;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.nav-dot {
  width: 5px;
  height: 5px;
  border-radius: 50%;
  background: var(--oracle-gold);
  opacity: 0;
  transform: scale(0.5);
  transition: all 0.3s ease;
}

.oracle-header-nav-item:hover {
  color: var(--oracle-text);
  background: var(--oracle-panel-soft);
  border-color: var(--oracle-border-soft);
}

.oracle-header-nav-item.active {
  color: var(--oracle-gold-strong);
  background: linear-gradient(135deg, rgba(215, 174, 105, 0.12), rgba(142, 110, 194, 0.08));
  border-color: var(--oracle-border);
  box-shadow: 0 0 15px rgba(215, 174, 105, 0.05);
}

.oracle-header-nav-item.active .nav-dot {
  opacity: 1;
  transform: scale(1);
}

/* Header Right Control Pane */
.oracle-header-right {
  display: flex;
  align-items: center;
  gap: 24px;
}

.oracle-header-moon-phases {
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--oracle-gold);
  opacity: 0.8;
  font-size: 14px;
}

.phase-symbol {
  letter-spacing: 2px;
}

/* User Dropdown Trigger */
.oracle-header-user-wrapper {
  position: relative;
}

.oracle-header-profile-trigger {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  padding: 6px 12px;
  border-radius: 30px;
  border: 1px solid var(--oracle-border-soft);
  background: var(--oracle-panel-soft);
  transition: all 0.3s ease;
}

.oracle-header-profile-trigger:hover {
  border-color: var(--oracle-border);
  background: var(--oracle-panel);
  box-shadow: 0 0 10px var(--oracle-gold-glow);
}

.oracle-header-avatar {
  width: 32px;
  height: 32px;
  border: 1px solid var(--oracle-border);
  border-radius: 50%;
  background: linear-gradient(135deg, var(--oracle-purple-soft), rgba(215, 174, 105, 0.2));
  color: var(--oracle-text);
  display: grid;
  place-items: center;
  font-size: 14px;
  font-weight: 700;
  box-shadow: 0 0 6px rgba(215, 174, 105, 0.2);
}

.oracle-header-user-info {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.user-level-badge {
  font-size: 9px;
  background: linear-gradient(90deg, var(--oracle-gold), var(--oracle-gold-strong));
  color: #120e0a;
  padding: 1px 6px;
  border-radius: 10px;
  font-weight: 700;
  line-height: 1;
}

.user-trigger-name {
  font-size: 12px;
  font-weight: 600;
  color: var(--oracle-muted);
  margin-top: 2px;
}

/* Dropdown Menu Styles */
.oracle-header-dropdown-menu {
  position: absolute;
  top: calc(100% + 12px);
  right: 0;
  width: 200px;
  padding: 16px 0 8px 0;
  z-index: 10;
}

.dropdown-header {
  padding: 0 18px 12px 18px;
}

.dropdown-header strong {
  display: block;
  font-size: 15px;
  color: var(--oracle-text);
}

.dropdown-subtitle {
  display: block;
  font-size: 11px;
  color: var(--oracle-muted);
  margin-top: 2px;
}

.dropdown-list {
  list-style: none;
  padding: 8px 6px 0 6px;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.dropdown-list li {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 14px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 13px;
  font-weight: 600;
  color: var(--oracle-faint);
  transition: all 0.2s ease;
}

.dropdown-list li:hover {
  background: var(--oracle-panel-soft);
  color: var(--oracle-gold-strong);
}

.dropdown-icon {
  font-size: 14px;
  width: 16px;
  text-align: center;
}

.logout-item {
  border-top: 1px solid var(--oracle-border-soft);
  margin-top: 4px;
  border-radius: 0 0 8px 8px !important;
}

.logout-item:hover {
  color: var(--oracle-danger) !important;
}

/* Transition Animations */
.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}

.fade-slide-enter-from {
  opacity: 0;
  transform: translateY(-8px);
}

.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}

/* Main Area Layout */
.oracle-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 24px 0 48px;
}

.oracle-main-content {
  width: 100%;
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 24px;
  box-sizing: border-box;
}

/* Footer styling */
.oracle-layout-footer {
  text-align: center;
  padding: 24px;
  color: var(--oracle-muted);
  font-size: 12px;
  border-top: 1px solid var(--oracle-border-soft);
  background: rgba(0, 0, 0, 0.1);
  margin-top: auto;
}

/* Responsive Styles */
@media (max-width: 1024px) {
  .oracle-header-moon-phases {
    display: none;
  }
}

@media (max-width: 768px) {
  .oracle-header-inner {
    padding: 0 16px;
    height: 64px;
  }

  .oracle-header-nav {
    display: none; /* Can add burger or keep simple for mobile */
  }

  .oracle-header-user-info {
    display: none;
  }

  .oracle-main-content {
    padding: 0 16px;
  }
}
</style>
