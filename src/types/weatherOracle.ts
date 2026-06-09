export interface WeatherOracleRequest {
  city: string
  model_id?: string
  tarot_card_id?: string
}

export interface WeatherOracleWeather {
  temperature: number | null
  humidity: number | null
  pressure: number | null
  wind_speed: number | null
  wind_direction: string
  condition: string
  observed_at: string
}

export interface WeatherOracleTarot {
  id: string
  name_en: string
  name_zh: string
  image: string
  keywords: string[]
}

export interface WeatherOracleFortune {
  title: string
  summary: string
  lucky_color: string
  lucky_number: number
  good_for: string
  avoid: string
}

export interface WeatherOracleMoodGuide {
  title: string
  analysis: string
  suggestions: string[]
}

export interface WeatherOracleDailyAdvice {
  travel: string
  clothing: string
}

export interface WeatherOracleMapping {
  metric: 'temperature' | 'humidity' | 'pressure' | 'wind_speed'
  label: string
  value: string
  reading: string
  score: number
}

export interface WeatherOracleReading {
  city: string
  date: string
  timezone: 'Asia/Shanghai'
  updated_at: string
  weather: WeatherOracleWeather
  tarot: WeatherOracleTarot
  fortune: WeatherOracleFortune
  mood_guide: WeatherOracleMoodGuide
  daily_advice?: WeatherOracleDailyAdvice
  weather_mappings: WeatherOracleMapping[]
}
