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
        <svg viewBox="0 0 100 100" width="80" height="80" class="oracle-weather-svg">
          <defs>
            <linearGradient id="sunGradient" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stop-color="#FFF2A3" />
              <stop offset="50%" stop-color="#FFD700" />
              <stop offset="100%" stop-color="#FF8C00" />
            </linearGradient>
          </defs>
          <!-- Celestial outer ring -->
          <circle cx="50" cy="50" r="42" fill="none" stroke="rgba(215, 174, 105, 0.15)" stroke-width="1" />
          <circle cx="50" cy="50" r="42" fill="none" stroke="var(--oracle-gold)" stroke-width="1.2" stroke-dasharray="1 8" class="celestial-ticks" />
          
          <!-- Glowing celestial background -->
          <circle cx="50" cy="50" r="30" fill="rgba(255, 248, 214, 0.02)" />
          
          <!-- The Sun -->
          <circle cx="48" cy="42" r="15" fill="url(#sunGradient)" class="sun-body" />
          
          <!-- The Cloud with glassmorphic look -->
          <path d="M 32 62 h 36 a 10 10 0 0 0 10 -10 a 10 10 0 0 0 -10 -10 a 14 14 0 0 0 -26 -6 a 12 12 0 0 0 -20 10 a 10 10 0 0 0 10 16 Z" fill="rgba(255, 255, 255, 0.08)" stroke="var(--oracle-gold)" stroke-width="1.5" stroke-linejoin="round" class="cloud-body" />
          
          <!-- Star Sparkles (celestial/oracle style) -->
          <path d="M 75 30 L 77 35 L 82 37 L 77 39 L 75 44 L 73 39 L 68 37 L 73 35 Z" fill="var(--oracle-gold)" class="star-sparkle-1" />
          <path d="M 23 23 L 24 26 L 27 27 L 24 28 L 23 31 L 22 28 L 19 27 L 22 26 Z" fill="var(--oracle-gold)" class="star-sparkle-2" />
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

.oracle-weather-svg {
  filter: drop-shadow(0 0 8px var(--oracle-gold-glow));
}

@keyframes spin-slow {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
.celestial-ticks {
  transform-origin: 50px 50px;
  animation: spin-slow 120s linear infinite;
}

@keyframes sun-pulse {
  0%, 100% { transform: scale(1); filter: drop-shadow(0 0 3px rgba(255, 215, 0, 0.3)); }
  50% { transform: scale(1.06); filter: drop-shadow(0 0 10px rgba(255, 215, 0, 0.6)); }
}
.sun-body {
  transform-origin: 48px 42px;
  animation: sun-pulse 6s ease-in-out infinite;
}

@keyframes float-gentle {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-2.5px); }
}
.cloud-body {
  transform-origin: 50px 50px;
  animation: float-gentle 5s ease-in-out infinite;
}

@keyframes shine {
  0%, 100% { opacity: 0.4; transform: scale(0.8); }
  50% { opacity: 1; transform: scale(1.1); }
}
.star-sparkle-1 {
  transform-origin: 75px 37px;
  animation: shine 4s ease-in-out infinite;
}
.star-sparkle-2 {
  transform-origin: 23px 27px;
  animation: shine 3s ease-in-out infinite;
  animation-delay: 1.5s;
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
