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
      <span class="oracle-eyebrow">Daily Tips</span>
      <h3 class="card-title">每日气象贴士</h3>

      <div class="moon-phase-display">
        <!-- SVG Weather Graphic -->
        <svg viewBox="0 0 24 24" width="72" height="72" class="moon-svg" style="color: var(--oracle-gold);">
          <circle cx="12" cy="8" r="4" fill="currentColor" />
          <path fill="currentColor" opacity="0.85" d="M19.36 10.04C18.67 6.59 15.64 4 12 4 9.11 4 6.6 5.64 5.35 8.04 2.34 8.36 0 10.91 0 14c0 3.31 2.69 6 6 6h13c2.76 0 5-2.24 5-5 0-2.64-2.05-4.78-4.64-4.96z" />
        </svg>
      </div>

      <div class="horoscope-info">
        <strong class="moon-sign-title">{{ displayTip.title }}</strong>
        <p class="moon-sign-copy">{{ displayTip.advice }}</p>

        <router-link to="/knowledge-base" class="view-detail-link">
          查看详情 →
        </router-link>
      </div>
    </div>
  </aside>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { WeatherOracleTip } from '../../types/weatherOracle'
import { useAuthStore } from '../../stores/auth'

const props = defineProps<{
  weatherTip?: WeatherOracleTip
}>()

const authStore = useAuthStore()
const isAdmin = computed(() => authStore.isAdmin)

const weatherTips = [
  { title: '紫外线提示', advice: '夏季紫外线较强，外出建议涂抹防晒霜、佩戴遮阳帽' },
  { title: '防暑降温', advice: '高温天气注意补充水分，避免长时间户外暴晒' },
  { title: '雷雨天气', advice: '雷雨天气避免在空旷地带停留，远离金属物体' },
  { title: '台风预防', advice: '台风来临前检查门窗，储备必要物资，关注预警信息' },
  { title: '雾天出行', advice: '大雾天气能见度低，驾车请减速慢行、开启雾灯' },
  { title: '寒潮提醒', advice: '寒潮来临注意添衣保暖，预防感冒和心血管疾病' },
  { title: '空气质量', advice: '关注空气质量指数，污染天气减少户外活动' },
  { title: '干燥天气', advice: '秋冬干燥季节注意补水保湿，预防静电和皮肤干裂' },
  { title: '晨练建议', advice: '晴好天气适宜户外运动，但避开高温时段' },
  { title: '梅雨季节', advice: '梅雨期间注意防潮除湿，衣物及时晾晒烘干' },
  { title: '霜冻预警', advice: '霜冻天气注意农作物保护，行车注意路面结冰' },
  { title: '气压变化', advice: '气压剧烈波动可能引起头痛不适，注意休息调节' },
]

// Compute a dynamic tip based on the current date of the month
const displayTip = computed(() => {
  if (props.weatherTip && props.weatherTip.title && props.weatherTip.advice) {
    return props.weatherTip
  }
  const day = new Date().getDate()
  return weatherTips[day % weatherTips.length]
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
