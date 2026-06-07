<template>
  <OracleLayout>
    <div class="weather-oracle-dashboard-container">

      <!-- Notifications & Errors -->
      <transition name="fade">
        <div v-if="cacheNotice" class="oracle-notice-banner">
          <span class="banner-icon">🔔</span> {{ cacheNotice }}
          <button class="banner-close-btn" @click="cacheNotice = ''">×</button>
        </div>
      </transition>

      <transition name="fade">
        <div v-if="errorMessage" class="oracle-error-banner">
          <span class="banner-icon">⚠️</span> {{ errorMessage }}
          <button class="banner-close-btn" @click="errorMessage = ''">×</button>
        </div>
      </transition>

      <!-- Main Layout Grid: Left Sidebar, Middle Column, Right Sidebar -->
      <div class="oracle-dashboard-grid">

        <!-- Left Column: Navigation & Astrological status -->
        <div class="grid-left-col">
          <OracleLeftSidebar />
        </div>

        <!-- Middle Column: Tarot banner, weather mapping list, checklist -->
        <div class="grid-middle-col">
          <!-- Merged Tarot Display Card -->
          <TarotCardDisplay
            v-if="reading"
            :tarot="reading.tarot"
            :fortune="reading.fortune"
            :observed-at="reading.weather.observed_at"
            :current-city="reading.city"
            :loading="isLoading"
            @draw="drawCity"
          />

          <!-- Placeholder when loading or no reading is loaded yet -->
          <div v-else class="tarot-placeholder-card oracle-surface oracle-gold-corners">
            <div class="placeholder-content">
              <span class="placeholder-icon anim-pulse">🔮</span>
              <h3>正在召唤今日天气牌</h3>
              <p>读取气象要素与星相规律，正在生成你今天的能量映射...</p>
              <div class="placeholder-city-picker">
                <QuickCityPicker
                  :loading="isLoading"
                  current-city=""
                  @draw="drawCity"
                />
              </div>
            </div>
          </div>

          <!-- Mappings Row -->
          <WeatherMetricGrid
            v-if="reading"
            :mappings="reading.weather_mappings"
            :wind-direction="reading.weather.wind_direction"
          />

          <!-- Mood Guide Row -->
          <MoodGuidePanel
            v-if="reading"
            :guide="reading.mood_guide"
          />
        </div>

        <!-- Right Column: Contextual Chat -->
        <div class="grid-right-col">
          <OracleChatPanel
            :city="reading?.city || '未知'"
            :reading="reading || undefined"
          />
        </div>
      </div>

      <!-- Bottom Row: 4 detailed rating cards -->
      <div class="oracle-dashboard-bottom-row">
        <OracleBottomCards :lucky-number="reading?.fortune.lucky_number" />
      </div>

    </div>
  </OracleLayout>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import OracleLayout from '../layouts/OracleLayout.vue'
import OracleLeftSidebar from '../components/oracle/OracleLeftSidebar.vue'
import QuickCityPicker from '../components/oracle/QuickCityPicker.vue'
import TarotCardDisplay from '../components/oracle/TarotCardDisplay.vue'
import WeatherMetricGrid from '../components/oracle/WeatherMetricGrid.vue'
import MoodGuidePanel from '../components/oracle/MoodGuidePanel.vue'
import OracleChatPanel from '../components/oracle/OracleChatPanel.vue'
import OracleBottomCards from '../components/oracle/OracleBottomCards.vue'
import { generateWeatherOracleReading } from '../api/weatherOracle'
import { useAuthStore } from '../stores/auth'
import { getTarotCardById, tarotAssetsReady } from '../data/tarotCards'
import { getShanghaiDateKey } from '../utils/tarot'
import type { WeatherOracleReading, WeatherOracleTarot } from '../types/weatherOracle'

const authStore = useAuthStore()
const reading = ref<WeatherOracleReading | null>(null)
const isLoading = ref(false)
const errorMessage = ref('')
const cacheNotice = ref('')

const cacheKey = computed(() => `weather_oracle:last_reading:${authStore.username || 'guest'}`)

onMounted(async () => {
  const restored = restoreCachedReading()
  if (!restored) {
    // Dynamically query a default city so they see the gorgeous tarot right away!
    await drawCity('杭州')
  }
})

function restoreCachedReading(): boolean {
  const cached = localStorage.getItem(cacheKey.value)
  if (!cached) return false
  try {
    const data = normalizeReading(JSON.parse(cached) as WeatherOracleReading)
    if (isStaleReading(data)) {
      localStorage.removeItem(cacheKey.value)
      cacheNotice.value = '上次抽到的是旧日期天气牌，今天需要重新抽取。'
      return false
    }
    reading.value = data
    return true
  } catch {
    localStorage.removeItem(cacheKey.value)
    return false
  }
}

async function drawCity(city: string) {
  const nextCity = city.trim()
  if (!nextCity) return
  const dailyReading = reading.value && !isStaleReading(reading.value) ? reading.value : null
  isLoading.value = true
  errorMessage.value = ''
  cacheNotice.value = ''
  try {
    const data = normalizeReading(await generateWeatherOracleReading({
      city: nextCity,
      tarot_card_id: dailyReading?.tarot.id,
    }))
    const nextReading = dailyReading ? preserveDailyTarotReading(data, dailyReading) : data
    reading.value = nextReading
    localStorage.setItem(cacheKey.value, JSON.stringify(nextReading))
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : '抽取失败'
  } finally {
    isLoading.value = false
  }
}

function preserveDailyTarotReading(
  nextReading: WeatherOracleReading,
  dailyReading: WeatherOracleReading,
): WeatherOracleReading {
  return {
    ...nextReading,
    tarot: dailyReading.tarot,
    fortune: dailyReading.fortune,
  }
}

function isStaleReading(data: WeatherOracleReading) {
  return data.date !== getShanghaiDateKey()
}

function normalizeReading(data: WeatherOracleReading): WeatherOracleReading {
  return {
    ...data,
    tarot: mergeLocalTarot(data.tarot),
  }
}

function mergeLocalTarot(tarot: WeatherOracleTarot): WeatherOracleTarot {
  const localCard = getTarotCardById(tarot.id)
  if (!localCard) {
    return {
      ...tarot,
      name_en: tarot.name_en || tarot.id,
      name_zh: tarot.name_zh || tarot.name_en || tarot.id,
      image: tarotAssetsReady ? tarot.image || '' : '',
      keywords: tarot.keywords?.length ? tarot.keywords : ['天气', '提示'],
    }
  }

  return {
    id: tarot.id,
    name_en: localCard.nameEn,
    name_zh: localCard.nameZh,
    image: tarotAssetsReady ? localCard.image : '',
    keywords: localCard.keywords,
  }
}
</script>

<style scoped>
.weather-oracle-dashboard-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
  width: 100%;
}

/* Banner Alerts */
.oracle-notice-banner,
.oracle-error-banner {
  padding: 12px 20px;
  border-radius: var(--oracle-radius);
  font-size: 13.5px;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border: 1px solid var(--oracle-border);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(8px);
}

.oracle-notice-banner {
  background: rgba(215, 174, 105, 0.12);
  color: var(--oracle-gold-strong);
  border-color: var(--oracle-border);
}

.oracle-error-banner {
  background: rgba(207, 110, 91, 0.12);
  color: var(--oracle-danger);
  border-color: rgba(207, 110, 91, 0.3);
}

.banner-icon {
  margin-right: 8px;
  font-size: 15px;
}

.banner-close-btn {
  background: none;
  border: none;
  font-size: 18px;
  line-height: 1;
  color: inherit;
  cursor: pointer;
  opacity: 0.7;
  transition: opacity 0.2s ease;
}

.banner-close-btn:hover {
  opacity: 1;
}

/* Dashboard Columns Grid */
.oracle-dashboard-grid {
  display: grid;
  grid-template-columns: 240px 1fr 320px;
  gap: 20px;
  align-items: stretch;
}

.grid-left-col {
  min-width: 0;
}

.grid-middle-col {
  display: flex;
  flex-direction: column;
  gap: 20px;
  min-width: 0;
}

.grid-right-col {
  min-width: 0;
}

/* Bottom Rating cards Row */
.oracle-dashboard-bottom-row {
  margin-top: 8px;
}

/* Middle Column Placeholder Loader */
.tarot-placeholder-card {
  padding: 50px 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  min-height: 360px;
}

.placeholder-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  max-width: 420px;
}

.placeholder-icon {
  font-size: 48px;
  filter: drop-shadow(0 0 10px var(--oracle-gold-glow));
}

.placeholder-content h3 {
  font-family: var(--oracle-font-serif);
  font-size: 22px;
  color: var(--oracle-text);
  margin: 4px 0 0 0;
}

.placeholder-content p {
  font-size: 13.5px;
  color: var(--oracle-muted);
  line-height: 1.6;
  margin: 0;
}

.placeholder-city-picker {
  margin-top: 14px;
}

/* Modify banner slide-fade transitions */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 200ms ease-out, transform 200ms cubic-bezier(0.23, 1, 0.32, 1);
}

.fade-enter-from {
  opacity: 0;
  transform: translateY(-8px);
}

.fade-leave-to {
  opacity: 0;
  transform: translateY(-4px);
}

/* Responsiveness adjustments */
@media (max-width: 1200px) {
  .oracle-dashboard-grid {
    grid-template-columns: 220px 1fr;
  }
  .grid-right-col {
    grid-column: 1 / span 2;
  }
}

@media (max-width: 900px) {
  .oracle-dashboard-grid {
    grid-template-columns: 1fr;
  }
  .grid-left-col,
  .grid-middle-col,
  .grid-right-col {
    grid-column: auto;
  }
}
</style>
