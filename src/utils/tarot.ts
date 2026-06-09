import { tarotCards } from '../data/tarotCards'

export function getShanghaiDateKey(date = new Date()): string {
  const formatter = new Intl.DateTimeFormat('en-CA', {
    timeZone: 'Asia/Shanghai',
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
  })
  return formatter.format(date)
}

export function createWeatherFingerprint(input: {
  temperature: number | null
  humidity: number | null
  pressure: number | null
  wind_speed: number | null
  condition: string
}): string {
  return [
    input.temperature,
    input.humidity,
    input.pressure,
    input.wind_speed,
    input.condition,
  ].join('|')
}

function hashString(value: string): number {
  let hash = 2166136261
  for (let i = 0; i < value.length; i += 1) {
    hash ^= value.charCodeAt(i)
    hash = Math.imul(hash, 16777619)
  }
  return hash >>> 0
}

export function pickTarotCard(city: string, dateKey: string, weatherFingerprint: string) {
  const index = hashString(`${city}|${dateKey}|${weatherFingerprint}`) % tarotCards.length
  return tarotCards[index]
}
