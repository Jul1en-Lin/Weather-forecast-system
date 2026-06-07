<template>
  <aside class="oracle-left-sidebar">
    <!-- Quick Entry Card -->
    <div class="quick-entry-card oracle-surface oracle-gold-corners">
      <span class="oracle-eyebrow">Quick Navigation</span>
      <h3 class="card-title">快捷入口</h3>

      <nav class="sidebar-menu">
        <router-link to="/intelligent-assistant" class="menu-item">
          <span class="menu-icon">💬</span>
          <span class="menu-text">智能对话</span>
        </router-link>
        <router-link to="/oracle" class="menu-item" @click="handleSearchTrigger">
          <span class="menu-icon">🌤️</span>
          <span class="menu-text">天气查询</span>
        </router-link>
        <router-link to="/knowledge-base" class="menu-item">
          <span class="menu-icon">📖</span>
          <span class="menu-text">知识库</span>
        </router-link>
        <router-link v-if="isAdmin" to="/admin/users" class="menu-item">
          <span class="menu-icon">👥</span>
          <span class="menu-text">用户管理</span>
        </router-link>
      </nav>
    </div>

    <!-- Horoscope Card -->
    <div class="horoscope-card oracle-surface oracle-gold-corners">
      <span class="oracle-eyebrow">Astrology</span>
      <h3 class="card-title">今日星象</h3>

      <div class="moon-phase-display">
        <!-- SVG Moon Phase Graphic -->
        <svg viewBox="0 0 100 100" width="72" height="72" class="moon-svg">
          <defs>
            <radialGradient id="moonGlow" cx="50%" cy="50%" r="50%">
              <stop offset="0%" stop-color="#fff" stop-opacity="0.8" />
              <stop offset="60%" stop-color="#fff8d6" stop-opacity="0.3" />
              <stop offset="100%" stop-color="#d7ae69" stop-opacity="0" />
            </radialGradient>
          </defs>
          <circle cx="50" cy="50" r="40" fill="rgba(255,255,255,0.03)" stroke="var(--oracle-border-soft)" stroke-width="1" />
          <circle cx="50" cy="50" r="30" fill="url(#moonGlow)" class="glow-circle" />
          <!-- Draw dynamic crescent mask -->
          <path :d="moonPath" fill="var(--oracle-bg)" opacity="0.8" />
        </svg>
      </div>

      <div class="horoscope-info">
        <strong class="moon-sign-title">月亮进入{{ currentZodiac.sign }}</strong>
        <p class="moon-sign-copy">{{ currentZodiac.advice }}</p>

        <router-link to="/knowledge-base" class="view-detail-link">
          查看详情 →
        </router-link>
      </div>
    </div>
  </aside>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useAuthStore } from '../../stores/auth'

const authStore = useAuthStore()
const isAdmin = computed(() => authStore.isAdmin)

const zodiacSigns = [
  { sign: '白羊座', advice: '激情重燃，宜开启全新挑战与计划' },
  { sign: '金牛座', advice: '感官敏锐，宜享受美食、安稳身心' },
  { sign: '双子座', advice: '灵思泉涌，宜头脑风暴与信息交流' },
  { sign: '巨蟹座', advice: '情感丰盈，宜陪伴家人、整理情绪' },
  { sign: '狮子座', advice: '自信倍增，宜展示才华、积极社交' },
  { sign: '处女座', advice: '思维缜密，宜整理收纳、推敲细节' },
  { sign: '天秤座', advice: '审美提升，宜寻觅美好、维持人际平衡' },
  { sign: '天蝎座', advice: '直觉深邃，宜探寻隐秘、疗愈内心' },
  { sign: '射手座', advice: '胸怀旷达，宜登高望远、学习新知' },
  { sign: '摩羯座', advice: '沉稳务实，宜稳步推进、落实阶段目标' },
  { sign: '水瓶座', advice: '特立独行，宜践行创意、打破旧有成见' },
  { sign: '双鱼座', advice: '直觉增强，适合内容与分析创作' },
]

// Compute a dynamic zodiac sign based on the current date of the month
const currentZodiac = computed(() => {
  const day = new Date().getDate()
  return zodiacSigns[day % zodiacSigns.length]
})

// Compute a dynamic moon path SVG string based on the day of the month
const moonPath = computed(() => {
  const day = new Date().getDate()
  const phase = day % 30
  if (phase === 0 || phase === 15) {
    return '' // Full Moon or New Moon
  }
  // Draw simple crescent paths
  if (phase < 15) {
    // Waxing Crescent / Quarter
    return 'M 50 20 A 30 30 0 0 1 50 80 A 15 30 0 0 1 50 20 Z'
  } else {
    // Waning Crescent / Quarter
    return 'M 50 20 A 15 30 0 0 1 50 80 A 30 30 0 0 1 50 20 Z'
  }
})

function handleSearchTrigger() {
  const el = document.querySelector('.oracle-city-select-trigger') as HTMLElement
  if (el) el.click()
}
</script>

<style scoped>
.oracle-left-sidebar {
  display: flex;
  flex-direction: column;
  gap: 20px;
  width: 100%;
}

.quick-entry-card,
.horoscope-card {
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.card-title {
  font-family: var(--oracle-font-serif);
  font-size: 18px;
  color: var(--oracle-text);
  margin: 0;
  letter-spacing: 0.02em;
}

/* Sidebar Menu */
.sidebar-menu {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-top: 4px;
}

.menu-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  border-radius: 8px;
  border: 1px solid var(--oracle-border-soft);
  background: var(--oracle-panel-soft);
  color: var(--oracle-faint);
  font-size: 14px;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.menu-item:hover {
  border-color: var(--oracle-gold);
  color: var(--oracle-gold-strong);
  background: var(--oracle-panel);
  box-shadow: 0 4px 12px var(--oracle-gold-glow);
}

.menu-icon {
  font-size: 16px;
}

/* Horoscope Card display */
.moon-display-wrapper {
  display: flex;
  justify-content: center;
}

.moon-phase-display {
  display: grid;
  place-items: center;
  padding: 10px 0;
}

.moon-svg {
  filter: drop-shadow(0 0 8px var(--oracle-gold-glow));
}

.glow-circle {
  animation: pulse-mystical 4s ease-in-out infinite;
}

.horoscope-info {
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  margin-top: 6px;
}

.moon-sign-title {
  font-family: var(--oracle-font-serif);
  color: var(--oracle-text);
  font-size: 15px;
}

.moon-sign-copy {
  color: var(--oracle-muted);
  font-size: 12.5px;
  line-height: 1.6;
  margin: 0;
}

.view-detail-link {
  font-size: 12px;
  color: var(--oracle-gold);
  font-weight: 600;
  text-decoration: none;
  margin-top: 4px;
  transition: all 0.2s ease;
}

.view-detail-link:hover {
  color: var(--oracle-gold-strong);
  transform: translateX(2px);
}
</style>
