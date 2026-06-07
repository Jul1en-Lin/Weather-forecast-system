<template>
  <div class="oracle-city-picker-wrapper" ref="dropdownRef">
    <!-- Trigger Button -->
    <button
      type="button"
      class="oracle-city-select-trigger"
      :disabled="loading"
      @click="toggleDropdown"
    >
      <span class="trigger-icon">📍</span>
      <span class="trigger-text">{{ loading ? '查询中' : currentCity || '选择城市' }}</span>
      <span class="trigger-arrow">▾</span>
    </button>

    <!-- Floating Dropdown Panel -->
    <transition name="fade-scale">
      <div v-if="isDropdownOpen" class="oracle-city-dropdown-panel oracle-surface oracle-gold-corners">
        <form class="city-search-form" @submit.prevent="submitSearch">
          <input
            v-model.trim="searchQuery"
            type="text"
            placeholder="输入城市，如上海"
            class="city-search-input"
            ref="searchInputRef"
          />
          <button type="submit" class="city-search-btn" :disabled="!searchQuery || loading">
            {{ loading ? '...' : '确认' }}
          </button>
        </form>

        <div class="quick-cities-title">常用城市</div>
        <div class="quick-cities-grid">
          <button
            v-for="city in cities"
            :key="city"
            type="button"
            class="quick-city-btn"
            :class="{ active: city === currentCity }"
            :disabled="loading"
            @click="selectCity(city)"
          >
            {{ city }}
          </button>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, nextTick } from 'vue'

const props = defineProps<{
  loading?: boolean
  currentCity?: string
}>()

const emit = defineEmits<{ draw: [city: string] }>()

const cities = ['上海', '北京', '杭州', '广州', '深圳', '成都', '南京', '武汉']
const searchQuery = ref('')
const isDropdownOpen = ref(false)
const dropdownRef = ref<HTMLElement | null>(null)
const searchInputRef = ref<HTMLInputElement | null>(null)

function toggleDropdown() {
  isDropdownOpen.value = !isDropdownOpen.value
  if (isDropdownOpen.value) {
    searchQuery.value = ''
    nextTick(() => {
      searchInputRef.value?.focus()
    })
  }
}

function selectCity(city: string) {
  isDropdownOpen.value = false
  emit('draw', city)
}

function submitSearch() {
  if (searchQuery.value) {
    selectCity(searchQuery.value)
  }
}

function handleClickOutside(event: MouseEvent) {
  if (dropdownRef.value && !dropdownRef.value.contains(event.target as Node)) {
    isDropdownOpen.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
.oracle-city-picker-wrapper {
  position: relative;
  display: inline-block;
}

/* Trigger Button */
.oracle-city-select-trigger {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 18px;
  border: 1px solid var(--oracle-border);
  border-radius: 20px;
  background: var(--oracle-panel-soft);
  color: var(--oracle-text);
  font-size: 15px;
  font-weight: 700;
  cursor: pointer;
  transition: transform 160ms cubic-bezier(0.23, 1, 0.32, 1), border-color 160ms ease-out, background-color 160ms ease-out, box-shadow 160ms ease-out;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

@media (hover: hover) and (pointer: fine) {
  .oracle-city-select-trigger:hover:not(:disabled) {
    border-color: var(--oracle-gold);
    background: var(--oracle-panel);
    box-shadow: 0 0 10px var(--oracle-gold-glow);
    transform: translateY(-1px);
  }
}

.oracle-city-select-trigger:active:not(:disabled) {
  transform: scale(0.97);
}

.oracle-city-select-trigger:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.trigger-icon {
  font-size: 14px;
}

.trigger-arrow {
  color: var(--oracle-gold);
  font-size: 12px;
}

/* Dropdown Panel */
.oracle-city-dropdown-panel {
  position: absolute;
  top: calc(100% + 10px);
  left: 0;
  width: 280px;
  padding: 16px;
  z-index: 50;
  transform-origin: top left;
}

/* Search Form */
.city-search-form {
  display: flex;
  gap: 8px;
  margin-bottom: 14px;
}

.city-search-input {
  min-width: 0;
  flex: 1;
  height: 38px;
  border: 1px solid var(--oracle-border);
  border-radius: 6px;
  padding: 0 12px;
  background: var(--oracle-panel-soft);
  color: var(--oracle-text);
  font-size: 13.5px;
  transition: border-color 180ms ease-out, box-shadow 180ms ease-out;
}

.city-search-input:focus {
  border-color: var(--oracle-gold);
  box-shadow: 0 0 8px var(--oracle-gold-glow);
}

.city-search-btn {
  padding: 0 12px;
  height: 38px;
  border: 1px solid var(--oracle-border);
  border-radius: 6px;
  background: linear-gradient(135deg, var(--oracle-gold), var(--oracle-gold-strong));
  color: #120e0a;
  font-size: 12.5px;
  font-weight: 700;
  cursor: pointer;
  transition: transform 160ms cubic-bezier(0.23, 1, 0.32, 1), filter 160ms ease-out, box-shadow 160ms ease-out;
}

@media (hover: hover) and (pointer: fine) {
  .city-search-btn:hover:not(:disabled) {
    filter: brightness(1.1);
    box-shadow: 0 0 8px var(--oracle-gold-glow);
  }
}

.city-search-btn:active:not(:disabled) {
  transform: scale(0.97);
}

.city-search-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Quick Cities */
.quick-cities-title {
  font-size: 11px;
  color: var(--oracle-muted);
  font-weight: 700;
  margin-bottom: 8px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.quick-cities-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 6px;
}

.quick-city-btn {
  padding: 6px 4px;
  border: 1px solid var(--oracle-border-soft);
  border-radius: 4px;
  background: var(--oracle-panel-soft);
  color: var(--oracle-faint);
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  text-align: center;
  transition: transform 160ms cubic-bezier(0.23, 1, 0.32, 1), border-color 160ms ease-out, color 160ms ease-out, background-color 160ms ease-out;
}

@media (hover: hover) and (pointer: fine) {
  .quick-city-btn:hover:not(:disabled) {
    border-color: var(--oracle-gold);
    color: var(--oracle-gold-strong);
    background: var(--oracle-panel);
  }
}

.quick-city-btn:active:not(:disabled) {
  transform: scale(0.96);
}

.quick-city-btn.active {
  border-color: var(--oracle-gold);
  color: var(--oracle-gold-strong);
  background: var(--oracle-purple-soft);
}

.quick-city-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Transition */
.fade-scale-enter-active,
.fade-scale-leave-active {
  transition: opacity 180ms cubic-bezier(0.23, 1, 0.32, 1), transform 180ms cubic-bezier(0.23, 1, 0.32, 1);
}

.fade-scale-enter-from,
.fade-scale-leave-to {
  opacity: 0;
  transform: scale(0.96) translateY(-4px);
}
</style>
