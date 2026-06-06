export interface TarotCard {
  id: string
  nameEn: string
  nameZh: string
  arcana: 'major' | 'minor'
  suit: 'major' | 'wands' | 'cups' | 'swords' | 'pentacles'
  rank: string
  image: string
  keywords: string[]
}

const image = (id: string) => `/tarot/cards/${id}.png`

export const tarotAssetsReady = true

export const tarotCards: TarotCard[] = [
  { id: 'major-00-fool', nameEn: 'The Fool', nameZh: '愚者', arcana: 'major', suit: 'major', rank: '0', image: image('major-00-fool'), keywords: ['开始', '自由', '冒险'] },
  { id: 'major-01-magician', nameEn: 'The Magician', nameZh: '魔术师', arcana: 'major', suit: 'major', rank: '1', image: image('major-01-magician'), keywords: ['行动', '资源', '表达'] },
  { id: 'major-02-high-priestess', nameEn: 'The High Priestess', nameZh: '女祭司', arcana: 'major', suit: 'major', rank: '2', image: image('major-02-high-priestess'), keywords: ['直觉', '沉静', '观察'] },
  { id: 'major-03-empress', nameEn: 'The Empress', nameZh: '皇后', arcana: 'major', suit: 'major', rank: '3', image: image('major-03-empress'), keywords: ['滋养', '创造', '丰盛'] },
  { id: 'major-04-emperor', nameEn: 'The Emperor', nameZh: '皇帝', arcana: 'major', suit: 'major', rank: '4', image: image('major-04-emperor'), keywords: ['秩序', '边界', '掌控'] },
  { id: 'major-05-hierophant', nameEn: 'The Hierophant', nameZh: '教皇', arcana: 'major', suit: 'major', rank: '5', image: image('major-05-hierophant'), keywords: ['传统', '学习', '建议'] },
  { id: 'major-06-lovers', nameEn: 'The Lovers', nameZh: '恋人', arcana: 'major', suit: 'major', rank: '6', image: image('major-06-lovers'), keywords: ['选择', '关系', '协调'] },
  { id: 'major-07-chariot', nameEn: 'The Chariot', nameZh: '战车', arcana: 'major', suit: 'major', rank: '7', image: image('major-07-chariot'), keywords: ['推进', '方向', '意志'] },
  { id: 'major-08-strength', nameEn: 'Strength', nameZh: '力量', arcana: 'major', suit: 'major', rank: '8', image: image('major-08-strength'), keywords: ['耐心', '柔韧', '内力'] },
  { id: 'major-09-hermit', nameEn: 'The Hermit', nameZh: '隐者', arcana: 'major', suit: 'major', rank: '9', image: image('major-09-hermit'), keywords: ['独处', '思考', '寻找'] },
  { id: 'major-10-wheel-of-fortune', nameEn: 'Wheel of Fortune', nameZh: '命运之轮', arcana: 'major', suit: 'major', rank: '10', image: image('major-10-wheel-of-fortune'), keywords: ['变化', '周期', '转机'] },
  { id: 'major-11-justice', nameEn: 'Justice', nameZh: '正义', arcana: 'major', suit: 'major', rank: '11', image: image('major-11-justice'), keywords: ['判断', '平衡', '原则'] },
  { id: 'major-12-hanged-man', nameEn: 'The Hanged Man', nameZh: '倒吊人', arcana: 'major', suit: 'major', rank: '12', image: image('major-12-hanged-man'), keywords: ['暂停', '换位', '等待'] },
  { id: 'major-13-death', nameEn: 'Death', nameZh: '死神', arcana: 'major', suit: 'major', rank: '13', image: image('major-13-death'), keywords: ['结束', '转化', '告别'] },
  { id: 'major-14-temperance', nameEn: 'Temperance', nameZh: '节制', arcana: 'major', suit: 'major', rank: '14', image: image('major-14-temperance'), keywords: ['调和', '修复', '节奏'] },
  { id: 'major-15-devil', nameEn: 'The Devil', nameZh: '恶魔', arcana: 'major', suit: 'major', rank: '15', image: image('major-15-devil'), keywords: ['欲望', '束缚', '清醒'] },
  { id: 'major-16-tower', nameEn: 'The Tower', nameZh: '高塔', arcana: 'major', suit: 'major', rank: '16', image: image('major-16-tower'), keywords: ['打破', '突变', '释放'] },
  { id: 'major-17-star', nameEn: 'The Star', nameZh: '星星', arcana: 'major', suit: 'major', rank: '17', image: image('major-17-star'), keywords: ['希望', '治愈', '指引'] },
  { id: 'major-18-moon', nameEn: 'The Moon', nameZh: '月亮', arcana: 'major', suit: 'major', rank: '18', image: image('major-18-moon'), keywords: ['潜意识', '梦境', '不安'] },
  { id: 'major-19-sun', nameEn: 'The Sun', nameZh: '太阳', arcana: 'major', suit: 'major', rank: '19', image: image('major-19-sun'), keywords: ['明朗', '活力', '坦诚'] },
  { id: 'major-20-judgement', nameEn: 'Judgement', nameZh: '审判', arcana: 'major', suit: 'major', rank: '20', image: image('major-20-judgement'), keywords: ['回应', '复盘', '觉察'] },
  { id: 'major-21-world', nameEn: 'The World', nameZh: '世界', arcana: 'major', suit: 'major', rank: '21', image: image('major-21-world'), keywords: ['完成', '整合', '抵达'] },
]

const minorNames: Record<string, string> = {
  ace: 'Ace',
  two: 'Two',
  three: 'Three',
  four: 'Four',
  five: 'Five',
  six: 'Six',
  seven: 'Seven',
  eight: 'Eight',
  nine: 'Nine',
  ten: 'Ten',
  king: 'King',
  knight: 'Knight',
  page: 'Page',
  queen: 'Queen',
}

const minorZh: Record<string, string> = {
  wands: '权杖',
  cups: '圣杯',
  swords: '宝剑',
  pentacles: '星币',
  ace: '一',
  two: '二',
  three: '三',
  four: '四',
  five: '五',
  six: '六',
  seven: '七',
  eight: '八',
  nine: '九',
  ten: '十',
  king: '国王',
  knight: '骑士',
  page: '侍从',
  queen: '王后',
}

const minorRanks = [
  'ace',
  'two',
  'three',
  'four',
  'five',
  'six',
  'seven',
  'eight',
  'nine',
  'ten',
  'king',
  'knight',
  'page',
  'queen',
] as const

for (const suit of ['wands', 'cups', 'swords', 'pentacles'] as const) {
  minorRanks.forEach((rank, index) => {
    const cardNo = String(index + 1).padStart(2, '0')
    const id = `${suit}-${cardNo}-${rank}`
    tarotCards.push({
      id,
      nameEn: `${minorNames[rank]} of ${suit[0].toUpperCase()}${suit.slice(1)}`,
      nameZh: `${minorZh[suit]}${minorZh[rank]}`,
      arcana: 'minor',
      suit,
      rank,
      image: image(id),
      keywords: ['行动', '情绪', '提醒'],
    })
  })
}

export function getTarotCardById(id: string): TarotCard | undefined {
  return tarotCards.find(card => card.id === id)
}
