<template>
  <section class="mood-guide-panel">
    <span class="oracle-eyebrow">情绪状态指南</span>
    <h2>{{ guide.title }}</h2>
    <p>{{ guide.analysis }}</p>
    <ul>
      <li v-for="item in guide.suggestions" :key="item">{{ item }}</li>
    </ul>
  </section>
</template>

<script setup lang="ts">
import type { WeatherOracleMoodGuide } from '../../types/weatherOracle'

defineProps<{ guide: WeatherOracleMoodGuide }>()
</script>

<style scoped>
.mood-guide-panel {
  display: grid;
  align-content: start;
  gap: 13px;
  min-width: 0;
  padding: 22px;
  border: 1px solid var(--oracle-border);
  border-radius: 8px;
  background:
    linear-gradient(135deg, rgba(168, 138, 223, 0.12), transparent 45%),
    var(--oracle-panel);
  box-shadow: var(--oracle-shadow);
}

.mood-guide-panel h2 {
  margin: 0;
  color: var(--oracle-text);
  font-size: 24px;
}

.mood-guide-panel p {
  margin: 0;
  color: var(--oracle-faint);
  line-height: 1.8;
  overflow-wrap: anywhere;
}

.mood-guide-panel ul {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin: 0;
  padding: 0;
  color: var(--oracle-text);
  list-style: none;
}

.mood-guide-panel li {
  max-width: 100%;
  padding: 9px 11px;
  border: 1px solid var(--oracle-border-soft);
  border-radius: 8px;
  background: var(--oracle-panel-soft);
  color: var(--oracle-text);
  font-size: 14px;
  overflow-wrap: anywhere;
}

@media (max-width: 560px) {
  .mood-guide-panel {
    padding: 18px;
  }
}
</style>
