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
                <option value="deepseek-32b">DeepSeek R1 32B (高质量)</option>
                <option value="qwen-32b">Qwen3 32B (快速响应)</option>
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
                <div class="message-text">{{ msg.content }}</div>
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
import { ref, computed, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

// 类型定义
interface Message {
  role: 'user' | 'assistant'
  content: string
  time: string
}

interface Conversation {
  id: string
  title: string
  messages: Message[]
}

// 认证相关
const router = useRouter()
const authStore = useAuthStore()
const username = computed(() => authStore.username)
const userInitial = computed(() => {
  const name = username.value
  return name ? name.charAt(0).toUpperCase() : 'U'
})

// 智能助手数据
const conversations = ref<Conversation[]>([])
const currentConvId = ref<string | null>(null)
const inputMessage = ref('')
const isTyping = ref(false)
const messagesContainer = ref<HTMLElement | null>(null)

// 模型、知识库、工具选择
const selectedModel = ref('deepseek-32b')
const selectedKnowledgeBases = ref<string[]>([])
const selectedTools = ref<string[]>([])

// 当前对话的消息
const currentMessages = computed(() => {
  const conv = conversations.value.find(c => c.id === currentConvId.value)
  return conv ? conv.messages : []
})

// 辅助函数
function generateId(): string {
  return Date.now() + '-' + Math.random().toString(36).substr(2, 6)
}

function formatTime(): string {
  const now = new Date()
  const hours = String(now.getHours()).padStart(2, '0')
  const minutes = String(now.getMinutes()).padStart(2, '0')
  return `${hours}:${minutes}`
}

function saveToLocal() {
  localStorage.setItem('assistant_conversations', JSON.stringify(conversations.value))
  localStorage.setItem('assistant_currentConvId', currentConvId.value as string)
}

function loadFromLocal() {
  const saved = localStorage.getItem('assistant_conversations')
  if (saved) {
    conversations.value = JSON.parse(saved)
  }
  const savedId = localStorage.getItem('assistant_currentConvId')
  if (savedId && conversations.value.some(c => c.id === savedId)) {
    currentConvId.value = savedId
  } else if (conversations.value.length > 0) {
    currentConvId.value = conversations.value[0].id
  } else {
    const defaultId = generateId()
    conversations.value = [{
      id: defaultId,
      title: '新对话',
      messages: [{ role: 'assistant', content: '你好！我是智能气象助手 🌤️，有什么可以帮你的吗？', time: formatTime() }]
    }]
    currentConvId.value = defaultId
  }
}

function scrollToBottom() {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
  })
}

function updateConversationTitle(convId: string, userMsg: string) {
  const conv = conversations.value.find(c => c.id === convId)
  if (conv && (conv.title === '新对话' || !conv.title)) {
    let newTitle = userMsg.slice(0, 20)
    if (userMsg.length > 20) newTitle += '...'
    conv.title = newTitle
    saveToLocal()
  }
}

// 对话操作
function createNewChat() {
  const newId = generateId()
  conversations.value.unshift({
    id: newId,
    title: '新对话',
    messages: [{ role: 'assistant', content: '你好！我是智能气象助手 🌤️，有什么可以帮你的吗？', time: formatTime() }]
  })
  currentConvId.value = newId
  saveToLocal()
  scrollToBottom()
}

function switchConversation(id: string) {
  if (currentConvId.value === id) return
  currentConvId.value = id
  saveToLocal()
  scrollToBottom()
}

function deleteConversation(id: string) {
  if (conversations.value.length === 1) {
    // 提示不能删除最后一个
    return
  }
  const idx = conversations.value.findIndex(c => c.id === id)
  if (idx !== -1) {
    conversations.value.splice(idx, 1)
    if (currentConvId.value === id) {
      currentConvId.value = conversations.value[0].id
    }
    saveToLocal()
    scrollToBottom()
  }
}

// 模拟流式回复（等后端接口好后替换）
async function mockStreamReply(userMessage: string, onChunk: (chunk: string) => void, onEnd: () => void) {
  const mockFull = `这是对“${userMessage}”的模拟回复。\n\n我是智能气象助手，目前运行在前端演示模式。等后端同学根据API文档实现接口后，我就会调用真正的大模型，为你提供专业的气象分析、文档校正、材料生成等服务。\n\n你可以继续提问，我会尽力模拟回答。`
  let index = 0
  const interval = setInterval(() => {
    if (index < mockFull.length) {
      onChunk(mockFull[index])
      index++
    } else {
      clearInterval(interval)
      onEnd()
    }
  }, 30)
}

// 发送消息
async function sendMessage() {
  if (!inputMessage.value.trim() || isTyping.value) return
  
  const userText = inputMessage.value.trim()
  inputMessage.value = ''

  let conv = conversations.value.find(c => c.id === currentConvId.value)
  if (!conv) {
    createNewChat()
    conv = conversations.value.find(c => c.id === currentConvId.value)!
  }

  // 添加用户消息
  const userMessage: Message = {
    role: 'user',
    content: userText,
    time: formatTime()
  }
  conv.messages.push(userMessage)
  saveToLocal()
  scrollToBottom()
  updateConversationTitle(currentConvId.value!, userText)

  // 添加占位的助手消息
  const assistantMsgIndex = conv.messages.length
  conv.messages.push({ role: 'assistant', content: '', time: formatTime() })
  saveToLocal()
  scrollToBottom()

  isTyping.value = true

  let accumulated = ''
  await mockStreamReply(userText,
    (chunk) => {
      accumulated += chunk
      conv.messages[assistantMsgIndex].content = accumulated
      saveToLocal()
      scrollToBottom()
    },
    () => {
      isTyping.value = false
      saveToLocal()
    }
  )
  if (isTyping.value) {
    isTyping.value = false
    saveToLocal()
  }
}

function sendSuggestion(text: string) {
  inputMessage.value = text
  sendMessage()
}

// 语音输入（模拟）
function startVoiceInput() {
  if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
    alert('您的浏览器不支持麦克风，请使用 Chrome/Edge 等现代浏览器。')
    return
  }
  // 模拟语音识别
  setTimeout(() => {
    inputMessage.value = '模拟语音输入：今天天气怎么样？'
  }, 1000)
}

// 退出登录
const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}

// 初始化
loadFromLocal()
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