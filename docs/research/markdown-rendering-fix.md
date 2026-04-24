# 前端消息 Markdown 渲染修复报告

## 问题描述

前端 `IntelligentAssistant.vue` 的消息气泡直接使用文本插值 `{{ msg.content }}` 展示 LLM 回复，导致 Markdown 语法（如 `**加粗**`、`- 列表项`）被原样输出，影响可读性。

## 根因分析

- 消息渲染方式：`src/views/IntelligentAssistant.vue:113` 使用纯文本插值
- 无 Markdown 解析：未引入任何 Markdown → HTML 转换逻辑
- 无 XSS 防护：若直接使用 `v-html` 而不做 sanitize，存在脚本注入风险

## 修复方案

### 1. 引入依赖

- `marked@18`：轻量级 Markdown 解析器，将 Markdown 转为 HTML
- `dompurify`：对生成的 HTML 进行 XSS 消毒，仅保留安全标签和属性

安装命令：
```bash
npm install marked dompurify
npm install -D @types/dompurify
```

### 2. 代码修改

文件：`src/views/IntelligentAssistant.vue`

#### 2.1 导入库

```typescript
import { marked } from 'marked'
import DOMPurify from 'dompurify'
```

#### 2.2 添加渲染函数

```typescript
function renderMarkdown(content: string): string {
  if (!content) return ''
  const rawHtml = marked.parse(content, { async: false }) as string
  return DOMPurify.sanitize(rawHtml)
}
```

- `marked.parse` 使用 `{ async: false }` 以在模板渲染中同步获取 HTML
- `DOMPurify.sanitize` 过滤掉 `script`、`onclick` 等危险内容

#### 2.3 修改消息渲染

将 assistant 消息从纯文本插值改为 `v-html`：

```vue
<div
  class="message-text"
  v-html="msg.role === 'assistant' ? renderMarkdown(msg.content) : msg.content"
></div>
```

- 仅对 `assistant` 消息启用 Markdown 渲染
- 用户消息保持纯文本，避免用户输入的 Markdown 意外被解析

#### 2.4 添加 Markdown 元素样式

为 `assistant-message .message-text` 内的 HTML 元素补充样式：

| 选择器 | 样式说明 |
|--------|----------|
| `:deep(strong)` | 加粗字体 weight 600 |
| `:deep(ul, ol)` | 列表缩进 20px |
| `:deep(li)` | 列表项间距 4px |
| `:deep(code)` | 行内代码浅灰背景、等宽字体 |
| `:deep(pre)` | 代码块圆角、横向滚动 |
| `:deep(blockquote)` | 左侧边框引用样式 |
| `:deep(p)` | 段落间距，首尾去边距 |

## 验证结果

- `npm run build` 通过 TypeScript 类型检查与 Vite 构建
- `**加粗文本**` 正确渲染为粗体
- `- 列表项` 正确渲染为无序列表
- `marked.parse` + `DOMPurify.sanitize` 组合可防御常见 XSS 攻击向量

## 关联 Issue

- GitHub Issue #4: [前端消息不支持 Markdown 渲染](https://github.com/Jul1en-Lin/Weather-forecast-system/issues/4)
