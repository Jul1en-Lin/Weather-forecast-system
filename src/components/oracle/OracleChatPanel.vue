<template>
  <section class="oracle-chat-panel">
    <header>
      <div>
        <span>天气牌问答</span>
        <h2>{{ city }} 今日追问</h2>
      </div>
      <small v-if="modelName">模型：{{ modelName }}</small>
    </header>

    <div class="oracle-chat-suggestions">
      <button
        v-for="item in suggestions"
        :key="item"
        type="button"
        :disabled="isSending || !selectedModel"
        @click="sendMessage(item)"
      >
        {{ item }}
      </button>
    </div>

    <div class="oracle-chat-messages" aria-live="polite">
      <p v-if="messages.length === 0" class="oracle-chat-empty">
        可以追问今日天气、出行和状态建议。
      </p>
      <article
        v-for="(message, index) in messages"
        :key="`${message.role}-${index}`"
        :class="['oracle-chat-message', `is-${message.role}`]"
      >
        <span>{{ message.role === 'user' ? '你' : '天气牌' }}</span>
        <p>{{ message.content }}</p>
      </article>
    </div>

    <form class="oracle-chat-input" @submit.prevent="submitCustomMessage">
      <input
        v-model.trim="draftMessage"
        type="text"
        placeholder="继续追问今日天气牌"
        :disabled="isSending || !selectedModel"
      />
      <button type="submit" :disabled="!draftMessage || isSending || !selectedModel">
        {{ isSending ? '发送中' : '发送' }}
      </button>
    </form>

    <p v-if="errorMessage" class="oracle-chat-error">{{ errorMessage }}</p>
  </section>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import type { WeatherOracleReading } from '../../types/weatherOracle'

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
  city: string
  reading: WeatherOracleReading
}>()

const suggestions = ['今天天气如何影响我的状态？', '今日运势解析', '适合出行吗？', '给我一句天气签文。']
const models = ref<ModelInfo[]>([])
const selectedModel = ref('')
const messages = ref<ChatMessage[]>([])
const draftMessage = ref('')
const isSending = ref(false)
const errorMessage = ref('')

const modelName = computed(() => {
  return models.value.find(model => model.id === selectedModel.value)?.name || ''
})

onMounted(() => {
  loadModels()
})

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
    selectedModel.value = models.value[0]?.id || ''
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
  const weather = props.reading.weather
  return [
    '你是天气占卜师，请结合以下天气牌上下文回答用户追问。',
    `城市：${props.city}`,
    `日期：${props.reading.date}`,
    `塔罗牌：${props.reading.tarot.name_zh || props.reading.tarot.name_en}`,
    `天气：${weather.condition}，温度 ${weather.temperature ?? '未知'}°C，湿度 ${weather.humidity ?? '未知'}%，气压 ${weather.pressure ?? '未知'} hPa，风速 ${weather.wind_speed ?? '未知'} km/h，风向 ${weather.wind_direction || '未知'}`,
    `今日运势：${props.reading.fortune.summary}`,
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
          if (data === '[DONE]') return
          try {
            const parsed = JSON.parse(data) as { chunk?: string; error?: string }
            if (parsed.error) throw new Error(parsed.error)
            if (parsed.chunk) assistantMessage.content += parsed.chunk
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
  }
}
</script>

<style scoped>
.oracle-chat-panel {
  display: grid;
  grid-template-rows: auto auto minmax(220px, 1fr) auto auto;
  gap: 16px;
  min-width: 0;
  min-height: 100%;
  padding: 22px;
  border: 1px solid var(--oracle-border);
  border-radius: 8px;
  background:
    linear-gradient(180deg, rgba(127, 183, 255, 0.11), transparent 30%),
    var(--oracle-panel);
  box-shadow: var(--oracle-shadow);
}

.oracle-chat-panel header {
  display: flex;
  align-items: start;
  justify-content: space-between;
  gap: 16px;
  min-width: 0;
}

.oracle-chat-panel header span,
.oracle-chat-panel header small {
  color: var(--oracle-muted);
  font-size: 13px;
}

.oracle-chat-panel h2 {
  margin: 4px 0 0;
  color: var(--oracle-text);
  font-size: 22px;
  overflow-wrap: anywhere;
}

.oracle-chat-suggestions {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.oracle-chat-suggestions button,
.oracle-chat-input button {
  border: 1px solid var(--oracle-border-soft);
  border-radius: 8px;
  background: var(--oracle-panel-soft);
  color: var(--oracle-text);
  cursor: pointer;
  font-size: 14px;
  font-weight: 700;
  transition: border-color 0.2s ease, background-color 0.2s ease, color 0.2s ease;
}

.oracle-chat-suggestions button {
  padding: 8px 12px;
  max-width: 100%;
  overflow-wrap: anywhere;
}

.oracle-chat-suggestions button:not(:disabled):hover,
.oracle-chat-input button:not(:disabled):hover {
  border-color: var(--oracle-gold);
  color: var(--oracle-gold-strong);
}

.oracle-chat-suggestions button:disabled,
.oracle-chat-input button:disabled,
.oracle-chat-input input:disabled {
  cursor: not-allowed;
  opacity: 0.55;
}

.oracle-chat-messages {
  display: grid;
  align-content: start;
  gap: 12px;
  min-height: 0;
  max-height: 520px;
  overflow: auto;
  padding-right: 4px;
}

.oracle-chat-empty {
  margin: 0;
  color: var(--oracle-muted);
}

.oracle-chat-message {
  display: grid;
  gap: 4px;
  padding: 12px 14px;
  border: 1px solid var(--oracle-border-soft);
  border-radius: 8px;
  background: var(--oracle-panel-soft);
}

.oracle-chat-message.is-user {
  border-color: rgba(168, 138, 223, 0.32);
  background: rgba(168, 138, 223, 0.14);
}

.oracle-chat-message span {
  color: var(--oracle-muted);
  font-size: 12px;
  font-weight: 700;
}

.oracle-chat-message p {
  margin: 0;
  color: var(--oracle-text);
  line-height: 1.7;
  white-space: pre-wrap;
  overflow-wrap: anywhere;
}

.oracle-chat-input {
  display: flex;
  gap: 10px;
  min-width: 0;
}

.oracle-chat-input input {
  min-width: 0;
  flex: 1;
  height: 42px;
  border: 1px solid var(--oracle-border);
  border-radius: 8px;
  padding: 0 12px;
  background: var(--oracle-panel-soft);
  color: var(--oracle-text);
}

.oracle-chat-input input::placeholder {
  color: var(--oracle-muted);
}

.oracle-chat-input button {
  min-width: 78px;
  height: 42px;
  border-color: var(--oracle-border);
  background: linear-gradient(135deg, var(--oracle-purple), var(--oracle-gold));
  color: #141015;
}

.oracle-chat-error {
  margin: 0;
  color: var(--oracle-danger);
  font-size: 14px;
  overflow-wrap: anywhere;
}

@media (max-width: 1280px) {
  .oracle-chat-messages {
    max-height: 360px;
  }
}

@media (max-width: 560px) {
  .oracle-chat-panel {
    grid-template-rows: auto auto minmax(190px, auto) auto auto;
    padding: 18px;
  }

  .oracle-chat-panel header {
    display: grid;
  }

  .oracle-chat-input {
    display: grid;
    grid-template-columns: minmax(0, 1fr) 72px;
  }

  .oracle-chat-input button {
    min-width: 0;
  }
}
</style>
