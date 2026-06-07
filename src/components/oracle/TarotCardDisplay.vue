<template>
  <section class="oracle-tarot-merged-card oracle-surface oracle-gold-corners">
    <!-- Left Column: Title & Selector -->
    <div class="tarot-left-col">
      <div class="tarot-card-title-wrap">
        <span class="oracle-eyebrow">Tarot Weather Divination</span>
        <h2>今日天气塔罗牌</h2>
        <p class="tarot-subtitle">AI 为你抽取今日的天气指引</p>
      </div>

      <div class="tarot-city-picker-wrap">
        <!-- Integrate QuickCityPicker inline here -->
        <QuickCityPicker
          :loading="loading"
          :current-city="currentCity"
          @draw="emitDraw"
        />
      </div>

      <div class="tarot-timestamp-wrap" v-if="observedAt">
        <small class="obs-time">更新于 {{ formattedObservedAt }}</small>
      </div>
    </div>

    <!-- Center Column: Card Image -->
    <div class="tarot-center-col">
      <div class="tarot-card-container">
        <div class="tarot-card-frame">
          <img
            v-if="tarot.image && !imageFailed"
            :src="tarot.image"
            :alt="tarot.name_zh || tarot.name_en || tarot.id"
            class="tarot-card-img"
            @error="imageFailed = true"
          />
          <div v-else class="tarot-card-fallback-frame" aria-hidden="true">
            <span class="fallback-char">{{ fallbackInitial }}</span>
            <small class="fallback-copy">牌面待导出</small>
          </div>
          <!-- Filigree gold border decorations -->
          <div class="frame-gold-border"></div>
        </div>
      </div>
    </div>

    <!-- Right Column: Fortune Guidance -->
    <div class="tarot-right-col">
      <div class="fortune-guidance-header">
        <span class="guidance-marker">✦</span>
        <span class="guidance-title">今日指引</span>
        <span class="guidance-marker">✦</span>
      </div>

      <div class="fortune-main-details">
        <h3 class="fortune-title-mix">
          {{ tarot.name_zh }} · {{ fortune.title }}
        </h3>

        <div class="fortune-keywords-chips">
          <span
            v-for="kw in fortuneKeywords"
            :key="kw"
            class="kw-chip"
          >
            {{ kw }}
          </span>
        </div>

        <p class="fortune-summary-text">
          {{ fortune.summary }}
        </p>
      </div>

      <div class="fortune-dl-metrics">
        <div class="fortune-dl-row">
          <span class="dl-label">幸运色</span>
          <span class="dl-value">
            <span class="color-indicator" :style="{ backgroundColor: getColorCode(fortune.lucky_color) }"></span>
            {{ fortune.lucky_color }}
          </span>
        </div>
        <div class="fortune-dl-row">
          <span class="dl-label">幸运数字</span>
          <span class="dl-value num-val">{{ fortune.lucky_number }}</span>
        </div>
        <div class="fortune-dl-row flex-top">
          <span class="dl-label">宜</span>
          <span class="dl-value do-avoid-val positive">{{ fortune.good_for }}</span>
        </div>
        <div class="fortune-dl-row flex-top">
          <span class="dl-label">忌</span>
          <span class="dl-value do-avoid-val negative">{{ fortune.avoid }}</span>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import type { WeatherOracleTarot, WeatherOracleFortune } from '../../types/weatherOracle'
import QuickCityPicker from './QuickCityPicker.vue'

const props = defineProps<{
  tarot: WeatherOracleTarot
  fortune: WeatherOracleFortune
  observedAt?: string
  currentCity?: string
  loading?: boolean
}>()

const emit = defineEmits<{ draw: [city: string] }>()

const imageFailed = ref(false)

const fallbackInitial = computed(() => {
  const label = props.tarot.name_zh || props.tarot.name_en || props.tarot.id
  return label.charAt(0).toUpperCase()
})

const fortuneKeywords = computed(() => {
  if (props.tarot.keywords && props.tarot.keywords.length > 0) {
    return props.tarot.keywords
  }
  return ['启示', '冥想', '感知']
})

const formattedObservedAt = computed(() => {
  if (!props.observedAt) return ''
  // Format observed time for a clean layout: e.g. 2026-06-06 20:56
  // Check if it's ISO format or simple text
  try {
    const date = new Date(props.observedAt)
    if (!isNaN(date.getTime())) {
      const y = date.getFullYear()
      const m = String(date.getMonth() + 1).padStart(2, '0')
      const d = String(date.getDate()).padStart(2, '0')
      const hr = String(date.getHours()).padStart(2, '0')
      const min = String(date.getMinutes()).padStart(2, '0')
      return `${y}-${m}-${d} ${hr}:${min}`
    }
  } catch {
    // fallback
  }
  return props.observedAt
})

watch(
  () => props.tarot.image,
  () => {
    imageFailed.value = false
  },
)

function emitDraw(city: string) {
  emit('draw', city)
}

// Map color names to hex codes for the color indicator badge
function getColorCode(colorName: string): string {
  const colorMap: Record<string, string> = {
    '雾紫色': '#9d81ba',
    '星空蓝': '#3c6ea5',
    '浅金色': '#d6b678',
    '琥珀黄': '#d99d55',
    '墨绿色': '#3a6e50',
    '玫瑰粉': '#c98194',
    '银灰色': '#abb3b8',
    '象牙白': '#f2ebd9',
    '朱红色': '#c45248',
    '黛黑色': '#2b313a'
  }
  return colorMap[colorName] || '#d7ae69'
}
</script>

<style scoped>
.oracle-tarot-merged-card {
  display: grid;
  grid-template-columns: 1.1fr 1fr 1.3fr;
  gap: 24px;
  padding: 30px 24px;
  align-items: stretch;
}

/* Left Column Styling */
.tarot-left-col {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 20px;
}

.tarot-card-title-wrap h2 {
  font-family: var(--oracle-font-serif);
  font-size: 26px;
  color: var(--oracle-text);
  margin: 6px 0 2px 0;
  letter-spacing: 0.05em;
}

.tarot-subtitle {
  color: var(--oracle-muted);
  font-size: 13.5px;
  margin: 0;
}

.tarot-city-picker-wrap {
  margin: auto 0;
}

.tarot-timestamp-wrap {
  margin-top: auto;
}

.obs-time {
  color: var(--oracle-muted);
  font-size: 11px;
}

/* Center Column (Tarot Card) Styling */
.tarot-center-col {
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Tarot Card Container */
.tarot-card-container {
  width: 100%;
  max-width: 220px;
  aspect-ratio: 500 / 836;
}

.tarot-card-frame {
  position: relative;
  width: 100%;
  max-width: none;
  aspect-ratio: 500 / 836;
  border-radius: var(--oracle-radius-inner);
  border: 1px solid var(--oracle-border);
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
  background: linear-gradient(160deg, #091220, #16243a 50%, #46341f);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.tarot-card-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.tarot-card-fallback-frame {
  text-align: center;
  color: var(--oracle-text);
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.fallback-char {
  font-family: var(--oracle-font-display);
  font-size: 40px;
  font-weight: bold;
  color: var(--oracle-gold);
}

.fallback-copy {
  font-size: 11px;
  color: var(--oracle-muted);
}

/* Filigree gold border inside the card frame */
.frame-gold-border {
  position: absolute;
  inset: 6px;
  border: 1px solid rgba(215, 174, 105, 0.4);
  border-radius: calc(var(--oracle-radius-inner) - 4px);
  pointer-events: none;
}

/* Right Column (Fortune details) Styling */
.tarot-right-col {
  display: flex;
  flex-direction: column;
  gap: 16px;
  border-left: 1px dashed var(--oracle-border-soft);
  padding-left: 24px;
}

.fortune-guidance-header {
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--oracle-gold);
}

.guidance-marker {
  font-size: 11px;
}

.guidance-title {
  font-family: var(--oracle-font-display);
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0.1em;
  text-transform: uppercase;
}

.fortune-title-mix {
  font-family: var(--oracle-font-serif);
  font-size: 20px;
  color: var(--oracle-text);
  margin: 4px 0 8px 0;
}

.fortune-keywords-chips {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
  margin-bottom: 10px;
}

.kw-chip {
  font-size: 11px;
  color: var(--oracle-gold-strong);
  background: var(--oracle-purple-soft);
  border: 1px solid var(--oracle-border-soft);
  padding: 3px 10px;
  border-radius: 12px;
  font-weight: 600;
}

.fortune-summary-text {
  color: var(--oracle-faint);
  font-size: 13.5px;
  line-height: 1.7;
  margin: 0;
}

/* Fortune details list */
.fortune-dl-metrics {
  display: flex;
  flex-direction: column;
  gap: 8px;
  border-top: 1px solid var(--oracle-border-soft);
  padding-top: 12px;
  margin-top: auto;
}

.fortune-dl-row {
  display: flex;
  align-items: center;
  font-size: 13px;
}

.fortune-dl-row.flex-top {
  align-items: flex-start;
}

.dl-label {
  width: 72px;
  color: var(--oracle-muted);
  font-weight: 600;
}

.dl-value {
  flex: 1;
  color: var(--oracle-text);
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 6px;
}

.color-indicator {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.num-val {
  font-family: var(--oracle-font-display);
  color: var(--oracle-gold);
}

.do-avoid-val {
  font-weight: 600;
}

.do-avoid-val.positive {
  color: var(--oracle-success);
}

.do-avoid-val.negative {
  color: var(--oracle-danger);
}

/* Responsive Styles */
@media (max-width: 1200px) {
  .oracle-tarot-merged-card {
    grid-template-columns: 1fr 1.2fr;
    gap: 20px;
  }
  .tarot-left-col {
    grid-column: 1 / span 2;
    flex-direction: row;
    align-items: center;
    border-bottom: 1px solid var(--oracle-border-soft);
    padding-bottom: 20px;
  }
  .tarot-timestamp-wrap {
    margin-top: 0;
  }
}

@media (max-width: 768px) {
  .oracle-tarot-merged-card {
    grid-template-columns: 1fr;
    gap: 24px;
    padding: 24px 16px;
  }
  .tarot-left-col {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
  .tarot-right-col {
    border-left: none;
    border-top: 1px dashed var(--oracle-border-soft);
    padding-left: 0;
    padding-top: 20px;
  }
}
</style>
