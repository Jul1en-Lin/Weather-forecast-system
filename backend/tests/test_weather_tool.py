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


class StructuredWeatherNowTests(unittest.TestCase):
    @patch("app.services.weather_tool.httpx.Client")
    @patch("app.services.weather_tool._get_qweather_config")
    def test_fetch_realtime_weather_parses_qweather_response(self, get_qweather_config, client_cls):
        get_qweather_config.return_value = ("demo-key", "devapi.qweather.com")

        class FakeResponse:
            def __init__(self, payload):
                self._payload = payload

            def json(self):
                return self._payload

        class FakeClient:
            def __init__(self, *args, **kwargs):
                self.requests = []

            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc, tb):
                return False

            def get(self, url, params=None):
                self.requests.append((url, params))
                if url.endswith("/geo/v2/city/lookup"):
                    return FakeResponse(
                        {
                            "code": "200",
                            "location": [
                                {
                                    "id": "101020100",
                                    "name": "上海",
                                }
                            ],
                        }
                    )
                if url.endswith("/v7/weather/now"):
                    return FakeResponse(
                        {
                            "code": "200",
                            "now": {
                                "obsTime": "2026-06-06T09:00+08:00",
                                "temp": "22",
                                "humidity": "78",
                                "pressure": "1012",
                                "windSpeed": "12",
                                "windDir": "东北风",
                                "text": "多云",
                            },
                        }
                    )
                raise AssertionError(f"Unexpected URL: {url}")

        fake_client = FakeClient()
        client_cls.return_value = fake_client

        result = WeatherToolService.fetch_realtime_weather("上海")

        self.assertEqual(
            result,
            {
                "city": "上海",
                "temperature": 22,
                "humidity": 78,
                "pressure": 1012,
                "wind_speed": 12,
                "wind_direction": "东北风",
                "condition": "多云",
                "observed_at": "2026-06-06T09:00+08:00",
            },
        )

    @patch("app.services.weather_tool.httpx.Client")
    @patch("app.services.weather_tool._get_qweather_config")
    def test_fetch_realtime_weather_returns_none_without_api_key(self, get_qweather_config, client_cls):
        get_qweather_config.return_value = ("", "devapi.qweather.com")

        result = WeatherToolService.fetch_realtime_weather("上海")

        self.assertIsNone(result)
        client_cls.assert_not_called()

    @patch("app.services.weather_tool.httpx.Client")
    @patch("app.services.weather_tool._get_qweather_config")
    def test_fetch_realtime_weather_keeps_trying_other_geo_hosts(self, get_qweather_config, client_cls):
        get_qweather_config.return_value = ("demo-key", "devapi.qweather.com")

        class FakeResponse:
            def __init__(self, payload):
                self._payload = payload

            def json(self):
                return self._payload

        class FakeClient:
            def __init__(self, *args, **kwargs):
                self.requests = []

            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc, tb):
                return False

            def get(self, url, params=None):
                self.requests.append((url, params))
                if url.startswith("https://devapi.qweather.com/geo/v2/city/lookup"):
                    raise RuntimeError("dev geo host down")
                if url.endswith("/geo/v2/city/lookup"):
                    return FakeResponse(
                        {
                            "code": "200",
                            "location": [
                                {
                                    "id": "101020100",
                                    "name": "上海",
                                }
                            ],
                        }
                    )
                if url.endswith("/v7/weather/now"):
                    return FakeResponse(
                        {
                            "code": "200",
                            "now": {
                                "obsTime": None,
                                "temp": "22",
                                "humidity": "78",
                                "pressure": "1012",
                                "windSpeed": "12",
                                "windDir": None,
                                "text": None,
                            },
                        }
                    )
                raise AssertionError(f"Unexpected URL: {url}")

        client_cls.return_value = FakeClient()

        result = WeatherToolService.fetch_realtime_weather("上海")

        self.assertEqual(
            result,
            {
                "city": "上海",
                "temperature": 22,
                "humidity": 78,
                "pressure": 1012,
                "wind_speed": 12,
                "wind_direction": "",
                "condition": "",
                "observed_at": "",
            },
        )


if __name__ == "__main__":
    unittest.main()
