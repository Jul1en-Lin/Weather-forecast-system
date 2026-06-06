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
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 14px;
}

.weather-metric-grid article {
  display: grid;
  gap: 8px;
  min-height: 160px;
  padding: 18px;
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.72);
}

.weather-metric-grid span {
  color: #6b7280;
  font-size: 13px;
}

.weather-metric-grid strong {
  color: #111827;
  font-size: 24px;
}

.weather-metric-grid p {
  margin: 0;
  color: #374151;
  font-size: 14px;
  line-height: 1.6;
}

.weather-metric-grid meter {
  width: 100%;
  height: 10px;
  align-self: end;
}

@media (max-width: 1100px) {
  .weather-metric-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 620px) {
  .weather-metric-grid {
    grid-template-columns: 1fr;
  }
}
</style>
