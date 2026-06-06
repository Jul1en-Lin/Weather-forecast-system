<template>
  <OracleLayout>
    <div class="weather-oracle-page">
      <section class="oracle-hero">
        <div>
          <p>AI 为你抽取今日的天气指引</p>
          <h1>今日天气塔罗牌</h1>
          <span v-if="reading">
            {{ reading.city }} · {{ reading.weather.condition || '实时天气' }} · {{ reading.date }}
          </span>
        </div>
        <QuickCityPicker :loading="isLoading" @draw="drawCity" />
      </section>

      <section v-if="cacheNotice" class="oracle-notice">{{ cacheNotice }}</section>
      <section v-if="errorMessage" class="oracle-error">{{ errorMessage }}</section>

      <section v-if="!reading" class="oracle-empty">
        <h2>{{ isLoading ? '正在抽取今日天气牌' : '先输入或选择城市' }}</h2>
        <p>我会读取温度、湿度、气压和风速，再生成今日天气塔罗牌。</p>
      </section>

      <section v-else class="oracle-dashboard">
        <TarotCardDisplay :tarot="reading.tarot" />
        <div class="oracle-fortune">
          <h2>{{ reading.fortune.title }}</h2>
          <p>{{ reading.fortune.summary }}</p>
          <dl>
            <dt>幸运色</dt>
            <dd>{{ reading.fortune.lucky_color }}</dd>
            <dt>幸运数字</dt>
            <dd>{{ reading.fortune.lucky_number }}</dd>
            <dt>宜</dt>
            <dd>{{ reading.fortune.good_for }}</dd>
            <dt>忌</dt>
            <dd>{{ reading.fortune.avoid }}</dd>
          </dl>
          <small v-if="reading.weather.observed_at">
            天气观测时间：{{ reading.weather.observed_at }}
          </small>
        </div>
        <WeatherMetricGrid :mappings="reading.weather_mappings" />
        <MoodGuidePanel :guide="reading.mood_guide" />
        <OracleChatPanel :city="reading.city" :reading="reading" />
      </section>
    </div>
  </OracleLayout>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import OracleLayout from '../layouts/OracleLayout.vue'
import QuickCityPicker from '../components/oracle/QuickCityPicker.vue'
import TarotCardDisplay from '../components/oracle/TarotCardDisplay.vue'
import WeatherMetricGrid from '../components/oracle/WeatherMetricGrid.vue'
import MoodGuidePanel from '../components/oracle/MoodGuidePanel.vue'
import OracleChatPanel from '../components/oracle/OracleChatPanel.vue'
import { generateWeatherOracleReading } from '../api/weatherOracle'
import { useAuthStore } from '../stores/auth'
import { getTarotCardById } from '../data/tarotCards'
import { getShanghaiDateKey } from '../utils/tarot'
import type { WeatherOracleReading, WeatherOracleTarot } from '../types/weatherOracle'

const authStore = useAuthStore()
const reading = ref<WeatherOracleReading | null>(null)
const isLoading = ref(false)
const errorMessage = ref('')
const cacheNotice = ref('')

const cacheKey = computed(() => `weather_oracle:last_reading:${authStore.username || 'guest'}`)

onMounted(() => {
  restoreCachedReading()
})

function restoreCachedReading() {
  const cached = localStorage.getItem(cacheKey.value)
  if (!cached) return
  try {
    const data = normalizeReading(JSON.parse(cached) as WeatherOracleReading)
    if (isStaleReading(data)) {
      localStorage.removeItem(cacheKey.value)
      cacheNotice.value = '上次抽到的是旧日期天气牌，今天需要重新抽取。'
      return
    }
    reading.value = data
  } catch {
    localStorage.removeItem(cacheKey.value)
  }
}

async function drawCity(city: string) {
  if (!city.trim()) return
  isLoading.value = true
  errorMessage.value = ''
  cacheNotice.value = ''
  try {
    const data = normalizeReading(await generateWeatherOracleReading({ city: city.trim() }))
    reading.value = data
    localStorage.setItem(cacheKey.value, JSON.stringify(data))
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : '抽取失败'
  } finally {
    isLoading.value = false
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
      image: tarot.image || '',
      keywords: tarot.keywords?.length ? tarot.keywords : ['天气', '提示'],
    }
  }

  return {
    id: tarot.id,
    name_en: localCard.nameEn,
    name_zh: localCard.nameZh,
    image: localCard.image,
    keywords: localCard.keywords,
  }
}
</script>

<style scoped>
.weather-oracle-page {
  display: grid;
  gap: 22px;
  min-height: 100vh;
  padding: 36px;
}

.oracle-hero {
  display: flex;
  align-items: end;
  justify-content: space-between;
  gap: 24px;
  padding: 28px;
  border-radius: 22px;
  background: rgba(255, 255, 255, 0.68);
}

.oracle-hero p,
.oracle-hero span {
  margin: 0;
  color: #4b5563;
  line-height: 1.6;
}

.oracle-hero h1 {
  margin: 8px 0;
  color: #111827;
  font-size: 40px;
  line-height: 1.1;
}

.oracle-notice,
.oracle-error,
.oracle-empty {
  padding: 18px 20px;
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.76);
}

.oracle-notice {
  color: #6b4f00;
}

.oracle-error {
  color: #b42318;
}

.oracle-empty {
  display: grid;
  gap: 10px;
  min-height: 260px;
  place-content: center;
  text-align: center;
}

.oracle-empty h2,
.oracle-empty p {
  margin: 0;
}

.oracle-empty h2 {
  color: #111827;
  font-size: 28px;
}

.oracle-empty p {
  color: #4b5563;
}

.oracle-dashboard {
  display: grid;
  grid-template-columns: minmax(0, 1.35fr) minmax(280px, 0.65fr);
  gap: 18px;
}

.weather-metric-grid,
.mood-guide-panel,
.oracle-chat-panel {
  grid-column: 1 / -1;
}

.oracle-fortune {
  display: grid;
  gap: 14px;
  padding: 24px;
  border-radius: 18px;
  background: rgba(255, 255, 255, 0.72);
}

.oracle-fortune h2,
.oracle-fortune p {
  margin: 0;
}

.oracle-fortune h2 {
  color: #111827;
  font-size: 24px;
}

.oracle-fortune p {
  color: #374151;
  line-height: 1.8;
}

.oracle-fortune dl {
  display: grid;
  grid-template-columns: 88px 1fr;
  gap: 10px 12px;
  margin: 0;
}

.oracle-fortune dt {
  color: #6b7280;
}

.oracle-fortune dd {
  margin: 0;
  color: #111827;
}

.oracle-fortune small {
  color: #6b7280;
}

@media (max-width: 980px) {
  .weather-oracle-page {
    padding: 24px;
  }

  .oracle-hero {
    align-items: stretch;
    flex-direction: column;
  }

  .oracle-dashboard {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .weather-oracle-page {
    padding: 18px;
  }

  .oracle-hero h1 {
    font-size: 32px;
  }
}
</style>
