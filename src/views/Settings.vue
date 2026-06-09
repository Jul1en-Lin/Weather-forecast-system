<template>
  <OracleLayout>
    <div class="settings-page">
      <div class="content-wrapper">
        <!-- 标签页切换 -->
        <div class="tab-nav">
          <button
            v-for="tab in tabs"
            :key="tab.id"
            :class="['tab-btn', { active: activeTab === tab.id }]"
            @click="activeTab = tab.id"
          >
            <span class="tab-icon">{{ tab.icon }}</span>
            <span class="tab-text">{{ tab.label }}</span>
          </button>
        </div>

        <!-- 加载状态 -->
        <div v-if="loading" class="loading-container">
          <div class="spinner"></div>
          <p>加载中...</p>
        </div>

        <div v-else>
          <!-- 模型管理 Tab -->
          <div v-show="activeTab === 'models'" class="settings-form">
            <div class="section-header flex-between">
              <div class="flex-align-center">
                <span class="section-icon">🤖</span>
                <span>模型管理</span>
              </div>
              <button v-if="!showModelForm" @click="startAddModel" class="btn-add-model">
                ➕ 添加模型
              </button>
            </div>

            <!-- 添加/编辑模型表单 -->
            <div v-if="showModelForm" class="model-form-card animate-slide-up">
              <h3 class="form-title">{{ isEditingModel ? '编辑模型' : '新增模型' }}</h3>
              <form @submit.prevent="saveModel" class="model-inner-form">
                <div class="form-grid">
                  <div class="form-group">
                    <label>模型唯一 ID (ID)</label>
                    <input
                      v-model="modelForm.id"
                      type="text"
                      placeholder="例如: kimi-k2.5"
                      :disabled="isEditingModel"
                      required
                    />
                  </div>
                  <div class="form-group">
                    <label>模型显示名称</label>
                    <input
                      v-model="modelForm.name"
                      type="text"
                      placeholder="例如: Kimi K2.5"
                      required
                    />
                  </div>
                  <div class="form-group">
                    <label>实际接口模型参数 (model)</label>
                    <input
                      v-model="modelForm.model"
                      type="text"
                      placeholder="例如: kimi-k2.5"
                      required
                    />
                  </div>
                  <div class="form-group">
                    <label>API 接口地址 (base_url)</label>
                    <input
                      v-model="modelForm.base_url"
                      type="text"
                      placeholder="例如: https://api.moonshot.cn/v1"
                    />
                  </div>
                  <div class="form-group">
                    <label>API Key / 密钥</label>
                    <input
                      v-model="modelForm.api_key"
                      type="password"
                      placeholder="不修改或使用系统默认配置请留空"
                      autocomplete="off"
                    />
                    <span v-if="modelForm.masked_api_key" class="current-value">
                      当前生效值: <code>{{ modelForm.masked_api_key }}</code>
                    </span>
                  </div>
                  <div class="form-group">
                    <label>温度参数 (temperature)</label>
                    <input
                      v-model.number="modelForm.temperature"
                      type="number"
                      step="0.1"
                      min="0"
                      max="2"
                      placeholder="留空则使用模型或调用默认"
                    />
                  </div>
                  <div class="form-group flex-row">
                    <label class="checkbox-label">
                      <input v-model="modelForm.supports_tools" type="checkbox" />
                      支持调用天气/预警工具
                    </label>
                  </div>
                  <div class="form-group flex-row">
                    <label class="checkbox-label">
                      <input v-model="modelForm.is_local" type="checkbox" />
                      是本地模型 (Ollama)
                    </label>
                  </div>
                  <div class="form-group full-width">
                    <label>模型描述</label>
                    <textarea
                      v-model="modelForm.description"
                      rows="2"
                      placeholder="模型的简短介绍..."
                    ></textarea>
                  </div>
                </div>
                <div class="form-actions">
                  <button type="button" @click="cancelModelForm" class="btn-reset">取消</button>
                  <button type="submit" class="btn-save" :disabled="modelSaving">
                    <span v-if="modelSaving" class="btn-spinner"></span>
                    <span v-else>保存模型</span>
                  </button>
                </div>
              </form>
            </div>

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
          </div>

          <!-- 天气服务 Tab -->
          <div v-show="activeTab === 'tools'" class="settings-form">
            <div class="section-header flex-between">
              <div class="flex-align-center">
                <span class="section-icon">🌤️</span>
                <span>天气服务与工具管理</span>
              </div>
            </div>

            <!-- 工具编辑表单 -->
            <div v-if="showToolForm" class="model-form-card animate-slide-up">
              <h3 class="form-title">编辑工具配置: {{ toolForm.name }}</h3>
              <form @submit.prevent="saveTool" class="model-inner-form">
                <div class="form-grid">
                  <div class="form-group">
                    <label>工具 ID</label>
                    <input v-model="toolForm.id" type="text" disabled />
                  </div>
                  <div class="form-group">
                    <label>工具名称</label>
                    <input v-model="toolForm.name" type="text" required />
                  </div>
                  <div class="form-group" v-if="toolForm.id === 'alert_query'">
                    <label>和风天气 API Host</label>
                    <input v-model="toolForm.api_host" type="text" placeholder="devapi.qweather.com" />
                  </div>
                  <div class="form-group">
                    <label>API Key / 密钥</label>
                    <input
                      v-model="toolForm.api_key"
                      type="password"
                      placeholder="不修改请留空"
                      autocomplete="off"
                    />
                    <span v-if="toolForm.masked_api_key" class="current-value">
                      当前生效值: <code>{{ toolForm.masked_api_key }}</code>
                    </span>
                  </div>
                  <div class="form-group full-width">
                    <label>工具描述</label>
                    <textarea v-model="toolForm.description" rows="2"></textarea>
                  </div>
                </div>
                <div class="form-actions">
                  <button type="button" @click="showToolForm = false" class="btn-reset">取消</button>
                  <button type="submit" class="btn-save" :disabled="toolSaving">
                    <span v-if="toolSaving" class="btn-spinner"></span>
                    <span v-else>保存配置</span>
                  </button>
                </div>
              </form>
            </div>

            <!-- 工具列表展示 -->
            <div v-else class="models-list-wrapper">
              <div class="models-grid">
                <div v-for="t in toolList" :key="t.id" class="model-card-item">
                  <div class="model-card-header">
                    <div class="model-title-desc">
                      <h4>{{ t.name }}</h4>
                      <span class="model-badge">系统内置</span>
                    </div>
                    <div class="model-card-actions">
                      <button @click="editTool(t)" class="btn-card-action edit-btn">配置 API</button>
                    </div>
                  </div>
                  <div class="model-card-body">
                    <p class="model-desc">{{ t.description || '无描述' }}</p>
                    <div class="model-meta-info">
                      <div class="meta-row">
                        <span class="meta-label">工具 ID:</span>
                        <code class="meta-value">{{ t.id }}</code>
                      </div>
                      <div class="meta-row" v-if="t.id === 'alert_query'">
                        <span class="meta-label">API Host:</span>
                        <span class="meta-value">{{ t.api_host || 'devapi.qweather.com' }}</span>
                      </div>
                      <div class="meta-row">
                        <span class="meta-label">API Key:</span>
                        <span class="meta-value text-truncate" :title="t.masked_api_key || '使用默认/未配置'">
                          {{ t.masked_api_key || '使用默认/未配置' }}
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 消息提示 -->
        <transition name="fade">
          <p v-if="successMessage" class="success-message">{{ successMessage }}</p>
        </transition>
        <transition name="fade">
          <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
        </transition>
      </div>
    </div>
  </OracleLayout>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import OracleLayout from '../layouts/OracleLayout.vue'

const router = useRouter()
const authStore = useAuthStore()

const tabs = [
  { id: 'models', label: '模型管理', icon: '🤖' },
  { id: 'tools', label: '天气服务', icon: '🌤️' },
]

const activeTab = ref('models')

const loading = ref(false)
const successMessage = ref('')
const errorMessage = ref('')

// Model Config interface
interface ModelConfig {
  id: string
  name: string
  description?: string
  model: string
  base_url?: string
  api_key?: string
  masked_api_key?: string
  temperature?: number
  supports_tools: boolean
  is_local: boolean
}

// Tool Config interface
interface ToolConfig {
  id: string
  name: string
  description?: string
  api_key?: string
  masked_api_key?: string
  api_host?: string
}

const modelList = ref<ModelConfig[]>([])
const showModelForm = ref(false)
const isEditingModel = ref(false)
const modelSaving = ref(false)

const modelForm = ref<ModelConfig>({
  id: '',
  name: '',
  description: '',
  model: '',
  base_url: '',
  api_key: '',
  masked_api_key: '',
  temperature: undefined,
  supports_tools: true,
  is_local: false
})

const toolList = ref<ToolConfig[]>([])
const showToolForm = ref(false)
const toolSaving = ref(false)

const toolForm = ref<ToolConfig>({
  id: '',
  name: '',
  description: '',
  api_key: '',
  masked_api_key: '',
  api_host: ''
})

const handleUnauthorized = () => {
  authStore.logout()
  router.push('/login')
}

const fetchConfig = async () => {
  loading.value = true
  try {
    await fetchModels()
    await fetchTools()
  } catch {
    showError('获取配置失败')
  } finally {
    loading.value = false
  }
}

const fetchModels = async () => {
  try {
    const res = await fetch('/api/v1/config/models/', { credentials: 'include' })
    if (res.ok) {
      const data = await res.json()
      modelList.value = data.models
    } else if (res.status === 401) {
      handleUnauthorized()
    }
  } catch (err) {
    showError('获取模型配置失败')
  }
}

const fetchTools = async () => {
  try {
    const res = await fetch('/api/v1/config/tools/', { credentials: 'include' })
    if (res.ok) {
      const data = await res.json()
      toolList.value = data.tools
    } else if (res.status === 401) {
      handleUnauthorized()
    }
  } catch (err) {
    showError('获取天气服务配置失败')
  }
}

const startAddModel = () => {
  isEditingModel.value = false
  modelForm.value = {
    id: '',
    name: '',
    description: '',
    model: '',
    base_url: '',
    api_key: '',
    masked_api_key: '',
    temperature: undefined,
    supports_tools: true,
    is_local: false
  }
  showModelForm.value = true
}

const editModel = (model: ModelConfig) => {
  isEditingModel.value = true
  modelForm.value = {
    id: model.id,
    name: model.name,
    description: model.description || '',
    model: model.model,
    base_url: model.base_url || '',
    api_key: '', // Secure placeholder
    masked_api_key: model.masked_api_key || '',
    temperature: model.temperature ?? undefined,
    supports_tools: model.supports_tools,
    is_local: model.is_local
  }
  showModelForm.value = true
}

const cancelModelForm = () => {
  showModelForm.value = false
}

const saveModel = async () => {
  modelSaving.value = true
  errorMessage.value = ''
  successMessage.value = ''

  try {
    const payload = { ...modelForm.value }
    if (!payload.base_url) delete payload.base_url
    if (!payload.api_key) delete payload.api_key
    if (payload.temperature === undefined || payload.temperature === null || isNaN(payload.temperature)) {
      delete payload.temperature
    }

    const url = isEditingModel.value 
      ? `/api/v1/config/models/${payload.id}` 
      : '/api/v1/config/models/'
      
    const method = isEditingModel.value ? 'PUT' : 'POST'

    const res = await fetch(url, {
      method: method,
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify(payload)
    })

    if (res.ok) {
      showSuccess(isEditingModel.value ? '模型已成功更新' : '模型已成功添加')
      showModelForm.value = false
      await fetchModels()
    } else {
      const data = await res.json()
      showError(data.detail || '保存模型失败')
    }
  } catch (err) {
    showError('保存模型出错，请检查网络连接')
  } finally {
    modelSaving.value = false
  }
}

const confirmDeleteModel = async (model: ModelConfig) => {
  if (confirm(`确认要删除模型 "${model.name}" 吗？`)) {
    try {
      const res = await fetch(`/api/v1/config/models/${model.id}`, {
        method: 'DELETE',
        credentials: 'include'
      })
      if (res.ok) {
        showSuccess('模型已成功删除')
        await fetchModels()
      } else {
        const data = await res.json()
        showError(data.detail || '删除模型失败')
      }
    } catch {
      showError('删除模型出错')
    }
  }
}

const editTool = (tool: ToolConfig) => {
  toolForm.value = {
    id: tool.id,
    name: tool.name,
    description: tool.description || '',
    api_key: '', // Secure placeholder
    masked_api_key: tool.masked_api_key || '',
    api_host: tool.api_host || ''
  }
  showToolForm.value = true
}

const saveTool = async () => {
  toolSaving.value = true
  errorMessage.value = ''
  successMessage.value = ''

  try {
    const payload = { ...toolForm.value }
    if (!payload.api_key) delete payload.api_key
    if (!payload.api_host) delete payload.api_host

    const res = await fetch(`/api/v1/config/tools/${payload.id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify(payload)
    })

    if (res.ok) {
      showSuccess('天气服务工具已成功更新')
      showToolForm.value = false
      await fetchTools()
    } else {
      const data = await res.json()
      showError(data.detail || '保存工具配置失败')
    }
  } catch (err) {
    showError('保存配置出错，请检查网络连接')
  } finally {
    toolSaving.value = false
  }
}

const showSuccess = (msg: string) => {
  successMessage.value = msg
  setTimeout(() => { successMessage.value = '' }, 3000)
}

const showError = (msg: string) => {
  errorMessage.value = msg
  setTimeout(() => { errorMessage.value = '' }, 4000)
}

onMounted(fetchConfig)
</script>

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
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(15px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 12px;
  font-size: 16px;
  font-weight: 500;
  color: #1d1d1f;
  cursor: pointer;
  transition: all 0.3s ease;
}

.tab-btn:hover {
  background: rgba(255, 255, 255, 0.35);
  transform: translateY(-2px);
}

.tab-btn.active {
  background: #007aff;
  border-color: #007aff;
  color: white;
}

.tab-icon {
  font-size: 22px;
}

/* Spinner */
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 0;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid rgba(255, 255, 255, 0.3);
  border-top-color: #007aff;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin-bottom: 16px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Configurations Form Card */
.settings-form {
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(15px);
  border-radius: 20px;
  padding: 40px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.config-section {
  margin-bottom: 40px;
}

.section-header {
  display: flex;
  align-items: center;
  font-size: 22px;
  font-weight: 600;
  color: #1d1d1f;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}

.flex-between {
  justify-content: space-between;
}

.flex-align-center {
  display: flex;
  align-items: center;
  gap: 12px;
}

.section-icon {
  font-size: 28px;
}

.config-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 20px;
}

.config-card {
  background: rgba(255, 255, 255, 0.3);
  border-radius: 16px;
  padding: 24px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.04);
}

.config-card label {
  display: block;
  font-size: 14px;
  font-weight: 600;
  color: #1d1d1f;
  margin-bottom: 10px;
}

.config-card input {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid rgba(0, 0, 0, 0.15);
  border-radius: 10px;
  font-size: 15px;
  background: rgba(255, 255, 255, 0.8);
  transition: all 0.3s ease;
  box-sizing: border-box;
}

.config-card input:focus {
  outline: none;
  border-color: #007aff;
  box-shadow: 0 0 0 3px rgba(0, 122, 255, 0.1);
}

.current-value {
  display: block;
  margin-top: 10px;
  font-size: 12px;
  color: #86868b;
}

/* Add model button */
.btn-add-model {
  background: #007aff;
  color: white;
  border-radius: 10px;
  padding: 10px 20px;
  font-size: 15px;
  font-weight: 600;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(0, 122, 255, 0.2);
}

.btn-add-model:hover {
  transform: translateY(-1px);
  box-shadow: 0 6px 16px rgba(0, 122, 255, 0.3);
}

/* Models Grid / Cards */
.models-list-wrapper {
  margin-top: 10px;
}

.empty-models {
  text-align: center;
  padding: 60px 0;
  color: #86868b;
  font-size: 16px;
}

.models-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
  gap: 24px;
}

.model-card-item {
  background: rgba(255, 255, 255, 0.45);
  backdrop-filter: blur(10px);
  border-radius: 18px;
  border: 1px solid rgba(255, 255, 255, 0.5);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.04);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.model-card-item:hover {
  transform: translateY(-4px);
  background: rgba(255, 255, 255, 0.6);
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.1);
  border-color: rgba(0, 122, 255, 0.2);
}

.model-card-header {
  padding: 20px 24px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.model-title-desc h4 {
  font-size: 18px;
  font-weight: 600;
  color: #1d1d1f;
  margin: 0 0 6px 0;
}

.model-badge {
  display: inline-block;
  padding: 4px 10px;
  border-radius: 6px;
  font-size: 11px;
  font-weight: 600;
  background: rgba(0, 122, 255, 0.1);
  color: #007aff;
}

.model-badge.local-badge {
  background: rgba(52, 199, 89, 0.1);
  color: #34c759;
}

.model-card-actions {
  display: flex;
  gap: 8px;
}

.btn-card-action {
  font-size: 13px;
  padding: 6px 12px;
  border-radius: 8px;
  font-weight: 500;
  transition: all 0.2s ease;
}

.btn-card-action.edit-btn {
  background: rgba(0, 0, 0, 0.05);
  color: #1d1d1f;
}

.btn-card-action.edit-btn:hover {
  background: rgba(0, 0, 0, 0.1);
}

.btn-card-action.delete-btn {
  background: rgba(255, 59, 48, 0.1);
  color: #ff3b30;
}

.btn-card-action.delete-btn:hover {
  background: rgba(255, 59, 48, 0.2);
}

.model-card-body {
  padding: 24px;
  display: flex;
  flex-direction: column;
  flex: 1;
}

.model-desc {
  font-size: 14px;
  color: #86868b;
  margin: 0 0 20px 0;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  height: 42px;
}

.model-meta-info {
  background: rgba(0, 0, 0, 0.02);
  border-radius: 12px;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.meta-row {
  display: flex;
  font-size: 13px;
  line-height: 1.4;
}

.meta-label {
  color: #86868b;
  width: 80px;
  font-weight: 500;
  flex-shrink: 0;
}

.meta-value {
  color: #1d1d1f;
  word-break: break-all;
  font-family: inherit;
}

.meta-value.text-truncate {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

code.meta-value {
  font-family: SFMono-Regular, Consolas, 'Liberation Mono', Menlo, monospace;
  background: rgba(0, 0, 0, 0.05);
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 12px;
}

/* Model Form Card */
.model-form-card {
  background: rgba(255, 255, 255, 0.45);
  border-radius: 20px;
  padding: 30px;
  border: 1px solid rgba(255, 255, 255, 0.5);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
}

.form-title {
  font-size: 18px;
  font-weight: 600;
  color: #1d1d1f;
  margin-bottom: 20px;
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
  color: #1d1d1f;
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
}

.form-group input[type="text"],
.form-group input[type="number"],
.form-group input[type="password"],
.form-group textarea {
  padding: 12px 14px;
  border: 1px solid rgba(0, 0, 0, 0.15);
  border-radius: 10px;
  font-size: 14px;
  background: white;
  transition: all 0.2s ease;
}

.form-group input:focus,
.form-group textarea:focus {
  border-color: #007aff;
  box-shadow: 0 0 0 3px rgba(0, 122, 255, 0.1);
  outline: none;
}

/* Actions buttons styling */
.form-actions {
  display: flex;
  justify-content: center;
  gap: 16px;
  margin-top: 32px;
  padding-top: 24px;
  border-top: 1px solid rgba(0, 0, 0, 0.05);
}

.btn-reset {
  padding: 12px 30px;
  background: white;
  border: 1px solid #d2d2d7;
  border-radius: 10px;
  font-size: 15px;
  font-weight: 500;
  color: #1d1d1f;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-reset:hover {
  background: #f5f5f7;
}

.btn-save {
  padding: 12px 32px;
  background: linear-gradient(135deg, #007aff 0%, #0056cc 100%);
  border: none;
  border-radius: 10px;
  font-size: 15px;
  font-weight: 600;
  color: white;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(0, 122, 255, 0.2);
  display: flex;
  align-items: center;
  gap: 8px;
}

.btn-save:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 6px 16px rgba(0, 122, 255, 0.3);
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
  background: rgba(52, 199, 89, 0.15);
  color: #34c759;
  border-radius: 10px;
  font-size: 14px;
  text-align: center;
  font-weight: 500;
}

.error-message {
  margin: 24px 0 0 0;
  padding: 14px 20px;
  background: rgba(255, 59, 48, 0.15);
  color: #ff3b30;
  border-radius: 10px;
  font-size: 14px;
  text-align: center;
  font-weight: 500;
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
