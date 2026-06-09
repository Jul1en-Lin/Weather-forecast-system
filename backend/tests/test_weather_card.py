import json
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app
from app.routers.assistant import (
    TAROT_CARD_META,
    build_weather_fingerprint,
    build_weather_daily_advice,
    build_weather_oracle_prompt,
    clean_json_object_text,
    select_tarot_card_id,
    select_preferred_weather_oracle_model_id,
)


class WeatherCardHelperTests(unittest.TestCase):
    def test_clean_json_object_text_removes_markdown_fence(self):
        raw = '```json\n{"title": "星辰希望"}\n```'

        self.assertEqual(clean_json_object_text(raw), '{"title": "星辰希望"}')

    def test_select_tarot_card_id_is_deterministic(self):
        first = select_tarot_card_id("user:1", "2026-06-06")
        second = select_tarot_card_id("user:1", "2026-06-06")

        self.assertEqual(first, second)
        self.assertTrue(first)

    def test_select_tarot_card_id_ignores_city_weather_when_user_and_date_match(self):
        first = select_tarot_card_id("user:1", "2026-06-06", "上海|22|78|1012|12|多云")
        second = select_tarot_card_id("user:1", "2026-06-06", "武汉|29|70|1004|9|阴")

        self.assertEqual(first, second)

    def test_build_weather_fingerprint_uses_core_metrics(self):
        weather = {
            "temperature": 22,
            "humidity": 78,
            "pressure": 1012,
            "wind_speed": 12,
            "condition": "多云",
        }

        self.assertEqual(build_weather_fingerprint(weather), "22|78|1012|12|多云")

    def test_build_weather_daily_advice_uses_weather_conditions(self):
        advice = build_weather_daily_advice({
            "temperature": 31,
            "humidity": 86,
            "wind_speed": 8,
            "condition": "多云",
        })

        self.assertIn("防晒", advice["travel"])
        self.assertIn("透气", advice["clothing"])

    def test_select_preferred_weather_oracle_model_id_prefers_available_models(self):
        models = [
            SimpleNamespace(id="kimi-k2.5"),
            SimpleNamespace(id="MiniMax-M2.5"),
            SimpleNamespace(id="mimo-v2.5"),
        ]

        self.assertEqual(select_preferred_weather_oracle_model_id(models), "mimo-v2.5")
        self.assertEqual(
            select_preferred_weather_oracle_model_id(models[:2]),
            "MiniMax-M2.5",
        )
        self.assertEqual(
            select_preferred_weather_oracle_model_id([SimpleNamespace(id="kimi-k2.5")]),
            "kimi-k2.5",
        )

    def test_tarot_card_meta_contains_complete_deck_meanings(self):
        self.assertEqual(len(TAROT_CARD_META), 78)

        lovers = TAROT_CARD_META["major-06-lovers"]
        self.assertEqual(lovers["name_en"], "The Lovers")
        self.assertEqual(lovers["name_zh"], "恋人")
        self.assertEqual(lovers["arcana"], "major")
        self.assertEqual(lovers["rank"], "6")
        self.assertEqual(lovers["keywords"], ["选择", "关系", "协调"])
        self.assertIn("关系", lovers["core_meaning"])
        self.assertIn("选择", lovers["weather_oracle_hint"])

        ace_of_cups = TAROT_CARD_META["cups-01-ace"]
        self.assertEqual(ace_of_cups["name_en"], "Ace of Cups")
        self.assertEqual(ace_of_cups["name_zh"], "圣杯一")
        self.assertEqual(ace_of_cups["suit"], "cups")
        self.assertIn("情绪", ace_of_cups["core_meaning"])
        self.assertIn("感受", ace_of_cups["weather_oracle_hint"])

    def test_weather_oracle_prompt_stays_compact_with_card_meaning(self):
        weather = {
            "city": "杭州",
            "temperature": 23,
            "humidity": 78,
            "pressure": 1004,
            "wind_speed": 17,
            "wind_direction": "东风",
            "condition": "阴",
            "observed_at": "2026-06-08T00:28+08:00",
        }

        prompt = build_weather_oracle_prompt(
            weather=weather,
            date_key="2026-06-08",
            tarot=TAROT_CARD_META["major-06-lovers"],
        )

        self.assertLess(len(prompt), 800)
        self.assertIn("恋人", prompt)
        self.assertIn("The Lovers", prompt)
        self.assertIn("core_meaning", prompt)
        self.assertIn("weather_oracle_hint", prompt)
        self.assertIn("fortune={title,summary,lucky_color,lucky_number,good_for,avoid}", prompt)


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
            prompt = ""

            def invoke(self, prompt):
                self.prompt = prompt
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
                    "daily_advice": {
                        "travel": "云量偏多，通勤正常，长时间户外记得看路况。",
                        "clothing": "体感清爽，薄外套加长袖更舒服。",
                    },
                    "weather_mappings": [
                        {"metric": "temperature", "label": "温度", "value": "22°C", "reading": "平和舒适", "score": 70},
                        {"metric": "humidity", "label": "湿度", "value": "78%", "reading": "内收敏感", "score": 78},
                        {"metric": "pressure", "label": "气压", "value": "1012 hPa", "reading": "掌控感提升", "score": 65},
                        {"metric": "wind_speed", "label": "风速", "value": "12 km/h", "reading": "思绪流动", "score": 60},
                    ],
                }, ensure_ascii=False))

        fake_llm = FakeLLM()
        get_llm.return_value = fake_llm

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
        self.assertEqual(data["daily_advice"]["travel"], "云量偏多，通勤正常，长时间户外记得看路况。")
        self.assertEqual(data["daily_advice"]["clothing"], "体感清爽，薄外套加长袖更舒服。")
        self.assertNotIn("daily_advice={travel,clothing}", fake_llm.prompt)
        self.assertNotIn("weather_mappings=[", fake_llm.prompt)
        self.assertIn("The Star", fake_llm.prompt)
        self.assertIn("星星", fake_llm.prompt)
        self.assertIn("希望", fake_llm.prompt)
        self.assertIn("core_meaning", fake_llm.prompt)
        self.assertIn("weather_oracle_hint", fake_llm.prompt)
        self.assertEqual(get_llm.call_args.kwargs["timeout"], 20.0)
        self.assertEqual(get_llm.call_args.kwargs["max_retries"], 0)
        self.assertFalse(get_llm.call_args.kwargs["use_env_proxy"])

    @patch("app.routers.assistant.get_llm")
    @patch("app.services.weather_tool.WeatherToolService.fetch_realtime_weather")
    def test_weather_card_keeps_same_daily_tarot_when_city_changes(self, fetch_weather, get_llm):
        weather_by_city = {
            "上海": {
                "city": "上海",
                "temperature": 22,
                "humidity": 78,
                "pressure": 1012,
                "wind_speed": 12,
                "wind_direction": "东北风",
                "condition": "多云",
                "observed_at": "2026-06-06T09:00+08:00",
            },
            "武汉": {
                "city": "武汉",
                "temperature": 29,
                "humidity": 70,
                "pressure": 1004,
                "wind_speed": 9,
                "wind_direction": "东风",
                "condition": "阴",
                "observed_at": "2026-06-06T09:00+08:00",
            },
        }
        fetch_weather.side_effect = lambda city: weather_by_city[city]

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
                        "analysis": "湿度偏高，给自己一点空隙。",
                        "suggestions": ["留二十分钟独处"],
                    },
                    "weather_mappings": [
                        {"metric": "temperature", "label": "温度", "value": "22°C", "reading": "平和舒适", "score": 70},
                        {"metric": "humidity", "label": "湿度", "value": "78%", "reading": "内收敏感", "score": 78},
                        {"metric": "pressure", "label": "气压", "value": "1012 hPa", "reading": "掌控感提升", "score": 65},
                        {"metric": "wind_speed", "label": "风速", "value": "12 km/h", "reading": "思绪流动", "score": 60},
                    ],
                }, ensure_ascii=False))

        get_llm.return_value = FakeLLM()

        first = self.client.post(
            "/api/v1/assistant/weather-card",
            json={"city": "上海", "model_id": "kimi-k2.5"},
        )
        second = self.client.post(
            "/api/v1/assistant/weather-card",
            json={"city": "武汉", "model_id": "kimi-k2.5"},
        )

        self.assertEqual(first.status_code, 200)
        self.assertEqual(second.status_code, 200)
        self.assertEqual(first.json()["tarot"]["id"], second.json()["tarot"]["id"])
        self.assertEqual(second.json()["city"], "武汉")

    @patch("app.services.weather_tool.WeatherToolService.fetch_realtime_weather")
    def test_weather_card_rejects_unknown_city_before_llm(self, fetch_weather):
        fetch_weather.return_value = None

        response = self.client.post(
            "/api/v1/assistant/weather-card",
            json={"city": "不存在城市"},
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("未能获取", response.json()["detail"])

    @patch("app.routers.assistant.get_llm")
    @patch("app.services.weather_tool.WeatherToolService.fetch_realtime_weather")
    def test_weather_card_falls_back_when_llm_payload_structure_is_invalid(self, fetch_weather, get_llm):
        fetch_weather.return_value = {
            "city": "上海",
            "temperature": None,
            "humidity": 78,
            "pressure": 1012,
            "wind_speed": None,
            "wind_direction": "东北风",
            "condition": "多云",
            "observed_at": "2026-06-06T09:00+08:00",
        }

        class FakeLLM:
            def invoke(self, prompt):
                return SimpleNamespace(content='{"fortune": {}}')

        get_llm.return_value = FakeLLM()

        response = self.client.post(
            "/api/v1/assistant/weather-card",
            json={"city": "上海", "model_id": "kimi-k2.5", "tarot_card_id": "major-17-star"},
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["fortune"]["title"], "云隙微光")
        self.assertEqual(data["weather_mappings"][0]["value"], "未知")
        self.assertEqual(data["weather_mappings"][3]["value"], "未知")

    @patch("app.routers.assistant.get_llm")
    @patch("app.services.weather_tool.WeatherToolService.fetch_realtime_weather")
    def test_weather_card_coerces_common_llm_summary_shape(self, fetch_weather, get_llm):
        fetch_weather.return_value = {
            "city": "江门",
            "temperature": 26,
            "humidity": 92,
            "pressure": 1003,
            "wind_speed": 12,
            "wind_direction": "西南风",
            "condition": "阴",
            "observed_at": "2026-06-06T23:40+08:00",
        }

        class FakeLLM:
            def invoke(self, prompt):
                return SimpleNamespace(content=json.dumps({
                    "fortune": "今天的核心指引是守住边界，先确认安全感和物质基础。",
                    "mood_guide": "阴天的温暖和高湿会让心情变黏，适合把沟通放慢一点。",
                    "weather_mappings": {
                        "temperature": "26°C：温度偏暖，适合慢慢推进。",
                        "humidity": "92%：湿度高，情绪容易滞留。",
                        "pressure": "1003 hPa：气压偏低，减少硬碰硬。",
                        "wind_speed": "12 km/h：风在推动思路流动。",
                    },
                }, ensure_ascii=False))

        get_llm.return_value = FakeLLM()

        response = self.client.post(
            "/api/v1/assistant/weather-card",
            json={"city": "江门", "model_id": "kimi-k2.5", "tarot_card_id": "pentacles-04-four"},
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["city"], "江门")
        self.assertEqual(data["fortune"]["summary"], "今天的核心指引是守住边界，先确认安全感和物质基础。")
        self.assertEqual(data["mood_guide"]["analysis"], "阴天的温暖和高湿会让心情变黏，适合把沟通放慢一点。")
        self.assertEqual(data["weather_mappings"][0]["metric"], "temperature")
        self.assertEqual(data["weather_mappings"][0]["value"], "26°C")
        self.assertIn("温度偏暖", data["weather_mappings"][0]["reading"])

    @patch("app.routers.assistant.get_llm")
    @patch("app.services.weather_tool.WeatherToolService.fetch_realtime_weather")
    def test_weather_card_falls_back_when_llm_invoke_raises(self, fetch_weather, get_llm):
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
                raise RuntimeError("llm boom")

        get_llm.return_value = FakeLLM()

        response = self.client.post(
            "/api/v1/assistant/weather-card",
            json={"city": "上海", "model_id": "kimi-k2.5", "tarot_card_id": "major-17-star"},
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["fortune"]["title"], "云隙微光")
        self.assertEqual(data["weather_mappings"][0]["value"], "22°C")
        self.assertIn("正常出门", data["daily_advice"]["travel"])
        self.assertIn("薄外套", data["daily_advice"]["clothing"])

    @patch("app.routers.assistant.get_llm")
    @patch("app.services.weather_tool.WeatherToolService.fetch_realtime_weather")
    def test_weather_tip_generation_and_fallback(self, fetch_weather, get_llm):
        fetch_weather.return_value = {
            "city": "北京",
            "temperature": 25,
            "humidity": 50,
            "pressure": 1010,
            "wind_speed": 10,
            "wind_direction": "南风",
            "condition": "晴",
            "observed_at": "2026-06-06T09:00+08:00",
        }

        # First, test fallback behavior when LLM fails
        class FakeLLMFail:
            def invoke(self, prompt):
                raise RuntimeError("llm fail")

        get_llm.return_value = FakeLLMFail()

        response = self.client.post(
            "/api/v1/assistant/weather-card",
            json={"city": "北京", "model_id": "kimi-k2.5"},
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("weather_tip", data)
        self.assertIsNotNone(data["weather_tip"])
        self.assertIn("title", data["weather_tip"])
        self.assertIn("advice", data["weather_tip"])

        # Second, test LLM prompt updates and parsed tip when LLM succeeds
        class FakeLLMSuccess:
            def invoke(self, prompt):
                self.prompt = prompt
                return SimpleNamespace(content=json.dumps({
                    "fortune": {
                        "title": "星辰希望",
                        "summary": "今天适合把节奏放慢。",
                        "lucky_color": "雾紫色",
                        "lucky_number": 7,
                        "good_for": "整理思路",
                        "avoid": "冲动争执",
                    },
                    "mood_guide": {
                        "title": "内收敏感",
                        "analysis": "湿度偏高，给自己一点空隙。",
                        "suggestions": ["留二十分钟独处"],
                    },
                    "weather_mappings": [
                        {"metric": "temperature", "label": "温度", "value": "25°C", "reading": "平和舒适", "score": 70},
                    ],
                    "weather_tip": {
                        "title": "测试贴士",
                        "advice": "测试气象建议内容"
                    }
                }, ensure_ascii=False))

        fake_llm = FakeLLMSuccess()
        get_llm.return_value = fake_llm

        response = self.client.post(
            "/api/v1/assistant/weather-card",
            json={"city": "北京", "model_id": "kimi-k2.5"},
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("weather_tip", data)
        self.assertEqual(data["weather_tip"]["title"], "测试贴士")
        self.assertEqual(data["weather_tip"]["advice"], "测试气象建议内容")



if __name__ == "__main__":
    unittest.main()
