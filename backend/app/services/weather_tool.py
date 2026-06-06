import logging
import re
from typing import Optional
import httpx
from langchain_tavily import TavilySearch
from langchain_core.tools import StructuredTool
from app.config import settings
from app.database import SessionLocal
from app.models.alert import Alert

logger = logging.getLogger(__name__)


def _query_alerts(alert_type: str = "", level: str = "") -> str:
    """Query meteorological alert definitions from database."""
    db = SessionLocal()
    try:
        q = db.query(Alert)
        if alert_type:
            q = q.filter(Alert.alert_type.contains(alert_type))
        if level:
            q = q.filter(Alert.level == level)
        alerts = q.limit(10).all()
        if not alerts:
            return "未查询到相关预警信号定义。"
        parts = []
        for a in alerts:
            parts.append(f"{a.alert_type}{a.level}预警: 标准={a.criteria}; 防御={a.response_guide or '无'}")
        return "\n".join(parts)
    finally:
        db.close()


from app.models.tool_config import ToolConfig


def _get_tool_config(tool_id: str) -> tuple[str, str]:
    db = SessionLocal()
    try:
        tool_cfg = db.query(ToolConfig).filter(ToolConfig.id == tool_id).first()
        if tool_cfg:
            return tool_cfg.api_key or "", tool_cfg.api_host or ""
    except Exception:
        logger.exception("Failed to load tool config: %s", tool_id)
    finally:
        db.close()
    return "", ""


def _normalize_forecast_days(days: int) -> int:
    try:
        parsed = int(days)
    except (TypeError, ValueError):
        parsed = 1
    return max(1, min(parsed, 7))


def _infer_forecast_days(text: str) -> int:
    if not text:
        return 1
    if "七天" in text or "7天" in text or "一周" in text:
        return 7
    if "三天" in text or "3天" in text:
        return 3
    match = re.search(r"未来\s*(\d+)\s*天", text)
    if match:
        return _normalize_forecast_days(int(match.group(1)))
    return 1


def _infer_location_from_query(query: str) -> str:
    if not query:
        return ""
    match = re.search(r"(?:未来(?:\d+|[一二三四五六七])天的?|今天|明天)?([\u4e00-\u9fa5]{2,8})(?:天气|预报)", query)
    if match:
        location = match.group(1)
        for prefix in ("的", "查询", "看看"):
            location = location.removeprefix(prefix)
        return location
    return ""


def _get_qweather_config() -> tuple[str, str]:
    api_key, api_host = _get_tool_config("alert_query")
    if api_key:
        return api_key, api_host or settings.qweather_api_host or "devapi.qweather.com"
    return settings.qweather_api_key, settings.qweather_api_host or api_host or "devapi.qweather.com"


def _qweather_geo_hosts(api_host: str) -> list[str]:
    hosts = []
    if api_host:
        hosts.append(api_host)
    if "geoapi.qweather.com" not in hosts:
        hosts.append("geoapi.qweather.com")
    return hosts


def _to_int_or_none(value):
    try:
        if value is None or value == "":
            return None
        return int(float(value))
    except (TypeError, ValueError):
        return None


def _get_tavily_key() -> str:
    api_key, _ = _get_tool_config("weather_query")
    return api_key or settings.tavily_api_key

def _fetch_realtime_alerts(location: str = "") -> str:
    """Fetch real-time weather alerts via QWeather API, fallback to DB definitions."""
    qweather_key, qweather_host = _get_qweather_config()

    if not qweather_key:
        logger.info("QWeather API key not configured, falling back to DB alert definitions")
        db_result = _query_alerts(alert_type=location)
        if "未查询到" in db_result:
            return "暂未查询到实时气象预警信息。（实时预警服务未配置，仅提供预警信号标准定义查询）"
        return f"【预警信号标准定义】\n{db_result}\n\n（以上为预警信号标准定义，非实时预警）"

    try:
        # QWeather uses location ID or lat/lon; here we try a geo lookup first
        # For simplicity, use the city-warning endpoint with location keyword
        host = qweather_host
        geo_url = f"https://{host}/geo/v2/city/lookup"
        geo_params = {"location": location or "", "key": qweather_key, "number": 1}
        with httpx.Client(timeout=10.0) as client:
            geo_resp = client.get(geo_url, params=geo_params)
            geo_data = geo_resp.json()
            location_id = ""
            if geo_data.get("code") == "200" and geo_data.get("location"):
                location_id = geo_data["location"][0].get("id", "")

            if location_id:
                warn_url = f"https://{host}/v7/warning/now"
                warn_params = {"location": location_id, "key": qweather_key}
                warn_resp = client.get(warn_url, params=warn_params)
                warn_data = warn_resp.json()

                if warn_data.get("code") == "200":
                    warnings = warn_data.get("warning", [])
                    if not warnings:
                        return f"{location or '该地区'} 当前暂无生效的气象预警信号。"
                    parts = [f"【实时气象预警 — {location or '查询地区'}】"]
                    for w in warnings:
                        parts.append(
                            f"- {w.get('title', '未知预警')}（{w.get('pubTime', '时间未知')}）\n"
                            f"  类型：{w.get('typeName', '未知')} | 级别：{w.get('level', '未知')}\n"
                            f"  发布单位：{w.get('sender', '未知')}\n"
                            f"  防御建议：{w.get('text', '暂无详细防御建议')[:300]}"
                        )
                    return "\n".join(parts)

        # API call succeeded but no valid data
        logger.warning("QWeather API returned no valid warning data")
    except Exception as e:
        logger.exception("QWeather API call failed: %s", e)

    # Fallback to DB definitions
    db_result = _query_alerts(alert_type=location)
    if "未查询到" in db_result:
        return "预警查询服务暂不可用，未获取到实时预警信息。"
    return f"【预警信号标准定义】\n{db_result}\n\n（以上为预警信号标准定义，非实时预警）"


def _fetch_qweather_realtime(location: str) -> Optional[dict]:
    qweather_key, qweather_host = _get_qweather_config()
    if not qweather_key or not location:
        return None

    try:
        with httpx.Client(timeout=10.0) as client:
            geo_data = {}
            for geo_host in _qweather_geo_hosts(qweather_host):
                try:
                    geo_resp = client.get(
                        f"https://{geo_host}/geo/v2/city/lookup",
                        params={"location": location, "key": qweather_key, "number": 1},
                    )
                    geo_data = geo_resp.json()
                    if geo_data.get("code") == "200" and geo_data.get("location"):
                        break
                except Exception as e:
                    logger.warning("QWeather geo lookup failed for %s on %s: %s", location, geo_host, e)
                    continue
            else:
                logger.warning(
                    "QWeather geo lookup returned no location for %s, code=%s",
                    location,
                    geo_data.get("code"),
                )
                return None

            location_data = geo_data["location"][0]
            location_id = location_data.get("id", "")
            location_name = location_data.get("name", location)
            if not location_id:
                return None

            weather_resp = client.get(
                f"https://{qweather_host}/v7/weather/now",
                params={"location": location_id, "key": qweather_key},
            )
            weather_data = weather_resp.json()
            if weather_data.get("code") != "200" or not weather_data.get("now"):
                logger.warning("QWeather realtime returned code %s", weather_data.get("code"))
                return None

            now = weather_data["now"]
            return {
                "city": location_name,
                "temperature": _to_int_or_none(now.get("temp")),
                "humidity": _to_int_or_none(now.get("humidity")),
                "pressure": _to_int_or_none(now.get("pressure")),
                "wind_speed": _to_int_or_none(now.get("windSpeed")),
                "wind_direction": now.get("windDir") or "",
                "condition": now.get("text") or "",
                "observed_at": now.get("obsTime") or "",
            }
    except Exception as e:
        logger.exception("QWeather realtime call failed: %s", e)
        return None


def _fetch_qweather_forecast(location: str, days: int) -> Optional[str]:
    qweather_key, qweather_host = _get_qweather_config()
    if not qweather_key or not location:
        return None

    try:
        with httpx.Client(timeout=10.0) as client:
            geo_data = {}
            for geo_host in _qweather_geo_hosts(qweather_host):
                geo_resp = client.get(
                    f"https://{geo_host}/geo/v2/city/lookup",
                    params={"location": location, "key": qweather_key, "number": 1},
                )
                geo_data = geo_resp.json()
                if geo_data.get("code") == "200" and geo_data.get("location"):
                    break
            else:
                logger.warning(
                    "QWeather geo lookup returned no location for %s, code=%s",
                    location,
                    geo_data.get("code"),
                )
                return None

            location_id = geo_data["location"][0].get("id", "")
            location_name = geo_data["location"][0].get("name", location)
            if not location_id:
                return None

            forecast_days = 7 if days > 3 else 3
            weather_resp = client.get(
                f"https://{qweather_host}/v7/weather/{forecast_days}d",
                params={"location": location_id, "key": qweather_key},
            )
            weather_data = weather_resp.json()
            if weather_data.get("code") != "200":
                logger.warning("QWeather forecast returned code %s", weather_data.get("code"))
                return None

            weather_data["daily"] = weather_data.get("daily", [])[:days]
            return WeatherToolService.format_qweather_forecast(location_name, weather_data)
    except Exception as e:
        logger.exception("QWeather forecast call failed: %s", e)
        return None


def _fetch_tavily_weather(location: str, days: int, query: str = "") -> str:
    tavily_key = _get_tavily_key()
    if not tavily_key:
        return "天气查询服务未配置 API Key，暂时无法获取实时预报。"

    search = TavilySearch(
        tavily_api_key=tavily_key,
        max_results=5,
        search_depth="basic",
    )
    query_text = query or f"{location} 未来{days}天天气预报"
    try:
        result = search.invoke({"query": query_text})
        return WeatherToolService.format_search_results(result)
    except Exception as e:
        logger.exception("Tavily weather search failed: %s", e)
        return "天气搜索服务暂不可用，请稍后重试。"


def _query_weather(location: str = "", days: int = 1, query: str = "") -> str:
    """Query structured weather forecast. Args: location city name, days 1-7, query original user question."""
    normalized_days = _normalize_forecast_days(days)
    if normalized_days == 1:
        normalized_days = _infer_forecast_days(query)
    location = location or _infer_location_from_query(query)
    forecast = _fetch_qweather_forecast(location, normalized_days)
    if forecast:
        return forecast
    return _fetch_tavily_weather(location, normalized_days, query)


class WeatherToolService:
    @staticmethod
    def get_tool():
        return StructuredTool.from_function(
            name="weather_query",
            description=(
                "查询指定城市的结构化天气预报。参数：location（城市/地区名称，如北京、江门）、"
                "days（预报天数，1-7；用户问未来七天时传 7）、query（用户原始问题，可选）。"
            ),
            func=_query_weather,
        )

    @staticmethod
    def get_alert_tool():
        return StructuredTool.from_function(
            name="alert_query",
            description="查询实时气象预警信号。参数：location（城市/地区名称，如北京、上海）、alert_type（可选，如暴雨、台风）。",
            func=_fetch_realtime_alerts,
        )

    @staticmethod
    def fetch_realtime_weather(location: str) -> Optional[dict]:
        return _fetch_qweather_realtime(location)

    @staticmethod
    def format_tool_result(result) -> str:
        """Format TavilySearch result for LLM prompt."""
        if hasattr(result, "content"):
            return str(result.content)
        return str(result)

    @staticmethod
    def format_search_results(result) -> str:
        """Parse TavilySearch result into structured text with time annotations."""
        raw = WeatherToolService.format_tool_result(result)
        # Try to parse as list of dicts (TavilySearch may return a dict, list, or object)
        items = []
        if isinstance(result, dict):
            items = result.get("results", [])
        elif isinstance(result, list):
            items = result
        elif hasattr(result, "results"):
            items = result.results
        elif hasattr(result, "content"):
            # Already plain text, return as-is with a header
            return f"【天气搜索结果】\n{raw}"

        if not items:
            return f"【天气搜索结果】\n{raw}"

        parts = ["【天气搜索结果】"]
        for idx, item in enumerate(items[:3], start=1):
            if isinstance(item, dict):
                title = item.get("title", "无标题")
                url = item.get("url", "")
                content = item.get("content", "")
                published = item.get("published_date", "")
            else:
                title = getattr(item, "title", "无标题")
                url = getattr(item, "url", "")
                content = getattr(item, "content", "")
                published = getattr(item, "published_date", "")

            date_str = published if published else "时间未知"
            content_snippet = (content[:500] + "...") if len(str(content)) > 500 else content
            parts.append(
                f"{idx}. {title}（{date_str}）\n"
                f"   来源：{url}\n"
                f"   摘要：{content_snippet}"
            )

        return "\n\n".join(parts)

    @staticmethod
    def format_qweather_forecast(location: str, data: dict) -> str:
        """Format QWeather daily forecast into compact rows for LLM prompt."""
        daily = data.get("daily", [])
        if not daily:
            return f"未查询到{location}天气预报数据。"

        parts = [f"【结构化天气预报 - {location}】"]
        for item in daily:
            date = item.get("fxDate", "日期未知")
            day_text = item.get("textDay", "")
            night_text = item.get("textNight", "")
            if day_text and night_text and day_text != night_text:
                weather_text = f"{day_text}转{night_text}"
            else:
                weather_text = day_text or night_text or "天气未知"
            temp_min = item.get("tempMin", "?")
            temp_max = item.get("tempMax", "?")
            wind_dir = item.get("windDirDay") or item.get("windDirNight") or "风向未知"
            wind_scale = item.get("windScaleDay") or item.get("windScaleNight") or "?"
            humidity = item.get("humidity", "?")
            parts.append(
                f"{date} | {weather_text} | {temp_min}℃~{temp_max}℃ | "
                f"{wind_dir}{wind_scale}级 | 湿度{humidity}%"
            )
        return "\n".join(parts)
