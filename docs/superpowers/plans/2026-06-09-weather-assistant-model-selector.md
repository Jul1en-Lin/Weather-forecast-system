# Weather Assistant Model Selector Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a model selection dropdown to the homepage right-side weather assistant panel (`OracleChatPanel.vue`), defaulting to the `mimo-v2.5` model (if configured), and persist the user's choice in `localStorage`.

**Architecture:** Bind the select component to `selectedModel` inside `OracleChatPanel.vue`. Read selection from `localStorage` during initialization. If absent, fallback to a preference order: `mimo-v2.5`, `MiniMax-M2.5`, `kimi-k2.5`, and finally the first available model. Watch changes on `selectedModel` to update `localStorage` dynamically.

**Tech Stack:** Vue 3, TypeScript, CSS, localStorage

---

### Task 1: Update OracleChatPanel UI, Script Logic, and Styles

**Files:**
- Modify: `src/components/oracle/OracleChatPanel.vue`

- [ ] **Step 1: Modify UI Template in OracleChatPanel.vue**

Replace the static model badge:
```html
      <div class="model-badge" v-if="modelName">
        <span>{{ modelName }}</span>
      </div>
```
With the select dropdown:
```html
      <div class="model-picker" v-if="models.length > 0">
        <select
          v-model="selectedModel"
          class="model-select"
          :disabled="isSending"
          aria-label="选择模型"
        >
          <option v-for="model in models" :key="model.id" :value="model.id">
            {{ model.name }}
          </option>
        </select>
      </div>
```

- [ ] **Step 2: Modify Script Logic in OracleChatPanel.vue**

Add the `STORAGE_KEY`, update `loadModels()`, and add a watcher for `selectedModel` to persist state:
```typescript
const STORAGE_KEY = 'weather_oracle:chat_model'

// Inside loadModels() after models.value = data.models || []:
    const stored = localStorage.getItem(STORAGE_KEY)
    const ids = models.value.map(m => m.id)
    if (stored && ids.includes(stored)) {
      selectedModel.value = stored
    } else {
      // Find preferred model: mimo-v2.5, MiniMax-M2.5, kimi-k2.5
      const preferred = models.value.find(m => m.id === 'mimo-v2.5' || m.id === 'mimo')
        || models.value.find(m => m.id === 'MiniMax-M2.5')
        || models.value.find(m => m.id === 'kimi-k2.5')
        || models.value[0]
      selectedModel.value = preferred ? preferred.id : ''
    }

// Add watcher at script level:
watch(selectedModel, (newVal) => {
  if (newVal) {
    localStorage.setItem(STORAGE_KEY, newVal)
  }
})
```

- [ ] **Step 3: Modify Scoped CSS Styles in OracleChatPanel.vue**

Remove the `.model-badge` style block and add styles for `.model-picker` and `.model-select`:
```css
.model-picker {
  position: relative;
  display: flex;
  align-items: center;
}

.model-select {
  appearance: none;
  -webkit-appearance: none;
  background: var(--oracle-panel-soft);
  border: 1px solid var(--oracle-border-soft);
  border-radius: 12px;
  padding: 3px 22px 3px 10px;
  font-size: 10.5px;
  color: var(--oracle-gold);
  font-weight: 600;
  cursor: pointer;
  outline: none;
  font-family: var(--oracle-font-sans);
  transition: border-color 0.2s, box-shadow 0.2s;
}

.model-select option {
  background-color: var(--oracle-panel-solid);
  color: var(--oracle-text);
}

.model-select:focus:not(:disabled) {
  border-color: var(--oracle-gold);
  box-shadow: 0 0 8px var(--oracle-gold-glow);
}

.model-select:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.model-picker::after {
  content: '▾';
  position: absolute;
  right: 8px;
  font-size: 9px;
  color: var(--oracle-gold);
  pointer-events: none;
}

@media (hover: hover) and (pointer: fine) {
  .model-select:hover:not(:disabled) {
    border-color: var(--oracle-gold);
    box-shadow: 0 0 6px var(--oracle-gold-glow);
  }
}
```

- [ ] **Step 4: Run Vite build to verify compilation**

Run: `npm run build`
Expected: Successful production build without TypeScript type or syntax errors.

- [ ] **Step 5: Run backend tests to verify no regressions**

Run: `venv/bin/python -m pytest tests -q` from `backend` directory
Expected: All 36 backend tests pass.

- [ ] **Step 6: Commit changes**

Run: `git add src/components/oracle/OracleChatPanel.vue`
Run: `git commit -m "feat: add model selector to weather assistant and default to mimo"`
