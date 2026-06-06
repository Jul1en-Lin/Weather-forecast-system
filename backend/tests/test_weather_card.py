import unittest

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


if __name__ == "__main__":
    unittest.main()
