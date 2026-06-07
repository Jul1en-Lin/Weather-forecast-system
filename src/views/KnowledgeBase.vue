<template>
  <OracleLayout>
    <div class="knowledge-base-page">
      <!-- Header Section -->
      <section class="kb-hero oracle-surface oracle-gold-corners anim-float">
        <span class="oracle-eyebrow">Weather Wisdom</span>
        <h1>气象占卜知识库</h1>
        <p>探索天气要素、气相星曜与人类情绪、命运脉络的隐秘联系。在这里，科学数据转化为心灵启示。</p>

        <!-- Search bar -->
        <div class="kb-search-container">
          <span class="search-icon">🔍</span>
          <input
            v-model="searchQuery"
            type="text"
            placeholder="搜寻气压、温度、二十四节气或塔罗映射..."
            class="kb-search-input"
          />
        </div>
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

      <!-- Article Grid -->
      <div class="kb-grid">
        <transition-group name="grid-fade">
          <article
            v-for="article in filteredArticles"
            :key="article.id"
            class="kb-article-card oracle-surface"
          >
            <div class="article-icon-wrap">
              <span class="article-icon">{{ article.icon }}</span>
              <span class="article-category-badge">{{ getCategoryLabel(article.category) }}</span>
            </div>
            <h3>{{ article.title }}</h3>
            <p class="article-summary">{{ article.summary }}</p>
            <div class="oracle-divider"></div>
            <div class="article-content" v-html="article.content"></div>
            <div class="article-footer">
              <span class="article-meta">对应牌面：<strong>{{ article.tarot }}</strong></span>
            </div>
          </article>
        </transition-group>
      </div>

      <div v-if="filteredArticles.length === 0" class="kb-empty">
        <span class="empty-icon">🔮</span>
        <p>未找到相关的星象学识，换个词试试看吧。</p>
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
  tarot: string
}

const searchQuery = ref('')
const activeCategory = ref<'all' | 'metric' | 'cycle' | 'theory'>('all')

const categories: { label: string; value: 'all' | 'metric' | 'cycle' | 'theory' }[] = [
  { label: '全部知识', value: 'all' },
  { label: '气象要素隐喻', value: 'metric' },
  { label: '岁时节气能量', value: 'cycle' },
  { label: '占卜基础理论', value: 'theory' },
]

const articles: Article[] = [
  {
    id: 'temp-metaphor',
    title: '气温的命运隐喻：生命的寒暑刻度',
    category: 'metric',
    icon: '🌡️',
    summary: '温度是外界环境对生命的包容度。在占卜中，它直接投射个人的热情、安全感与表达欲。',
    content: '<ul><li><strong>极寒（&lt;0°C）</strong>：对应塔罗‘隐士’或‘死神’，代表能量收敛、深度自我反思与蛰伏。</li><li><strong>舒适（20°C-25°C）</strong>：对应‘星辰’或‘皇后’，暗示万物繁茂、情绪松弛与灵感涌现。</li><li><strong>酷暑（&gt;35°C）</strong>：对应‘战车’或‘塔’，表明意志力高度紧绷、情绪容易宣泄，属于爆发性相。</li></ul>',
    tarot: '皇后 & 战车'
  },
  {
    id: 'humidity-emotion',
    title: '湿度的情绪共鸣：潜意识的活跃程度',
    category: 'metric',
    icon: '💧',
    summary: '水分是直觉与情感的载体。湿度的高低，决定了潜意识直觉的折射能力。',
    content: '当湿度偏高（&gt;75%）时，空气充满感性因子，对应‘女祭司’与‘圣杯’牌组。此时人会更加敏感、富有同情心，适合进行艺术创作或心理疗愈。反之，干燥（&lt;35%）则带来理性、敏捷与利落（对应‘宝剑’），利于逻辑思考与边界建立。',
    tarot: '女祭司 (The High Priestess)'
  },
  {
    id: 'pressure-will',
    title: '气压与秩序张力：掌控感与外界阻力',
    category: 'metric',
    icon: '🌀',
    summary: '气压是无形物质投射在万物上的负荷，反映了个人承受现实压力与掌控周遭的能力。',
    content: '高气压（&gt;1015 hPa）对应‘皇帝’或‘正义’。高压环境下，精神集中，秩序井然，人们容易拥有掌控全局的自信。低气压（&lt;1000 hPa）则对应‘吊人’或‘恶魔’。气压降低常带来思绪的沉重、惰性与被迫顺应，此时宜于放下掌控欲，随遇而安。',
    tarot: '皇帝 (The Emperor)'
  },
  {
    id: 'wind-mind',
    title: '风速与风向：思维的信使与情绪迁移',
    category: 'metric',
    icon: '💨',
    summary: '风是空气流动的轨迹，象征思想在无形中的迁移与改变。',
    content: '微风如细碎的灵感之雨，激发创作欲；强风（风速&gt;25 km/h）对应‘愚者’或‘命运之轮’，代表着变化与冲刷旧观念。在方向上，<strong>东风</strong>代表开启（创造力），<strong>南风</strong>代表热忱（行动），<strong>西风</strong>代表情感共鸣，<strong>北风</strong>代表收割与沉静（智慧）。',
    tarot: '愚者 (The Fool)'
  },
  {
    id: 'solstice-energy',
    title: '二至二分：天球能量轴线的交替',
    category: 'cycle',
    icon: '📅',
    summary: '春分、秋分、夏至、冬至，是地球与太阳关系最显著的四个拐点，主导了地表能量的大循环。',
    content: '<ul><li><strong>春分</strong>：日夜平分，万物复苏，象征平衡与初始，对应‘魔术师’。</li><li><strong>夏至</strong>：白昼最长，阳气鼎盛，象征极致的绽放与繁盛，对应‘太阳’。</li><li><strong>秋分</strong>：收获与均分，冷暖交叠，代表反思与收敛，对应‘正义’。</li><li><strong>冬至</strong>：黑夜最长，万物归藏，代表转化、沉思与重生的希望，对应‘世界’。</li></ul>',
    tarot: '太阳 & 命运之轮'
  },
  {
    id: 'divination-base',
    title: '气象占卜的核心原则：天人感应与符号学',
    category: 'theory',
    icon: '🔮',
    summary: '气象占卜并非伪科学，而是一种基于大自然状态对个体意识影响的符号共鸣系统。',
    content: '占卜的本质是‘共时性’（Synchronicity）。通过现代传感器获取实时的温度、湿度、气压、风速，我们将这些物理参量转化为塔罗符号的权重，再利用自然语言模型将这些权重重构为人类能够理解的心灵隐喻。以天象知人心，顺天时以达人谋。',
    tarot: '命运之轮 (Wheel of Fortune)'
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
    // Search query filter
    if (searchQuery.value.trim() !== '') {
      const q = searchQuery.value.toLowerCase()
      return (
        art.title.toLowerCase().includes(q) ||
        art.summary.toLowerCase().includes(q) ||
        art.content.toLowerCase().includes(q) ||
        art.tarot.toLowerCase().includes(q)
      )
    }
    return true
  })
})
</script>

<style scoped>
.knowledge-base-page {
  padding: 12px 0;
  display: grid;
  gap: 32px;
}

/* Hero Section */
.kb-hero {
  padding: 40px 32px;
  background:
    linear-gradient(135deg, rgba(142, 110, 194, 0.08), transparent 60%),
    linear-gradient(225deg, rgba(215, 174, 105, 0.08), transparent 60%),
    var(--oracle-panel);
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}

.kb-hero h1 {
  font-family: var(--oracle-font-serif);
  font-size: 38px;
  color: var(--oracle-text);
  margin: 0;
  letter-spacing: 0.05em;
  text-shadow: 0 0 10px rgba(215, 174, 105, 0.1);
}

.kb-hero p {
  color: var(--oracle-faint);
  font-size: 15px;
  line-height: 1.6;
  max-width: 680px;
  margin: 0;
}

/* Search Bar */
.kb-search-container {
  display: flex;
  align-items: center;
  background: var(--oracle-panel-soft);
  border: 1px solid var(--oracle-border);
  border-radius: 30px;
  width: min(100%, 480px);
  padding: 4px 16px;
  margin-top: 10px;
  transition: all 0.3s ease;
}

.kb-search-container:focus-within {
  border-color: var(--oracle-gold);
  box-shadow: 0 0 15px var(--oracle-gold-glow);
  transform: translateY(-1px);
}

.search-icon {
  font-size: 16px;
  margin-right: 8px;
  color: var(--oracle-muted);
}

.kb-search-input {
  background: transparent;
  border: none;
  color: var(--oracle-text);
  font-size: 14px;
  height: 38px;
  width: 100%;
}

.kb-search-input::placeholder {
  color: var(--oracle-muted);
}

/* Category Filter Buttons */
.kb-categories {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 12px;
}

.kb-cat-btn {
  padding: 8px 20px;
  border-radius: 20px;
  border: 1px solid var(--oracle-border-soft);
  background: var(--oracle-panel-soft);
  color: var(--oracle-faint);
  font-size: 13px;
  font-weight: 600;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.kb-cat-btn:hover {
  color: var(--oracle-text);
  border-color: var(--oracle-border);
  background: var(--oracle-panel);
}

.kb-cat-btn.active {
  color: var(--oracle-gold-strong);
  background: linear-gradient(135deg, rgba(215, 174, 105, 0.12), rgba(142, 110, 194, 0.08));
  border-color: var(--oracle-gold);
  box-shadow: 0 4px 15px var(--oracle-gold-glow);
}

/* Article Grid */
.kb-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
  gap: 24px;
}

.kb-article-card {
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 14px;
  align-items: stretch;
}

.article-icon-wrap {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.article-icon {
  font-size: 28px;
  filter: drop-shadow(0 0 4px var(--oracle-gold-glow));
}

.article-category-badge {
  font-size: 10px;
  border: 1px solid var(--oracle-border-soft);
  padding: 3px 8px;
  border-radius: 12px;
  color: var(--oracle-gold);
  background: var(--oracle-panel-soft);
  font-weight: 600;
}

.kb-article-card h3 {
  font-family: var(--oracle-font-serif);
  color: var(--oracle-text);
  font-size: 18px;
  margin: 0;
  letter-spacing: 0.02em;
}

.article-summary {
  color: var(--oracle-muted);
  font-size: 13px;
  line-height: 1.5;
  margin: 0;
}

.article-content {
  color: var(--oracle-faint);
  font-size: 13.5px;
  line-height: 1.7;
}

.article-content :deep(ul) {
  padding-left: 20px;
  margin: 8px 0;
}

.article-content :deep(li) {
  margin-bottom: 6px;
}

.article-footer {
  margin-top: auto;
  font-size: 12px;
  color: var(--oracle-muted);
}

.article-footer strong {
  color: var(--oracle-gold);
}

/* Empty State */
.kb-empty {
  text-align: center;
  padding: 60px 20px;
  color: var(--oracle-muted);
}

.empty-icon {
  font-size: 40px;
  display: block;
  margin-bottom: 16px;
}

/* Animations */
.grid-fade-enter-active,
.grid-fade-leave-active {
  transition: all 0.3s ease;
}

.grid-fade-enter-from,
.grid-fade-leave-to {
  opacity: 0;
  transform: translateY(12px);
}

@media (max-width: 768px) {
  .kb-hero {
    padding: 30px 20px;
  }
  .kb-hero h1 {
    font-size: 28px;
  }
  .kb-grid {
    grid-template-columns: 1fr;
  }
}
</style>
