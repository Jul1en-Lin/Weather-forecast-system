<template>
  <form class="quick-city-picker" @submit.prevent="submitCity">
    <label for="oracle-city">城市</label>
    <div class="city-input-row">
      <input
        id="oracle-city"
        v-model.trim="draftCity"
        type="text"
        placeholder="输入城市，例如上海"
        :disabled="loading"
      />
      <button type="submit" :disabled="!draftCity || loading">
        {{ loading ? '抽取中' : '抽取' }}
      </button>
    </div>
    <div class="quick-cities" aria-label="常用城市">
      <button
        v-for="city in cities"
        :key="city"
        type="button"
        :disabled="loading"
        @click="chooseCity(city)"
      >
        {{ city }}
      </button>
    </div>
  </form>
</template>

<script setup lang="ts">
import { ref } from 'vue'

defineProps<{ loading?: boolean }>()

const emit = defineEmits<{ draw: [city: string] }>()
const cities = ['上海', '北京', '杭州', '广州', '深圳', '成都', '南京', '武汉']
const draftCity = ref('')

function submitCity() {
  if (draftCity.value) emit('draw', draftCity.value)
}

function chooseCity(city: string) {
  draftCity.value = city
  emit('draw', city)
}
</script>

<style scoped>
.quick-city-picker {
  display: grid;
  gap: 12px;
  width: min(100%, 460px);
  min-width: min(100%, 360px);
}

.quick-city-picker label {
  font-size: 14px;
  font-weight: 700;
  color: var(--oracle-gold-strong);
}

.city-input-row {
  display: flex;
  gap: 10px;
}

.city-input-row input {
  min-width: 0;
  flex: 1;
  height: 44px;
  border: 1px solid var(--oracle-border);
  border-radius: 8px;
  padding: 0 14px;
  background: var(--oracle-panel-soft);
  color: var(--oracle-text);
  font-size: 15px;
}

.city-input-row input::placeholder {
  color: var(--oracle-muted);
}

.city-input-row button,
.quick-cities button {
  border: 1px solid var(--oracle-border-soft);
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 700;
  transition: border-color 0.2s ease, background-color 0.2s ease, color 0.2s ease;
}

.city-input-row button {
  min-width: 88px;
  height: 44px;
  border-color: var(--oracle-border);
  background: linear-gradient(135deg, var(--oracle-gold), var(--oracle-gold-strong));
  color: #141015;
}

.city-input-row button:not(:disabled):hover,
.quick-cities button:not(:disabled):hover {
  border-color: var(--oracle-gold);
  background: rgba(215, 174, 105, 0.16);
  color: var(--oracle-gold-strong);
}

.city-input-row button:disabled,
.quick-cities button:disabled {
  cursor: not-allowed;
  opacity: 0.55;
}

.quick-cities {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.quick-cities button {
  padding: 8px 12px;
  background: var(--oracle-panel-soft);
  color: var(--oracle-text);
}

@media (max-width: 560px) {
  .quick-city-picker {
    min-width: 0;
  }

  .city-input-row {
    display: grid;
    grid-template-columns: minmax(0, 1fr) 78px;
  }

  .city-input-row button {
    min-width: 0;
  }
}
</style>
