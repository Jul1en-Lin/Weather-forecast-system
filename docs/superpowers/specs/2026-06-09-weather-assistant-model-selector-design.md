# Weather Assistant Model Selector Design

Design specification for adding a model selector to the homepage right-side weather assistant panel and setting the default model to `mimo-v2.5`.

## Requirements

1. **Model Selector**: Add a dropdown select element to the Weather Assistant panel on the homepage.
2. **Default Model**: Change the default model to `mimo-v2.5` (if configured), falling back to `MiniMax-M2.5`, `kimi-k2.5`, or the first available model.
3. **Selection Persistence**: Save the selected model in `localStorage` so the user's choice is remembered across page refreshes.
4. **Theme Adaptation**: Ensure the dropdown matches the gold-accented, glassmorphic layout of the Weather Oracle page.

## Proposed Changes

### Frontend Changes

#### [OracleChatPanel.vue](file:///Users/lien/GitRepo/Weather-forecast-system/src/components/oracle/OracleChatPanel.vue)

1. **Header Template**: Replace the static model badge with a select dropdown:
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

2. **Initialization and Persistence Logic**:
   - Save the selected model using a watcher on `selectedModel` to `localStorage` under key `weather_oracle:chat_model`.
   - Restore the model in `loadModels()` from `localStorage`. If not present, default to `mimo-v2.5` (or fallback models in preference order).

3. **Styling**:
   - Style `.model-picker` and `.model-select` using variables from `oracle-theme.css`.
   - Implement custom arrow indicator and glassmorphic inputs.

## Verification Plan

1. **Vite Build**: Run `npm run build` to confirm compilation.
2. **Browser Verification**: Inspect the Weather Assistant header and verify that the dropdown works and updates the active model for stream chat calls.
3. **Persistence Verification**: Refresh the page to confirm that the selected model is remembered.
