import unittest

from app.services.weather_tool import WeatherToolService


class WeatherToolTests(unittest.TestCase):
    def test_format_search_results_parses_tavily_dict_response(self):
        result = {
            "query": "北京天气",
            "results": [
                {
                    "title": "北京天气预报",
                    "url": "https://example.com/weather",
                    "content": "北京今日晴，北风二级。",
                    "published_date": "2026-05-30",
                }
            ],
        }

        formatted = WeatherToolService.format_search_results(result)

        self.assertIn("【天气搜索结果】", formatted)
        self.assertIn("1. 北京天气预报（2026-05-30）", formatted)
        self.assertIn("来源：https://example.com/weather", formatted)
        self.assertIn("摘要：北京今日晴，北风二级。", formatted)
        self.assertNotIn("'results':", formatted)


if __name__ == "__main__":
    unittest.main()
