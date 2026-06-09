<template>
  <section class="weather-metric-grid-card oracle-surface oracle-gold-corners">
    <div class="metric-card-header">
      <span class="oracle-eyebrow">Real-time Weather Data</span>
      <h3 class="metric-card-title">实时天气数据</h3>
      <p class="metric-card-subtitle">当前城市气象要素综合分析</p>
    </div>

    <div class="metrics-row" :key="mappings.map(m => m.metric + m.value).join('-')">
      <article
        v-for="(item, idx) in mappings"
        :key="item.metric"
        class="metric-block stagger-item"
        :style="{ '--stagger-idx': idx }"
      >
        <div class="metric-icon-wrap">
          <!-- Render custom SVG icon per metric -->
          <svg class="metric-svg" viewBox="0 0 24 24" width="24" height="24">
            <path v-if="item.metric === 'temperature'" fill="currentColor" d="M15 13V5c0-1.66-1.34-3-3-3S9 3.34 9 5v8c-1.21.91-2 2.37-2 4 0 2.76 2.24 5 5 5s5-2.24 5-5c0-1.63-.79-3.09-2-4zm-3-9c.55 0 1 .45 1 1v3h-2V5c0-.55.45-1 1-1z" />
            <path v-else-if="item.metric === 'humidity'" fill="currentColor" d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z" />
            <path v-else-if="item.metric === 'pressure'" fill="currentColor" d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z" />
            <path v-else-if="item.metric === 'wind_speed'" fill="currentColor" d="M12.72 2.03A10 10 0 0 0 12 2C6.48 2 2 6.48 2 12s4.48 10 10 10a10 10 0 0 0 .72-.03c-.42-.8-.72-1.7-.72-2.7a3.5 3.5 0 0 1 3.5-3.5h.5c1.63 0 3-1.37 3-3s-1.37-3-3-3h-4.5a1 1 0 0 1 0-2h4.5a5 5 0 0 1 5 5c0 2.2-1.47 4.07-3.5 4.7l-.03-.01A1.5 1.5 0 0 0 15.5 17h-.5a5.5 5.5 0 0 0-5.5 5.5z" />
          </svg>
        </div>
        <div class="metric-info">
          <span class="metric-label">{{ item.label }}</span>
          <strong class="metric-value">{{ item.value }}</strong>
          <span class="metric-reading">{{ item.reading }}</span>
        </div>
        <div class="metric-progress-wrap">
          <div class="metric-progress-bar" :style="{ width: `${item.score}%` }"></div>
        </div>
      </article>
    </div>

    <!-- Decorative divider -->
    <div class="oracle-divider"></div>

    <!-- Daily advice footer -->
    <div class="metric-footer-quote">
      <div class="wind-line">
        <span class="sparkle-icon">✨</span>
        <span>今日风向：<strong>{{ windDirection || '和风' }}</strong></span>
      </div>
      <div class="advice-lines">
        <p>
          <span class="advice-label">出行：</span>
          <span>{{ dailyTravelAdvice }}</span>
        </p>
        <p>
          <span class="advice-label">穿衣：</span>
          <span>{{ dailyClothingAdvice }}</span>
        </p>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { WeatherOracleDailyAdvice, WeatherOracleMapping } from '../../types/weatherOracle'

const props = defineProps<{
  mappings: WeatherOracleMapping[]
  windDirection?: string
  dailyAdvice?: WeatherOracleDailyAdvice
}>()

const windSpeed = computed(() => {
  const windMetric = props.mappings.find(m => m.metric === 'wind_speed')
  if (!windMetric) return null
  const parsed = parseFloat(windMetric.value)
  return Number.isFinite(parsed) ? parsed : null
})

const dailyTravelAdvice = computed(() => {
  const advice = props.dailyAdvice?.travel?.trim()
  if (advice) return advice
  if (windSpeed.value !== null && windSpeed.value >= 25) {
    return '风比较大，骑车慢一点，帽子别戴太松。'
  }
  return '正常出门就行，早晚留意临近预报。'
})

const dailyClothingAdvice = computed(() => {
  const advice = props.dailyAdvice?.clothing?.trim()
  if (advice) return advice
  return '穿日常衣物即可，怕冷就加一件薄外套。'
})
</script>

<style scoped>
.weather-metric-grid-card {
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.metric-card-header {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.metric-card-title {
  font-family: var(--oracle-font-serif);
  font-size: 20px;
  color: var(--oracle-text);
  margin: 4px 0 0 0;
  letter-spacing: 0.02em;
}

.metric-card-subtitle {
  color: var(--oracle-muted);
  font-size: 13px;
  margin: 0;
}

/* Horizontal Metrics Row */
.metrics-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}

/* Stagger slide up enter animation */
.stagger-item {
  opacity: 0;
  animation: slideUpStagger 400ms cubic-bezier(0.23, 1, 0.32, 1) forwards;
  animation-delay: calc(var(--stagger-idx) * 45ms);
}

@keyframes slideUpStagger {
  from {
    opacity: 0;
    transform: translateY(12px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Metric block exact transitions, hovers, and active states */
.metric-block {
  border: 1px solid var(--oracle-border-soft);
  border-radius: var(--oracle-radius-inner);
  background: var(--oracle-panel-soft);
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  min-width: 0;
  position: relative;
  transition: transform 180ms cubic-bezier(0.23, 1, 0.32, 1), border-color 180ms ease-out, background-color 180ms ease-out, box-shadow 180ms ease-out;
}

@media (hover: hover) and (pointer: fine) {
  .metric-block:hover {
    border-color: var(--oracle-border);
    background: var(--oracle-panel);
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(0, 0, 0, 0.2);
  }
}

.metric-block:active {
  transform: translateY(-1px) scale(0.97);
}

.metric-icon-wrap {
  width: 38px;
  height: 38px;
  border-radius: 50%;
  background: var(--oracle-purple-soft);
  border: 1px solid var(--oracle-border-soft);
  color: var(--oracle-gold);
  display: grid;
  place-items: center;
  box-shadow: 0 0 6px rgba(215, 174, 105, 0.1);
}

.metric-svg {
  filter: drop-shadow(0 0 2px var(--oracle-gold-glow));
}

.metric-info {
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.metric-label {
  font-size: 12px;
  color: var(--oracle-muted);
  font-weight: 600;
}

.metric-value {
  font-family: var(--oracle-font-serif);
  font-size: 20px;
  color: var(--oracle-text);
  line-height: 1.1;
}

.metric-reading {
  font-size: 12.5px;
  color: var(--oracle-gold-strong);
  font-weight: 600;
  margin-top: 1px;
}

/* Progress indicator under block */
.metric-progress-wrap {
  height: 4px;
  border-radius: 2px;
  background: rgba(255, 255, 255, 0.05);
  overflow: hidden;
  margin-top: auto;
}

/* Progress bar initial loading animation */
@keyframes fillProgress {
  from {
    width: 0%;
  }
}

.metric-progress-bar {
  height: 100%;
  border-radius: 2px;
  background: linear-gradient(90deg, var(--oracle-purple), var(--oracle-gold));
  animation: fillProgress 850ms cubic-bezier(0.23, 1, 0.32, 1) forwards;
}

.metric-footer-quote {
  display: grid;
  grid-template-columns: auto 1fr;
  column-gap: 22px;
  row-gap: 8px;
  align-items: start;
  font-size: 13.5px;
  color: var(--oracle-faint);
  padding: 4px 8px 2px;
  line-height: 1.7;
}

.wind-line {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  white-space: nowrap;
}

.sparkle-icon {
  font-size: 14px;
}

.metric-footer-quote strong {
  color: var(--oracle-gold);
}

.advice-label {
  color: var(--oracle-gold);
  font-weight: 700;
}

.advice-lines {
  display: grid;
  gap: 2px;
  min-width: 0;
}

.advice-lines p {
  margin: 0;
  overflow-wrap: anywhere;
}

/* Responsive Grid styling */
@media (max-width: 1024px) {
  .metrics-row {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 560px) {
  .metrics-row {
    grid-template-columns: 1fr;
  }
  .metric-block {
    padding: 14px;
  }
  .metric-footer-quote {
    grid-template-columns: 1fr;
    gap: 6px;
  }
}
</style>
