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
      </nav>
      
      <div class="sidebar-footer">
        <div class="user-info">
          <div class="user-avatar">
            {{ userInitial }}
          </div>
          <div class="user-details">
            <p class="username">{{ username }}</p>
            <p class="user-role">管理员</p>
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
        <!-- 历史对话侧边栏（新增） -->
        <aside class="history-sidebar">
          <div class="new-chat-btn" @click="createNewChat">✨ 新建对话</div>
          <div class="history-title">📋 历史对话</div>
          <div class="conversation-list">
            <div
              v-for="conv in conversations"
              :key="conv.id"
              class="conversation-item"
              :class="{ active: conv.id === currentConvId }"
              @click="switchConversation(conv.id)"
            >
              <span class="conv-title">{{ conv.title || '未命名' }}</span>
              <button class="delete-btn" @click.stop="deleteConversation(conv.id)">🗑️</button>
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
              <select v-model="selectedKnowledgeBases" multiple size="1" style="height:32px">
                <option value="kb_weather">气象术语库</option>
                <option value="kb_alert">预警信号库</option>
              </select>
              <select v-model="selectedTools" multiple size="1" style="height:32px">
                <option value="weather_query">天气查询工具</option>
                <option value="alert_query">预警查询工具</option>
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
              <button @click="startVoiceInput" class="voice-button">🎤</button>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, nextTick, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { marked } from 'marked'
import DOMPurify from 'dompurify'

const API_BASE = 'http://localhost:8000'

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

// 选择
const models = ref<ModelOption[]>([])
const selectedModel = ref('')
const selectedKnowledgeBases = ref<string[]>([])
const selectedTools = ref<string[]>([])

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

async function apiFetch(path: string, opts?: RequestInit) {
  const res = await fetch(`${API_BASE}${path}`, {
    credentials: 'include',
    headers: { 'Content-Type': 'application/json', ...(opts?.headers || {}) },
    ...opts,
  })
  if (!res.ok) {
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
  currentMessages.value = data.messages.map((m: { role: string; content: string; created_at?: string }) => ({
    role: m.role as 'user' | 'assistant',
    content: m.content,
    time: m.created_at ? fmtTimeFromDate(m.created_at) : formatTime(),
  }))
  scrollToBottom()
}

// 对话操作
async function createNewChat() {
  const data = await apiFetch('/api/v1/assistant/conversations', {
    method: 'POST',
    body: JSON.stringify({ title: '新对话', model_id: selectedModel.value }),
  })
  conversations.value.unshift(data)
  currentConvId.value = data.id
  currentMessages.value = []
  scrollToBottom()
}

async function switchConversation(id: string) {
  if (currentConvId.value === id) return
  currentConvId.value = id
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
      knowledge_base_ids: selectedKnowledgeBases.value,
      tool_ids: selectedTools.value,
    }),
  })
  if (!res.ok) throw new Error('请求失败')
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

// 发送消息
async function sendMessage() {
  if (!inputMessage.value.trim() || isTyping.value) return
  const userText = inputMessage.value.trim()
  inputMessage.value = ''

  if (!currentConvId.value) {
    await createNewChat()
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
      () => { isTyping.value = false }
    )
  } catch {
    currentMessages.value[assistantIdx].content = '服务暂时不可用，请稍后重试。'
    isTyping.value = false
  }
}

function sendSuggestion(text: string) {
  inputMessage.value = text
  sendMessage()
}

function startVoiceInput() {
  if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
    alert('您的浏览器不支持麦克风，请使用 Chrome/Edge 等现代浏览器。')
    return
  }
  setTimeout(() => {
    inputMessage.value = '模拟语音输入：今天天气怎么样？'
  }, 1000)
}

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}

// 初始化
onMounted(() => {
  loadModels()
  loadConversations()
})
</script>

<style scoped>
/* 原有样式保留，新增样式适配 */
.assistant-container {
  display: flex;
  min-height: 100vh;
  background: #f5f5f7;
}

/* 左侧导航栏样式（与Home.vue一致） */
.sidebar {
  width: 260px;
  background: white;
  display: flex;
  flex-direction: column;
  box-shadow: 2px 0 10px rgba(0, 0, 0, 0.05);
  position: fixed;
  height: 100vh;
  left: 0;
  top: 0;
}

.sidebar-header {
  padding: 30px 20px;
  border-bottom: 1px solid #f0f0f0;
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
  background: #f5f5f7;
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
  border-top: 1px solid #f0f0f0;
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

/* 右侧主内容区 */
.main-content {
  flex: 1;
  margin-left: 260px;
  padding: 20px;
  background: #f5f5f7;
  min-height: 100vh;
}

.chat-layout {
  display: flex;
  gap: 20px;
  height: calc(100vh - 40px);
}

/* 历史对话侧边栏 */
.history-sidebar {
  width: 260px;
  background: white;
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

.history-title {
  font-size: 14px;
  color: #6e6e6e;
  margin-bottom: 12px;
  font-weight: 500;
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
  background: white;
  border: 1px solid #e5e5e5;
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

.delete-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 16px;
  color: #aaa;
}

.delete-btn:hover {
  color: #e5484d;
}

/* 聊天主区域 */
.chat-wrapper {
  flex: 1;
  background: white;
  border-radius: 16px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.chat-header {
  padding: 20px 24px;
  border-bottom: 1px solid #f0f0f0;
  background: white;
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
  border: 1px solid #d0d0d0;
  font-size: 14px;
  background: white;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 20px;
  background: #fafafa;
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
  background: white;
  border: 1px solid #d2d2d7;
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
  background: white;
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
  background: white;
  border-top: 1px solid #f0f0f0;
}

.input-wrapper {
  display: flex;
  gap: 12px;
  align-items: center;
}

.chat-input {
  flex: 1;
  padding: 14px 20px;
  border: 1px solid #d2d2d7;
  border-radius: 24px;
  font-size: 15px;
  outline: none;
  transition: all 0.3s ease;
  background: #f5f5f7;
}

.chat-input:focus {
  border-color: #007aff;
  background: white;
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

.voice-button {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: #f5f5f7;
  border: 1px solid #d2d2d7;
  font-size: 20px;
  cursor: pointer;
  transition: all 0.2s;
}

.voice-button:hover {
  background: #e8e8ed;
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