<template>
  <section class="oracle-tarot-merged-card oracle-surface oracle-gold-corners">
    <!-- Left Column: Title & Selector -->
    <div class="tarot-left-col">
      <div class="tarot-card-title-wrap">
        <span class="oracle-eyebrow">Weather Intelligence</span>
        <h2>今日天气概览</h2>
        <p class="tarot-subtitle">AI 为你解读今日天气</p>
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
            <small class="fallback-copy">天气卡片加载中</small>
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
        <span class="guidance-title">今日提示</span>
        <span class="guidance-marker">✦</span>
      </div>

      <div class="fortune-main-details">
        <h3 class="fortune-title-mix">
          {{ fortune.title }}
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
          <span class="dl-label">今日色彩</span>
          <span class="dl-value">
            <span class="color-indicator" :style="{ backgroundColor: getColorCode(fortune.lucky_color) }"></span>
            {{ fortune.lucky_color }}
          </span>
        </div>
        <div class="fortune-dl-row">
          <span class="dl-label">今日数字</span>
          <span class="dl-value num-val">{{ fortune.lucky_number }}</span>
        </div>
        <div class="fortune-dl-row flex-top">
          <span class="dl-label">适宜</span>
          <span class="dl-value do-avoid-val positive">{{ fortune.good_for }}</span>
        </div>
        <div class="fortune-dl-row flex-top">
          <span class="dl-label">注意</span>
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
    // 紫色系
    '雾紫色': '#9d81ba', '薰衣草紫': '#967bb6', '紫色': '#8b5cf6',
    '深紫色': '#5b21b6', '浅紫色': '#c4b5fd', '丁香紫': '#b57bee',
    '葡萄紫': '#6b21a8', '烟紫色': '#a78bca', '紫罗兰': '#8b5cf6',
    '藤紫色': '#7c5cbf', '蓝紫色': '#7c3aed',
    // 蓝色系
    '星空蓝': '#3c6ea5', '星空蓝色': '#3c6ea5', '湖蓝色': '#2196a8',
    '天蓝色': '#4ca3c9', '海蓝色': '#1a6fa8', '深蓝色': '#1e3a5f',
    '宝蓝色': '#1a4fa8', '蔚蓝色': '#3a9ad9', '青蓝色': '#3a8fa8',
    '钴蓝色': '#2563eb', '靛蓝色': '#3730a3', '蓝色': '#3b82f6',
    '浅蓝色': '#93c5fd', '冰蓝色': '#bae6fd', '水蓝色': '#38bdf8',
    '孔雀蓝': '#009b8d', '矢车菊蓝': '#6495ed',
    // 绿色系
    '墨绿色': '#3a6e50', '翠绿色': '#3cb371', '翡翠绿': '#50c878',
    '薄荷绿': '#98ff98', '草绿色': '#7cba5a', '苔绿色': '#6b7c4d',
    '绿色': '#4ade80', '深绿色': '#166534', '浅绿色': '#86efac',
    '竹绿色': '#6aa84f', '橄榄绿': '#808000', '碧绿色': '#3b9c6d',
    // 黄/金色系
    '浅金色': '#d6b678', '琥珀黄': '#d99d55', '金黄色': '#f5c842',
    '柠檬黄': '#fff44f', '鹅黄色': '#f9e45e', '鸡蛋黄': '#f5cc6a',
    '明黄色': '#ffdd00', '姜黄色': '#c8961c', '土黄色': '#c8a05a',
    '黄色': '#facc15', '浅黄色': '#fef08a', '金色': '#d4af37',
    '香槟色': '#f7e7ce', '奶油色': '#fffdd0',
    // 橙色系
    '橙色': '#fb923c', '暖橙色': '#f97316', '珊瑚橙': '#ff6b6b',
    '橙红色': '#ea580c', '蜜橙色': '#fb923c', '南瓜橙': '#d2691e',
    // 红色系
    '朱红色': '#c45248', '玫瑰红': '#e11d48', '桃红色': '#f43f5e',
    '绯红色': '#dc2626', '深红色': '#991b1b', '大红色': '#ef4444',
    '砖红色': '#b84343', '酒红色': '#800020', '胭脂红': '#cb3e4b',
    '樱桃红': '#de3163', '红色': '#ef4444',
    // 粉色系
    '玫瑰粉': '#c98194', '樱花粉': '#f9a8b8', '浅粉色': '#fecdd3',
    '粉色': '#f472b6', '蜜桃粉': '#f9a8d4', '肉粉色': '#f4a0a0',
    '浅玫瑰': '#ffb6c1', '婴儿粉': '#ffb8c6',
    // 中性/灰白系
    '银灰色': '#abb3b8', '象牙白': '#f2ebd9', '月白色': '#f0f4f8',
    '珍珠白': '#f8f4f0', '米白色': '#faf0e6', '灰色': '#9ca3af',
    '浅灰色': '#d1d5db', '深灰色': '#4b5563', '白色': '#f8f8f8',
    '雾白色': '#e8e8e8', '烟灰色': '#9e9e9e',
    // 棕/褐色系
    '黛黑色': '#2b313a', '黑色': '#1a1a2e', '炭黑色': '#333333',
    '深棕色': '#795548', '棕色': '#a1724a', '咖啡色': '#7b5e49',
    '巧克力色': '#6b3a2a', '栗色': '#800000',
    // 特殊诗意色名
    '月影银': '#c0c8d8', '晨曦橙': '#f9a860', '暮霭紫': '#a07cb5',
    '烟霞红': '#c96b6b', '山岚绿': '#6ba888', '霜蓝色': '#87ceeb',
    '竹影青': '#5f9ea0', '枯荷棕': '#a08060', '冷灰蓝': '#778899',
  }

  if (colorMap[colorName]) return colorMap[colorName]

  // Keyword-based fallback: detect hue from the name
  const name = colorName || ''
  if (/紫|蓝紫|紫罗兰/.test(name)) return '#9d81ba'
  if (/蓝|靛|青/.test(name)) return '#3c6ea5'
  if (/绿|碧|翠|翡/.test(name)) return '#3a6e50'
  if (/黄|金|橙|琥珀/.test(name)) return '#d6b678'
  if (/红|玫瑰|朱|绯|桃/.test(name)) return '#c45248'
  if (/粉|樱/.test(name)) return '#c98194'
  if (/白|银|灰|米|珍珠/.test(name)) return '#abb3b8'
  if (/黑|炭|墨/.test(name)) return '#2b313a'
  if (/棕|褐|咖啡|栗/.test(name)) return '#a1724a'

  return '#d7ae69' // gold fallback
}
</script>

<style scoped>
.oracle-tarot-merged-card {
  display: grid;
  grid-template-columns: 1.1fr 1fr 1.3fr;
  gap: 24px;
  padding: 30px 24px;
  align-items: stretch;
  z-index: 3;
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
