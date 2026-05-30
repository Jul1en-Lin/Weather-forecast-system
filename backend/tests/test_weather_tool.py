import unittest
from unittest.mock import patch

from app.services.weather_tool import WeatherToolService, _get_qweather_config, _qweather_geo_hosts


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

    def test_format_qweather_forecast_keeps_multiple_days(self):
        data = {
            "code": "200",
            "daily": [
                {
                    "fxDate": "2026-05-30",
                    "textDay": "中雨",
                    "textNight": "多云",
                    "tempMin": "26",
                    "tempMax": "33",
                    "windDirDay": "南风",
                    "windScaleDay": "3-4",
                    "humidity": "80",
                },
                {
                    "fxDate": "2026-05-31",
                    "textDay": "多云",
                    "textNight": "阵雨",
                    "tempMin": "25",
                    "tempMax": "32",
                    "windDirDay": "东南风",
                    "windScaleDay": "1-3",
                    "humidity": "76",
                },
            ],
        }

        formatted = WeatherToolService.format_qweather_forecast("江门", data)

        self.assertIn("【结构化天气预报 - 江门】", formatted)
        self.assertIn("2026-05-30 | 中雨转多云 | 26℃~33℃ | 南风3-4级 | 湿度80%", formatted)
        self.assertIn("2026-05-31 | 多云转阵雨 | 25℃~32℃ | 东南风1-3级 | 湿度76%", formatted)

    def test_qweather_geo_hosts_falls_back_to_public_geo_api(self):
        self.assertEqual(
            _qweather_geo_hosts("devapi.qweather.com"),
            ["devapi.qweather.com", "geoapi.qweather.com"],
        )
        self.assertEqual(_qweather_geo_hosts("geoapi.qweather.com"), ["geoapi.qweather.com"])

    @patch("app.services.weather_tool.settings")
    @patch("app.services.weather_tool._get_tool_config")
    def test_qweather_config_keeps_key_and_host_from_same_source(self, get_tool_config, settings):
        get_tool_config.return_value = ("", "devapi.qweather.com")
        settings.qweather_api_key = "env-key"
        settings.qweather_api_host = "env-host.example.com"

        self.assertEqual(_get_qweather_config(), ("env-key", "env-host.example.com"))


if __name__ == "__main__":
    unittest.main()
