<template>
  <section class="tarot-card-display">
    <img
      v-if="tarot.image && !imageFailed"
      :src="tarot.image"
      :alt="tarot.name_zh || tarot.name_en || tarot.id"
      @error="imageFailed = true"
    />
    <div v-else class="tarot-card-fallback" aria-hidden="true">
      <span>{{ fallbackInitial }}</span>
    </div>
    <div class="tarot-card-copy">
      <span>今日天气塔罗牌</span>
      <h2>{{ tarot.name_zh || tarot.name_en || tarot.id }}</h2>
      <p>{{ tarot.keywords.join(' · ') }}</p>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import type { WeatherOracleTarot } from '../../types/weatherOracle'

const props = defineProps<{ tarot: WeatherOracleTarot }>()
const imageFailed = ref(false)

const fallbackInitial = computed(() => {
  const label = props.tarot.name_zh || props.tarot.name_en || props.tarot.id
  return label.charAt(0).toUpperCase()
})

watch(
  () => props.tarot.image,
  () => {
    imageFailed.value = false
  },
)
</script>

<style scoped>
.tarot-card-display {
  display: grid;
  grid-template-columns: minmax(120px, 180px) 1fr;
  gap: 24px;
  align-items: center;
  padding: 24px;
  border-radius: 18px;
  background: rgba(255, 255, 255, 0.72);
  box-shadow: 0 20px 50px rgba(31, 41, 55, 0.12);
}

.tarot-card-display img,
.tarot-card-fallback {
  width: 100%;
  aspect-ratio: 2 / 3;
  border-radius: 14px;
  object-fit: cover;
  background: linear-gradient(160deg, #233047, #6c5b7b 52%, #f8b195);
  box-shadow: 0 14px 30px rgba(31, 41, 55, 0.22);
}

.tarot-card-fallback {
  display: grid;
  place-items: center;
  color: #fff;
  font-size: 48px;
  font-weight: 700;
}

.tarot-card-copy {
  display: grid;
  gap: 10px;
}

.tarot-card-copy span {
  font-size: 13px;
  color: #6b7280;
}

.tarot-card-copy h2 {
  margin: 0;
  color: #111827;
  font-size: 30px;
  line-height: 1.15;
}

.tarot-card-copy p {
  margin: 0;
  color: #374151;
  line-height: 1.7;
}

@media (max-width: 720px) {
  .tarot-card-display {
    grid-template-columns: 1fr;
  }

  .tarot-card-display img,
  .tarot-card-fallback {
    max-width: 180px;
  }
}
</style>
