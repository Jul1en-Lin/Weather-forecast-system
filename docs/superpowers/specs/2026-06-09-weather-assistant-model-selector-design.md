# Weather Assistant Model Selector Design - Cards Dropdown Rev

Design specification for creating a floating card-style dropdown selector for the weather assistant model selection, matching the city picker's style.

## Requirements

1. **Card-Style Dropdown selector**: Instead of a native HTML `<select>` element, implement a button trigger that opens a floating panel (`.model-dropdown-panel`) styled as an `.oracle-surface` with `.oracle-gold-corners`.
2. **Model Option Cards**: Inside the dropdown panel, list the available models vertically as clickable buttons, showing their names and descriptions (if available).
3. **No Header Subtitle**: Remove the subtitle text `<span>你的智能气象服务助理</span>` from the panel header to avoid any layout crowding.
4. **Clean Interactive Transitions**: Implement the `fade-scale` transition for the dropdown toggle, click-outside auto-close listener, hover-translate, and active-scale micro-animations on buttons.

## Proposed Changes

### Frontend Changes

#### [OracleChatPanel.vue](file:///Users/lien/GitRepo/Weather-forecast-system/src/components/oracle/OracleChatPanel.vue)

1. **Template**:
   - Clean up subtitle span inside `.diviner-meta`.
   - Replace `<div class="model-picker">` with the new structure:
     ```html
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
     ```

2. **Script Setup**:
   - Re-introduce `modelName` computed property.
   - Add `isDropdownOpen` and `dropdownRef` template references.
   - Implement `toggleDropdown()`, `selectModel()`, and `handleClickOutside()` logic.
   - Register the click listener on `onMounted` and clean up on `onUnmounted`.

3. **CSS**:
   - Add `.model-picker-wrapper`, `.model-select-trigger`, `.model-dropdown-panel`, `.model-options-list`, `.model-option-btn`, `.model-option-name`, `.model-option-desc`, and the `.fade-scale` transition styles.

## Verification Plan

1. **Vite Build**: Verify zero compilation/type errors via `npm run build`.
2. **Unit Tests**: Confirm that no backend tests are affected.
