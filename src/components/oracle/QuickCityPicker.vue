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
}

.quick-city-picker label {
  font-size: 14px;
  font-weight: 600;
  color: #1d1d1f;
}

.city-input-row {
  display: flex;
  gap: 10px;
}

.city-input-row input {
  min-width: 0;
  flex: 1;
  height: 44px;
  border: 1px solid rgba(0, 0, 0, 0.12);
  border-radius: 10px;
  padding: 0 14px;
  background: rgba(255, 255, 255, 0.78);
  color: #1d1d1f;
  font-size: 15px;
}

.city-input-row button,
.quick-cities button {
  border: 0;
  border-radius: 10px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
}

.city-input-row button {
  min-width: 88px;
  height: 44px;
  background: #1d1d1f;
  color: #fff;
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
  background: rgba(255, 255, 255, 0.72);
  color: #1d1d1f;
}
</style>
