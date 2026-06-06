import json
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app
from app.routers.assistant import (
    build_weather_fingerprint,
    clean_json_object_text,
    select_tarot_card_id,
)


class WeatherCardHelperTests(unittest.TestCase):
    def test_clean_json_object_text_removes_markdown_fence(self):
        raw = '```json\n{"title": "星辰希望"}\n```'

        self.assertEqual(clean_json_object_text(raw), '{"title": "星辰希望"}')

    def test_select_tarot_card_id_is_deterministic(self):
        first = select_tarot_card_id("上海", "2026-06-06", "22|78|1012|12|多云")
        second = select_tarot_card_id("上海", "2026-06-06", "22|78|1012|12|多云")

        self.assertEqual(first, second)
        self.assertTrue(first)

    def test_build_weather_fingerprint_uses_core_metrics(self):
        weather = {
            "temperature": 22,
            "humidity": 78,
            "pressure": 1012,
            "wind_speed": 12,
            "condition": "多云",
        }

        self.assertEqual(build_weather_fingerprint(weather), "22|78|1012|12|多云")


class WeatherCardEndpointTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        response = self.client.post(
            "/api/v1/auth/login",
            json={"username": "admin", "password": "admin123"},
        )
        self.assertEqual(response.status_code, 200)

    @patch("app.routers.assistant.get_llm")
    @patch("app.services.weather_tool.WeatherToolService.fetch_realtime_weather")
    def test_weather_card_returns_oracle_payload(self, fetch_weather, get_llm):
        fetch_weather.return_value = {
            "city": "上海",
            "temperature": 22,
            "humidity": 78,
            "pressure": 1012,
            "wind_speed": 12,
            "wind_direction": "东北风",
            "condition": "多云",
            "observed_at": "2026-06-06T09:00+08:00",
        }

        class FakeLLM:
            def invoke(self, prompt):
                return SimpleNamespace(content=json.dumps({
                    "fortune": {
                        "title": "星辰希望",
                        "summary": "今天适合把节奏放慢，先处理眼前的小事。",
                        "lucky_color": "雾紫色",
                        "lucky_number": 7,
                        "good_for": "整理思路",
                        "avoid": "冲动争执",
                    },
                    "mood_guide": {
                        "title": "内收敏感",
                        "analysis": "湿度偏高，情绪容易把小事放大。给自己一点空隙，别急着回应。",
                        "suggestions": ["留二十分钟独处", "喝点热饮", "把决定放到明天"],
                    },
                    "weather_mappings": [
                        {"metric": "temperature", "label": "温度", "value": "22°C", "reading": "平和舒适", "score": 70},
                        {"metric": "humidity", "label": "湿度", "value": "78%", "reading": "内收敏感", "score": 78},
                        {"metric": "pressure", "label": "气压", "value": "1012 hPa", "reading": "掌控感提升", "score": 65},
                        {"metric": "wind_speed", "label": "风速", "value": "12 km/h", "reading": "思绪流动", "score": 60},
                    ],
                }, ensure_ascii=False))

        get_llm.return_value = FakeLLM()

        response = self.client.post(
            "/api/v1/assistant/weather-card",
            json={"city": "上海", "model_id": "kimi-k2.5", "tarot_card_id": "major-17-star"},
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["city"], "上海")
        self.assertEqual(data["timezone"], "Asia/Shanghai")
        self.assertEqual(data["weather"]["temperature"], 22)
        self.assertEqual(data["tarot"]["id"], "major-17-star")
        self.assertEqual(data["fortune"]["title"], "星辰希望")
        self.assertEqual(len(data["weather_mappings"]), 4)

    @patch("app.services.weather_tool.WeatherToolService.fetch_realtime_weather")
    def test_weather_card_rejects_unknown_city_before_llm(self, fetch_weather):
        fetch_weather.return_value = None

        response = self.client.post(
            "/api/v1/assistant/weather-card",
            json={"city": "不存在城市"},
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("未能获取", response.json()["detail"])


if __name__ == "__main__":
    unittest.main()
