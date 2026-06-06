<template>
  <section class="weather-metric-grid">
    <article v-for="item in mappings" :key="item.metric">
      <span>{{ item.label }}</span>
      <strong>{{ item.value }}</strong>
      <p>{{ item.reading }}</p>
      <meter min="0" max="100" :value="item.score" />
    </article>
  </section>
</template>

<script setup lang="ts">
import type { WeatherOracleMapping } from '../../types/weatherOracle'

defineProps<{ mappings: WeatherOracleMapping[] }>()
</script>

<style scoped>
.weather-metric-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
  min-width: 0;
}

.weather-metric-grid article {
  display: grid;
  gap: 9px;
  min-height: 148px;
  min-width: 0;
  padding: 16px;
  border: 1px solid var(--oracle-border);
  border-radius: 8px;
  background: var(--oracle-panel);
  box-shadow: var(--oracle-shadow);
}

.weather-metric-grid span {
  color: var(--oracle-muted);
  font-size: 13px;
  font-weight: 700;
}

.weather-metric-grid strong {
  color: var(--oracle-text);
  font-size: 25px;
  line-height: 1.05;
  overflow-wrap: anywhere;
}

.weather-metric-grid p {
  margin: 0;
  color: var(--oracle-faint);
  font-size: 14px;
  line-height: 1.6;
  overflow-wrap: anywhere;
}

.weather-metric-grid meter {
  width: 100%;
  height: 10px;
  align-self: end;
  accent-color: var(--oracle-purple);
}

.weather-metric-grid meter::-webkit-meter-bar {
  border: 0;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.08);
}

.weather-metric-grid meter::-webkit-meter-optimum-value {
  border-radius: 999px;
  background: linear-gradient(90deg, var(--oracle-purple), var(--oracle-gold));
}

@media (max-width: 620px) {
  .weather-metric-grid {
    grid-template-columns: 1fr;
  }
}
</style>
