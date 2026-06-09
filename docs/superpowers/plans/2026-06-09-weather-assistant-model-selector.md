# Weather Assistant Model Selector Implementation Plan - Revision

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement a card-style floating dropdown selector for the weather assistant model selection, matching the city picker's visual design.

**Architecture:** Create a custom toggle button trigger and floating panel inside `OracleChatPanel.vue`. Close the dropdown when clicking outside. Style using `oracle-theme.css` variables.

**Tech Stack:** Vue 3, TypeScript, CSS, localStorage

---

### Task 1: Refactor Template, Script, and CSS in OracleChatPanel.vue

**Files:**
- Modify: `src/components/oracle/OracleChatPanel.vue`

- [ ] **Step 1: Replace Template Markup**

Update `<header class="chat-panel-header">` to remove the subtitle and replace `.model-picker` with the new button and floating dropdown:
```html
    <header class="chat-panel-header">
      <div class="diviner-profile">
        <div class="diviner-avatar-wrap">
          <svg class="diviner-avatar-svg" viewBox="0 0 24 24" width="20" height="20">
            <path fill="currentColor" d="M12 22c5.52 0 10-4.48 10-10S17.52 2 12 2 2 6.48 2 12s4.48 10 10 10zm1-17.5c.83 0 1.5.67 1.5 1.5s-.67 1.5-1.5 1.5-1.5-.67-1.5-1.5.67-1.5 1.5-1.5zm-2.5 12h-1v-1h1v1zm3-3.5c-.83 0-1.5-.67-1.5-1.5s.67-1.5 1.5-1.5 1.5.67 1.5 1.5-.67 1.5-1.5 1.5zm-3.5 1.5c-.83 0-1.5-.67-1.5-1.5s.67-1.5 1.5-1.5 1.5.67 1.5 1.5-.67 1.5-1.5 1.5z" />
          </svg>
        </div>
        <div class="diviner-meta">
          <h4>天气助手</h4>
        </div>
      </div>
      <div class="model-picker-wrapper" ref="dropdownRef">
        <button
          type="button"
          class="model-select-trigger"
          :disabled="isSending"
          @click="toggleDropdown"
        >
          <span class="trigger-icon">🤖</span>
          <span class="trigger-text">{{ modelName || '选择模型' }}</span>
          <span class="trigger-arrow">▾</span>
        </button>

        <transition name="fade-scale">
          <div v-if="isDropdownOpen" class="model-dropdown-panel oracle-surface oracle-gold-corners">
            <div class="model-options-list">
              <button
                v-for="model in models"
                :key="model.id"
                type="button"
                class="model-option-btn"
                :class="{ active: model.id === selectedModel }"
                @click="selectModel(model.id)"
              >
                <div class="model-option-name">{{ model.name }}</div>
                <div class="model-option-desc" v-if="model.description">{{ model.description }}</div>
              </button>
            </div>
          </div>
        </transition>
      </div>
    </header>
```

- [ ] **Step 2: Update Vue Imports and Script State**

Modify script imports, state declarations, lifecycle events, and methods:
```typescript
import { computed, onMounted, ref, nextTick, watch, onUnmounted } from 'vue'
...
const isDropdownOpen = ref(false)
const dropdownRef = ref<HTMLElement | null>(null)

const modelName = computed(() => {
  return models.value.find(model => model.id === selectedModel.value)?.name || ''
})

function toggleDropdown() {
  isDropdownOpen.value = !isDropdownOpen.value
}

function selectModel(modelId: string) {
  selectedModel.value = modelId
  isDropdownOpen.value = false
}

function handleClickOutside(event: MouseEvent) {
  if (dropdownRef.value && !dropdownRef.value.contains(event.target as Node)) {
    isDropdownOpen.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
  loadModels()
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
```

- [ ] **Step 3: Replace selector CSS styles**

Replace the `.model-picker` and `.model-select` styles with the new dropdown & cards CSS classes:
```css
.model-picker-wrapper {
  position: relative;
  display: inline-block;
  z-index: 20;
}

.model-select-trigger {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 14px;
  border: 1px solid var(--oracle-border);
  border-radius: 20px;
  background: var(--oracle-panel-soft);
  color: var(--oracle-text);
  font-size: 11.5px;
  font-weight: 700;
  cursor: pointer;
  transition: transform 160ms cubic-bezier(0.23, 1, 0.32, 1), border-color 160ms ease-out, background-color 160ms ease-out, box-shadow 160ms ease-out;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

@media (hover: hover) and (pointer: fine) {
  .model-select-trigger:hover:not(:disabled) {
    border-color: var(--oracle-gold);
    background: var(--oracle-panel);
    box-shadow: 0 0 10px var(--oracle-gold-glow);
    transform: translateY(-1px);
  }
}

.model-select-trigger:active:not(:disabled) {
  transform: scale(0.97);
}

.model-select-trigger:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.trigger-icon {
  font-size: 11px;
}

.trigger-arrow {
  color: var(--oracle-gold);
  font-size: 10px;
}

.model-dropdown-panel {
  position: absolute;
  top: calc(100% + 8px);
  right: 0;
  width: 240px;
  padding: 10px;
  z-index: 100;
  transform-origin: top right;
}

.model-options-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.model-option-btn {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid var(--oracle-border-soft);
  border-radius: 8px;
  background: var(--oracle-panel-soft);
  color: var(--oracle-faint);
  cursor: pointer;
  text-align: left;
  transition: transform 160ms cubic-bezier(0.23, 1, 0.32, 1), border-color 160ms ease-out, color 160ms ease-out, background-color 160ms ease-out;
}

@media (hover: hover) and (pointer: fine) {
  .model-option-btn:hover {
    border-color: var(--oracle-gold);
    color: var(--oracle-gold-strong);
    background: var(--oracle-panel);
  }
}

.model-option-btn:active {
  transform: scale(0.98);
}

.model-option-btn.active {
  border-color: var(--oracle-gold);
  color: var(--oracle-gold-strong);
  background: var(--oracle-purple-soft);
  box-shadow: 0 0 8px var(--oracle-gold-glow);
}

.model-option-name {
  font-size: 12.5px;
  font-weight: 700;
  margin-bottom: 2px;
}

.model-option-desc {
  font-size: 10.5px;
  color: var(--oracle-muted);
  font-weight: 400;
  line-height: 1.4;
}

.fade-scale-enter-active,
.fade-scale-leave-active {
  transition: opacity 180ms cubic-bezier(0.23, 1, 0.32, 1), transform 180ms cubic-bezier(0.23, 1, 0.32, 1);
}

.fade-scale-enter-from,
.fade-scale-leave-to {
  opacity: 0;
  transform: scale(0.96) translateY(-4px);
}
```

- [ ] **Step 4: Verify production compilation**

Run: `npm run build`
Expected: Successful compile and bundle without type errors.

- [ ] **Step 5: Run pytest regression checks**

Run: `venv/bin/python -m pytest tests -q` in `backend/`
Expected: 36/36 tests pass.

- [ ] **Step 6: Commit changes**

Run: `git add src/components/oracle/OracleChatPanel.vue`
Run: `git commit -m "feat: design optimized card-style dropdown selector for weather assistant"`
