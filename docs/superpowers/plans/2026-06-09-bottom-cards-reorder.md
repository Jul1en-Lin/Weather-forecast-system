# Bottom Cards Layout and Links Refactoring Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Modify the bottom cards layout in `OracleBottomCards.vue`. Remove the redirection links to the knowledge base from the "生活气象指数" (Life Weather Index) and "出行建议" (Travel Advisory) cards, and swap the positions of the "出行建议" card and "天气签文" (Weather Verse Scroll) card.

**Architecture:** Edit `OracleBottomCards.vue` template structure to reorder the nodes and remove the targeted `<router-link>` tags.

**Tech Stack:** Vue 3, HTML

---

### Task 1: Modify HTML Template in OracleBottomCards.vue

**Files:**
- Modify: `src/components/oracle/OracleBottomCards.vue`

- [ ] **Step 1: Edit the template layout in OracleBottomCards.vue**
  - Locate `<div class="oracle-bottom-cards-row">`.
  - In Card 1 (生活气象指数), delete:
  ```html
  <router-link to="/knowledge-base" class="card-link-footer">查看详情 →</router-link>
  ```
  - Swap Card 2 (天气签文) and Card 3 (出行建议) blocks.
  - In Card 3 (now Card 2, 出行建议), delete:
  ```html
  <router-link to="/knowledge-base" class="card-link-footer">获取更多建议 →</router-link>
  ```

Here is the targeted template structure:

```html
<template>
  <div class="oracle-bottom-cards-row">
    <!-- Card 1: Daily ratings -->
    <div class="oracle-bottom-card oracle-surface oracle-gold-corners">
      <span class="oracle-eyebrow">Life Weather Index</span>
      <h4 class="card-title">
        <span class="card-icon">🌡️</span> 生活气象指数
      </h4>
      <div class="ratings-list">
        <div class="rating-row">
          <span class="rating-label">穿衣指数</span>
          <span class="stars-wrap">{{ getStarsString(overallRating) }}</span>
        </div>
        <div class="rating-row">
          <span class="rating-label">运动指数</span>
          <span class="stars-wrap">{{ getStarsString(loveRating) }}</span>
        </div>
        <div class="rating-row">
          <span class="rating-label">紫外线指数</span>
          <span class="stars-wrap">{{ getStarsString(wealthRating) }}</span>
        </div>
      </div>
    </div>

    <!-- Card 2: Travel Advisory -->
    <div class="oracle-bottom-card oracle-surface oracle-gold-corners">
      <span class="oracle-eyebrow">Travel Advisory</span>
      <h4 class="card-title">
        <span class="card-icon">☂️</span> 出行建议
      </h4>
      <p class="tip-content-text">
        晴天外出注意防晒与补水，雨天出行备好雨具并减速慢行。关注温差适度增减衣物。
      </p>
    </div>

    <!-- Card 3: Weather Verse Scroll -->
    <div class="oracle-bottom-card oracle-surface oracle-gold-corners">
      <span class="oracle-eyebrow">Weather Verse</span>
      <h4 class="card-title">
        <span class="card-icon">📜</span> 天气签文
      </h4>
      <p class="verse-content-text">
        “{{ currentVerse }}”
      </p>
      <div class="verse-action-footer">
        <button type="button" class="change-verse-btn" @click="rotateVerse">
          换一签 🔄
        </button>
      </div>
    </div>

    <!-- Card 4: Knowledge Base Recommend -->
    <div class="oracle-bottom-card oracle-surface oracle-gold-corners">
      <span class="oracle-eyebrow">Recommended Readings</span>
      <h4 class="card-title">
        <span class="card-icon">📚</span> 知识库推荐
      </h4>
      <ul class="rec-links-list">
        <li>
          <router-link to="/knowledge-base" class="rec-link-item">📖 常见天气符号解读</router-link>
        </li>
        <li>
          <router-link to="/knowledge-base" class="rec-link-item">📖 气象灾害防御指南</router-link>
        </li>
        <li>
          <router-link to="/knowledge-base" class="rec-link-item">📖 天气预报入门知识</router-link>
        </li>
      </ul>
      <router-link to="/knowledge-base" class="card-link-footer">进入知识库 →</router-link>
    </div>
  </div>
</template>
```

---

### Task 2: Verify & Build

- [ ] **Step 1: Check Vite Compilation**
  - Run: `npm run build`
  - Expected: Clean build with zero errors.

- [ ] **Step 2: Check Backend Tests**
  - Run: `PYTHONPATH=. venv/bin/pytest tests -q` inside `backend/`
  - Expected: All tests pass.

- [ ] **Step 3: Commit changes**
  - Run:
  ```bash
  git add src/components/oracle/OracleBottomCards.vue docs/project_status.md
  git commit -m "style: remove bottom cards footer links and swap weather verse with travel advisory"
  ```
