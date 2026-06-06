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
      <small>牌面待导出</small>
    </div>
    <div class="tarot-card-copy">
      <span class="oracle-eyebrow">今日天气塔罗牌</span>
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
  align-content: start;
  gap: 18px;
  min-width: 0;
  padding: 22px;
  border: 1px solid var(--oracle-border);
  border-radius: 8px;
  background:
    linear-gradient(180deg, rgba(215, 174, 105, 0.1), transparent 32%),
    var(--oracle-panel);
  box-shadow: var(--oracle-shadow);
}

.tarot-card-display img,
.tarot-card-fallback {
  width: 100%;
  max-width: 278px;
  aspect-ratio: 2 / 3;
  justify-self: center;
  border: 1px solid var(--oracle-border);
  border-radius: 8px;
  object-fit: cover;
  background:
    linear-gradient(180deg, rgba(246, 234, 216, 0.12), transparent 34%),
    linear-gradient(160deg, #0f1c31, #26395b 48%, #6b5435);
  box-shadow: 0 18px 34px rgba(0, 0, 0, 0.32);
}

.tarot-card-fallback {
  display: grid;
  align-content: center;
  place-items: center;
  gap: 10px;
  color: var(--oracle-text);
  font-size: 48px;
  font-weight: 800;
}

.tarot-card-fallback small {
  color: var(--oracle-muted);
  font-size: 13px;
  font-weight: 700;
}

.tarot-card-copy {
  display: grid;
  gap: 10px;
}

.tarot-card-copy h2 {
  margin: 0;
  color: var(--oracle-text);
  font-size: clamp(26px, 3vw, 34px);
  line-height: 1.15;
}

.tarot-card-copy p {
  margin: 0;
  color: var(--oracle-faint);
  line-height: 1.7;
  overflow-wrap: anywhere;
}

@media (max-width: 1280px) {
  .tarot-card-display {
    align-content: center;
  }
}

@media (max-width: 560px) {
  .tarot-card-display {
    padding: 18px;
  }

  .tarot-card-display img,
  .tarot-card-fallback {
    max-width: 210px;
  }
}
</style>
