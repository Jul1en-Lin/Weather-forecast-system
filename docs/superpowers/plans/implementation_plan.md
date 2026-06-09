# 前端改造：气象服务为主，占卜为辅

## 背景

当前页面以「Weather Oracle 气象占卜台」为品牌定位，塔罗牌、星象、运势等占卜元素在标题、文案、功能模块上占据了与气象数据同等甚至更高的视觉权重。根据[用户使用手册](file:///Users/lien/Library/Containers/com.tencent.xinWeChat/Data/Documents/xwechat_files/wxid_rngo810dcck632_8d52/msg/file/2026-05/3.%20用户使用手册.pdf)，系统定位为「基于大语言模型技术的**气象业务智能辅助平台**」，核心功能是：智能助手对话、天气数据查询、知识库管理、系统配置等。

**目标**：保留现有的神秘美学风格（深色/金色主题、玻璃态面板、金角装饰等），但在**文案语言体系、信息层级、功能定位**上将占卜降级为趣味辅助层，让气象服务成为绝对主角。

> [!IMPORTANT]
> 本次改造**只改前端文案 + 局部组件内容**，不改变任何功能逻辑、API 调用、路由结构、CSS 主题系统。所有后端代码保持不变。

---

## Proposed Changes

### 1. OracleLayout（全局导航栏 + 页脚）

#### [MODIFY] [OracleLayout.vue](file:///Users/lien/GitRepo/Weather-forecast-system/src/layouts/OracleLayout.vue)

**文案替换：**

| 位置（行号） | 现有文案 | 修改为 |
|---|---|---|
| L14 `<strong>` | `Weather Oracle` | `Weather Oracle` （保留，英文品牌名不变） |
| L15 `<span>` | `气象占卜台` | `智能气象助手` |
| L64 下拉菜单副标题 | `皇家大占卜师` / `占卜师学徒` | `系统管理员` / `气象助手用户` |
| L95 页脚 | `© 2026 Weather Oracle 气象占卜台 \| 以天象知人心` | `© 2026 Weather Oracle 智能气象助手 \| 科学预报，智慧服务` |
| L117 `userTitle` computed | `'Lv.5 皇家大占卜师'` / `'Lv.3 占卜师学徒'` | `'管理员'` / `'用户'` |

**布局微调：**
- Header 右侧的月相装饰符号 `) ☽ ◯ ☾ (`（L42-46）→ 改为天气相关装饰 `☀ ⛅ 🌤 ⛈ ❄`，或直接去掉，让 header 更简洁专业

---

### 2. TarotCardDisplay（中间主卡片——核心改动）

#### [MODIFY] [TarotCardDisplay.vue](file:///Users/lien/GitRepo/Weather-forecast-system/src/components/oracle/TarotCardDisplay.vue)

**文案替换：**

| 位置 | 现有文案 | 修改为 |
|---|---|---|
| L6 eyebrow | `Tarot Weather Divination` | `Weather Intelligence` |
| L7 h2 | `今日天气塔罗牌` | `今日天气概览` |
| L8 副标题 | `AI 为你抽取今日的天气指引` | `AI 为你解读今日天气` |
| L49-51 右侧guidance标题 | `✦ 今日指引 ✦` | `✦ 今日提示 ✦`（微调） |

**信息层级调整（重要）：**

目前卡片结构是：左列（标题+城市）→ 中列（塔罗牌图）→ 右列（运势指引）。建议做以下调整来**突出天气数据**：

1. **右列标题**：`{{ tarot.name_zh }} · {{ fortune.title }}` → 改为 `{{ fortune.title }}`（去掉塔罗牌中文名，让标题更聚焦天气含义）
2. **右列 keywords chips 文案**：保留不变（这些来自后端，是"行动/情绪/提醒"类标签，与天气关联度高）
3. **右列"宜/忌"标签**：`宜` / `忌` → 改为 `适宜` / `注意`
4. **右列"幸运色/幸运数字"**：改为 `今日色彩` / `今日数字`（降低"幸运"的占卜感）
5. **塔罗牌图片区域**：保留不变（这是页面的视觉亮点，作为"AI 生成的每日天气插画"概念存在完全合理）
6. **左列 fallback 文案**（L38）：`牌面待导出` → `天气卡片加载中`

---

### 3. WeatherMetricGrid（天气数据面板）

#### [MODIFY] [WeatherMetricGrid.vue](file:///Users/lien/GitRepo/Weather-forecast-system/src/components/oracle/WeatherMetricGrid.vue)

**文案替换：**

| 位置 | 现有文案 | 修改为 |
|---|---|---|
| L4 eyebrow | `Weather & Destiny Mapping` | `Real-time Weather Data` |
| L5 标题 | `天气数据 · 命运映射` | `实时天气数据` |
| L6 副标题 | `将物理天气要素转化为今日的心灵能量指引` | `当前城市气象要素综合分析` |

> [!NOTE]
> 这个组件的实际功能（温度/湿度/气压/风速四宫格）完全是正经的气象数据展示，只是原来的文案太「占卜」了。改完文案后气象属性会非常突出。

---

### 4. OracleLeftSidebar（左侧边栏）

#### [MODIFY] [OracleLeftSidebar.vue](file:///Users/lien/GitRepo/Weather-forecast-system/src/components/oracle/OracleLeftSidebar.vue)

**"今日星象"卡片 → "今日气象小贴士"**

| 位置 | 现有文案 | 修改为 |
|---|---|---|
| L30 eyebrow | `Astrology` | `Daily Tips` |
| L31 标题 | `今日星象` | `每日气象贴士` |
| L51 `月亮进入{{ currentZodiac.sign }}` | 星座运势文本 | 改为气象生活贴士（见下方） |

**星座运势数组 → 气象生活贴士数组**

将 `zodiacSigns` 数组替换为气象生活提示，例如：

```typescript
const weatherTips = [
  { title: '紫外线提示', advice: '夏季紫外线较强，外出建议涂抹防晒霜、佩戴遮阳帽' },
  { title: '防暑降温', advice: '高温天气注意补充水分，避免长时间户外暴晒' },
  { title: '雷雨天气', advice: '雷雨天气避免在空旷地带停留，远离金属物体' },
  { title: '台风预防', advice: '台风来临前检查门窗，储备必要物资，关注预警信息' },
  { title: '雾天出行', advice: '大雾天气能见度低，驾车请减速慢行、开启雾灯' },
  { title: '寒潮提醒', advice: '寒潮来临注意添衣保暖，预防感冒和心血管疾病' },
  { title: '空气质量', advice: '关注空气质量指数，污染天气减少户外活动' },
  { title: '干燥天气', advice: '秋冬干燥季节注意补水保湿，预防静电和皮肤干裂' },
  { title: '晨练建议', advice: '晴好天气适宜户外运动，但避开高温时段' },
  { title: '梅雨季节', advice: '梅雨期间注意防潮除湿，衣物及时晾晒烘干' },
  { title: '霜冻预警', advice: '霜冻天气注意农作物保护，行车注意路面结冰' },
  { title: '气压变化', advice: '气压剧烈波动可能引起头痛不适，注意休息调节' },
]
```

**月相 SVG → 天气图标 SVG**

将月相 SVG 图形替换为一个简约的**太阳/云朵/雨滴**组合 SVG 装饰图标（保留金色发光效果）。

**"查看详情 →" 链接**：保留，指向知识库。

---

### 5. OracleBottomCards（底部四卡片）

#### [MODIFY] [OracleBottomCards.vue](file:///Users/lien/GitRepo/Weather-forecast-system/src/components/oracle/OracleBottomCards.vue)

**四卡片内容调整：**

| 卡片 | 现有内容 | 修改为 |
|---|---|---|
| 卡片1 | 🧭 每日运势（星级评分：综合/爱情/财富） | 🌡️ **生活气象指数**（穿衣指数/运动指数/紫外线指数，同样用星级展示） |
| 卡片2 | 📜 天气签文（古诗句） | 📜 **天气签文**（✅ 保留不变，这个结合天气场景感很好，诗句本身也与天气有关） |
| 卡片3 | 🔮 灵感建议（水晶球） | ☂️ **出行建议**（基于天气给出的出行/运动/户外活动建议） |
| 卡片4 | 📚 知识库推荐 | 📚 **气象知识推荐**（✅ 基本保留，更新推荐文章标题为气象科普类） |

**卡片1 具体修改：**
- eyebrow: `Fortune Ratings` → `Life Weather Index`
- 标题: `🧭 每日运势` → `🌡️ 生活气象指数`
- 三行评分: `综合运势/爱情运势/财富运势` → `穿衣指数/运动指数/紫外线指数`

**卡片3 具体修改：**
- eyebrow: `Crystal Ball Tips` → `Travel Advisory`
- 标题: `🔮 灵感建议` → `☂️ 出行建议`
- 内容文案: 固定文本 → 改为与天气相关的出行建议文案

**卡片4 推荐文章更新：**
- `📖 解读云的语言` → `📖 常见天气符号解读`
- `📖 天气与情绪的关系` → `📖 气象灾害防御指南`
- `📖 风的象征意义` → `📖 天气预报入门知识`

---

### 6. OracleChatPanel（右侧聊天面板）

#### [MODIFY] [OracleChatPanel.vue](file:///Users/lien/GitRepo/Weather-forecast-system/src/components/oracle/OracleChatPanel.vue)

**文案替换：**

| 位置 | 现有文案 | 修改为 |
|---|---|---|
| L12 h4 | `天气占卜师` | `天气助手` |
| L13 span | `你的专属天气与心灵向导` | `你的智能气象服务助理` |
| L32 助手头像 emoji | `🔮` | `🌤️` |
| L37 sender name | `天气占卜师` | `天气助手` |
| L75 input placeholder | `继续追问今日天气牌...` | `输入天气相关问题...` |
| L118 suggestions 数组 | `['今天天气如何影响我的状态？', '今日运势解析', '适合出行吗？', '给我一句天气签文。']` | `['今天需要带伞吗？', '本周天气预报', '适合户外运动吗？', '今天穿什么合适？']` |
| L128 初始欢迎消息 | `你好，我是你的天气占卜师。今天想了解什么呢？` | `你好，我是你的智能天气助手。有什么天气问题可以问我~` |
| L184 / L190 system prompt | `你是天气占卜师` | `你是智能天气助手` |
| L184 prompt 详细内容 | `请以占卜师的温柔口吻...` | `请友好地提醒用户可以...` |

---

### 7. MoodGuidePanel（情绪状态指南面板）

#### [MODIFY] [MoodGuidePanel.vue](file:///Users/lien/GitRepo/Weather-forecast-system/src/components/oracle/MoodGuidePanel.vue)

**文案替换：**

| 位置 | 现有文案 | 修改为 |
|---|---|---|
| L4 eyebrow | `Mood & Activity Guide` | `Weather Life Guide` |
| L5 标题 | `今日情绪状态指南` | `今日天气生活指南` |

> [!NOTE]
> 这个面板实际展示的是后端返回的 `mood_guide` 数据（analysis + suggestions），内容是基于天气生成的生活建议。改完标题后，与实际内容非常匹配。

---

### 8. WeatherOracle 主页面（占位符状态文案）

#### [MODIFY] [WeatherOracle.vue](file:///Users/lien/GitRepo/Weather-forecast-system/src/views/WeatherOracle.vue)

**占位符文案替换：**

| 位置 | 现有文案 | 修改为 |
|---|---|---|
| L44 emoji | `🔮` | `🌤️` |
| L45 h3 | `正在召唤今日天气牌` | `正在获取今日天气` |
| L46 p | `读取气象要素与星相规律，正在生成你今天的能量映射...` | `正在查询气象数据，为你生成今日天气报告...` |

---

### 9. QuickCityPicker（城市选择器）

#### [MODIFY] [QuickCityPicker.vue](file:///Users/lien/GitRepo/Weather-forecast-system/src/components/oracle/QuickCityPicker.vue)

检查是否有占卜相关文案（如按钮文字"抽取"等），如有则替换：
- `抽取` → `查询`
- `抽牌` → `查看天气`

---

### 10. index.html 页面标题

#### [MODIFY] [index.html](file:///Users/lien/GitRepo/Weather-forecast-system/index.html)

- `<title>` 标签内容如果包含"占卜"，改为 `Weather Oracle - 智能气象助手`

---

## 不修改的部分

> [!TIP]
> 以下内容保持不变，作为页面的"视觉特色/趣味元素"存在：

1. **CSS 主题系统**（`oracle-theme.css`）—— 深色金色的神秘美学风格完全保留
2. **塔罗牌图片展示** —— 作为"AI 生成的每日天气艺术卡"概念保留
3. **金色角标装饰**（`.oracle-gold-corners`）—— 纯装饰，保留
4. **天气签文卡片**（底部卡片2）—— 诗句与天气强相关，保留
5. **所有后端逻辑和 API** —— 不做任何修改
6. **路由路径**（`/oracle`）—— 保留不改
7. **组件文件名** —— 保留 `Oracle*` 命名不改（避免大范围重构）

---

## 修改汇总

共涉及 **10 个文件**，全部为**纯文案/静态内容修改**，无逻辑变更：

| 文件 | 改动类型 | 复杂度 |
|---|---|---|
| [OracleLayout.vue](file:///Users/lien/GitRepo/Weather-forecast-system/src/layouts/OracleLayout.vue) | 文案替换 (5处) | ⭐ 低 |
| [TarotCardDisplay.vue](file:///Users/lien/GitRepo/Weather-forecast-system/src/components/oracle/TarotCardDisplay.vue) | 文案替换 (6处) | ⭐ 低 |
| [WeatherMetricGrid.vue](file:///Users/lien/GitRepo/Weather-forecast-system/src/components/oracle/WeatherMetricGrid.vue) | 文案替换 (3处) | ⭐ 低 |
| [OracleLeftSidebar.vue](file:///Users/lien/GitRepo/Weather-forecast-system/src/components/oracle/OracleLeftSidebar.vue) | 文案 + 数据数组重写 + SVG 替换 | ⭐⭐ 中 |
| [OracleBottomCards.vue](file:///Users/lien/GitRepo/Weather-forecast-system/src/components/oracle/OracleBottomCards.vue) | 文案 + 部分内容重写 | ⭐⭐ 中 |
| [OracleChatPanel.vue](file:///Users/lien/GitRepo/Weather-forecast-system/src/components/oracle/OracleChatPanel.vue) | 文案替换 (8处) + system prompt 修改 | ⭐⭐ 中 |
| [MoodGuidePanel.vue](file:///Users/lien/GitRepo/Weather-forecast-system/src/components/oracle/MoodGuidePanel.vue) | 文案替换 (2处) | ⭐ 低 |
| [WeatherOracle.vue](file:///Users/lien/GitRepo/Weather-forecast-system/src/views/WeatherOracle.vue) | 文案替换 (3处) | ⭐ 低 |
| [QuickCityPicker.vue](file:///Users/lien/GitRepo/Weather-forecast-system/src/components/oracle/QuickCityPicker.vue) | 文案替换（检查后决定） | ⭐ 低 |
| [index.html](file:///Users/lien/GitRepo/Weather-forecast-system/index.html) | title 标签 | ⭐ 低 |

---

## Verification Plan

### 构建验证
```bash
npm run build
```
确保无 TypeScript 编译错误。

### 手动验证
1. 启动 `npm run dev`，浏览器打开首页
2. 逐项检查所有修改的文案是否正确显示
3. 确认功能不受影响：城市切换、天气查询、右侧聊天、底部卡片交互
4. 确认深色/浅色主题切换正常
5. 确认响应式布局在窄屏下正常

---

## 执行建议

建议按以下优先级分批执行：

**第一批（最高优先级 - 15 分钟内完成）：**
1. OracleLayout.vue 文案
2. TarotCardDisplay.vue 文案
3. WeatherMetricGrid.vue 文案
4. OracleChatPanel.vue 文案
5. MoodGuidePanel.vue 文案
6. WeatherOracle.vue 文案
7. index.html title

**第二批（中优先级 - 30 分钟内完成）：**
8. OracleBottomCards.vue 卡片内容重写
9. OracleLeftSidebar.vue 星象→气象贴士重写

**第三批（低优先级 - 可选）：**
10. QuickCityPicker.vue 检查

