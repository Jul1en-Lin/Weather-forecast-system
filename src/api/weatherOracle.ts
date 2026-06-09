import type { WeatherOracleReading, WeatherOracleRequest } from '../types/weatherOracle'

export async function generateWeatherOracleReading(
  payload: WeatherOracleRequest,
): Promise<WeatherOracleReading> {
  const res = await fetch('/api/v1/assistant/weather-card', {
    method: 'POST',
    credentials: 'include',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })

  if (!res.ok) {
    const data = await res.json().catch(() => ({ detail: '请求失败' }))
    throw new Error(data.detail || '请求失败')
  }

  return res.json()
}
