<template>
  <OracleLayout>
    <div class="assistant-page">
      <div class="chat-layout">
        <!-- 历史对话侧边栏 -->
        <aside class="history-sidebar oracle-gold-corners">
          <div v-if="isBatchMode" class="batch-actions-container">
            <button class="batch-action-btn select-all-btn" @click="selectAllConversations">
              {{ isAllSelected ? '取消全选' : '全选' }}
            </button>
            <button
              class="batch-action-btn batch-delete-btn"
              :disabled="selectedConvIds.length === 0"
              @click="batchDeleteConversations"
            >
              <svg class="btn-icon" viewBox="0 0 24 24" width="14" height="14" style="fill: currentColor; margin-right: 4px; vertical-align: middle;">
                <path d="M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6v12zM19 4h-3.5l-1-1h-5l-1 1H5v2h14V4z"/>
              </svg>
              删除 ({{ selectedConvIds.length }})
            </button>
          </div>
          <div v-else class="new-chat-btn" @click="createNewChat">
            <svg class="btn-icon" viewBox="0 0 24 24" width="16" height="16" style="fill: currentColor; margin-right: 4px; vertical-align: middle;">
              <path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z"/>
            </svg>
            新建对话
          </div>
          
          <div class="history-sidebar-header">
            <span class="history-title">
              <svg class="btn-icon" viewBox="0 0 24 24" width="14" height="14" style="fill: currentColor; margin-right: 6px; color: var(--oracle-gold); vertical-align: middle;">
                <path d="M19 3h-4.18C14.4 1.84 13.3 1 12 1c-1.3 0-2.4.84-2.82 2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-7 0c.55 0 1 .45 1 1s-.45 1-1 1-1-.45-1-1 .45-1 1-1zm2 14H7v-2h7v2zm3-4H7v-2h10v2zm0-4H7V7h10v2z"/>
              </svg>
              历史对话
            </span>
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
                <button class="action-btn rename-btn" @click.stop="renameConversationPrompt(conv.id, conv.title)" title="重命名">
                  <svg viewBox="0 0 24 24" width="13" height="13" fill="currentColor">
                    <path d="M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25zM20.71 7.04c.39-.39.39-1.02 0-1.41l-2.34-2.34c-.39-.39-1.02-.39-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z"/>
                  </svg>
                </button>
                <button class="action-btn delete-btn" @click.stop="deleteConversation(conv.id)" title="删除">
                  <svg viewBox="0 0 24 24" width="13" height="13" fill="currentColor">
                    <path d="M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6v12zM19 4h-3.5l-1-1h-5l-1 1H5v2h14V4z"/>
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </aside>

        <!-- 聊天主区域 -->
        <div class="chat-wrapper oracle-gold-corners">
          <div class="chat-header">
            <div class="header-content">
              <div class="assistant-avatar">
                <svg class="assistant-avatar-svg" viewBox="0 0 24 24" width="24" height="24">
                  <circle cx="12" cy="8" r="4" fill="currentColor" />
                  <path fill="currentColor" opacity="0.85" d="M19.36 10.04C18.67 6.59 15.64 4 12 4 9.11 4 6.6 5.64 5.35 8.04 2.34 8.36 0 10.91 0 14c0 3.31 2.69 6 6 6h13c2.76 0 5-2.24 5-5 0-2.64-2.05-4.78-4.64-4.96z" />
                </svg>
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
              <div class="empty-icon">
                <svg viewBox="0 0 24 24" width="72" height="72" style="color: var(--oracle-gold);">
                  <circle cx="12" cy="8" r="4" fill="currentColor" />
                  <path fill="currentColor" opacity="0.85" d="M19.36 10.04C18.67 6.59 15.64 4 12 4 9.11 4 6.6 5.64 5.35 8.04 2.34 8.36 0 10.91 0 14c0 3.31 2.69 6 6 6h13c2.76 0 5-2.24 5-5 0-2.64-2.05-4.78-4.64-4.96z" />
                </svg>
              </div>
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
                <span v-if="msg.role === 'user'">{{ userInitial }}</span>
                <svg v-else class="assistant-avatar-svg" viewBox="0 0 24 24" width="20" height="20">
                  <circle cx="12" cy="8" r="4" fill="currentColor" />
                  <path fill="currentColor" opacity="0.85" d="M19.36 10.04C18.67 6.59 15.64 4 12 4 9.11 4 6.6 5.64 5.35 8.04 2.34 8.36 0 10.91 0 14c0 3.31 2.69 6 6 6h13c2.76 0 5-2.24 5-5 0-2.64-2.05-4.78-4.64-4.96z" />
                </svg>
              </div>
              <div class="message-content">
                <div class="message-text" v-html="msg.role === 'assistant' ? renderMarkdown(msg.content) : msg.content"></div>
                <div class="message-time">{{ msg.time }}</div>
              </div>
            </div>
            
            <div v-if="isTyping" class="message assistant-message">
              <div class="message-avatar">
                <svg class="assistant-avatar-svg" viewBox="0 0 24 24" width="20" height="20">
                  <circle cx="12" cy="8" r="4" fill="currentColor" />
                  <path fill="currentColor" opacity="0.85" d="M19.36 10.04C18.67 6.59 15.64 4 12 4 9.11 4 6.6 5.64 5.35 8.04 2.34 8.36 0 10.91 0 14c0 3.31 2.69 6 6 6h13c2.76 0 5-2.24 5-5 0-2.64-2.05-4.78-4.64-4.96z" />
                </svg>
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
    </div>
  </OracleLayout>
</template>

<script setup lang="ts">
import { ref, computed, nextTick, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { marked } from 'marked'
import DOMPurify from 'dompurify'
import OracleLayout from '../layouts/OracleLayout.vue'

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
const userInitial = computed(() => {
  const name = authStore.username
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
.assistant-page {
  padding: 24px;
  min-height: calc(100vh - var(--oracle-header-height, 64px));
  box-sizing: border-box;
}

.chat-layout {
  display: flex;
  gap: 20px;
  height: calc(100vh - 120px);
}

/* 历史对话侧边栏 */
.history-sidebar {
  width: 260px;
  background: var(--oracle-panel-soft);
  backdrop-filter: blur(16px);
  border: 1px solid var(--oracle-border);
  border-radius: var(--oracle-radius);
  display: flex;
  flex-direction: column;
  padding: 16px;
  box-shadow: var(--oracle-shadow);
  overflow-y: auto;
  position: relative;
}

.new-chat-btn {
  background: linear-gradient(135deg, var(--oracle-purple-soft), rgba(215, 174, 105, 0.15));
  border: 1px solid var(--oracle-border);
  color: var(--oracle-gold-strong);
  text-align: center;
  padding: 12px;
  border-radius: 12px;
  cursor: pointer;
  font-size: 15px;
  font-weight: 600;
  margin-bottom: 20px;
  box-shadow: 0 4px 12px var(--oracle-gold-glow);
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  align-items: center;
  justify-content: center;
}

.new-chat-btn:hover {
  border-color: var(--oracle-gold);
  color: var(--oracle-text);
  background: var(--oracle-panel);
  box-shadow: 0 6px 16px var(--oracle-gold-glow);
  transform: translateY(-1px);
}

.new-chat-btn:active {
  transform: scale(0.98) translateY(0);
}

.history-sidebar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
  border-bottom: 1px solid var(--oracle-border-soft);
  padding-bottom: 8px;
}

.history-title {
  font-size: 13.5px;
  color: var(--oracle-muted);
  font-weight: 600;
  display: flex;
  align-items: center;
}

.batch-toggle-btn {
  background: none;
  border: none;
  font-size: 12px;
  color: var(--oracle-gold);
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 6px;
  font-weight: 600;
  transition: background-color 0.2s, color 0.2s;
}

.batch-toggle-btn:hover {
  background-color: var(--oracle-purple-soft);
  color: var(--oracle-gold-strong);
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
  border: 1px solid var(--oracle-border);
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
}

.select-all-btn {
  background: var(--oracle-panel-soft);
  color: var(--oracle-text);
}

.select-all-btn:hover {
  background: var(--oracle-panel);
  border-color: var(--oracle-gold);
}

.batch-delete-btn {
  background: var(--oracle-danger);
  border-color: rgba(207, 110, 91, 0.4);
  color: white;
}

.batch-delete-btn:hover:not(:disabled) {
  background: #bd523e;
  box-shadow: 0 0 10px rgba(207, 110, 91, 0.2);
}

.batch-delete-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.conversation-item.selected {
  background: var(--oracle-purple-soft);
  border-color: var(--oracle-gold);
}

.custom-checkbox {
  width: 16px;
  height: 16px;
  border-radius: 50%;
  border: 1px solid var(--oracle-border);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  margin-right: 8px;
  flex-shrink: 0;
  transition: all 0.2s ease;
  background: var(--oracle-bg-deep);
}

.custom-checkbox.checked {
  background: var(--oracle-gold);
  border-color: var(--oracle-gold);
}

.custom-checkbox.checked::after {
  content: '✓';
  color: var(--oracle-bg-deep);
  font-size: 10px;
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
  margin-bottom: 8px;
  border-radius: var(--oracle-radius-inner);
  cursor: pointer;
  background: rgba(215, 174, 105, 0.03);
  border: 1px solid var(--oracle-border-soft);
  color: var(--oracle-faint);
  transition: all 0.2s ease;
}

.conversation-item:hover {
  border-color: var(--oracle-border);
  background: rgba(215, 174, 105, 0.06);
  color: var(--oracle-text);
}

.conversation-item.active {
  background: var(--oracle-purple-soft);
  border-color: var(--oracle-gold);
  color: var(--oracle-text);
  box-shadow: inset 0 0 10px rgba(215, 174, 105, 0.05);
}

.conv-title {
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-size: 13.5px;
}

.conv-actions {
  display: flex;
  gap: 4px;
}

.action-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 4px;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--oracle-muted);
  transition: all 0.2s ease;
}

.rename-btn:hover {
  color: var(--oracle-gold);
  background: rgba(215, 174, 105, 0.1);
}

.delete-btn:hover {
  color: var(--oracle-danger);
  background: rgba(207, 110, 91, 0.15);
}

/* 聊天主区域 */
.chat-wrapper {
  flex: 1;
  background: var(--oracle-panel);
  backdrop-filter: blur(16px);
  border: 1px solid var(--oracle-border);
  border-radius: var(--oracle-radius);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  box-shadow: var(--oracle-shadow);
  position: relative;
}

.chat-header {
  padding: 18px 24px;
  border-bottom: 1px solid var(--oracle-border-soft);
  background: transparent;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.header-content {
  display: flex;
  align-items: center;
  gap: 12px;
}

.assistant-avatar {
  width: 38px;
  height: 38px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--oracle-purple-soft), rgba(215, 174, 105, 0.2));
  border: 1px solid var(--oracle-border);
  color: var(--oracle-gold);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
}

.header-info h1 {
  font-family: var(--oracle-font-serif);
  font-size: 18px;
  font-weight: 600;
  color: var(--oracle-text);
  margin: 0 0 2px 0;
  letter-spacing: 0.05em;
}

.header-info p {
  font-size: 12px;
  color: var(--oracle-muted);
  margin: 0;
}

.toolbar {
  display: flex;
  gap: 12px;
  align-items: center;
}

.toolbar select {
  padding: 6px 14px;
  border-radius: 20px;
  border: 1px solid var(--oracle-border);
  font-size: 13.5px;
  background: var(--oracle-panel-soft);
  color: var(--oracle-text);
  outline: none;
  cursor: pointer;
  transition: all 0.2s ease;
}

.toolbar select:hover {
  border-color: var(--oracle-gold);
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
  margin-bottom: 20px;
  animation: float-mystical 4s ease-in-out infinite;
}

.empty-state h2 {
  font-family: var(--oracle-font-serif);
  font-size: 22px;
  font-weight: 600;
  color: var(--oracle-text);
  margin: 0 0 10px 0;
  letter-spacing: 0.05em;
}

.empty-state p {
  font-size: 14px;
  color: var(--oracle-muted);
  margin: 0 0 24px 0;
}

.suggestion-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  justify-content: center;
}

.chip {
  padding: 10px 18px;
  background: var(--oracle-purple-soft);
  border: 1px solid var(--oracle-border-soft);
  border-radius: 20px;
  color: var(--oracle-text);
  font-size: 13.5px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.chip:hover {
  background: var(--oracle-panel);
  color: var(--oracle-gold-strong);
  border-color: var(--oracle-gold);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px var(--oracle-gold-glow);
}

.chip:active {
  transform: scale(0.97);
}

.message {
  display: flex;
  gap: 12px;
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
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--oracle-purple-soft), rgba(215, 174, 105, 0.2));
  color: var(--oracle-gold);
  border: 1px solid var(--oracle-border);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: 700;
  flex-shrink: 0;
}

.assistant-message .message-avatar {
  background: linear-gradient(135deg, var(--oracle-purple-soft), rgba(215, 174, 105, 0.2));
  color: var(--oracle-gold);
  border-color: rgba(215, 174, 105, 0.3);
}

.message-content {
  max-width: 75%;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.user-message .message-content {
  align-items: flex-end;
}

.message-text {
  padding: 12px 16px;
  border-radius: 14px;
  font-size: 14px;
  line-height: 1.6;
  word-break: break-word;
  box-sizing: border-box;
}

.user-message .message-text {
  background: var(--oracle-purple-soft);
  border: 1px solid var(--oracle-border);
  color: var(--oracle-text);
  border-bottom-right-radius: 4px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.assistant-message .message-text {
  background: var(--oracle-panel-soft);
  border: 1px solid var(--oracle-border-soft);
  color: var(--oracle-text);
  border-bottom-left-radius: 4px;
  box-shadow: var(--oracle-shadow);
}

.assistant-message .message-text :deep(strong) {
  color: var(--oracle-gold);
  font-weight: 600;
}

.assistant-message .message-text :deep(ul),
.assistant-message .message-text :deep(ol) {
  margin: 6px 0;
  padding-left: 20px;
}

.assistant-message .message-text :deep(li) {
  margin: 4px 0;
}

.assistant-message .message-text :deep(code) {
  background: rgba(255, 255, 255, 0.05);
  padding: 2px 6px;
  border-radius: 4px;
  font-family: 'SF Mono', Monaco, monospace;
  font-size: 12.5px;
  color: var(--oracle-gold-strong);
}

.assistant-message .message-text :deep(pre) {
  background: rgba(0, 0, 0, 0.2);
  border: 1px solid var(--oracle-border-soft);
  padding: 12px;
  border-radius: 8px;
  overflow-x: auto;
  margin: 8px 0;
}

.assistant-message .message-text :deep(pre code) {
  background: transparent;
  padding: 0;
  color: var(--oracle-text);
}

.assistant-message .message-text :deep(blockquote) {
  border-left: 3px solid var(--oracle-gold);
  margin: 8px 0;
  padding-left: 12px;
  color: var(--oracle-muted);
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
  font-size: 11px;
  color: var(--oracle-muted);
  margin-top: 2px;
}

.typing {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 12px 16px;
}

.dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--oracle-muted);
  animation: bounce 1.4s ease-in-out infinite;
}

.dot:nth-child(1) { animation-delay: 0s; }
.dot:nth-child(2) { animation-delay: 0.2s; }
.dot:nth-child(3) { animation-delay: 0.4s; }

@keyframes bounce {
  0%, 60%, 100% { transform: translateY(0); }
  30% { transform: translateY(-4px); }
}

.chat-input-container {
  padding: 16px 24px 20px;
  background: transparent;
  border-top: 1px solid var(--oracle-border-soft);
}

.input-wrapper {
  display: flex;
  gap: 12px;
  align-items: center;
}

.chat-input {
  flex: 1;
  padding: 12px 18px;
  border: 1px solid var(--oracle-border);
  border-radius: 24px;
  font-size: 14px;
  outline: none;
  transition: all 0.2s ease;
  background: var(--oracle-panel-soft);
  color: var(--oracle-text);
}

.chat-input::placeholder {
  color: var(--oracle-muted);
  opacity: 0.7;
}

.chat-input:focus {
  border-color: var(--oracle-gold);
  background: var(--oracle-panel);
  box-shadow: 0 0 0 3px var(--oracle-gold-glow);
}

.send-button {
  padding: 12px 24px;
  background: var(--oracle-gold);
  color: var(--oracle-bg-deep);
  border: none;
  border-radius: 24px;
  font-size: 14.5px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s ease;
}

.send-button:hover:not(:disabled) {
  background: var(--oracle-gold-strong);
  box-shadow: 0 4px 12px var(--oracle-gold-glow);
  transform: translateY(-1px);
}

.send-button:active:not(:disabled) {
  transform: scale(0.97) translateY(0);
}

.send-button:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

@media (max-width: 768px) {
  .history-sidebar {
    display: none;
  }
  .message-content {
    max-width: 85%;
  }
}
</style>
