<template>
  <section class="mood-guide-panel-card oracle-surface oracle-gold-corners">
    <div class="mood-card-header">
      <span class="oracle-eyebrow">Mood & Activity Guide</span>
      <h3 class="mood-card-title">今日情绪状态指南</h3>
    </div>

    <div class="mood-grid-layout">
      <!-- Left side: Quote bubble -->
      <div class="mood-quote-side">
        <div class="quote-bubble">
          <span class="quote-mark open">“</span>
          <p class="quote-text">{{ guide.analysis }}</p>
          <span class="quote-mark close">”</span>
        </div>
      </div>

      <!-- Right side: Suggestion checklist -->
      <div class="mood-checklist-side">
        <ul class="suggestions-list">
          <li v-for="item in guide.suggestions" :key="item" class="suggestion-item">
            <span class="checklist-bullet">
              <svg viewBox="0 0 24 24" width="14" height="14">
                <path fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" d="M20 6L9 17l-5-5" />
              </svg>
            </span>
            <span class="suggestion-text">{{ item }}</span>
          </li>
        </ul>

        <!-- Coffee Cup SVG Decoration -->
        <div class="coffee-cup-decoration anim-float">
          <svg viewBox="0 0 24 24" width="48" height="48" class="coffee-svg">
            <path fill="var(--oracle-gold)" opacity="0.15" d="M2 21h18v-2H2v2z" />
            <path fill="currentColor" d="M2 19h16v-6H2v6zm14-10H2v2h14V9zm4 2c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2h-2v10h2c1.1 0 2-.9 2-2zm-2-6h2v4h-2V5zm-4-3c-1.1 0-2 .9-2 2v2h2V4c0-.55-.45-1-1-1z" />
            <!-- Steam lines -->
            <path d="M6 6c.55 0 1-.45 1-1V3c0-.55-.45-1-1-1s-1 .45-1 1v2c0 .55.45 1 1 1zm4 0c.55 0 1-.45 1-1V3c0-.55-.45-1-1-1s-1 .45-1 1v2c0 .55.45 1 1 1z" fill="var(--oracle-gold)" class="steam-line" />
          </svg>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import type { WeatherOracleMoodGuide } from '../../types/weatherOracle'

defineProps<{ guide: WeatherOracleMoodGuide }>()
</script>

<style scoped>
.mood-guide-panel-card {
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.mood-card-header {
  display: flex;
  flex-direction: column;
  gap: 4px;
  border-bottom: 1px solid var(--oracle-border-soft);
  padding-bottom: 12px;
}

.mood-card-title {
  font-family: var(--oracle-font-serif);
  font-size: 20px;
  color: var(--oracle-text);
  margin: 4px 0 0 0;
  letter-spacing: 0.02em;
}

/* Grid Layout */
.mood-grid-layout {
  display: grid;
  grid-template-columns: 1.1fr 0.9fr;
  gap: 32px;
  align-items: center;
}

/* Quote Bubble on the Left */
.mood-quote-side {
  position: relative;
}

.quote-bubble {
  background: var(--oracle-panel-soft);
  border: 1px solid var(--oracle-border-soft);
  border-radius: var(--oracle-radius-inner);
  padding: 24px 32px;
  position: relative;
  box-shadow: inset 0 0 15px rgba(215, 174, 105, 0.03);
}

.quote-bubble::after {
  content: '';
  position: absolute;
  top: 50%;
  right: -10px;
  transform: translateY(-50%) rotate(45deg);
  width: 20px;
  height: 20px;
  background: var(--oracle-panel-soft);
  border-right: 1px solid var(--oracle-border-soft);
  border-top: 1px solid var(--oracle-border-soft);
  pointer-events: none;
}

.quote-mark {
  font-family: var(--oracle-font-serif);
  font-size: 40px;
  color: var(--oracle-gold);
  line-height: 1;
  position: absolute;
  opacity: 0.3;
}

.quote-mark.open {
  top: 6px;
  left: 10px;
}

.quote-mark.close {
  bottom: -16px;
  right: 14px;
}

.quote-text {
  color: var(--oracle-faint);
  font-size: 14px;
  line-height: 1.8;
  margin: 0;
  font-family: var(--oracle-font-serif);
  font-style: italic;
}

/* Checklist on the Right */
.mood-checklist-side {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  padding-left: 8px;
}

.suggestions-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 12px;
  flex: 1;
}

.suggestion-item {
  display: flex;
  align-items: center;
  gap: 12px;
}

.checklist-bullet {
  width: 22px;
  height: 22px;
  border-radius: 50%;
  border: 1px solid var(--oracle-border);
  background: var(--oracle-panel-soft);
  color: var(--oracle-gold);
  display: grid;
  place-items: center;
  flex-shrink: 0;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}

.suggestion-text {
  font-size: 13.5px;
  color: var(--oracle-text);
  font-weight: 600;
  line-height: 1.3;
}

/* Coffee Cup Graphic */
.coffee-cup-decoration {
  flex-shrink: 0;
  color: var(--oracle-gold);
  opacity: 0.85;
  padding-right: 8px;
}

.coffee-svg {
  filter: drop-shadow(0 0 6px var(--oracle-gold-glow));
}

@keyframes steam {
  0%, 100% {
    transform: translateY(0) scaleY(1);
    opacity: 0.4;
  }
  50% {
    transform: translateY(-2px) scaleY(1.1);
    opacity: 0.8;
  }
}

.steam-line {
  animation: steam 2.5s ease-in-out infinite;
  transform-origin: bottom;
}

.steam-line:nth-child(2) {
  animation-delay: 1.2s;
}

/* Responsive Styles */
@media (max-width: 900px) {
  .mood-grid-layout {
    grid-template-columns: 1fr;
    gap: 24px;
  }

  .quote-bubble::after {
    top: auto;
    bottom: -10px;
    left: 30px;
    right: auto;
    transform: rotate(135deg);
  }

  .mood-checklist-side {
    padding-left: 0;
    margin-top: 10px;
  }
}
</style>
