<template>
  <OracleLayout>
    <div class="knowledge-base-page">
      <!-- Header Section -->
      <section class="kb-hero">
        <span class="oracle-eyebrow">Model Built-in Knowledge Base</span>
        <h1>模型内置气象知识库</h1>
        <p class="kb-hero-desc">
          以下气象常识作为系统内置知识库，直接用于大语言模型在天气助手与智能问答服务时的常识检索与推理依据。通过注入专业气象学背景，确保智能解答科学、准确。
        </p>
      </section>

      <!-- Category Filter -->
      <div class="kb-categories">
        <button
          v-for="cat in categories"
          :key="cat.value"
          type="button"
          :class="['kb-cat-btn', { active: activeCategory === cat.value }]"
          @click="activeCategory = cat.value"
        >
          {{ cat.label }}
        </button>
      </div>

      <!-- Article List (Text-only Typography) -->
      <div class="kb-list">
        <transition-group name="list-fade">
          <article
            v-for="article in filteredArticles"
            :key="article.id"
            class="kb-article-item"
          >
            <header class="article-header">
              <div class="article-title-wrap">
                <span class="article-icon">{{ article.icon }}</span>
                <h3>{{ article.title }}</h3>
              </div>
              <div class="article-badges">
                <span class="article-category-badge">{{ getCategoryLabel(article.category) }}</span>
              </div>
            </header>
            
            <p class="article-summary">{{ article.summary }}</p>
            <div class="article-content" v-html="article.content"></div>
          </article>
        </transition-group>
      </div>

      <div v-if="filteredArticles.length === 0" class="kb-empty">
        <span class="empty-icon">🌤️</span>
        <p>未找到相关的气象学识。</p>
      </div>
    </div>
  </OracleLayout>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import OracleLayout from '../layouts/OracleLayout.vue'

interface Article {
  id: string
  title: string
  category: 'metric' | 'cycle' | 'theory'
  icon: string
  summary: string
  content: string
}

const activeCategory = ref<'all' | 'metric' | 'cycle' | 'theory'>('all')

const categories: { label: string; value: 'all' | 'metric' | 'cycle' | 'theory' }[] = [
  { label: '全部知识', value: 'all' },
  { label: '气象要素科普', value: 'metric' },
  { label: '岁时节气规律', value: 'cycle' },
  { label: '气象科普理论', value: 'theory' },
]

const articles: Article[] = [
  {
    id: 'temp-metaphor',
    title: '气温的科学规律：生命的寒暑刻度',
    category: 'metric',
    icon: '🌡️',
    summary: '温度是外界环境对生命的包容度。在气象学中，它直接反映了人体的热量平衡与舒适度状态。',
    content: '<ul><li><strong>极寒（&lt;0°C）</strong>：代表能量收敛、防寒保暖与蛰伏，适宜防寒保暖与减少户外活动。</li><li><strong>舒适（20°C-25°C）</strong>：代表万物繁茂、情绪松弛与户外活动，是人体最适宜的温区。</li><li><strong>酷暑（&gt;35°C）</strong>：代表热量积聚，需注意防暑降温与防范强对流天气。</li></ul>'
  },
  {
    id: 'humidity-emotion',
    title: '湿度的科学规律：环境对人体感官的影响',
    category: 'metric',
    icon: '💧',
    summary: '水分是影响环境体感的重要因素。湿度的高低直接影响人体汗液蒸发与舒适度。',
    content: '<ul><li><strong>潮湿（&gt;70%）</strong>：代表空气水分充沛、体感闷热黏腻，需注意室内防潮通风，防范霉菌与呼吸道敏感。</li><li><strong>适宜（40%-60%）</strong>：代表温润舒适、体感最适宜，利于呼吸道健康与日常活动。</li><li><strong>干燥（&lt;30%）</strong>：代表水分蒸发迅速、体感干爽，利于衣物晾晒，但需注意补水防晒及皮肤保湿。</li></ul>'
  },
  {
    id: 'pressure-will',
    title: '气压与人体体感：气压对身体和情绪的影响',
    category: 'metric',
    icon: '🌀',
    summary: '气压是大气压强作用于人体的物理载荷，直接关系到血氧饱和度与心血管舒张。',
    content: '<ul><li><strong>高气压（&gt;1015 hPa）</strong>：通常伴随晴空与稳定气流，人体血氧充足、精力集中，适宜户外出行。</li><li><strong>常压（1000 hPa - 1015 hPa）</strong>：气压处于平和状态，人体体感舒适，生理指标处于常态。</li><li><strong>低气压（&lt;1000 hPa）</strong>：通常伴随阴雨连绵或风暴，易导致胸闷、惰性与心血管负荷增加，需保持室内通风。</li></ul>'
  },
  {
    id: 'wind-mind',
    title: '风速与风向：大气的流动与能量迁移',
    category: 'metric',
    icon: '💨',
    summary: '风是空气流动的轨迹，体现了大气热量与湿度的循环和输送。',
    content: '<ul><li><strong>微风（&lt;12 km/h）</strong>：空气轻盈流动，体感舒适，能有效散热，是最适宜户外活动的风速。</li><li><strong>和风（12-24 km/h）</strong>：代表大气适度对流，能加速湿热扩散，但需防范局部天气转变。</li><li><strong>大风（&gt;25 km/h）</strong>：风力强劲，可能带来气温骤降，需注意加固门窗，出行时避免在临时广告牌或高大建筑物下逗留。</li></ul>'
  },
  {
    id: 'solstice-energy',
    title: '二至二分：天体运行与节气交替',
    category: 'cycle',
    icon: '📅',
    summary: '春分、夏至、秋分、冬至是太阳直射点变化的重要分界线，主导了地表季节的自然大循环。',
    content: '<ul><li><strong>春分 / 秋分</strong>：太阳直射赤道，全球昼夜平分。春分时气候回暖，万物复苏；秋分时天高气爽，冷暖交替，迎来秋收。</li><li><strong>夏至</strong>：太阳直射北回归线，北半球白昼最长，代表阳气达到顶点，气温最高，需注意防暑避烈日。</li><li><strong>冬至</strong>：太阳直射南回归线，北半球黑夜最长，气温降至全年低位，代表寒冬来临，需强化御寒保暖。</li></ul>'
  },
  {
    id: 'divination-base',
    title: '气象科普的核心原则：天人感应与生活指南',
    category: 'theory',
    icon: '💡',
    summary: '气象与人居环境密切相关，是通过大数据气象参数服务人类的智能共鸣系统。',
    content: '<ul><li><strong>物理观测</strong>：通过气象雷达、传感器和气象卫星，精准获取温度、湿度、气压和风速等核心大气物理参数。</li><li><strong>指数转化</strong>：将基础观测数据转化为与人体感官、出行安全直接关联的舒适度指数、紫外线指数和穿衣指南。</li><li><strong>决策辅助</strong>：利用智能预测模型和历史气象大数据，为农业生产、防灾减灾以及日常出行提供科学的决策支持。</li></ul>'
  }
]

function getCategoryLabel(val: string) {
  return categories.find(c => c.value === val)?.label || val
}

const filteredArticles = computed(() => {
  return articles.filter(art => {
    // Category filter
    if (activeCategory.value !== 'all' && art.category !== activeCategory.value) {
      return false
    }
    return true
  })
})
</script>

<style scoped>
.knowledge-base-page {
  padding: 12px 0;
  display: flex;
  flex-direction: column;
  gap: 32px;
  max-width: 860px;
  margin: 0 auto;
  width: 100%;
}

/* Hero Section */
.kb-hero {
  padding: 24px 0 32px 0;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  border-bottom: 1px solid var(--oracle-border-soft);
}

.kb-hero h1 {
  font-family: var(--oracle-font-serif);
  font-size: 36px;
  color: var(--oracle-text);
  margin: 0;
  letter-spacing: 0.05em;
}

.kb-hero-desc {
  color: var(--oracle-faint);
  font-size: 14.5px;
  line-height: 1.6;
  max-width: 720px;
  margin: 0;
}

/* Category Filter Buttons */
.kb-categories {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 10px;
}

.kb-cat-btn {
  padding: 6px 16px;
  border-radius: 20px;
  border: 1px solid var(--oracle-border-soft);
  background: var(--oracle-panel-soft);
  color: var(--oracle-faint);
  font-size: 12.5px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.kb-cat-btn:hover {
  color: var(--oracle-text);
  border-color: var(--oracle-border);
}

.kb-cat-btn.active {
  color: var(--oracle-gold-strong);
  background: rgba(215, 174, 105, 0.08);
  border-color: var(--oracle-gold);
}

/* Article List */
.kb-list {
  display: flex;
  flex-direction: column;
  gap: 28px;
  margin-top: 12px;
}

.kb-article-item {
  padding-bottom: 28px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  border-bottom: 1px solid var(--oracle-border-soft);
}

.kb-article-item:last-child {
  border-bottom: none;
}

.article-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 12px;
}

.article-title-wrap {
  display: flex;
  align-items: center;
  gap: 8px;
}

.article-icon {
  font-size: 24px;
}

.kb-article-item h3 {
  font-family: var(--oracle-font-serif);
  color: var(--oracle-text);
  font-size: 20px;
  margin: 0;
  letter-spacing: 0.02em;
}

.article-badges {
  display: flex;
  align-items: center;
  gap: 8px;
}

.article-category-badge {
  font-size: 10px;
  border: 1px solid var(--oracle-border-soft);
  padding: 2px 8px;
  border-radius: 10px;
  color: var(--oracle-gold);
  background: var(--oracle-panel-soft);
  font-weight: 600;
}

.article-summary {
  color: var(--oracle-muted);
  font-size: 13.5px;
  line-height: 1.5;
  margin: 0;
  border-left: 2px solid var(--oracle-border-soft);
  padding-left: 10px;
}

.article-content {
  color: var(--oracle-faint);
  font-size: 14.5px;
  line-height: 1.7;
}

.article-content :deep(ul) {
  padding-left: 20px;
  margin: 8px 0;
}

.article-content :deep(li) {
  margin-bottom: 6px;
}

/* Empty State */
.kb-empty {
  text-align: center;
  padding: 40px 20px;
  color: var(--oracle-muted);
}

.empty-icon {
  font-size: 36px;
  display: block;
  margin-bottom: 12px;
}

/* Animations */
.list-fade-enter-active,
.list-fade-leave-active {
  transition: all 0.25s ease;
}

.list-fade-enter-from,
.list-fade-leave-to {
  opacity: 0;
  transform: translateY(8px);
}

@media (max-width: 768px) {
  .kb-hero {
    padding: 20px 0 24px 0;
  }
  .kb-hero h1 {
    font-size: 28px;
  }
  .article-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
}
</style>
