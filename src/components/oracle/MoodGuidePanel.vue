<template>
  <section class="mood-guide-panel">
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
  gap: 14px;
  padding: 24px;
  border-radius: 18px;
  background: rgba(255, 255, 255, 0.72);
}

.mood-guide-panel h2 {
  margin: 0;
  color: #111827;
  font-size: 24px;
}

.mood-guide-panel p {
  margin: 0;
  color: #374151;
  line-height: 1.8;
}

.mood-guide-panel ul {
  display: grid;
  gap: 10px;
  margin: 0;
  padding-left: 20px;
  color: #1f2937;
}
</style>
