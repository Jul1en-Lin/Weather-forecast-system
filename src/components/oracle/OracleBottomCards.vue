<template>
  <div class="oracle-bottom-cards-row">
    <!-- Card 1: Daily ratings -->
    <div class="oracle-bottom-card oracle-surface oracle-gold-corners">
      <span class="oracle-eyebrow">Life Weather Index</span>
      <h4 class="card-title">
        <span class="card-icon">🌡️</span> 生活气象指数
      </h4>
      <div class="ratings-list">
        <div class="rating-row">
          <span class="rating-label">穿衣指数</span>
          <span class="stars-wrap">{{ getStarsString(overallRating) }}</span>
        </div>
        <div class="rating-row">
          <span class="rating-label">运动指数</span>
          <span class="stars-wrap">{{ getStarsString(loveRating) }}</span>
        </div>
        <div class="rating-row">
          <span class="rating-label">紫外线指数</span>
          <span class="stars-wrap">{{ getStarsString(wealthRating) }}</span>
        </div>
      </div>
    </div>

    <!-- Card 2: Travel Advisory -->
    <div class="oracle-bottom-card oracle-surface oracle-gold-corners">
      <span class="oracle-eyebrow">Travel Advisory</span>
      <h4 class="card-title">
        <span class="card-icon">☂️</span> 出行建议
      </h4>
      <p class="tip-content-text">
        晴天外出注意防晒与补水，雨天出行备好雨具并减速慢行。关注温差适度增减衣物。
      </p>
    </div>

    <!-- Card 3: Weather Verse Scroll -->
    <div class="oracle-bottom-card oracle-surface oracle-gold-corners">
      <span class="oracle-eyebrow">Weather Verse</span>
      <h4 class="card-title">
        <span class="card-icon">📜</span> 天气签文
      </h4>
      <p class="verse-content-text">
        “{{ currentVerse }}”
      </p>
      <div class="verse-action-footer">
        <button type="button" class="change-verse-btn" @click="rotateVerse">
          换一签 🔄
        </button>
      </div>
    </div>

    <!-- Card 4: Knowledge Base Recommend -->
    <div class="oracle-bottom-card oracle-surface oracle-gold-corners">
      <span class="oracle-eyebrow">Recommended Readings</span>
      <h4 class="card-title">
        <span class="card-icon">📚</span> 知识库推荐
      </h4>
      <ul class="rec-links-list">
        <li>
          <router-link to="/knowledge-base" class="rec-link-item">📖 常见天气符号解读</router-link>
        </li>
        <li>
          <router-link to="/knowledge-base" class="rec-link-item">📖 气象灾害防御指南</router-link>
        </li>
        <li>
          <router-link to="/knowledge-base" class="rec-link-item">📖 天气预报入门知识</router-link>
        </li>
      </ul>
      <router-link to="/knowledge-base" class="card-link-footer">进入知识库 →</router-link>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

const props = defineProps<{
  luckyNumber?: number
}>()

// Dyn ratings derived from the lucky number
const seed = computed(() => props.luckyNumber || 7)

const overallRating = computed(() => (seed.value % 3) + 3) // 3, 4, 5
const loveRating = computed(() => ((seed.value + 2) % 3) + 3)
const wealthRating = computed(() => ((seed.value + 1) % 3) + 3)

function getStarsString(rating: number): string {
  const fullStar = '★'
  const emptyStar = '☆'
  return fullStar.repeat(rating) + emptyStar.repeat(5 - rating)
}

// Collection of mystical poems
const verses = [
  '云卷云舒皆有意，雨落雨停总相宜。心若明朗，处处晴晴。',
  '长风破浪会有时，直挂云帆济沧海。今日有风，宜勇往直前。',
  '随风潜入夜，润物细无声。静待雨露滋润，思绪自然通达。',
  '千山鸟飞绝，万径人踪灭。适宜静坐内省，归零后再出发。',
  '东边日出西边雨，道是无晴却有晴。得失随缘，一切皆是最好安排。',
  '山重水复疑无路，柳暗花明又一村。拨云见日，微光在前。',
  '海阔凭鱼跃，天高任鸟飞。晴空万里，宜施展才干。',
  '清风徐来，水波不兴。理顺呼吸，以平常心静观万物之变。',
  '露从今夜白，月是故乡明。夜空寂静，宜与重要的人互致问候。',
  '忽如一夜春风来，千树万树梨花开。灵感如雪花，静静承接即可。',
  '青箬笠，绿蓑衣，斜风细雨不须归。细雨斜飞，亦是诗意人生。',
  '好雨知时节，当春乃发生。顺应天时，正是积蓄力量的时刻。',
  '天街小雨润如酥，草色遥看近却无。留意细微之处，惊喜正在酝酿。',
  '回首向来萧瑟处，归去，也无风雨也无晴。超然物外，心宽自安。',
  '月落乌啼霜满天，江枫渔火对愁眠。虽有清冷凝霜，沉静思索更显珍贵。',
  '昨夜星辰昨夜风，画楼西畔桂堂东。微风掠过，带走思绪中的繁杂。',
  '水光潋滟晴方好，山色空蒙雨亦奇。晴雨皆是风景，接纳生活的全部面貌。',
  '沾衣欲湿杏花雨，吹面不寒杨柳风。微风拂面，适宜放松身心，去户外走走。',
  '千里黄云白日曛，北风吹雁雪纷纷。风雪虽急，信念坚定即可驱散寒意。',
  '小楼一夜听春雨，深巷明朝卖杏花。雨后必有晴天，静候生活的美好绽放。',
  '行到水穷处，坐看云起时。不必急于求成，静观风起云涌。',
  '明月别枝惊鹊，清风半夜鸣蝉。夏夜清凉，宜安枕无忧。',
  '春风得意马蹄疾，一日看尽长安花。风和日丽，正是拼搏奋进的大好时机。',
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
.oracle-bottom-cards-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  width: 100%;
}

.oracle-bottom-card {
  padding: 18px 20px 22px 20px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  min-height: 172px;
  box-sizing: border-box;
}

.card-title {
  font-family: var(--oracle-font-serif);
  font-size: 15px;
  color: var(--oracle-text);
  margin: 2px 0 4px 0;
  display: flex;
  align-items: center;
  gap: 8px;
}

.card-icon {
  font-size: 15px;
}

/* Ratings */
.ratings-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-top: 4px;
}

.rating-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 12.5px;
}

.rating-label {
  color: var(--oracle-muted);
}

.stars-wrap {
  color: var(--oracle-gold);
  letter-spacing: 2px;
  font-size: 13px;
}

/* Texts */
.verse-content-text {
  font-family: var(--oracle-font-serif);
  font-style: italic;
  font-size: 13px;
  color: var(--oracle-faint);
  line-height: 1.6;
  margin: 0;
  flex: 1;
}

.tip-content-text {
  font-size: 12.5px;
  color: var(--oracle-muted);
  line-height: 1.6;
  margin: 0;
  flex: 1;
}

/* Rec Links */
.rec-links-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 6px;
  flex: 1;
}

.rec-link-item {
  font-size: 12px;
  color: var(--oracle-faint);
  text-decoration: none;
  transition: all 0.2s ease;
}

.rec-link-item:hover {
  color: var(--oracle-gold-strong);
  padding-left: 2px;
}

/* Footer elements */
.card-link-footer {
  font-size: 11px;
  color: var(--oracle-gold);
  font-weight: 700;
  text-decoration: none;
  margin-top: auto;
  align-self: flex-start;
  transition: all 0.2s ease;
}

.card-link-footer:hover {
  color: var(--oracle-gold-strong);
  transform: translateX(2px);
}

.verse-action-footer {
  margin-top: auto;
  display: flex;
}

.change-verse-btn {
  font-size: 11px;
  color: var(--oracle-gold);
  background: var(--oracle-panel-soft);
  border: 1px solid var(--oracle-border-soft);
  border-radius: 12px;
  padding: 4px 12px;
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

/* Responsiveness */
@media (max-width: 1024px) {
  .oracle-bottom-cards-row {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 560px) {
  .oracle-bottom-cards-row {
    grid-template-columns: 1fr;
  }
  .oracle-bottom-card {
    min-height: auto;
  }
}
</style>
