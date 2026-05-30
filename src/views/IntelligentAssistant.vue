<template>
  <div class="assistant-container">
    <!-- 左侧导航栏（保留原有样式） -->
    <aside class="sidebar">
      <div class="sidebar-header">
        <div class="logo">
          <span class="logo-icon">🌤️</span>
        </div>
        <h2 class="platform-name">气象平台</h2>
      </div>
      
      <nav class="nav-menu">
        <router-link to="/home" class="nav-item" active-class="active">
          <span class="nav-icon">🏠</span>
          <span class="nav-text">首页</span>
        </router-link>

        <router-link to="/intelligent-assistant" class="nav-item" active-class="active">
          <span class="nav-icon">🤖</span>
          <span class="nav-text">智能助手</span>
        </router-link>

        <router-link v-if="isAdmin" to="/settings" class="nav-item" active-class="active">
          <span class="nav-icon">⚙️</span>
          <span class="nav-text">系统设置</span>
        </router-link>

        <router-link v-if="isAdmin" to="/admin/users" class="nav-item" active-class="active">
          <span class="nav-icon">👥</span>
          <span class="nav-text">用户管理</span>
        </router-link>
      </nav>
      
      <div class="sidebar-footer">
        <div class="user-info">
          <div class="user-avatar">
            {{ userInitial }}
          </div>
          <div class="user-details">
            <p class="username">{{ username }}</p>
            <p class="user-role">{{ isAdmin ? '管理员' : '普通用户' }}</p>
          </div>
        </div>
        <button @click="handleLogout" class="logout-button">
          退出登录
        </button>
      </div>
    </aside>
    
    <!-- 右侧主内容区（智能助手完整功能） -->
    <main class="main-content">
      <div class="chat-layout">
        <!-- 历史对话侧边栏 -->
        <aside class="history-sidebar">
          <div v-if="isBatchMode" class="batch-actions-container">
            <button class="batch-action-btn select-all-btn" @click="selectAllConversations">
              {{ isAllSelected ? '取消全选' : '全选' }}
            </button>
            <button
              class="batch-action-btn batch-delete-btn"
              :disabled="selectedConvIds.length === 0"
              @click="batchDeleteConversations"
            >
              🗑️ 删除 ({{ selectedConvIds.length }})
            </button>
          </div>
          <div v-else class="new-chat-btn" @click="createNewChat">✨ 新建对话</div>
          
          <div class="history-sidebar-header">
            <span class="history-title">📋 历史对话</span>
            <button class="batch-toggle-btn" @click="toggleBatchMode">
              {{ isBatchMode ? '取消' : '批量操作' }}
            </button>
          </div>
          
          <div class="conversation-list">
            <div
              v-for="conv in conversations"
              :key="conv.id"
              class="conversation-item"
              :class="{
                active: !isBatchMode && conv.id === currentConvId,
                selected: isBatchMode && selectedConvIds.includes(conv.id)
              }"
              @click="handleConvItemClick(conv.id)"
            >
              <div
                v-if="isBatchMode"
                class="custom-checkbox"
                :class="{ checked: selectedConvIds.includes(conv.id) }"
                @click.stop="toggleSelectConv(conv.id)"
              ></div>
              <span class="conv-title">{{ conv.title || '未命名' }}</span>
              <div v-if="!isBatchMode" class="conv-actions">
                <button class="action-btn rename-btn" @click.stop="renameConversationPrompt(conv.id, conv.title)">✏️</button>
                <button class="action-btn delete-btn" @click.stop="deleteConversation(conv.id)">🗑️</button>
              </div>
            </div>
          </div>
        </aside>

        <!-- 聊天主区域 -->
        <div class="chat-wrapper">
          <div class="chat-header">
            <div class="header-content">
              <div class="assistant-avatar">
                🤖
              </div>
              <div class="header-info">
                <h1>气象智能助手</h1>
                <p>基于大语言模型的智能气象问答系统</p>
              </div>
            </div>
            <div class="toolbar">
              <select v-model="selectedModel">
                <option v-for="m in models" :key="m.id" :value="m.id">{{ m.name }}</option>
              </select>
            </div>
          </div>
          
          <div class="chat-messages" ref="messagesContainer">
            <div v-if="currentMessages.length === 0" class="empty-state">
              <div class="empty-icon">🤖</div>
              <h2>开始对话</h2>
              <p>我是气象智能助手，可以帮助您解答气象相关问题</p>
              <div class="suggestion-chips">
                <button @click="sendSuggestion('今天天气怎么样？')" class="chip">
                  今天天气怎么样？
                </button>
                <button @click="sendSuggestion('明天的温度是多少？')" class="chip">
                  明天的温度是多少？
                </button>
                <button @click="sendSuggestion('如何预防暴雨灾害？')" class="chip">
                  如何预防暴雨灾害？
                </button>
              </div>
            </div>
            
            <div v-for="(msg, idx) in currentMessages" :key="idx" 
                 class="message" 
                 :class="{ 'user-message': msg.role === 'user', 'assistant-message': msg.role === 'assistant' }">
              <div class="message-avatar">
                {{ msg.role === 'user' ? userInitial : '🤖' }}
              </div>
              <div class="message-content">
                <div class="message-text" v-html="msg.role === 'assistant' ? renderMarkdown(msg.content) : msg.content"></div>
                <div class="message-time">{{ msg.time }}</div>
              </div>
            </div>
            
            <div v-if="isTyping" class="message assistant-message">
              <div class="message-avatar">
                🤖
              </div>
              <div class="message-content">
                <div class="message-text typing">
                  <span class="dot"></span>
                  <span class="dot"></span>
                  <span class="dot"></span>
                </div>
              </div>
            </div>
          </div>
          
          <div class="chat-input-container">
            <div class="input-wrapper">
              <input
                v-model="inputMessage"
                @keyup.enter="sendMessage"
                type="text"
                placeholder="输入您的问题..."
                class="chat-input"
                :disabled="isTyping"
              />
              <button @click="sendMessage" 
                      class="send-button" 
                      :disabled="!inputMessage.trim() || isTyping">
                发送
              </button>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, nextTick, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { marked } from 'marked'
import DOMPurify from 'dompurify'

const API_BASE = ''  // 使用相对路径，通过 Vite 代理转发到后端

function renderMarkdown(content: string): string {
  if (!content) return ''
  const rawHtml = marked.parse(content, { async: false }) as string
  return DOMPurify.sanitize(rawHtml)
}

interface Message {
  role: 'user' | 'assistant'
  content: string
  time: string
}

interface Conversation {
  id: string
  title: string
  model_id: string
}

interface ModelOption {
  id: string
  name: string
  description: string
}

// 认证
const router = useRouter()
const authStore = useAuthStore()
const username = computed(() => authStore.username)
const isAdmin = computed(() => authStore.isAdmin)
const userInitial = computed(() => {
  const name = username.value
  return name ? name.charAt(0).toUpperCase() : 'U'
})

// 数据
const conversations = ref<Conversation[]>([])
const currentConvId = ref<string | null>(null)
const inputMessage = ref('')
const isTyping = ref(false)
const messagesContainer = ref<HTMLElement | null>(null)
const currentMessages = ref<Message[]>([])

// 批量操作
const isBatchMode = ref(false)
const selectedConvIds = ref<string[]>([])

const isAllSelected = computed(() => {
  return conversations.value.length > 0 && selectedConvIds.value.length === conversations.value.length
})

function toggleBatchMode() {
  isBatchMode.value = !isBatchMode.value
  selectedConvIds.value = []
}

function selectAllConversations() {
  if (isAllSelected.value) {
    selectedConvIds.value = []
  } else {
    selectedConvIds.value = conversations.value.map(c => c.id)
  }
}

function toggleSelectConv(id: string) {
  const index = selectedConvIds.value.indexOf(id)
  if (index > -1) {
    selectedConvIds.value.splice(index, 1)
  } else {
    selectedConvIds.value.push(id)
  }
}

function handleConvItemClick(id: string) {
  if (isBatchMode.value) {
    toggleSelectConv(id)
  } else {
    switchConversation(id)
  }
}

async function batchDeleteConversations() {
  if (selectedConvIds.value.length === 0) return
  
  const count = selectedConvIds.value.length
  if (!confirm(`确定要删除选中的 ${count} 个对话吗？`)) {
    return
  }
  
  try {
    await apiFetch('/api/v1/assistant/conversations/batch-delete', {
      method: 'POST',
      body: JSON.stringify({ conversation_ids: selectedConvIds.value }),
    })
    
    // 从本地状态移除已删除的对话
    conversations.value = conversations.value.filter(c => !selectedConvIds.value.includes(c.id))
    
    // 如果当前选中的对话被删除了，切换到剩余的第一个
    if (selectedConvIds.value.includes(currentConvId.value || '')) {
      if (conversations.value.length > 0) {
        currentConvId.value = conversations.value[0].id
        await loadMessages(currentConvId.value)
      } else {
        currentConvId.value = null
        currentMessages.value = []
        await createNewChat()
      }
    }
    
    selectedConvIds.value = []
    isBatchMode.value = false
  } catch (error) {
    alert('批量删除失败，请重试')
  }
}

// 选择
const models = ref<ModelOption[]>([])
const selectedModel = ref('')

watch(selectedModel, (newVal) => {
  if (currentConvId.value && newVal) {
    localStorage.setItem(`conv_model_${currentConvId.value}`, newVal)
  }
})

// 辅助
function formatTime(): string {
  const now = new Date()
  const h = String(now.getHours()).padStart(2, '0')
  const m = String(now.getMinutes()).padStart(2, '0')
  return `${h}:${m}`
}

function fmtTimeFromDate(dateStr: string): string {
  const d = new Date(dateStr)
  const h = String(d.getHours()).padStart(2, '0')
  const m = String(d.getMinutes()).padStart(2, '0')
  return `${h}:${m}`
}

function scrollToBottom() {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
  })
}

function handleUnauthorized() {
  authStore.isAuthenticated = false
  authStore.user = null
  router.push('/login')
}

async function apiFetch(path: string, opts?: RequestInit) {
  const res = await fetch(`${API_BASE}${path}`, {
    credentials: 'include',
    headers: { 'Content-Type': 'application/json', ...(opts?.headers || {}) },
    ...opts,
  })
  if (!res.ok) {
    if (res.status === 401) {
      handleUnauthorized()
      throw new Error('登录已过期')
    }
    const text = await res.text().catch(() => res.statusText)
    throw new Error(`${res.status}: ${text}`)
  }
  return res.json()
}

// 加载模型
async function loadModels() {
  const data = await apiFetch('/api/v1/assistant/models')
  models.value = data.models
  if (models.value.length > 0 && !selectedModel.value) {
    selectedModel.value = models.value[0].id
  }
}

async function ensureSelectedModel(): Promise<boolean> {
  if (selectedModel.value) return true
  if (models.value.length === 0) {
    await loadModels()
  }
  if (models.value.length === 0) {
    alert('暂无可用模型，请先联系管理员配置模型')
    return false
  }
  selectedModel.value = models.value[0].id
  return true
}

// 加载对话
async function loadConversations() {
  const data = await apiFetch('/api/v1/assistant/conversations')
  conversations.value = data.conversations
  if (!currentConvId.value && conversations.value.length > 0) {
    currentConvId.value = conversations.value[0].id
    await loadMessages(currentConvId.value)
  } else if (conversations.value.length === 0) {
    await createNewChat()
  }
}

// 加载消息
async function loadMessages(convId: string) {
  const data = await apiFetch(`/api/v1/assistant/conversations/${convId}`)
  const localModel = localStorage.getItem(`conv_model_${convId}`)
  if (localModel) {
    selectedModel.value = localModel
  } else if (data.model_id) {
    selectedModel.value = data.model_id
  }
  currentMessages.value = data.messages.map((m: { role: string; content: string; created_at?: string }) => ({
    role: m.role as 'user' | 'assistant',
    content: m.content,
    time: m.created_at ? fmtTimeFromDate(m.created_at) : formatTime(),
  }))
  scrollToBottom()
}

// 对话操作
async function createNewChat(): Promise<boolean> {
  if (!(await ensureSelectedModel())) return false
  const data = await apiFetch('/api/v1/assistant/conversations', {
    method: 'POST',
    body: JSON.stringify({ title: '新对话', model_id: selectedModel.value }),
  })
  conversations.value.unshift(data)
  currentConvId.value = data.id
  currentMessages.value = []
  scrollToBottom()
  return true
}

async function switchConversation(id: string) {
  if (currentConvId.value === id) return
  currentConvId.value = id
  const localModel = localStorage.getItem(`conv_model_${id}`)
  if (localModel) {
    selectedModel.value = localModel
  } else {
    const conv = conversations.value.find(c => c.id === id)
    if (conv && conv.model_id) {
      selectedModel.value = conv.model_id
    }
  }
  await loadMessages(id)
}

async function deleteConversation(id: string) {
  if (conversations.value.length === 1) {
    alert('不能删除最后一个对话')
    return
  }
  await apiFetch(`/api/v1/assistant/conversations/${id}`, { method: 'DELETE' })
  const idx = conversations.value.findIndex(c => c.id === id)
  if (idx !== -1) {
    conversations.value.splice(idx, 1)
    if (currentConvId.value === id) {
      currentConvId.value = conversations.value[0]?.id || null
      if (currentConvId.value) {
        await loadMessages(currentConvId.value)
      } else {
        currentMessages.value = []
      }
    }
  }
}

// SSE 流式对话
async function streamChat(userMessage: string, onChunk: (chunk: string) => void, onEnd: () => void) {
  const res = await fetch(`${API_BASE}/api/v1/assistant/chat/stream`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',
    body: JSON.stringify({
      model_id: selectedModel.value,
      message: userMessage,
      conversation_id: currentConvId.value,
    }),
  })
  if (!res.ok) {
    if (res.status === 401) {
      handleUnauthorized()
      throw new Error('登录已过期')
    }
    throw new Error('请求失败')
  }
  const reader = res.body!.getReader()
  const decoder = new TextDecoder()
  let buffer = ''
  while (true) {
    const { done, value } = await reader.read()
    if (done) break
    buffer += decoder.decode(value, { stream: true })
    const chunks = buffer.split('\n\n')
    buffer = chunks.pop() || ''
    for (const chunk of chunks) {
      const lines = chunk.trim().split('\n')
      for (const line of lines) {
        if (line.startsWith('data: ')) {
          const data = line.slice(6)
          if (data === '[DONE]') {
            onEnd()
            return
          }
          try {
            const parsed = JSON.parse(data)
            if (parsed.chunk) onChunk(parsed.chunk)
          } catch {
            // ignore
          }
        }
      }
    }
  }
  onEnd()
}

// 请求后端进行 AI 标题总结并重命名
async function triggerAiSummarize(id: string) {
  try {
    const data = await apiFetch(`/api/v1/assistant/conversations/${id}/summarize`, {
      method: 'POST'
    })
    if (data.title) {
      const conv = conversations.value.find(c => c.id === id)
      if (conv) {
        conv.title = data.title
      }
    }
  } catch (e) {
    // 自动总结重命名静默失败
  }
}

// 手动重命名对话
async function renameConversationPrompt(id: string, oldTitle: string) {
  const newTitle = prompt('请输入新的对话名称：', oldTitle)
  if (newTitle === null) return
  const trimmed = newTitle.trim()
  if (!trimmed) {
    alert('对话名称不能为空')
    return
  }
  try {
    await apiFetch(`/api/v1/assistant/conversations/${id}`, {
      method: 'PUT',
      body: JSON.stringify({ title: trimmed }),
    })
    const conv = conversations.value.find(c => c.id === id)
    if (conv) {
      conv.title = trimmed
    }
  } catch {
    alert('重命名对话失败')
  }
}

// 发送消息
async function sendMessage() {
  if (!inputMessage.value.trim() || isTyping.value) return
  const userText = inputMessage.value.trim()
  inputMessage.value = ''

  if (!currentConvId.value) {
    const created = await createNewChat()
    if (!created) return
  }

  currentMessages.value.push({ role: 'user', content: userText, time: formatTime() })
  scrollToBottom()

  const assistantIdx = currentMessages.value.length
  currentMessages.value.push({ role: 'assistant', content: '', time: formatTime() })
  scrollToBottom()

  isTyping.value = true
  let accumulated = ''

  try {
    await streamChat(userText,
      (chunk) => {
        accumulated += chunk
        currentMessages.value[assistantIdx].content = accumulated
        scrollToBottom()
      },
      () => {
        isTyping.value = false
        // 流式会话顺利结束后，若为默认标题则触发 AI 自动总结
        const currentConv = conversations.value.find(c => c.id === currentConvId.value)
        if (currentConv && currentConv.title === '新对话') {
          triggerAiSummarize(currentConvId.value!)
        }
      }
    )
  } catch (e) {
    currentMessages.value[assistantIdx].content =
      e instanceof Error && e.message === '登录已过期'
        ? '登录已过期，请重新登录。'
        : '服务暂时不可用，请稍后重试。'
    isTyping.value = false
  }
}

function sendSuggestion(text: string) {
  inputMessage.value = text
  sendMessage()
}

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}

// 初始化
onMounted(async () => {
  try {
    await loadModels()
    await loadConversations()
  } catch {
    // 401 已在 apiFetch 中处理，其它初始化错误保持静默
  }
})
</script>

<style scoped>
/* 原有样式保留，新增样式适配 */
.assistant-container {
  display: flex;
  min-height: 100vh;
  background-image: url('/background.jpg');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  position: relative;
}

.assistant-container::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.3);
  backdrop-filter: blur(2px);
  z-index: 0;
}

/* 左侧导航栏样式（与Home.vue一致） */
.sidebar {
  width: 260px;
  background: rgba(255, 255, 255, 0.4);
  backdrop-filter: blur(15px);
  border-right: 1px solid rgba(255, 255, 255, 0.2);
  display: flex;
  flex-direction: column;
  box-shadow: 2px 0 15px rgba(0, 0, 0, 0.1);
  position: fixed;
  height: 100vh;
  left: 0;
  top: 0;
  z-index: 10;
}

.sidebar-header {
  padding: 30px 20px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}

.logo {
  display: flex;
  justify-content: center;
  margin-bottom: 12px;
}

.logo-icon {
  font-size: 40px;
}

.platform-name {
  font-size: 18px;
  font-weight: 600;
  color: #1d1d1f;
  margin: 0;
  text-align: center;
}

.nav-menu {
  flex: 1;
  padding: 20px 12px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 16px;
  border-radius: 12px;
  text-decoration: none;
  color: #1d1d1f;
  font-size: 15px;
  font-weight: 500;
  transition: all 0.3s ease;
  cursor: pointer;
}

.nav-item:hover {
  background: rgba(0, 0, 0, 0.05);
}

.nav-item.active {
  background: #007aff;
  color: white;
}

.nav-icon {
  font-size: 20px;
}

.nav-text {
  flex: 1;
}

.sidebar-footer {
  padding: 20px;
  border-top: 1px solid rgba(0, 0, 0, 0.05);
}

.user-info {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  font-weight: 600;
}

.user-details {
  flex: 1;
}

.username {
  margin: 0;
  font-size: 14px;
  font-weight: 600;
  color: #1d1d1f;
}

.user-role {
  margin: 0;
  font-size: 12px;
  color: #86868b;
}

.logout-button {
  width: 100%;
  padding: 12px;
  background: #f5f5f7;
  border: none;
  border-radius: 10px;
  color: #1d1d1f;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.logout-button:hover {
  background: #e8e8ed;
}

.main-content {
  flex: 1;
  margin-left: 260px;
  padding: 20px;
  min-height: 100vh;
  background-image: url('/background.jpg');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  position: relative;
}

.main-content::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.3);
  backdrop-filter: blur(2px);
  z-index: 0;
}

.chat-layout {
  display: flex;
  gap: 20px;
  height: calc(100vh - 40px);
  position: relative;
  z-index: 1;
}

/* 历史对话侧边栏 */
.history-sidebar {
  width: 260px;
  background: rgba(255, 255, 255, 0.4);
  backdrop-filter: blur(15px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 16px;
  display: flex;
  flex-direction: column;
  padding: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  overflow-y: auto;
}

.new-chat-btn {
  background: #10a37f;
  color: white;
  text-align: center;
  padding: 12px;
  border-radius: 12px;
  cursor: pointer;
  font-size: 16px;
  font-weight: 500;
  margin-bottom: 20px;
  transition: background 0.2s;
}

.new-chat-btn:hover {
  background: #0e8e6e;
}

.history-sidebar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.history-title {
  font-size: 14px;
  color: #6e6e6e;
  margin: 0;
  font-weight: 500;
}

.batch-toggle-btn {
  background: none;
  border: none;
  font-size: 12px;
  color: #007aff;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 6px;
  transition: background-color 0.2s;
}

.batch-toggle-btn:hover {
  background-color: rgba(0, 122, 255, 0.1);
}

.batch-actions-container {
  display: flex;
  gap: 8px;
  margin-bottom: 20px;
}

.batch-action-btn {
  flex: 1;
  padding: 10px;
  border-radius: 12px;
  border: none;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
}

.select-all-btn {
  background: rgba(0, 0, 0, 0.05);
  color: #1d1d1f;
}

.select-all-btn:hover {
  background: rgba(0, 0, 0, 0.1);
}

.batch-delete-btn {
  background: #ff3b30;
  color: white;
}

.batch-delete-btn:hover:not(:disabled) {
  background: #d63027;
}

.batch-delete-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.conversation-item.selected {
  background: rgba(16, 163, 127, 0.1);
  border-color: rgba(16, 163, 127, 0.4);
}

.custom-checkbox {
  width: 18px;
  height: 18px;
  border-radius: 50%;
  border: 1.5px solid rgba(0, 0, 0, 0.2);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  margin-right: 8px;
  flex-shrink: 0;
  transition: all 0.2s ease;
  background: white;
}

.custom-checkbox.checked {
  background: #10a37f;
  border-color: #10a37f;
}

.custom-checkbox.checked::after {
  content: '✓';
  color: white;
  font-size: 11px;
  font-weight: bold;
}

.conversation-list {
  flex: 1;
  overflow-y: auto;
}

.conversation-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 12px;
  margin-bottom: 6px;
  border-radius: 10px;
  cursor: pointer;
  background: rgba(255, 255, 255, 0.5);
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.conversation-item.active {
  background: #e2f0e6;
  border-color: #10a37f;
}

.conv-title {
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-size: 14px;
}

.conv-actions {
  display: flex;
  gap: 4px;
}

.action-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 14px;
  color: #aaa;
  transition: color 0.2s ease;
  padding: 2px;
}

.rename-btn:hover {
  color: #007aff;
}

.delete-btn:hover {
  color: #e5484d;
}

/* 聊天主区域 */
.chat-wrapper {
  flex: 1;
  background: rgba(255, 255, 255, 0.4);
  backdrop-filter: blur(15px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 16px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.chat-header {
  padding: 20px 24px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  background: transparent;
}

.header-content {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 12px;
}

.assistant-avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
}

.header-info h1 {
  font-size: 20px;
  font-weight: 600;
  color: #1d1d1f;
  margin: 0 0 4px 0;
}

.header-info p {
  font-size: 13px;
  color: #86868b;
  margin: 0;
}

.toolbar {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  margin-top: 8px;
}

.toolbar select {
  padding: 6px 12px;
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  font-size: 14px;
  background: rgba(255, 255, 255, 0.5);
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 20px;
  background: transparent;
}

.empty-state {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 40px 20px;
}

.empty-icon {
  font-size: 80px;
  margin-bottom: 24px;
  animation: float 3s ease-in-out infinite;
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

.empty-state h2 {
  font-size: 24px;
  font-weight: 600;
  color: #1d1d1f;
  margin: 0 0 12px 0;
}

.empty-state p {
  font-size: 15px;
  color: #86868b;
  margin: 0 0 30px 0;
}

.suggestion-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  justify-content: center;
}

.chip {
  padding: 12px 20px;
  background: rgba(255, 255, 255, 0.5);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 20px;
  color: #1d1d1f;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.chip:hover {
  background: #007aff;
  color: white;
  border-color: #007aff;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 122, 255, 0.3);
}

.message {
  display: flex;
  gap: 16px;
  animation: slideIn 0.3s ease-out;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.user-message {
  flex-direction: row-reverse;
}

.message-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  font-weight: 600;
  flex-shrink: 0;
}

.assistant-message .message-avatar {
  background: linear-gradient(135deg, #007aff 0%, #0056cc 100%);
}

.message-content {
  max-width: 70%;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.user-message .message-content {
  align-items: flex-end;
}

.message-text {
  padding: 14px 18px;
  border-radius: 18px;
  font-size: 15px;
  line-height: 1.6;
  word-break: break-word;
}

.user-message .message-text {
  background: #007aff;
  color: white;
  border-bottom-right-radius: 6px;
}

.assistant-message .message-text {
  background: rgba(255, 255, 255, 0.7);
  color: #1d1d1f;
  border-bottom-left-radius: 6px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.assistant-message .message-text :deep(strong) {
  font-weight: 600;
}

.assistant-message .message-text :deep(ul),
.assistant-message .message-text :deep(ol) {
  margin: 8px 0;
  padding-left: 20px;
}

.assistant-message .message-text :deep(li) {
  margin: 4px 0;
}

.assistant-message .message-text :deep(code) {
  background: #f5f5f7;
  padding: 2px 6px;
  border-radius: 4px;
  font-family: 'SF Mono', Monaco, monospace;
  font-size: 13px;
}

.assistant-message .message-text :deep(pre) {
  background: #f5f5f7;
  padding: 12px;
  border-radius: 8px;
  overflow-x: auto;
  margin: 8px 0;
}

.assistant-message .message-text :deep(pre code) {
  background: transparent;
  padding: 0;
}

.assistant-message .message-text :deep(blockquote) {
  border-left: 3px solid #d1d1d6;
  margin: 8px 0;
  padding-left: 12px;
  color: #6e6e73;
}

.assistant-message .message-text :deep(p) {
  margin: 6px 0;
}

.assistant-message .message-text :deep(p:first-child) {
  margin-top: 0;
}

.assistant-message .message-text :deep(p:last-child) {
  margin-bottom: 0;
}

.message-time {
  font-size: 12px;
  color: #86868b;
}

.typing {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 14px 18px;
}

.dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #86868b;
  animation: bounce 1.4s ease-in-out infinite;
}

.dot:nth-child(1) { animation-delay: 0s; }
.dot:nth-child(2) { animation-delay: 0.2s; }
.dot:nth-child(3) { animation-delay: 0.4s; }

@keyframes bounce {
  0%, 60%, 100% { transform: translateY(0); }
  30% { transform: translateY(-6px); }
}

.chat-input-container {
  padding: 20px 24px 24px;
  background: transparent;
  border-top: 1px solid rgba(255, 255, 255, 0.2);
}

.input-wrapper {
  display: flex;
  gap: 12px;
  align-items: center;
}

.chat-input {
  flex: 1;
  padding: 14px 20px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 24px;
  font-size: 15px;
  outline: none;
  transition: all 0.3s ease;
  background: rgba(255, 255, 255, 0.6);
}

.chat-input:focus {
  border-color: #007aff;
  background: rgba(255, 255, 255, 0.85);
  box-shadow: 0 0 0 3px rgba(0, 122, 255, 0.1);
}

.send-button {
  padding: 14px 28px;
  background: linear-gradient(135deg, #007aff 0%, #0056cc 100%);
  color: white;
  border: none;
  border-radius: 24px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.send-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(0, 122, 255, 0.4);
}

.send-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

@media (max-width: 768px) {
  .sidebar {
    width: 80px;
  }
  .sidebar-header {
    padding: 20px 10px;
  }
  .platform-name {
    display: none;
  }
  .nav-text {
    display: none;
  }
  .nav-item {
    justify-content: center;
    padding: 14px;
  }
  .user-details {
    display: none;
  }
  .main-content {
    margin-left: 80px;
  }
  .history-sidebar {
    display: none;
  }
  .message-content {
    max-width: 85%;
  }
}
</style>
