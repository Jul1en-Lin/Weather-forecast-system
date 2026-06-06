<template>
  <OracleLayout>
    <div class="weather-oracle-page">
      <section class="oracle-hero">
        <div>
          <p class="oracle-eyebrow">Daily weather divination</p>
          <h1>今日天气塔罗牌</h1>
          <span v-if="reading">
            {{ reading.city }} · {{ reading.weather.condition || '实时天气' }} · {{ reading.date }}
          </span>
          <span v-else>输入城市，抽取当天的天气牌和状态建议</span>
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
        <TarotCardDisplay class="oracle-tarot-area" :tarot="reading.tarot" />
        <div class="oracle-fortune oracle-surface">
          <span class="oracle-eyebrow">今日指引</span>
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
        <WeatherMetricGrid class="oracle-metrics-area" :mappings="reading.weather_mappings" />
        <MoodGuidePanel class="oracle-mood-area" :guide="reading.mood_guide" />
        <OracleChatPanel class="oracle-chat-area" :city="reading.city" :reading="reading" />
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
import { getTarotCardById, tarotAssetsReady } from '../data/tarotCards'
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
.weather-oracle-page {
  display: grid;
  gap: 16px;
  min-width: 0;
}

.oracle-hero {
  display: flex;
  align-items: end;
  justify-content: space-between;
  gap: 24px;
  min-width: 0;
  padding: 24px;
  border: 1px solid var(--oracle-border);
  border-radius: 8px;
  background:
    linear-gradient(90deg, rgba(215, 174, 105, 0.09), transparent 38%),
    var(--oracle-panel);
  box-shadow: var(--oracle-shadow);
}

.oracle-hero p,
.oracle-hero span {
  margin: 0;
  color: var(--oracle-muted);
  line-height: 1.6;
}

.oracle-hero h1 {
  margin: 8px 0;
  color: var(--oracle-text);
  font-size: clamp(30px, 4vw, 44px);
  line-height: 1.1;
}

.oracle-notice,
.oracle-error,
.oracle-empty {
  padding: 18px 20px;
  border: 1px solid var(--oracle-border);
  border-radius: 8px;
  background: var(--oracle-panel);
}

.oracle-notice {
  color: var(--oracle-gold-strong);
}

.oracle-error {
  color: var(--oracle-danger);
}

.oracle-empty {
  display: grid;
  gap: 10px;
  min-height: 260px;
  place-content: center;
  padding: 34px 20px;
  text-align: center;
}

.oracle-empty h2,
.oracle-empty p {
  margin: 0;
}

.oracle-empty h2 {
  color: var(--oracle-text);
  font-size: 28px;
}

.oracle-empty p {
  color: var(--oracle-muted);
}

.oracle-dashboard {
  display: grid;
  grid-template-columns: minmax(260px, 0.8fr) minmax(360px, 1.2fr) minmax(300px, 0.9fr);
  gap: 16px;
  align-items: stretch;
  min-width: 0;
}

.oracle-tarot-area {
  grid-column: 1;
  grid-row: 1 / span 2;
}

.oracle-fortune {
  grid-column: 2;
  grid-row: 1;
}

.oracle-metrics-area {
  grid-column: 2;
  grid-row: 2;
}

.oracle-mood-area {
  grid-column: 1 / span 2;
  grid-row: 3;
}

.oracle-chat-area {
  grid-column: 3;
  grid-row: 1 / span 3;
}

.oracle-fortune {
  display: grid;
  align-content: start;
  gap: 13px;
  min-width: 0;
  padding: 22px;
}

.oracle-fortune h2,
.oracle-fortune p {
  margin: 0;
}

.oracle-fortune h2 {
  color: var(--oracle-text);
  font-size: 24px;
}

.oracle-fortune p {
  color: var(--oracle-faint);
  line-height: 1.75;
}

.oracle-fortune dl {
  display: grid;
  grid-template-columns: 76px minmax(0, 1fr);
  gap: 10px 12px;
  margin: 0;
  padding-top: 6px;
  border-top: 1px solid var(--oracle-border-soft);
}

.oracle-fortune dt {
  color: var(--oracle-muted);
}

.oracle-fortune dd {
  margin: 0;
  color: var(--oracle-text);
  min-width: 0;
  overflow-wrap: anywhere;
}

.oracle-fortune small {
  color: var(--oracle-muted);
}

@media (max-width: 1280px) {
  .oracle-dashboard {
    grid-template-columns: minmax(260px, 0.9fr) minmax(360px, 1.1fr);
  }

  .oracle-tarot-area {
    grid-column: 1;
    grid-row: 1 / span 2;
  }

  .oracle-fortune {
    grid-column: 2;
    grid-row: 1;
  }

  .oracle-metrics-area {
    grid-column: 2;
    grid-row: 2;
  }

  .oracle-mood-area {
    grid-column: 1;
    grid-row: 3;
  }

  .oracle-chat-area {
    grid-column: 2;
    grid-row: 3;
  }
}

@media (max-width: 980px) {
  .oracle-hero {
    align-items: stretch;
    flex-direction: column;
  }

  .oracle-dashboard {
    grid-template-columns: 1fr;
  }

  .oracle-tarot-area,
  .oracle-fortune,
  .oracle-metrics-area,
  .oracle-mood-area,
  .oracle-chat-area {
    grid-column: 1;
    grid-row: auto;
  }
}

@media (max-width: 560px) {
  .oracle-hero {
    padding: 18px;
  }

  .oracle-hero h1 {
    font-size: 30px;
  }

  .oracle-fortune {
    padding: 18px;
  }

  .oracle-fortune dl {
    grid-template-columns: 64px minmax(0, 1fr);
  }
}
</style>
