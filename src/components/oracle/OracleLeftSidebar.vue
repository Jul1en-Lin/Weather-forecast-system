<template>
  <aside class="oracle-left-sidebar">
    <!-- Quick Entry Card -->
    <div class="quick-entry-card oracle-surface oracle-gold-corners">
      <span class="oracle-eyebrow">Quick Navigation</span>
      <h3 class="card-title">快捷入口</h3>

      <nav class="sidebar-menu">
        <router-link to="/intelligent-assistant" class="menu-item">
          <span class="menu-icon">💬</span>
          <span class="menu-text">智能对话</span>
        </router-link>
        <router-link to="/oracle" class="menu-item" @click="handleSearchTrigger">
          <span class="menu-icon">🌤️</span>
          <span class="menu-text">天气查询</span>
        </router-link>
        <router-link to="/knowledge-base" class="menu-item">
          <span class="menu-icon">📖</span>
          <span class="menu-text">知识库</span>
        </router-link>
        <router-link v-if="isAdmin" to="/admin/users" class="menu-item">
          <span class="menu-icon">👥</span>
          <span class="menu-text">用户管理</span>
        </router-link>
      </nav>
    </div>

    <!-- Horoscope Card -->
    <div class="horoscope-card oracle-surface oracle-gold-corners">
      <span class="oracle-eyebrow">Daily Tips</span>
      <h3 class="card-title">每日气象贴士</h3>

      <div class="moon-phase-display">
        <!-- SVG Weather Graphic -->
        <svg viewBox="0 0 100 100" width="72" height="72" class="moon-svg">
          <defs>
            <radialGradient id="weatherGlow" cx="50%" cy="50%" r="50%">
              <stop offset="0%" stop-color="#fff" stop-opacity="0.8" />
              <stop offset="60%" stop-color="#fff8d6" stop-opacity="0.3" />
              <stop offset="100%" stop-color="#d7ae69" stop-opacity="0" />
            </radialGradient>
          </defs>
          <circle cx="50" cy="50" r="40" fill="rgba(255,255,255,0.03)" stroke="var(--oracle-border-soft)" stroke-width="1" />
          <circle cx="50" cy="50" r="30" fill="url(#weatherGlow)" class="glow-circle" />
          <circle cx="50" cy="50" r="20" fill="none" stroke="var(--oracle-gold)" stroke-width="1.5" stroke-dasharray="4 3" />
          <path d="M 35 65 A 10 10 0 0 1 45 55 A 12 12 0 0 1 67 55 A 10 10 0 0 1 77 65 Z" fill="rgba(255,255,255,0.15)" stroke="var(--oracle-gold)" stroke-width="1" />
        </svg>
      </div>

      <div class="horoscope-info">
        <strong class="moon-sign-title">{{ displayTip.title }}</strong>
        <p class="moon-sign-copy">{{ displayTip.advice }}</p>

        <router-link to="/knowledge-base" class="view-detail-link">
          查看详情 →
        </router-link>
      </div>
    </div>

    <!-- Weather Verse Scroll Card -->
    <div class="verse-card oracle-surface oracle-gold-corners">
      <span class="oracle-eyebrow">Weather Verse</span>
      <h3 class="card-title">天气签文</h3>

      <div class="verse-scroll-display">
        <span class="verse-scroll-icon">📜</span>
      </div>

      <p class="verse-content-text">&ldquo;{{ currentVerse }}&rdquo;</p>

      <div class="verse-footer">
        <button type="button" class="change-verse-btn" @click="rotateVerse">
          换一签 🔄
        </button>
      </div>
    </div>
  </aside>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import type { WeatherOracleTip } from '../../types/weatherOracle'
import { useAuthStore } from '../../stores/auth'

const props = defineProps<{
  weatherTip?: WeatherOracleTip
}>()

const authStore = useAuthStore()
const isAdmin = computed(() => authStore.isAdmin)

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

// Compute a dynamic tip based on the current date of the month
const displayTip = computed(() => {
  if (props.weatherTip && props.weatherTip.title && props.weatherTip.advice) {
    return props.weatherTip
  }
  const day = new Date().getDate()
  return weatherTips[day % weatherTips.length]
})

function handleSearchTrigger() {
  const el = document.querySelector('.oracle-city-select-trigger') as HTMLElement
  if (el) el.click()
}

// Weather verse data
const verses = [
  '云卷云舒皆有意，雨落雨停总相宜。心若明朗，处处晴晴。',
  '长风破浪会有时，直挂云帆济沧海。今日有风，宜勇往直前。',
  '随风潜入夜，漴物细无声。静待雨露滋润，思绪自然通达。',
  '千山鸟飞绝，万径人踪灭。适宜静坐内省，归零后再出发。',
  '东边日出西边雨，道是无晴却有晴。得失随缘，一切皆是最好安排。',
  '山重水复疑无路，柳暗花明又一村。拨云见日，微光在前。',
  '海阔凭鱼跃，天高任鸟飞。晴空万里，宜施展才干。',
  '清风徐来，水波不兴。理顺呼吸，以平常心静观万物之变。',
  '露从今夜白，月是故乡明。夹空寂静，宜与重要的人互致问候。',
  '志如一夜春风来，千树万树梨花开。灵感如雪花，静静承接即可。',
  '青笻筠，绳蜟衣，斜风细雨不须归。细雨斜飞，亦是诗意人生。',
  '好雨知时节，当春水发生。顺应天时，正是积蓄力量的时刻。',
  '天街小雨润如酯，草色遥看近却无。留意细微之处，惊喜正在醝酿。',
  '回首向来耙煅处，归去，也无风雨也无晴。超然物外，心宽自安。',
  '月落乌啊霜满天，江枫渔火对愁眠。虽有清冷凝霜，沉静思索更显珍贵。',
  '昨夜星辰昨夜风，画楼西畜桂堂东。微风掠过，带走思绪中的繁杂。',
  '水光潋滣晴方好，山色空蒙雨亦奇。晴雨皆是风景，接纳生活的全部面貌。',
  '沿衣欲湿杏花雨，吹面不寒杨柳风。微风拂面，适宜放松身心，去户外走走。',
  '千里黄云白日曲，北风吹雁雪纷纷。风雪虽急，信念坚定即可驱散寒意。',
  '小楼一夜听春雨，深巷明朝卖杏花。雨后必有晴天，静候生活的美好结放。',
  '行到水穷处，坐看云起时。不必急于求成，静观风起云溌。',
  '明月别枝惊鹊，清风半夜鸣蝉。夏夜清凁，宜安枕无忧。',
  '春风得意马蹄疾，一日看尽长安花。风和日丽，正是拼搯奋进的大好时机。',
  '溪云初起日沉阁，山雨欲来风满楼。风起之时，宜沉着应对，做好万全准备。',
  '白日依山尽，黄河入海流。欲穷千里目，更上一层楼。前路开阔，勇往直前。'
]

const currentVerseIndex = ref(new Date().getDate() % verses.length)
const currentVerse = computed(() => verses[currentVerseIndex.value])

function rotateVerse() {
  currentVerseIndex.value = (currentVerseIndex.value + 1) % verses.length
}
</script>

<style scoped>
.oracle-left-sidebar {
  display: flex;
  flex-direction: column;
  gap: 20px;
  width: 100%;
}

.quick-entry-card,
.horoscope-card {
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.card-title {
  font-family: var(--oracle-font-serif);
  font-size: 18px;
  color: var(--oracle-text);
  margin: 0;
  letter-spacing: 0.02em;
}

/* Sidebar Menu */
.sidebar-menu {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-top: 4px;
}

.menu-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  border-radius: 8px;
  border: 1px solid var(--oracle-border-soft);
  background: var(--oracle-panel-soft);
  color: var(--oracle-faint);
  font-size: 14px;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.menu-item:hover {
  border-color: var(--oracle-gold);
  color: var(--oracle-gold-strong);
  background: var(--oracle-panel);
  box-shadow: 0 4px 12px var(--oracle-gold-glow);
}

.menu-icon {
  font-size: 16px;
}

/* Horoscope Card display */
.moon-display-wrapper {
  display: flex;
  justify-content: center;
}

.moon-phase-display {
  display: grid;
  place-items: center;
  padding: 10px 0;
}

.moon-svg {
  filter: drop-shadow(0 0 8px var(--oracle-gold-glow));
}

.glow-circle {
  animation: pulse-mystical 4s ease-in-out infinite;
}

.horoscope-info {
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  margin-top: 6px;
}

.moon-sign-title {
  font-family: var(--oracle-font-serif);
  color: var(--oracle-text);
  font-size: 15px;
}

.moon-sign-copy {
  color: var(--oracle-muted);
  font-size: 12.5px;
  line-height: 1.6;
  margin: 0;
}

.view-detail-link {
  font-size: 12px;
  color: var(--oracle-gold);
  font-weight: 600;
  text-decoration: none;
  margin-top: 4px;
  transition: all 0.2s ease;
}

.view-detail-link:hover {
  color: var(--oracle-gold-strong);
  transform: translateX(2px);
}
.verse-card {
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.verse-scroll-display {
  display: grid;
  place-items: center;
  padding: 6px 0;
  font-size: 32px;
  filter: drop-shadow(0 0 6px var(--oracle-gold-glow));
}

.verse-content-text {
  font-family: var(--oracle-font-serif);
  font-style: italic;
  font-size: 13px;
  color: var(--oracle-faint);
  line-height: 1.75;
  margin: 0;
  flex: 1;
  text-align: center;
}

.verse-footer {
  display: flex;
  justify-content: center;
  margin-top: 4px;
}

.change-verse-btn {
  font-size: 11px;
  color: var(--oracle-gold);
  background: var(--oracle-panel-soft);
  border: 1px solid var(--oracle-border-soft);
  border-radius: 12px;
  padding: 5px 14px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s ease;
}

.change-verse-btn:hover {
  border-color: var(--oracle-gold);
  color: var(--oracle-gold-strong);
  background: var(--oracle-panel);
  box-shadow: 0 0 6px var(--oracle-gold-glow);
}
</style>
