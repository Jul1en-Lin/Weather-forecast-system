# Settings Page Visual Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Redesign the System Settings view (`src/views/Settings.vue`) to align with the gold-accented, glassmorphic dark/light theme, replacing generic colors and checkmark emojis with micro-indicator dots and pill badges.

**Architecture:** Use CSS theme variables defined in `oracle-theme.css`. Apply class `.oracle-surface` to form sections, use `.badge-pill` classes for model types, and introduce a CSS `.status-indicator` with `.status-dot` for tool support status.

**Tech Stack:** Vue 3, Vite, TypeScript, CSS Variables, SVG.

---

### Task 1: Redesign the UI Template Elements in Settings.vue

**Files:**
- Modify: `src/views/Settings.vue`
- Verify: `npm run build`

- [ ] **Step 1: Replace support-tools and Ollama badges/text in the template**

  In `src/views/Settings.vue` around lines 151-197:
  - Add `.oracle-surface` class to the model tab panel.
  - Replace `.model-badge` / `.local-badge` elements with `.badge-pill` / `.badge-pill-local`.
  - Replace the emojis `✅ 支持` and `❌ 不支持` with `.status-indicator` layout containing a status dot and text.

  *Exact target template block to modify:*
  ```html
            <!-- 模型列表展示 -->
            <div v-else class="models-list-wrapper">
              <div v-if="modelList.length === 0" class="empty-models">
                <p>暂无模型配置，请点击右上角添加模型</p>
              </div>
              <div v-else class="models-grid">
                <div v-for="m in modelList" :key="m.id" class="model-card-item">
                  <div class="model-card-header">
                    <div class="model-title-desc">
                      <h4>{{ m.name }}</h4>
                      <span class="model-badge" :class="{ 'local-badge': m.is_local }">
                        {{ m.is_local ? 'Ollama 本地' : '云端 API' }}
                      </span>
                    </div>
                    <div class="model-card-actions">
                      <button @click="editModel(m)" class="btn-card-action edit-btn">编辑</button>
                      <button @click="confirmDeleteModel(m)" class="btn-card-action delete-btn">删除</button>
                    </div>
                  </div>
                  <div class="model-card-body">
                    <p class="model-desc">{{ m.description || '无描述信息' }}</p>
                    <div class="model-meta-info">
                      <div class="meta-row">
                        <span class="meta-label">ID:</span>
                        <code class="meta-value">{{ m.id }}</code>
                      </div>
                      <div class="meta-row">
                        <span class="meta-label">模型参数:</span>
                        <code class="meta-value">{{ m.model }}</code>
                      </div>
                      <div class="meta-row">
                        <span class="meta-label">接口地址:</span>
                        <span class="meta-value text-truncate" :title="m.base_url || '使用系统默认/无'">
                          {{ m.base_url || '使用系统默认/无' }}
                        </span>
                      </div>
                      <div class="meta-row">
                        <span class="meta-label">API Key:</span>
                        <span class="meta-value text-truncate" :title="m.masked_api_key || '使用默认/未配置'">
                          {{ m.masked_api_key || '使用默认/未配置' }}
                        </span>
                      </div>
                      <div class="meta-row">
                        <span class="meta-label">工具支持:</span>
                        <span class="meta-value">{{ m.supports_tools ? '✅ 支持' : '❌ 不支持' }}</span>
                      </div>
                      <div class="meta-row">
                        <span class="meta-label">温度:</span>
                        <span class="meta-value">{{ m.temperature !== null && m.temperature !== undefined ? m.temperature : '系统默认(0.7)' }}</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
  ```

  *Exact replacement template block:*
  ```html
            <!-- 模型列表展示 -->
            <div v-else class="models-list-wrapper">
              <div v-if="modelList.length === 0" class="empty-models">
                <p>暂无模型配置，请点击右上角添加模型</p>
              </div>
              <div v-else class="models-grid">
                <div v-for="m in modelList" :key="m.id" class="model-card-item">
                  <div class="model-card-header">
                    <div class="model-title-desc">
                      <h4>{{ m.name }}</h4>
                      <span class="badge-pill" :class="{ 'badge-pill-local': m.is_local }">
                        {{ m.is_local ? 'Ollama 本地' : '云端 API' }}
                      </span>
                    </div>
                    <div class="model-card-actions">
                      <button @click="editModel(m)" class="btn-card-action edit-btn">编辑</button>
                      <button @click="confirmDeleteModel(m)" class="btn-card-action delete-btn">删除</button>
                    </div>
                  </div>
                  <div class="model-card-body">
                    <p class="model-desc">{{ m.description || '无描述信息' }}</p>
                    <div class="model-meta-info">
                      <div class="meta-row">
                        <span class="meta-label">ID:</span>
                        <code class="meta-value">{{ m.id }}</code>
                      </div>
                      <div class="meta-row">
                        <span class="meta-label">模型参数:</span>
                        <code class="meta-value">{{ m.model }}</code>
                      </div>
                      <div class="meta-row">
                        <span class="meta-label">接口地址:</span>
                        <span class="meta-value text-truncate" :title="m.base_url || '使用系统默认/无'">
                          {{ m.base_url || '使用系统默认/无' }}
                        </span>
                      </div>
                      <div class="meta-row">
                        <span class="meta-label">API Key:</span>
                        <span class="meta-value text-truncate" :title="m.masked_api_key || '使用默认/未配置'">
                          {{ m.masked_api_key || '使用默认/未配置' }}
                        </span>
                      </div>
                      <div class="meta-row">
                        <span class="meta-label">工具支持:</span>
                        <span class="meta-value status-indicator" :class="{ 'active': m.supports_tools }">
                          <span class="status-dot"></span>
                          <span class="status-text">{{ m.supports_tools ? '支持' : '不支持' }}</span>
                        </span>
                      </div>
                      <div class="meta-row">
                        <span class="meta-label">温度:</span>
                        <span class="meta-value">{{ m.temperature !== null && m.temperature !== undefined ? m.temperature : '系统默认(0.7)' }}</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
  ```

- [ ] **Step 2: Replace settings form panel elements and weather service tab elements**

  In `src/views/Settings.vue` around lines 33-35, and lines 202-212:
  - Add `.oracle-surface` class to the tab sections to apply glassmorphic base layers.

  *Exact target block 1 (lines 33-35):*
  ```html
          <!-- 模型管理 Tab -->
          <div v-show="activeTab === 'models'" class="settings-form oracle-gold-corners">
  ```
  *Replacement block 1:*
  ```html
          <!-- 模型管理 Tab -->
          <div v-show="activeTab === 'models'" class="settings-form oracle-surface oracle-gold-corners">
  ```

  *Exact target block 2 (lines 202-204):*
  ```html
          <!-- 天气服务 Tab -->
          <div v-show="activeTab === 'tools'" class="settings-form oracle-gold-corners">
  ```
  *Replacement block 2:*
  ```html
          <!-- 天气服务 Tab -->
          <div v-show="activeTab === 'tools'" class="settings-form oracle-surface oracle-gold-corners">
  ```

- [ ] **Step 3: Replace emojis/text in the tools list template**

  In `src/views/Settings.vue` around lines 258-292:
  - Apply badge-pill class to "系统内置" status.

  *Exact target block:*
  ```html
                      <div class="model-title-desc">
                        <h4>{{ t.name }}</h4>
                        <span class="model-badge">系统内置</span>
                      </div>
  ```
  *Replacement block:*
  ```html
                      <div class="model-title-desc">
                        <h4>{{ t.name }}</h4>
                        <span class="badge-pill badge-pill-builtin">系统内置</span>
                      </div>
  ```

- [ ] **Step 4: Verify template compilation**

  Run: `npm run build`
  Expected: Command succeeds with zero syntax errors.

---

### Task 2: Redesign the CSS Stylesheet block in Settings.vue

**Files:**
- Modify: `src/views/Settings.vue`
- Verify: `npm run build`

- [ ] **Step 1: Replace `<style scoped>` section in Settings.vue**

  Completely replace `<style scoped>` block from line 584 to the end of the file with the redesigned glassmorphic dark/light stylesheet.

  *Exact target code:*
  ```html
  <style scoped>
  .settings-page {
    min-height: 100vh;
  }
  ... (entire original CSS rules up to line 1115)
  </style>
  ```

  *Exact replacement code:*
  ```html
  <style scoped>
  .settings-page {
    min-height: 100vh;
  }

  .content-wrapper {
    padding: 40px;
    max-width: 1400px;
    margin: 0 auto;
  }

  /* Tab menu */
  .tab-nav {
    display: flex;
    justify-content: center;
    gap: 16px;
    margin-bottom: 32px;
  }

  .tab-btn {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 14px 28px;
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid var(--oracle-border-soft);
    border-radius: 12px;
    font-size: 16px;
    font-weight: 500;
    color: var(--oracle-muted);
    cursor: pointer;
    transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  }

  .tab-btn:hover {
    color: var(--oracle-text);
    border-color: var(--oracle-border);
    background: rgba(215, 174, 105, 0.05);
    transform: translateY(-2px);
  }

  .tab-btn.active {
    background: rgba(215, 174, 105, 0.08);
    border-color: var(--oracle-gold);
    color: var(--oracle-gold);
    box-shadow: 0 0 12px var(--oracle-gold-glow);
  }

  .tab-icon {
    display: flex;
    align-items: center;
    justify-content: center;
  }

  /* Spinner */
  .loading-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 60px 0;
    color: var(--oracle-muted);
  }

  .spinner {
    width: 40px;
    height: 40px;
    border: 4px solid var(--oracle-border-soft);
    border-top-color: var(--oracle-gold);
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
    margin-bottom: 16px;
  }

  @keyframes spin {
    to { transform: rotate(360deg); }
  }

  /* Configurations Form Card */
  .settings-form {
    border-radius: 20px;
    padding: 40px;
  }

  .config-section {
    margin-bottom: 40px;
  }

  .section-header {
    display: flex;
    align-items: center;
    font-size: 22px;
    font-weight: 600;
    color: var(--oracle-text);
    margin-bottom: 24px;
    padding-bottom: 16px;
    border-bottom: 1px solid var(--oracle-border-soft);
  }

  .flex-between {
    justify-content: space-between;
  }

  .flex-align-center {
    display: flex;
    align-items: center;
    gap: 12px;
  }

  .config-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
    gap: 20px;
  }

  .config-card {
    background: rgba(0, 0, 0, 0.1);
    border-radius: 16px;
    padding: 24px;
    border: 1px solid var(--oracle-border-soft);
    transition: border-color 0.3s, box-shadow 0.3s;
  }
  
  [data-oracle-theme='light'] .config-card {
    background: rgba(255, 255, 255, 0.3);
  }

  .config-card:hover {
    border-color: var(--oracle-gold);
    box-shadow: 0 0 10px var(--oracle-gold-glow);
  }

  .config-card label {
    display: block;
    font-size: 14px;
    font-weight: 600;
    color: var(--oracle-text);
    margin-bottom: 10px;
  }

  .config-card input {
    width: 100%;
    padding: 12px 16px;
    border: 1px solid var(--oracle-border);
    border-radius: 10px;
    font-size: 15px;
    color: var(--oracle-text);
    background: rgba(0, 0, 0, 0.15);
    transition: all 0.3s ease;
    box-sizing: border-box;
  }

  [data-oracle-theme='light'] .config-card input {
    background: rgba(255, 255, 255, 0.5);
  }

  .config-card input:focus {
    outline: none;
    border-color: var(--oracle-gold);
    box-shadow: 0 0 8px var(--oracle-gold-glow);
  }

  .current-value {
    display: block;
    margin-top: 10px;
    font-size: 12px;
    color: var(--oracle-muted);
  }

  .current-value code {
    background: rgba(255, 255, 255, 0.05);
    padding: 2px 6px;
    border-radius: 4px;
    font-family: SFMono-Regular, Consolas, monospace;
  }
  
  [data-oracle-theme='light'] .current-value code {
    background: rgba(0, 0, 0, 0.05);
  }

  /* Add model button */
  .btn-add-model {
    background: linear-gradient(135deg, var(--oracle-gold) 0%, #a47631 100%);
    border: none;
    color: var(--oracle-text);
    border-radius: 10px;
    padding: 10px 20px;
    font-size: 15px;
    font-weight: 600;
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    transition: all 0.3s ease;
  }

  .btn-add-model:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 15px var(--oracle-gold-glow);
    filter: brightness(1.1);
  }

  /* Models Grid / Cards */
  .models-list-wrapper {
    margin-top: 10px;
  }

  .empty-models {
    text-align: center;
    padding: 60px 0;
    color: var(--oracle-muted);
    font-size: 16px;
  }

  .models-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
    gap: 24px;
  }

  .model-card-item {
    background: rgba(0, 0, 0, 0.12);
    border-radius: 18px;
    border: 1px solid var(--oracle-border-soft);
    display: flex;
    flex-direction: column;
    overflow: hidden;
    transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  }

  [data-oracle-theme='light'] .model-card-item {
    background: rgba(255, 255, 255, 0.35);
  }

  .model-card-item:hover {
    transform: translateY(-4px);
    border-color: var(--oracle-gold);
    box-shadow: 0 12px 30px var(--oracle-gold-glow);
  }

  .model-card-header {
    padding: 20px 24px;
    border-bottom: 1px solid var(--oracle-border-soft);
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
  }

  .model-title-desc h4 {
    font-size: 18px;
    font-weight: 600;
    color: var(--oracle-text);
    margin: 0 0 6px 0;
    font-family: var(--oracle-font-serif);
  }

  /* Badges */
  .badge-pill {
    display: inline-block;
    padding: 4px 10px;
    border-radius: 99px;
    font-size: 11px;
    font-weight: 600;
    border: 1px solid rgba(215, 174, 105, 0.25);
    background: rgba(215, 174, 105, 0.08);
    color: var(--oracle-gold);
  }

  .badge-pill-local {
    border-color: rgba(84, 191, 163, 0.25);
    background: rgba(84, 191, 163, 0.08);
    color: var(--oracle-success);
  }

  .badge-pill-builtin {
    border-color: rgba(142, 110, 194, 0.25);
    background: rgba(142, 110, 194, 0.08);
    color: var(--oracle-purple);
  }

  /* Action Buttons */
  .model-card-actions {
    display: flex;
    gap: 8px;
  }

  .btn-card-action {
    font-size: 13px;
    padding: 6px 12px;
    border-radius: 8px;
    font-weight: 500;
    border: 1px solid var(--oracle-border-soft);
    background: rgba(255, 255, 255, 0.02);
    color: var(--oracle-text);
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .btn-card-action.edit-btn:hover {
    border-color: var(--oracle-gold);
    background: rgba(215, 174, 105, 0.08);
    color: var(--oracle-gold);
  }

  .btn-card-action.delete-btn {
    border-color: rgba(207, 110, 91, 0.25);
    background: rgba(207, 110, 91, 0.05);
    color: var(--oracle-danger);
  }

  .btn-card-action.delete-btn:hover {
    background: rgba(207, 110, 91, 0.15);
    border-color: var(--oracle-danger);
  }

  .model-card-body {
    padding: 24px;
    display: flex;
    flex-direction: column;
    flex: 1;
  }

  .model-desc {
    font-size: 14px;
    color: var(--oracle-muted);
    margin: 0 0 20px 0;
    line-height: 1.5;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
    height: 42px;
  }

  .model-meta-info {
    background: rgba(0, 0, 0, 0.15);
    border-radius: 12px;
    padding: 16px;
    display: flex;
    flex-direction: column;
    gap: 10px;
    border: 1px solid var(--oracle-border-soft);
  }

  [data-oracle-theme='light'] .model-meta-info {
    background: rgba(0, 0, 0, 0.03);
  }

  .meta-row {
    display: flex;
    font-size: 13px;
    line-height: 1.4;
    justify-content: space-between;
  }

  .meta-label {
    color: var(--oracle-muted);
    font-weight: 500;
    flex-shrink: 0;
  }

  .meta-value {
    color: var(--oracle-text);
    word-break: break-all;
    font-family: inherit;
    text-align: right;
  }

  .meta-value.text-truncate {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 200px;
  }

  code.meta-value {
    font-family: SFMono-Regular, Consolas, monospace;
    background: rgba(255, 255, 255, 0.05);
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 12px;
  }

  [data-oracle-theme='light'] code.meta-value {
    background: rgba(0, 0, 0, 0.05);
  }

  /* Status Indicator */
  .status-indicator {
    display: inline-flex;
    align-items: center;
    gap: 6px;
  }

  .status-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: var(--oracle-muted);
    transition: all 0.3s ease;
  }

  .status-indicator.active .status-dot {
    background: var(--oracle-success);
    box-shadow: 0 0 8px var(--oracle-success);
  }

  .status-indicator:not(.active) .status-dot {
    background: var(--oracle-danger);
    box-shadow: 0 0 8px var(--oracle-danger);
  }

  .status-text {
    color: var(--oracle-text);
  }

  /* Model Form Card */
  .model-form-card {
    background: rgba(0, 0, 0, 0.15);
    border-radius: 20px;
    padding: 30px;
    border: 1px solid var(--oracle-border-soft);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  }

  [data-oracle-theme='light'] .model-form-card {
    background: rgba(255, 255, 255, 0.4);
  }

  .form-title {
    font-size: 18px;
    font-weight: 600;
    color: var(--oracle-text);
    margin-bottom: 20px;
    font-family: var(--oracle-font-serif);
  }

  .form-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 20px;
  }

  .form-group {
    display: flex;
    flex-direction: column;
  }

  .form-group.full-width {
    grid-column: span 2;
  }

  .form-group.flex-row {
    flex-direction: row;
    align-items: center;
    grid-column: span 1;
    padding-top: 24px;
  }

  .form-group label {
    font-size: 14px;
    font-weight: 600;
    color: var(--oracle-text);
    margin-bottom: 8px;
  }

  .checkbox-label {
    display: flex;
    align-items: center;
    gap: 8px;
    cursor: pointer;
    font-weight: 500 !important;
  }

  .checkbox-label input {
    width: 18px;
    height: 18px;
    cursor: pointer;
    accent-color: var(--oracle-gold);
  }

  .form-group input[type="text"],
  .form-group input[type="number"],
  .form-group input[type="password"],
  .form-group textarea {
    padding: 12px 14px;
    border: 1px solid var(--oracle-border);
    border-radius: 10px;
    font-size: 14px;
    color: var(--oracle-text);
    background: rgba(0, 0, 0, 0.2);
    transition: all 0.2s ease;
  }

  [data-oracle-theme='light'] .form-group input,
  [data-oracle-theme='light'] .form-group textarea {
    background: rgba(255, 255, 255, 0.5);
  }

  .form-group input:focus,
  .form-group textarea:focus {
    border-color: var(--oracle-gold);
    box-shadow: 0 0 8px var(--oracle-gold-glow);
    outline: none;
  }

  /* Actions buttons styling */
  .form-actions {
    display: flex;
    justify-content: center;
    gap: 16px;
    margin-top: 32px;
    padding-top: 24px;
    border-top: 1px solid var(--oracle-border-soft);
  }

  .btn-reset {
    padding: 12px 30px;
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid var(--oracle-border-soft);
    border-radius: 10px;
    font-size: 15px;
    font-weight: 500;
    color: var(--oracle-text);
    cursor: pointer;
    transition: all 0.3s ease;
  }

  .btn-reset:hover {
    background: rgba(255, 255, 255, 0.08);
    border-color: var(--oracle-border);
  }

  .btn-save {
    padding: 12px 32px;
    background: linear-gradient(135deg, var(--oracle-gold) 0%, #a47631 100%);
    border: none;
    border-radius: 10px;
    font-size: 15px;
    font-weight: 600;
    color: var(--oracle-text);
    cursor: pointer;
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .btn-save:hover:not(:disabled) {
    transform: translateY(-1px);
    box-shadow: 0 4px 15px var(--oracle-gold-glow);
    filter: brightness(1.1);
  }

  .btn-save:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }

  .btn-spinner {
    width: 18px;
    height: 18px;
    border: 2px solid rgba(255, 255, 255, 0.3);
    border-top-color: white;
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
  }

  /* Animations and messages */
  .success-message {
    margin: 24px 0 0 0;
    padding: 14px 20px;
    background: rgba(84, 191, 163, 0.15);
    color: var(--oracle-success);
    border-radius: 10px;
    font-size: 14px;
    text-align: center;
    font-weight: 500;
    border: 1px solid rgba(84, 191, 163, 0.2);
  }

  .error-message {
    margin: 24px 0 0 0;
    padding: 14px 20px;
    background: rgba(207, 110, 91, 0.15);
    color: var(--oracle-danger);
    border-radius: 10px;
    font-size: 14px;
    text-align: center;
    font-weight: 500;
    border: 1px solid rgba(207, 110, 91, 0.2);
  }

  .fade-enter-active,
  .fade-leave-active {
    transition: opacity 0.3s;
  }

  .fade-enter-from,
  .fade-leave-to {
    opacity: 0;
  }

  .animate-slide-up {
    animation: slideUp 0.3s ease-out forwards;
  }

  @keyframes slideUp {
    from {
      opacity: 0;
      transform: translateY(20px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }

  /* Responsive */
  @media (max-width: 900px) {
    .form-grid {
      grid-template-columns: 1fr;
    }
    .form-group.full-width,
    .form-group.flex-row {
      grid-column: span 1;
    }
  }

  @media (max-width: 768px) {
    .content-wrapper {
      padding: 20px;
    }
    
    .settings-form {
      padding: 20px;
    }
  }
  </style>
  ```

- [ ] **Step 2: Verify Vite build compilation**

  Run: `npm run build`
  Expected: Command succeeds with zero compiler/Vite bundle errors.

- [ ] **Step 3: Commit changes**

  ```bash
  git add src/views/Settings.vue
  git commit -m "style: align settings page models/tools config lists and forms with oracle theme"
  ```
