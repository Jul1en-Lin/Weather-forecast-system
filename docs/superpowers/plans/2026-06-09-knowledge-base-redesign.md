# Knowledge Base Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Modify the Knowledge Base page to remove the search input box and floating card layout/effects, rendering a clean, text-based typography layout and adding copy emphasizing that these definitions serve as the model's built-in knowledge base context.

**Architecture:** Remove search input, filter state, and template tags. Refactor the grid into a single-column typographic layout using CSS variables, removing the card panels, border shadows, and floating hover effects. Update the description/header to state its functional integration with the AI model.

**Tech Stack:** Vue 3, CSS (oracle-theme.css variables)

---

### Task 1: Refactor Template & Script in KnowledgeBase.vue

**Files:**
- Modify: `src/views/KnowledgeBase.vue`

- [ ] **Step 1: Remove the search query state and simplify filter logic in `<script setup>`**
  - Delete `searchQuery` ref.
  - Simplify `filteredArticles` computed property to only filter by `activeCategory`.

```typescript
const activeCategory = ref<'all' | 'metric' | 'cycle' | 'theory'>('all')

const categories: { label: string; value: 'all' | 'metric' | 'cycle' | 'theory' }[] = [
  { label: '全部知识', value: 'all' },
  { label: '气象要素科普', value: 'metric' },
  { label: '岁时节气规律', value: 'cycle' },
  { label: '气象科普理论', value: 'theory' },
]

// ... (keep articles array as is)

const filteredArticles = computed(() => {
  return articles.filter(art => {
    // Category filter
    if (activeCategory.value !== 'all' && art.category !== activeCategory.value) {
      return false
    }
    return true
  })
})
```

- [ ] **Step 2: Update HTML template structure**
  - Remove `oracle-surface oracle-gold-corners anim-float` classes from the hero `<section class="kb-hero">`.
  - Update hero description to emphasize the built-in model knowledge base.
  - Remove the search container `<div class="kb-search-container">` completely.
  - Replace `.kb-grid` and `.kb-article-card` with `.kb-list` and `.kb-article-item`. Remove the card design class `oracle-surface`.
  - Add a sub-badge or explicit line stating `内置知识库` in the article layout.

```html
<template>
  <OracleLayout>
    <div class="knowledge-base-page">
      <!-- Header Section -->
      <section class="kb-hero">
        <span class="oracle-eyebrow">Model Built-in Knowledge Base</span>
        <h1>模型内置气象知识库</h1>
        <p class="kb-hero-desc">
          以下气象科普常识作为模型内置知识库，直接嵌入大语言模型的系统提示词中，用作天气助手与智能问答的常识检索、推理参考及事实比对依据。
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
                <span class="article-builtin-badge">内置常识</span>
              </div>
            </header>
            
            <p class="article-summary">{{ article.summary }}</p>
            <div class="article-content" v-html="article.content"></div>
            
            <footer class="article-footer">
              <span class="article-meta">对应牌面：<strong>{{ article.tarot }}</strong></span>
            </footer>
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
```

---

### Task 2: Refactor Scoped CSS Styles in KnowledgeBase.vue

**Files:**
- Modify: `src/views/KnowledgeBase.vue`

- [ ] **Step 1: Replace styles in `<style scoped>`**
  - Replace search styles and grid styles with the clean text list styling.
  - Remove any hover scale or translate effects, shadows, card borders.
  - Simplify category active button styling to avoid floating card/shadow effects.

```css
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

.article-builtin-badge {
  font-size: 10px;
  border: 1px solid rgba(215, 174, 105, 0.2);
  padding: 2px 8px;
  border-radius: 10px;
  color: var(--oracle-text);
  background: rgba(215, 174, 105, 0.05);
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

.article-footer {
  font-size: 12px;
  color: var(--oracle-muted);
}

.article-footer strong {
  color: var(--oracle-gold);
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
  .article-badges {
    align-self: flex-start;
  }
}
</style>
```

---

### Task 3: Verify the Changes & Compilation

- [ ] **Step 1: Check Vite Compilation**
  - Run: `npm run build`
  - Expected: Clean compilation with zero type errors.

- [ ] **Step 2: Check Backend Tests**
  - Run: `venv/bin/python -m pytest tests -q` (or `python -m pytest` inside `backend/` directory)
  - Expected: All backend tests pass successfully.

- [ ] **Step 3: Commit Changes**
  - Run:
  ```bash
  git add src/views/KnowledgeBase.vue docs/project_status.md
  git commit -m "style: remove search and card design from knowledge base view, styling as model built-in text list"
  ```
