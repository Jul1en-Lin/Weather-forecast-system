<template>
  <section class="oracle-chat-panel-card oracle-surface oracle-gold-corners">
    <!-- Panel Header -->
    <header class="chat-panel-header">
      <div class="diviner-profile">
        <div class="diviner-avatar-wrap">
          <svg class="diviner-avatar-svg" viewBox="0 0 24 24" width="20" height="20">
            <path fill="currentColor" d="M12 22c5.52 0 10-4.48 10-10S17.52 2 12 2 2 6.48 2 12s4.48 10 10 10zm1-17.5c.83 0 1.5.67 1.5 1.5s-.67 1.5-1.5 1.5-1.5-.67-1.5-1.5.67-1.5 1.5-1.5zm-2.5 12h-1v-1h1v1zm3-3.5c-.83 0-1.5-.67-1.5-1.5s.67-1.5 1.5-1.5 1.5.67 1.5 1.5-.67 1.5-1.5 1.5zm-3.5 1.5c-.83 0-1.5-.67-1.5-1.5s.67-1.5 1.5-1.5 1.5.67 1.5 1.5-.67 1.5-1.5 1.5z" />
          </svg>
        </div>
        <div class="diviner-meta">
          <h4>天气助手</h4>
          <span>你的智能气象服务助理</span>
        </div>
      </div>
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
    </header>

    <!-- Message History Area -->
    <div class="chat-messages-container" ref="messagesBoxRef">
      <div class="chat-messages-scroll-area">
        <div
          v-for="(message, index) in messages"
          :key="`${message.role}-${index}`"
          :class="['chat-bubble-item', `is-${message.role}`]"
        >
          <!-- Avatar inside bubble block -->
          <div class="bubble-avatar">
            <span v-if="message.role === 'user'">👤</span>
            <span v-else>🌤️</span>
          </div>

          <div class="bubble-content-wrap">
            <div class="bubble-sender-name">
              {{ message.role === 'user' ? '你' : '天气助手' }}
            </div>
            <div class="bubble-text-box">
              <p v-if="message.content">{{ message.content }}</p>
              <div v-else class="bubble-typing-loader">
                <span class="typing-dot"></span>
                <span class="typing-dot"></span>
                <span class="typing-dot"></span>
              </div>
            </div>

            <!-- Quick Suggestion Chips (Only show under the initial assistant message if no conversation has happened yet) -->
            <div
              v-if="message.role === 'assistant' && index === 0 && messages.length <= 2"
              class="chat-initial-suggestions"
            >
              <button
                v-for="item in suggestions"
                :key="item"
                type="button"
                class="suggestion-chip"
                :disabled="isSending || !selectedModel"
                @click="sendMessage(item)"
              >
                {{ item }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Chat Input Section -->
    <div class="chat-input-area-wrap">
      <form class="chat-input-form" @submit.prevent="submitCustomMessage">
        <input
          v-model.trim="draftMessage"
          type="text"
          placeholder="输入天气相关问题..."
          class="chat-text-input"
          :disabled="isSending || !selectedModel"
        />
        <button
          type="submit"
          class="chat-submit-btn"
          :disabled="!draftMessage || isSending || !selectedModel"
          aria-label="发送"
        >
          <!-- Paper Plane SVG -->
          <svg viewBox="0 0 24 24" width="18" height="18" class="plane-svg">
            <path fill="currentColor" d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z" />
          </svg>
        </button>
      </form>

      <p class="chat-disclaimer">内容由大模型生成，仅供参考</p>
      <p v-if="errorMessage" class="chat-error-log">{{ errorMessage }}</p>
    </div>
  </section>
</template>

<script setup lang="ts">
import { onMounted, ref, nextTick, watch } from 'vue'
import type { WeatherOracleReading } from '../../types/weatherOracle'

const STORAGE_KEY = 'weather_oracle:chat_model'

interface ModelInfo {
  id: string
  name: string
  description?: string
}

interface ChatMessage {
  role: 'user' | 'assistant'
  content: string
}

const props = defineProps<{
  city?: string
  reading?: WeatherOracleReading
}>()

const suggestions = ['今天需要带伞吗？', '本周天气预报', '适合户外运动吗？', '今天穿什么合适？']
const models = ref<ModelInfo[]>([])
const selectedModel = ref('')
const isSending = ref(false)
const errorMessage = ref('')
const draftMessage = ref('')
const messagesBoxRef = ref<HTMLElement | null>(null)

// Initialize messages with a default welcoming diviner message
const messages = ref<ChatMessage[]>([
  { role: 'assistant', content: '你好，我是你的智能天气助手。有什么天气问题可以问我~' }
])



onMounted(() => {
  loadModels()
})

// Scroll chat log to bottom whenever messages list grows
watch(
  () => messages.value.length,
  () => {
    scrollToBottom()
  }
)

watch(selectedModel, (newVal) => {
  if (newVal) {
    localStorage.setItem(STORAGE_KEY, newVal)
  }
})

function scrollToBottom() {
  nextTick(() => {
    if (messagesBoxRef.value) {
      messagesBoxRef.value.scrollTop = messagesBoxRef.value.scrollHeight
    }
  })
}

async function loadModels() {
  errorMessage.value = ''
  try {
    const res = await fetch('/api/v1/assistant/models', {
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
    })
    if (!res.ok) throw new Error(res.status === 401 ? '登录已过期' : '模型列表读取失败')
    const data = await res.json() as { models?: ModelInfo[] }
    models.value = data.models || []
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
    if (!selectedModel.value) {
      errorMessage.value = '暂无可用模型，请先到系统设置里配置。'
    }
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : '模型列表读取失败'
  }
}

function submitCustomMessage() {
  if (!draftMessage.value) return
  const message = draftMessage.value
  draftMessage.value = ''
  sendMessage(message)
}

function createContextualPrompt(message: string) {
  if (!props.reading) {
    return [
      '你是智能天气助手。目前用户尚未选择城市。请友好地提醒用户可以通过界面中的城市选择器输入或选择城市，以查看今日天气分析报告。',
      `用户追问：${message}`
    ].join('\n')
  }
  const weather = props.reading.weather
  return [
    '你是智能天气助手，请结合以下天气上下文回答用户追问。',
    `城市：${props.city}`,
    `日期：${props.reading.date}`,
    `天气：${weather.condition}，温度 ${weather.temperature ?? '未知'}°C，湿度 ${weather.humidity ?? '未知'}%，气压 ${weather.pressure ?? '未知'} hPa，风速 ${weather.wind_speed ?? '未知'} km/h，风向 ${weather.wind_direction || '未知'}`,
    `今日天气提示：${props.reading.fortune.summary}`,
    '回答要短，直接给建议，不要复述全部上下文。',
    `用户追问：${message}`,
  ].join('\n')
}

async function sendMessage(message: string) {
  if (!selectedModel.value || isSending.value) return
  errorMessage.value = ''
  isSending.value = true
  messages.value.push({ role: 'user', content: message })
  const assistantMessage: ChatMessage = { role: 'assistant', content: '' }
  messages.value.push(assistantMessage)

  try {
    const res = await fetch('/api/v1/assistant/chat/stream', {
      method: 'POST',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        model_id: selectedModel.value,
        message: createContextualPrompt(message),
      }),
    })
    if (!res.ok) throw new Error(res.status === 401 ? '登录已过期' : '请求失败')
    if (!res.body) throw new Error('浏览器不支持流式读取')

    const reader = res.body.getReader()
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
          if (!line.startsWith('data: ')) continue
          const data = line.slice(6)
          if (data === '[DONE]') {
            scrollToBottom()
            return
          }
          try {
            const parsed = JSON.parse(data) as { chunk?: string; error?: string }
            if (parsed.error) throw new Error(parsed.error)
            if (parsed.chunk) {
              assistantMessage.content += parsed.chunk
              // Scroll as text is streaming
              scrollToBottom()
            }
          } catch (error) {
            if (error instanceof SyntaxError) continue
            throw error
          }
        }
      }
    }
  } catch (error) {
    assistantMessage.content ||= '这次没有拿到回复。'
    errorMessage.value = error instanceof Error ? error.message : '请求失败'
  } finally {
    isSending.value = false
    scrollToBottom()
  }
}
</script>

<style scoped>
.oracle-chat-panel-card {
  display: flex;
  flex-direction: column;
  height: 100%;
  min-height: 520px;
  overflow: hidden;
  box-sizing: border-box;
}

/* Header */
.chat-panel-header {
  padding: 16px 20px;
  border-bottom: 1px solid var(--oracle-border-soft);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.diviner-profile {
  display: flex;
  align-items: center;
  gap: 12px;
}

.diviner-avatar-wrap {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  border: 1px solid var(--oracle-border);
  background: linear-gradient(135deg, var(--oracle-purple-soft), rgba(215, 174, 105, 0.2));
  color: var(--oracle-gold);
  display: grid;
  place-items: center;
  box-shadow: 0 0 8px var(--oracle-gold-glow);
}

.diviner-avatar-svg {
  filter: drop-shadow(0 0 2px var(--oracle-gold-glow));
}

.diviner-meta h4 {
  font-family: var(--oracle-font-serif);
  font-size: 14px;
  color: var(--oracle-text);
  margin: 0;
}

.diviner-meta span {
  font-size: 11px;
  color: var(--oracle-muted);
  display: block;
  margin-top: 1px;
}

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

/* Chat History Display */
.chat-messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
}

.chat-messages-scroll-area {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.chat-bubble-item {
  display: flex;
  gap: 12px;
  max-width: 90%;
}

.chat-bubble-item.is-user {
  align-self: flex-end;
  flex-direction: row-reverse;
}

.bubble-avatar {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  border: 1px solid var(--oracle-border-soft);
  background: var(--oracle-panel-soft);
  display: grid;
  place-items: center;
  font-size: 12px;
  flex-shrink: 0;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}

.bubble-content-wrap {
  display: flex;
  flex-direction: column;
  gap: 4px;
  flex: 1;
}

.chat-bubble-item.is-user .bubble-content-wrap {
  align-items: flex-end;
}

.bubble-sender-name {
  font-size: 11px;
  color: var(--oracle-muted);
  font-weight: 600;
}

.bubble-text-box {
  background: var(--oracle-panel-soft);
  border: 1px solid var(--oracle-border-soft);
  border-radius: 8px;
  padding: 10px 14px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.chat-bubble-item.is-user .bubble-text-box {
  border-color: rgba(142, 110, 194, 0.3);
  background: linear-gradient(135deg, rgba(142, 110, 194, 0.15), rgba(142, 110, 194, 0.05));
}

.bubble-text-box p {
  color: var(--oracle-text);
  font-size: 13px;
  line-height: 1.6;
  margin: 0;
  white-space: pre-wrap;
  word-break: break-all;
}

/* Typing Indicator animation */
.bubble-typing-loader {
  display: flex;
  gap: 4px;
  padding: 4px 6px;
  align-items: center;
}

.typing-dot {
  width: 5px;
  height: 5px;
  border-radius: 50%;
  background-color: var(--oracle-gold);
  animation: typing 1.4s infinite ease-in-out both;
}

.typing-dot:nth-child(1) { animation-delay: -0.32s; }
.typing-dot:nth-child(2) { animation-delay: -0.16s; }

@keyframes typing {
  0%, 80%, 100% { transform: scale(0); }
  40% { transform: scale(1); }
}

/* Suggestion Pills under welcoming message */
.chat-initial-suggestions {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-top: 10px;
}

.suggestion-chip {
  padding: 6px 12px;
  font-size: 11.5px;
  font-weight: 600;
  border-radius: 15px;
  border: 1px solid var(--oracle-border);
  background: var(--oracle-panel-soft);
  color: var(--oracle-faint);
  cursor: pointer;
  transition: transform 150ms cubic-bezier(0.23, 1, 0.32, 1), border-color 150ms ease-out, color 150ms ease-out, background-color 150ms ease-out, box-shadow 150ms ease-out;
}

@media (hover: hover) and (pointer: fine) {
  .suggestion-chip:hover:not(:disabled) {
    border-color: var(--oracle-gold);
    color: var(--oracle-gold-strong);
    background: var(--oracle-panel);
    box-shadow: 0 2px 8px var(--oracle-gold-glow);
  }
}

.suggestion-chip:active:not(:disabled) {
  transform: scale(0.96);
}

.suggestion-chip:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Input Form Controls */
.chat-input-area-wrap {
  padding: 16px 20px;
  border-top: 1px solid var(--oracle-border-soft);
  background: rgba(0, 0, 0, 0.05);
}

.chat-input-form {
  display: flex;
  gap: 10px;
}

.chat-text-input {
  min-width: 0;
  flex: 1;
  height: 40px;
  border: 1px solid var(--oracle-border);
  border-radius: 20px;
  padding: 0 16px;
  background: var(--oracle-panel-soft);
  color: var(--oracle-text);
  font-size: 13px;
  box-shadow: inset 0 2px 4px rgba(0,0,0,0.05);
  transition: border-color 180ms ease-out, box-shadow 180ms ease-out;
}

.chat-text-input:focus {
  border-color: var(--oracle-gold);
  box-shadow: 0 0 10px var(--oracle-gold-glow);
}

.chat-text-input::placeholder {
  color: var(--oracle-muted);
}

.chat-submit-btn {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: 1px solid var(--oracle-border);
  background: linear-gradient(135deg, var(--oracle-purple), var(--oracle-gold));
  color: #120e0a;
  display: grid;
  place-items: center;
  cursor: pointer;
  flex-shrink: 0;
  transition: transform 160ms cubic-bezier(0.23, 1, 0.32, 1), filter 160ms ease-out, box-shadow 160ms ease-out;
  box-shadow: 0 3px 10px rgba(0,0,0,0.2);
}

@media (hover: hover) and (pointer: fine) {
  .chat-submit-btn:hover:not(:disabled) {
    filter: brightness(1.15);
    box-shadow: 0 0 12px var(--oracle-gold);
    transform: scale(1.05);
  }
}

.chat-submit-btn:active:not(:disabled) {
  transform: scale(0.96);
}

.chat-submit-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.plane-svg {
  transform: rotate(0deg);
  transition: transform 0.2s ease;
}

.chat-submit-btn:hover .plane-svg {
  transform: translate(1px, -1px);
}

.chat-disclaimer {
  text-align: center;
  font-size: 10px;
  color: var(--oracle-muted);
  margin: 8px 0 0 0;
}

.chat-error-log {
  color: var(--oracle-danger);
  font-size: 11px;
  text-align: center;
  margin: 6px 0 0 0;
}

@media (max-width: 768px) {
  .oracle-chat-panel-card {
    min-height: 420px;
  }
}
</style>
