# Weather Oracle Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a Weather Oracle page that turns city weather data into a daily tarot card, personal fortune, and mood guide while preserving the current assistant app.

**Architecture:** Keep the existing Vue 3 and FastAPI app. Add a shared app shell, a new `/oracle` page, tarot card asset metadata, typed frontend API calls, and an upgraded `/api/v1/assistant/weather-card` endpoint that separates structured weather lookup from AI interpretation.

**Tech Stack:** Vue 3, Vite, TypeScript, Pinia, Vue Router, FastAPI, SQLAlchemy, Pydantic, QWeather, LangChain/OpenAI-compatible chat models.

---

## Inputs

- Concept references:
  - `docs/images/Divinatio-concept-map-lightmode.png`
  - `docs/images/Divination-concept-map-darkmode.png`
- Figma tarot source:
  - File key: `Ekroehh3gLkbPnj2raccJH`
  - Page: `0:1` / `All Cards`
  - Major Arcana section: `1:2`, 22 cards
  - Wands section: `1:26`, 14 cards
  - Cups section: `1:41`, 14 cards
  - Swords section: `1:56`, 14 cards
  - Pentacles section: `1:72`, 14 cards
- Existing API to upgrade:
  - `POST /api/v1/assistant/weather-card`
- Existing chat API to keep:
  - `POST /api/v1/assistant/chat/stream`

## File Responsibility Map

- `src/layouts/OracleLayout.vue`: shared logged-in app shell with nav, user area, and content slot.
- `src/views/WeatherOracle.vue`: page state, city draw workflow, cache handling, and dashboard composition.
- `src/components/oracle/*.vue`: focused visual panels for city input, tarot card, weather metrics, mood guide, and oracle chat.
- `src/api/weatherOracle.ts`: frontend fetch wrapper for `/api/v1/assistant/weather-card`.
- `src/types/weatherOracle.ts`: TypeScript request/response contracts.
- `src/data/tarotCards.ts`: 78-card manifest and local image paths.
- `src/utils/tarot.ts`: Shanghai date key, weather fingerprint, and deterministic card selection.
- `src/styles/oracle-theme.css`: dark/light theme variables and oracle page utilities.
- `backend/app/services/weather_tool.py`: structured QWeather live weather lookup, while keeping current forecast text behavior.
- `backend/app/schemas/assistant.py`: Pydantic contracts for the weather oracle response.
- `backend/app/routers/assistant.py`: weather-card endpoint orchestration and LLM JSON parsing.
- `backend/tests/test_weather_tool.py`: weather lookup regression coverage.
- `backend/tests/test_weather_card.py`: endpoint and LLM parsing coverage.

## Data Contracts

Frontend types to add in `src/types/weatherOracle.ts`:

```ts
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
  weather_mappings: WeatherOracleMapping[]
}
```

Backend response shape in `backend/app/schemas/assistant.py` must match this frontend contract.

## Task 1: Add Structured Live Weather Lookup

**Files:**
- Modify: `backend/app/services/weather_tool.py`
- Modify: `backend/tests/test_weather_tool.py`

- [ ] **Step 1: Add failing tests for live weather parsing**

Append this test class to `backend/tests/test_weather_tool.py`:

```python
class StructuredWeatherNowTests(unittest.TestCase):
    @patch("app.services.weather_tool._get_qweather_config")
    @patch("app.services.weather_tool.httpx.Client")
    def test_fetch_realtime_weather_parses_qweather_now(self, client_cls, get_config):
        get_config.return_value = ("key-123", "devapi.qweather.com")

        class FakeResponse:
            def __init__(self, payload):
                self.payload = payload

            def json(self):
                return self.payload

        class FakeClient:
            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc, tb):
                return False

            def get(self, url, params):
                if "/geo/v2/city/lookup" in url:
                    return FakeResponse({
                        "code": "200",
                        "location": [{"id": "101020100", "name": "上海"}],
                    })
                if "/v7/weather/now" in url:
                    return FakeResponse({
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
                    })
                raise AssertionError(url)

        client_cls.return_value = FakeClient()

        result = WeatherToolService.fetch_realtime_weather("上海")

        self.assertEqual(result["city"], "上海")
        self.assertEqual(result["temperature"], 22)
        self.assertEqual(result["humidity"], 78)
        self.assertEqual(result["pressure"], 1012)
        self.assertEqual(result["wind_speed"], 12)
        self.assertEqual(result["wind_direction"], "东北风")
        self.assertEqual(result["condition"], "多云")
        self.assertEqual(result["observed_at"], "2026-06-06T09:00+08:00")

    @patch("app.services.weather_tool._get_qweather_config")
    def test_fetch_realtime_weather_returns_none_without_key(self, get_config):
        get_config.return_value = ("", "devapi.qweather.com")

        self.assertIsNone(WeatherToolService.fetch_realtime_weather("上海"))
```

- [ ] **Step 2: Run tests to confirm failure**

Run:

```bash
cd backend && python3 -m pytest tests/test_weather_tool.py::StructuredWeatherNowTests -v
```

Expected: fail with `AttributeError: type object 'WeatherToolService' has no attribute 'fetch_realtime_weather'`.

- [ ] **Step 3: Add live weather implementation**

Insert this helper before `class WeatherToolService` in `backend/app/services/weather_tool.py`:

```python
def _to_int_or_none(value) -> Optional[int]:
    if value in (None, ""):
        return None
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return None


def _fetch_qweather_realtime(location: str) -> Optional[dict]:
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
                logger.warning("QWeather geo lookup returned no realtime location for %s", location)
                return None

            location_item = geo_data["location"][0]
            location_id = location_item.get("id", "")
            location_name = location_item.get("name", location)
            if not location_id:
                return None

            weather_resp = client.get(
                f"https://{qweather_host}/v7/weather/now",
                params={"location": location_id, "key": qweather_key},
            )
            weather_data = weather_resp.json()
            if weather_data.get("code") != "200":
                logger.warning("QWeather realtime returned code %s", weather_data.get("code"))
                return None

            now = weather_data.get("now", {})
            return {
                "city": location_name,
                "temperature": _to_int_or_none(now.get("temp")),
                "humidity": _to_int_or_none(now.get("humidity")),
                "pressure": _to_int_or_none(now.get("pressure")),
                "wind_speed": _to_int_or_none(now.get("windSpeed")),
                "wind_direction": now.get("windDir") or "未知",
                "condition": now.get("text") or "未知",
                "observed_at": now.get("obsTime") or "",
            }
    except Exception:
        logger.exception("QWeather realtime call failed")
        return None
```

Add this static method inside `WeatherToolService`:

```python
    @staticmethod
    def fetch_realtime_weather(location: str) -> Optional[dict]:
        return _fetch_qweather_realtime(location)
```

- [ ] **Step 4: Run task tests**

Run:

```bash
cd backend && python3 -m pytest tests/test_weather_tool.py::StructuredWeatherNowTests -v
```

Expected: pass.

- [ ] **Step 5: Commit task**

Run:

```bash
git add backend/app/services/weather_tool.py backend/tests/test_weather_tool.py
git commit -m "feat: add structured weather lookup"
```

## Task 2: Add Weather Oracle Schemas And Pure Helpers

**Files:**
- Modify: `backend/app/schemas/assistant.py`
- Modify: `backend/app/routers/assistant.py`
- Create: `backend/tests/test_weather_card.py`

- [ ] **Step 1: Add failing helper tests**

Create `backend/tests/test_weather_card.py` with:

```python
import json
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
```

- [ ] **Step 2: Run tests to confirm failure**

Run:

```bash
cd backend && python3 -m pytest tests/test_weather_card.py::WeatherCardHelperTests -v
```

Expected: fail because helpers are not defined.

- [ ] **Step 3: Replace weather-card schemas**

In `backend/app/schemas/assistant.py`, replace `WeatherCardResponse` with these models:

```python
class WeatherOracleWeather(BaseModel):
    temperature: Optional[int] = None
    humidity: Optional[int] = None
    pressure: Optional[int] = None
    wind_speed: Optional[int] = None
    wind_direction: str = ""
    condition: str = ""
    observed_at: str = ""


class WeatherOracleTarot(BaseModel):
    id: str
    name_en: str
    name_zh: str
    image: str
    keywords: List[str]


class WeatherOracleFortune(BaseModel):
    title: str
    summary: str
    lucky_color: str
    lucky_number: int
    good_for: str
    avoid: str


class WeatherOracleMoodGuide(BaseModel):
    title: str
    analysis: str
    suggestions: List[str]


class WeatherOracleMapping(BaseModel):
    metric: str
    label: str
    value: str
    reading: str
    score: int


class WeatherCardResponse(BaseModel):
    city: str
    date: str
    timezone: str
    updated_at: str
    weather: WeatherOracleWeather
    tarot: WeatherOracleTarot
    fortune: WeatherOracleFortune
    mood_guide: WeatherOracleMoodGuide
    weather_mappings: List[WeatherOracleMapping]
```

Keep `WeatherCardRequest` as:

```python
class WeatherCardRequest(BaseModel):
    city: str = Field(..., min_length=1)
    model_id: Optional[str] = None
    tarot_card_id: Optional[str] = None
```

- [ ] **Step 4: Add backend helpers**

Add these helpers near the top of `backend/app/routers/assistant.py` after constants:

```python
TAROT_CARD_IDS = [
    "major-00-fool", "major-01-magician", "major-02-high-priestess", "major-03-empress",
    "major-04-emperor", "major-05-hierophant", "major-06-lovers", "major-07-chariot",
    "major-08-strength", "major-09-hermit", "major-10-wheel-of-fortune", "major-11-justice",
    "major-12-hanged-man", "major-13-death", "major-14-temperance", "major-15-devil",
    "major-16-tower", "major-17-star", "major-18-moon", "major-19-sun",
    "major-20-judgement", "major-21-world",
    "wands-01-ace", "wands-02-two", "wands-03-three", "wands-04-four", "wands-05-five",
    "wands-06-six", "wands-07-seven", "wands-08-eight", "wands-09-nine", "wands-10-ten",
    "wands-11-king", "wands-12-knight", "wands-13-page", "wands-14-queen",
    "cups-01-ace", "cups-02-two", "cups-03-three", "cups-04-four", "cups-05-five",
    "cups-06-six", "cups-07-seven", "cups-08-eight", "cups-09-nine", "cups-10-ten",
    "cups-11-king", "cups-12-knight", "cups-13-page", "cups-14-queen",
    "swords-01-ace", "swords-02-two", "swords-03-three", "swords-04-four", "swords-05-five",
    "swords-06-six", "swords-07-seven", "swords-08-eight", "swords-09-nine", "swords-10-ten",
    "swords-11-king", "swords-12-knight", "swords-13-page", "swords-14-queen",
    "pentacles-01-ace", "pentacles-02-two", "pentacles-03-three", "pentacles-04-four",
    "pentacles-05-five", "pentacles-06-six", "pentacles-07-seven", "pentacles-08-eight",
    "pentacles-09-nine", "pentacles-10-ten", "pentacles-11-king", "pentacles-12-knight",
    "pentacles-13-page", "pentacles-14-queen",
]

TAROT_CARD_META = {
    card_id: {
        "id": card_id,
        "name_en": card_id,
        "name_zh": card_id,
        "image": f"/tarot/cards/{card_id}.png",
        "keywords": ["天气", "情绪", "今日指引"],
    }
    for card_id in TAROT_CARD_IDS
}


def clean_json_object_text(content: str) -> str:
    text = strip_thinking_tags(content or "").strip()
    if text.startswith("```"):
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1:
            return text[start:end + 1]
    return text


def build_weather_fingerprint(weather: dict) -> str:
    return "|".join([
        str(weather.get("temperature")),
        str(weather.get("humidity")),
        str(weather.get("pressure")),
        str(weather.get("wind_speed")),
        str(weather.get("condition")),
    ])


def select_tarot_card_id(city: str, date_key: str, weather_fingerprint: str) -> str:
    import hashlib

    seed = f"{city}|{date_key}|{weather_fingerprint}".encode("utf-8")
    digest = hashlib.sha256(seed).hexdigest()
    index = int(digest[:8], 16) % len(TAROT_CARD_IDS)
    return TAROT_CARD_IDS[index]
```

- [ ] **Step 5: Run helper tests**

Run:

```bash
cd backend && python3 -m pytest tests/test_weather_card.py::WeatherCardHelperTests -v
```

Expected: pass.

- [ ] **Step 6: Commit task**

Run:

```bash
git add backend/app/schemas/assistant.py backend/app/routers/assistant.py backend/tests/test_weather_card.py
git commit -m "feat: add weather oracle response schema"
```

## Task 3: Upgrade `/weather-card` Endpoint

**Files:**
- Modify: `backend/app/routers/assistant.py`
- Modify: `backend/tests/test_weather_card.py`

- [ ] **Step 1: Add endpoint tests**

Append to `backend/tests/test_weather_card.py`:

```python
from types import SimpleNamespace
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app


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
```

- [ ] **Step 2: Run endpoint tests to confirm failure**

Run:

```bash
cd backend && python3 -m pytest tests/test_weather_card.py::WeatherCardEndpointTests -v
```

Expected: fail until the endpoint is upgraded.

- [ ] **Step 3: Import `get_llm` at router module scope**

In `backend/app/routers/assistant.py`, change the existing import to include `get_llm` at module scope if it is not already available for patching:

```python
from app.services.llm import get_llm, stream_llm_response, strip_thinking_tags, ThinkingFilter, get_model_config
```

- [ ] **Step 4: Replace `generate_weather_card` implementation**

Use this behavior inside `generate_weather_card`:

```python
    from zoneinfo import ZoneInfo
    import json

    from app.models.model_config import ModelConfig
    from app.services.weather_tool import WeatherToolService

    city = req.city.strip()
    weather = WeatherToolService.fetch_realtime_weather(city)
    if not weather:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"未能获取到 {city} 的天气数据，请确认城市名称是否正确。",
        )

    now = datetime.now(ZoneInfo("Asia/Shanghai"))
    date_key = now.strftime("%Y-%m-%d")
    weather_fingerprint = build_weather_fingerprint(weather)
    tarot_id = req.tarot_card_id or select_tarot_card_id(weather["city"], date_key, weather_fingerprint)
    tarot = TAROT_CARD_META.get(tarot_id) or TAROT_CARD_META[select_tarot_card_id(weather["city"], date_key, weather_fingerprint)]

    model_id = req.model_id
    if not model_id:
        first_model = db.query(ModelConfig).order_by(ModelConfig.created_at.asc()).first()
        if not first_model:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="没有可用的模型配置，请先到系统设置中配置 LLM。",
            )
        model_id = first_model.id

    prompt = (
        "你是天气占卜师。你不会播报天气，而是把天气参数翻译成今天的个人运势和情绪状态指南。\n"
        "只使用给定天气数据和塔罗牌，不要编造额外天气事实。\n"
        "直接输出 JSON，不要 markdown，不要解释。\n"
        f"城市：{weather['city']}\n"
        f"日期：{date_key}，时区：Asia/Shanghai\n"
        f"天气数据：{json.dumps(weather, ensure_ascii=False)}\n"
        f"塔罗牌：{json.dumps(tarot, ensure_ascii=False)}\n"
        "JSON 结构必须包含 fortune、mood_guide、weather_mappings。"
    )

    fallback = {
        "fortune": {
            "title": "云隙微光",
            "summary": "今天适合先观察，再行动。把节奏放慢一点，很多事会自然变清楚。",
            "lucky_color": "雾紫色",
            "lucky_number": 7,
            "good_for": "整理思路",
            "avoid": "冲动争执",
        },
        "mood_guide": {
            "title": "缓慢回神",
            "analysis": "天气信号偏向内收，适合减少无效沟通，把精力留给真正需要处理的事。",
            "suggestions": ["留二十分钟独处", "喝点热饮", "把决定放到明天"],
        },
        "weather_mappings": [
            {"metric": "temperature", "label": "温度", "value": f"{weather.get('temperature')}°C", "reading": "平和舒适", "score": 70},
            {"metric": "humidity", "label": "湿度", "value": f"{weather.get('humidity')}%", "reading": "内收敏感", "score": 65},
            {"metric": "pressure", "label": "气压", "value": f"{weather.get('pressure')} hPa", "reading": "掌控感提升", "score": 68},
            {"metric": "wind_speed", "label": "风速", "value": f"{weather.get('wind_speed')} km/h", "reading": "思绪流动", "score": 60},
        ],
    }

    card_data = fallback
    try:
        llm = get_llm(model_id, temperature=0.7, streaming=False, db=db)
        resp = llm.invoke(prompt)
        card_data = json.loads(clean_json_object_text(resp.content))
    except Exception:
        logger.exception("Failed to generate weather oracle JSON; using fallback")

    return WeatherCardResponse(
        city=weather["city"],
        date=date_key,
        timezone="Asia/Shanghai",
        updated_at=now.isoformat(),
        weather=weather,
        tarot=tarot,
        fortune=card_data["fortune"],
        mood_guide=card_data["mood_guide"],
        weather_mappings=card_data["weather_mappings"],
    )
```

- [ ] **Step 5: Run endpoint tests**

Run:

```bash
cd backend && python3 -m pytest tests/test_weather_card.py tests/test_weather_tool.py -v
```

Expected: pass.

- [ ] **Step 6: Commit task**

Run:

```bash
git add backend/app/routers/assistant.py backend/tests/test_weather_card.py
git commit -m "feat: upgrade weather oracle api"
```

## Task 4: Add Tarot Asset Manifest

**Files:**
- Create: `public/tarot/cards/*.png`
- Create: `src/data/tarotCards.ts`
- Create: `src/utils/tarot.ts`

- [ ] **Step 1: Export Figma assets**

Use Figma file key `Ekroehh3gLkbPnj2raccJH`. Export each card node as PNG into `public/tarot/cards/` using this mapping:

```text
major-00-fool -> 1:3
major-01-magician -> 1:4
major-02-high-priestess -> 1:5
major-03-empress -> 1:6
major-04-emperor -> 1:7
major-05-hierophant -> 1:8
major-06-lovers -> 1:9
major-07-chariot -> 1:10
major-08-strength -> 1:11
major-09-hermit -> 1:12
major-10-wheel-of-fortune -> 1:13
major-11-justice -> 1:14
major-12-hanged-man -> 1:15
major-13-death -> 1:16
major-14-temperance -> 1:17
major-15-devil -> 1:18
major-16-tower -> 1:19
major-17-star -> 1:20
major-18-moon -> 1:21
major-19-sun -> 1:22
major-20-judgement -> 1:23
major-21-world -> 1:24
wands-01-ace -> 1:27
wands-02-two -> 1:28
wands-03-three -> 1:29
wands-04-four -> 1:30
wands-05-five -> 1:31
wands-06-six -> 1:32
wands-07-seven -> 1:33
wands-08-eight -> 1:34
wands-09-nine -> 1:35
wands-10-ten -> 1:36
wands-11-king -> 1:37
wands-12-knight -> 1:38
wands-13-page -> 1:39
wands-14-queen -> 1:40
cups-01-ace -> 1:42
cups-02-two -> 1:43
cups-03-three -> 1:44
cups-04-four -> 1:45
cups-05-five -> 1:46
cups-06-six -> 1:47
cups-07-seven -> 1:48
cups-08-eight -> 1:49
cups-09-nine -> 1:50
cups-10-ten -> 1:51
cups-11-king -> 1:52
cups-12-knight -> 1:53
cups-13-page -> 1:54
cups-14-queen -> 1:55
swords-01-ace -> 1:58
swords-02-two -> 1:59
swords-03-three -> 1:60
swords-04-four -> 1:61
swords-05-five -> 1:62
swords-06-six -> 1:63
swords-07-seven -> 1:64
swords-08-eight -> 1:65
swords-09-nine -> 1:66
swords-10-ten -> 1:67
swords-11-king -> 1:68
swords-12-knight -> 1:69
swords-13-page -> 1:70
swords-14-queen -> 1:71
pentacles-01-ace -> 1:73
pentacles-02-two -> 1:74
pentacles-03-three -> 1:75
pentacles-04-four -> 1:76
pentacles-05-five -> 1:77
pentacles-06-six -> 1:78
pentacles-07-seven -> 1:79
pentacles-08-eight -> 1:80
pentacles-09-nine -> 1:81
pentacles-10-ten -> 1:82
pentacles-11-king -> 1:83
pentacles-12-knight -> 1:84
pentacles-13-page -> 1:85
pentacles-14-queen -> 1:86
```

- [ ] **Step 2: Add card manifest**

Create `src/data/tarotCards.ts`:

```ts
export interface TarotCard {
  id: string
  nameEn: string
  nameZh: string
  arcana: 'major' | 'minor'
  suit: 'major' | 'wands' | 'cups' | 'swords' | 'pentacles'
  rank: string
  image: string
  keywords: string[]
}

const image = (id: string) => `/tarot/cards/${id}.png`

export const tarotCards: TarotCard[] = [
  { id: 'major-00-fool', nameEn: 'The Fool', nameZh: '愚者', arcana: 'major', suit: 'major', rank: '0', image: image('major-00-fool'), keywords: ['开始', '自由', '冒险'] },
  { id: 'major-01-magician', nameEn: 'The Magician', nameZh: '魔术师', arcana: 'major', suit: 'major', rank: '1', image: image('major-01-magician'), keywords: ['行动', '资源', '表达'] },
  { id: 'major-02-high-priestess', nameEn: 'The High Priestess', nameZh: '女祭司', arcana: 'major', suit: 'major', rank: '2', image: image('major-02-high-priestess'), keywords: ['直觉', '沉静', '观察'] },
  { id: 'major-03-empress', nameEn: 'The Empress', nameZh: '皇后', arcana: 'major', suit: 'major', rank: '3', image: image('major-03-empress'), keywords: ['滋养', '创造', '丰盛'] },
  { id: 'major-04-emperor', nameEn: 'The Emperor', nameZh: '皇帝', arcana: 'major', suit: 'major', rank: '4', image: image('major-04-emperor'), keywords: ['秩序', '边界', '掌控'] },
  { id: 'major-05-hierophant', nameEn: 'The Hierophant', nameZh: '教皇', arcana: 'major', suit: 'major', rank: '5', image: image('major-05-hierophant'), keywords: ['传统', '学习', '建议'] },
  { id: 'major-06-lovers', nameEn: 'The Lovers', nameZh: '恋人', arcana: 'major', suit: 'major', rank: '6', image: image('major-06-lovers'), keywords: ['选择', '关系', '协调'] },
  { id: 'major-07-chariot', nameEn: 'The Chariot', nameZh: '战车', arcana: 'major', suit: 'major', rank: '7', image: image('major-07-chariot'), keywords: ['推进', '方向', '意志'] },
  { id: 'major-08-strength', nameEn: 'Strength', nameZh: '力量', arcana: 'major', suit: 'major', rank: '8', image: image('major-08-strength'), keywords: ['耐心', '柔韧', '内力'] },
  { id: 'major-09-hermit', nameEn: 'The Hermit', nameZh: '隐者', arcana: 'major', suit: 'major', rank: '9', image: image('major-09-hermit'), keywords: ['独处', '思考', '寻找'] },
  { id: 'major-10-wheel-of-fortune', nameEn: 'Wheel of Fortune', nameZh: '命运之轮', arcana: 'major', suit: 'major', rank: '10', image: image('major-10-wheel-of-fortune'), keywords: ['变化', '周期', '转机'] },
  { id: 'major-11-justice', nameEn: 'Justice', nameZh: '正义', arcana: 'major', suit: 'major', rank: '11', image: image('major-11-justice'), keywords: ['判断', '平衡', '原则'] },
  { id: 'major-12-hanged-man', nameEn: 'The Hanged Man', nameZh: '倒吊人', arcana: 'major', suit: 'major', rank: '12', image: image('major-12-hanged-man'), keywords: ['暂停', '换位', '等待'] },
  { id: 'major-13-death', nameEn: 'Death', nameZh: '死神', arcana: 'major', suit: 'major', rank: '13', image: image('major-13-death'), keywords: ['结束', '转化', '告别'] },
  { id: 'major-14-temperance', nameEn: 'Temperance', nameZh: '节制', arcana: 'major', suit: 'major', rank: '14', image: image('major-14-temperance'), keywords: ['调和', '修复', '节奏'] },
  { id: 'major-15-devil', nameEn: 'The Devil', nameZh: '恶魔', arcana: 'major', suit: 'major', rank: '15', image: image('major-15-devil'), keywords: ['欲望', '束缚', '清醒'] },
  { id: 'major-16-tower', nameEn: 'The Tower', nameZh: '高塔', arcana: 'major', suit: 'major', rank: '16', image: image('major-16-tower'), keywords: ['打破', '突变', '释放'] },
  { id: 'major-17-star', nameEn: 'The Star', nameZh: '星星', arcana: 'major', suit: 'major', rank: '17', image: image('major-17-star'), keywords: ['希望', '治愈', '指引'] },
  { id: 'major-18-moon', nameEn: 'The Moon', nameZh: '月亮', arcana: 'major', suit: 'major', rank: '18', image: image('major-18-moon'), keywords: ['潜意识', '梦境', '不安'] },
  { id: 'major-19-sun', nameEn: 'The Sun', nameZh: '太阳', arcana: 'major', suit: 'major', rank: '19', image: image('major-19-sun'), keywords: ['明朗', '活力', '坦诚'] },
  { id: 'major-20-judgement', nameEn: 'Judgement', nameZh: '审判', arcana: 'major', suit: 'major', rank: '20', image: image('major-20-judgement'), keywords: ['回应', '复盘', '觉察'] },
  { id: 'major-21-world', nameEn: 'The World', nameZh: '世界', arcana: 'major', suit: 'major', rank: '21', image: image('major-21-world'), keywords: ['完成', '整合', '抵达'] },
]

const minorNames: Record<string, string> = {
  ace: 'Ace', two: 'Two', three: 'Three', four: 'Four', five: 'Five',
  six: 'Six', seven: 'Seven', eight: 'Eight', nine: 'Nine', ten: 'Ten',
  king: 'King', knight: 'Knight', page: 'Page', queen: 'Queen',
}

const minorZh: Record<string, string> = {
  wands: '权杖', cups: '圣杯', swords: '宝剑', pentacles: '星币',
  ace: '一', two: '二', three: '三', four: '四', five: '五',
  six: '六', seven: '七', eight: '八', nine: '九', ten: '十',
  king: '国王', knight: '骑士', page: '侍从', queen: '王后',
}

for (const suit of ['wands', 'cups', 'swords', 'pentacles'] as const) {
  const ranks = ['ace', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'king', 'knight', 'page', 'queen']
  ranks.forEach((rank, index) => {
    const cardNo = String(index + 1).padStart(2, '0')
    const id = `${suit}-${cardNo}-${rank}`
    tarotCards.push({
      id,
      nameEn: `${minorNames[rank]} of ${suit[0].toUpperCase()}${suit.slice(1)}`,
      nameZh: `${minorZh[suit]}${minorZh[rank]}`,
      arcana: 'minor',
      suit,
      rank,
      image: image(id),
      keywords: ['行动', '情绪', '提醒'],
    })
  })
}

export function getTarotCardById(id: string): TarotCard | undefined {
  return tarotCards.find(card => card.id === id)
}
```

- [ ] **Step 3: Add deterministic picker**

Create `src/utils/tarot.ts`:

```ts
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
```

- [ ] **Step 4: Run frontend build**

Run:

```bash
npm run build
```

Expected: pass.

- [ ] **Step 5: Commit task**

Run:

```bash
git add public/tarot/cards src/data/tarotCards.ts src/utils/tarot.ts
git commit -m "feat: add tarot card assets"
```

## Task 5: Add Frontend API And Types

**Files:**
- Create: `src/types/weatherOracle.ts`
- Create: `src/api/weatherOracle.ts`

- [ ] **Step 1: Add TypeScript response types**

Create `src/types/weatherOracle.ts` using the exact contract from the `Data Contracts` section.

- [ ] **Step 2: Add API wrapper**

Create `src/api/weatherOracle.ts`:

```ts
import type { WeatherOracleReading, WeatherOracleRequest } from '../types/weatherOracle'

export async function generateWeatherOracleReading(payload: WeatherOracleRequest): Promise<WeatherOracleReading> {
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
```

- [ ] **Step 3: Run frontend build**

Run:

```bash
npm run build
```

Expected: pass.

- [ ] **Step 4: Commit task**

Run:

```bash
git add src/types/weatherOracle.ts src/api/weatherOracle.ts
git commit -m "feat: add weather oracle api client"
```

## Task 6: Extract Shared App Shell

**Files:**
- Create: `src/layouts/OracleLayout.vue`
- Modify: `src/views/Home.vue`
- Modify: `src/views/IntelligentAssistant.vue`
- Modify: `src/views/Settings.vue`
- Modify: `src/views/AdminUsers.vue`

- [ ] **Step 1: Create layout shell**

Create `src/layouts/OracleLayout.vue` with these public slots:

```vue
<template>
  <div class="oracle-layout">
    <aside class="oracle-sidebar">
      <div class="oracle-brand">
        <span class="oracle-brand-icon">☁</span>
        <div>
          <strong>Weather Oracle</strong>
          <span>气象占卜台</span>
        </div>
      </div>

      <nav class="oracle-nav">
        <router-link to="/oracle" class="oracle-nav-item" active-class="active">首页</router-link>
        <router-link to="/intelligent-assistant" class="oracle-nav-item" active-class="active">智能对话</router-link>
        <router-link v-if="isAdmin" to="/settings" class="oracle-nav-item" active-class="active">系统设置</router-link>
        <router-link v-if="isAdmin" to="/admin/users" class="oracle-nav-item" active-class="active">用户管理</router-link>
      </nav>

      <div class="oracle-user">
        <div class="oracle-avatar">{{ userInitial }}</div>
        <div class="oracle-user-copy">
          <strong>{{ username }}</strong>
          <span>{{ isAdmin ? '管理员' : '普通用户' }}</span>
        </div>
        <button type="button" @click="handleLogout">退出</button>
      </div>
    </aside>

    <main class="oracle-main">
      <slot />
    </main>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const username = computed(() => authStore.username)
const isAdmin = computed(() => authStore.isAdmin)
const userInitial = computed(() => username.value ? username.value.charAt(0).toUpperCase() : 'U')

async function handleLogout() {
  await authStore.logout()
  router.push('/login')
}
</script>
```

- [ ] **Step 2: Add minimal layout CSS**

Put scoped CSS in `OracleLayout.vue`; keep it small because Task 9 handles visual polish:

```css
.oracle-layout {
  min-height: 100vh;
  display: flex;
  background: var(--oracle-bg, #07111f);
  color: var(--oracle-text, #f6ead8);
}

.oracle-sidebar {
  width: 260px;
  min-height: 100vh;
  padding: 24px;
  border-right: 1px solid var(--oracle-border, rgba(215, 174, 105, 0.22));
}

.oracle-main {
  flex: 1;
  min-width: 0;
  padding: 24px;
}

.oracle-nav {
  display: grid;
  gap: 8px;
  margin-top: 32px;
}

.oracle-nav-item {
  padding: 12px 14px;
  border-radius: 8px;
}

.oracle-nav-item.active {
  color: var(--oracle-gold, #d7ae69);
}
```

- [ ] **Step 3: Wrap existing views**

For each logged-in page, import layout:

```ts
import OracleLayout from '../layouts/OracleLayout.vue'
```

Then wrap existing main page content:

```vue
<template>
  <OracleLayout>
    <!-- keep the page-specific content here -->
  </OracleLayout>
</template>
```

Remove copied sidebar markup from each page after confirming the page still has its own content.

- [ ] **Step 4: Run frontend build**

Run:

```bash
npm run build
```

Expected: pass.

- [ ] **Step 5: Commit task**

Run:

```bash
git add src/layouts/OracleLayout.vue src/views/Home.vue src/views/IntelligentAssistant.vue src/views/Settings.vue src/views/AdminUsers.vue
git commit -m "refactor: extract shared app shell"
```

## Task 7: Add Weather Oracle Page And Components

**Files:**
- Create: `src/views/WeatherOracle.vue`
- Create: `src/components/oracle/QuickCityPicker.vue`
- Create: `src/components/oracle/TarotCardDisplay.vue`
- Create: `src/components/oracle/WeatherMetricGrid.vue`
- Create: `src/components/oracle/MoodGuidePanel.vue`
- Create: `src/components/oracle/OracleChatPanel.vue`

- [ ] **Step 1: Create quick city picker**

Create `src/components/oracle/QuickCityPicker.vue`:

```vue
<template>
  <form class="quick-city-picker" @submit.prevent="submitCity">
    <label for="oracle-city">城市</label>
    <div class="city-input-row">
      <input id="oracle-city" v-model.trim="draftCity" type="text" placeholder="输入城市，例如上海" />
      <button type="submit" :disabled="!draftCity">抽取</button>
    </div>
    <div class="quick-cities">
      <button v-for="city in cities" :key="city" type="button" @click="chooseCity(city)">
        {{ city }}
      </button>
    </div>
  </form>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const emit = defineEmits<{ draw: [city: string] }>()
const cities = ['上海', '北京', '杭州', '广州', '深圳', '成都', '南京', '武汉']
const draftCity = ref('')

function submitCity() {
  if (draftCity.value) emit('draw', draftCity.value)
}

function chooseCity(city: string) {
  draftCity.value = city
  emit('draw', city)
}
</script>
```

- [ ] **Step 2: Create display components**

Each display component accepts typed props from `WeatherOracleReading`. Keep props read-only and avoid fetch logic inside display components.

`TarotCardDisplay.vue`:

```vue
<template>
  <section class="tarot-card-display">
    <img :src="tarot.image" :alt="tarot.name_zh" />
    <div>
      <span>今日天气塔罗牌</span>
      <h2>{{ tarot.name_zh }}</h2>
      <p>{{ tarot.keywords.join(' · ') }}</p>
    </div>
  </section>
</template>

<script setup lang="ts">
import type { WeatherOracleTarot } from '../../types/weatherOracle'

defineProps<{ tarot: WeatherOracleTarot }>()
</script>
```

`WeatherMetricGrid.vue`:

```vue
<template>
  <section class="weather-metric-grid">
    <article v-for="item in mappings" :key="item.metric">
      <span>{{ item.label }}</span>
      <strong>{{ item.value }}</strong>
      <p>{{ item.reading }}</p>
      <meter min="0" max="100" :value="item.score" />
    </article>
  </section>
</template>

<script setup lang="ts">
import type { WeatherOracleMapping } from '../../types/weatherOracle'

defineProps<{ mappings: WeatherOracleMapping[] }>()
</script>
```

`MoodGuidePanel.vue`:

```vue
<template>
  <section class="mood-guide-panel">
    <h2>{{ guide.title }}</h2>
    <p>{{ guide.analysis }}</p>
    <ul>
      <li v-for="item in guide.suggestions" :key="item">{{ item }}</li>
    </ul>
  </section>
</template>

<script setup lang="ts">
import type { WeatherOracleMoodGuide } from '../../types/weatherOracle'

defineProps<{ guide: WeatherOracleMoodGuide }>()
</script>
```

- [ ] **Step 3: Create page state**

Create `WeatherOracle.vue` with this state flow:

```vue
<template>
  <OracleLayout>
    <div class="weather-oracle-page">
      <section class="oracle-hero">
        <div>
          <p>AI 为你抽取今日的天气指引</p>
          <h1>今日天气塔罗牌</h1>
        </div>
        <QuickCityPicker @draw="drawCity" />
      </section>

      <section v-if="errorMessage" class="oracle-error">{{ errorMessage }}</section>

      <section v-if="!reading" class="oracle-empty">
        <h2>先输入或选择城市</h2>
        <p>我会读取温度、湿度、气压和风速，再生成今日天气塔罗牌。</p>
      </section>

      <section v-else class="oracle-dashboard">
        <TarotCardDisplay :tarot="reading.tarot" />
        <div class="oracle-fortune">
          <h2>{{ reading.fortune.title }}</h2>
          <p>{{ reading.fortune.summary }}</p>
          <dl>
            <dt>幸运色</dt><dd>{{ reading.fortune.lucky_color }}</dd>
            <dt>幸运数字</dt><dd>{{ reading.fortune.lucky_number }}</dd>
            <dt>宜</dt><dd>{{ reading.fortune.good_for }}</dd>
            <dt>忌</dt><dd>{{ reading.fortune.avoid }}</dd>
          </dl>
        </div>
        <WeatherMetricGrid :mappings="reading.weather_mappings" />
        <MoodGuidePanel :guide="reading.mood_guide" />
        <OracleChatPanel :city="reading.city" :reading="reading" />
      </section>
    </div>
  </OracleLayout>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import OracleLayout from '../layouts/OracleLayout.vue'
import QuickCityPicker from '../components/oracle/QuickCityPicker.vue'
import TarotCardDisplay from '../components/oracle/TarotCardDisplay.vue'
import WeatherMetricGrid from '../components/oracle/WeatherMetricGrid.vue'
import MoodGuidePanel from '../components/oracle/MoodGuidePanel.vue'
import OracleChatPanel from '../components/oracle/OracleChatPanel.vue'
import { generateWeatherOracleReading } from '../api/weatherOracle'
import { useAuthStore } from '../stores/auth'
import { getShanghaiDateKey } from '../utils/tarot'
import type { WeatherOracleReading } from '../types/weatherOracle'

const authStore = useAuthStore()
const reading = ref<WeatherOracleReading | null>(null)
const isLoading = ref(false)
const errorMessage = ref('')

const cacheKey = computed(() => `weather_oracle:last_reading:${authStore.username || 'guest'}`)

onMounted(() => {
  const cached = localStorage.getItem(cacheKey.value)
  if (!cached) return
  try {
    reading.value = JSON.parse(cached)
  } catch {
    localStorage.removeItem(cacheKey.value)
  }
})

async function drawCity(city: string) {
  isLoading.value = true
  errorMessage.value = ''
  try {
    const data = await generateWeatherOracleReading({ city })
    reading.value = data
    localStorage.setItem(cacheKey.value, JSON.stringify(data))
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : '抽取失败'
  } finally {
    isLoading.value = false
  }
}

function shouldRefreshToday() {
  return reading.value ? reading.value.date !== getShanghaiDateKey() : false
}
</script>
```

- [ ] **Step 4: Add oracle chat panel**

Create `OracleChatPanel.vue` as a compact wrapper that sends suggestion prompts to the existing assistant stream. Start with non-streaming visible placeholders if integrating stream code would duplicate too much; if stream is copied, keep it local to this component.

Use these quick prompts:

```ts
const suggestions = ['今天天气如何影响我的状态？', '今日运势解析', '适合出行吗？', '给我一句天气签文。']
```

- [ ] **Step 5: Run frontend build**

Run:

```bash
npm run build
```

Expected: pass.

- [ ] **Step 6: Commit task**

Run:

```bash
git add src/views/WeatherOracle.vue src/components/oracle
git commit -m "feat: add weather oracle page"
```

## Task 8: Wire Routes And Nav

**Files:**
- Modify: `src/router/index.ts`
- Modify: `src/layouts/OracleLayout.vue`

- [ ] **Step 1: Add route**

In `src/router/index.ts`, import route component lazily:

```ts
{
  path: '/oracle',
  name: 'WeatherOracle',
  component: () => import('../views/WeatherOracle.vue'),
  meta: { requiresAuth: true }
}
```

- [ ] **Step 2: Change authenticated redirects**

Change:

```ts
next('/home')
```

to:

```ts
next('/oracle')
```

for authenticated login/register redirects and non-admin fallback. Keep `/home` as a valid route.

- [ ] **Step 3: Confirm nav links**

In `OracleLayout.vue`, ensure:

```vue
<router-link to="/oracle" class="oracle-nav-item" active-class="active">首页</router-link>
<router-link to="/intelligent-assistant" class="oracle-nav-item" active-class="active">智能对话</router-link>
```

- [ ] **Step 4: Run frontend build**

Run:

```bash
npm run build
```

Expected: pass.

- [ ] **Step 5: Commit task**

Run:

```bash
git add src/router/index.ts src/layouts/OracleLayout.vue
git commit -m "feat: route weather oracle home"
```

## Task 9: Add Oracle Theme And Responsive Layout

**Files:**
- Create: `src/styles/oracle-theme.css`
- Modify: `src/style.css`
- Modify: `src/views/WeatherOracle.vue`
- Modify: `src/components/oracle/*.vue`

- [ ] **Step 1: Add theme variables**

Create `src/styles/oracle-theme.css`:

```css
:root {
  --oracle-bg: #07111f;
  --oracle-panel: rgba(10, 20, 35, 0.78);
  --oracle-panel-soft: rgba(17, 28, 48, 0.72);
  --oracle-border: rgba(215, 174, 105, 0.24);
  --oracle-gold: #d7ae69;
  --oracle-purple: #a88adf;
  --oracle-text: #f6ead8;
  --oracle-muted: #b7a891;
  --oracle-danger: #d78372;
}

[data-oracle-theme='light'] {
  --oracle-bg: #fbf6ec;
  --oracle-panel: rgba(255, 252, 246, 0.84);
  --oracle-panel-soft: rgba(255, 248, 238, 0.72);
  --oracle-border: rgba(177, 132, 65, 0.24);
  --oracle-gold: #b18441;
  --oracle-purple: #8d71bd;
  --oracle-text: #2d2418;
  --oracle-muted: #7d715f;
  --oracle-danger: #b25f53;
}
```

- [ ] **Step 2: Import theme CSS**

In `src/style.css`, add:

```css
@import './styles/oracle-theme.css';
```

- [ ] **Step 3: Apply dashboard grid**

In `WeatherOracle.vue` scoped CSS, use:

```css
.weather-oracle-page {
  display: grid;
  gap: 16px;
}

.oracle-hero,
.oracle-empty,
.oracle-error,
.oracle-dashboard > * {
  border: 1px solid var(--oracle-border);
  background: var(--oracle-panel);
  border-radius: 8px;
}

.oracle-dashboard {
  display: grid;
  grid-template-columns: minmax(260px, 0.8fr) minmax(360px, 1.2fr) minmax(300px, 0.9fr);
  gap: 16px;
  align-items: stretch;
}

@media (max-width: 1280px) {
  .oracle-dashboard {
    grid-template-columns: minmax(280px, 0.9fr) minmax(360px, 1.1fr);
  }
}

@media (max-width: 760px) {
  .oracle-dashboard {
    grid-template-columns: 1fr;
  }
}
```

- [ ] **Step 4: Run frontend build**

Run:

```bash
npm run build
```

Expected: pass.

- [ ] **Step 5: Manual visual check**

Run:

```bash
npm run dev
```

Open:

```text
http://localhost:5173/oracle
```

Check:
- First visit shows city prompt.
- Shanghai draw shows tarot image, weather metrics, fortune, and mood guide.
- Refresh keeps cached reading.
- 1280px width does not crush the tarot card.
- Mobile width uses one column.

- [ ] **Step 6: Commit task**

Run:

```bash
git add src/styles/oracle-theme.css src/style.css src/views/WeatherOracle.vue src/components/oracle
git commit -m "style: add weather oracle theme"
```

## Task 10: Docs And Final Verification

**Files:**
- Modify: `docs/project_status.md`
- Optional modify: `README.md`

- [ ] **Step 1: Update project status**

Set current goal to:

```markdown
Goal: Add Weather Oracle page with tarot-based weather interpretation.

Status: Implementation planned; ready for task-by-task execution.
```

Add this to Done:

```markdown
- Wrote implementation plan at `docs/superpowers/plans/2026-06-06-weather-oracle.md`.
- Confirmed Figma tarot source file `Ekroehh3gLkbPnj2raccJH` contains 78 card nodes.
```

- [ ] **Step 2: Run backend tests**

Run:

```bash
cd backend && python3 -m pytest
```

Expected: pass.

- [ ] **Step 3: Run frontend build**

Run:

```bash
npm run build
```

Expected: pass.

- [ ] **Step 4: Run whitespace check on touched paths**

Run:

```bash
git diff --check -- src backend/app backend/tests docs/project_status.md docs/superpowers/plans/2026-06-06-weather-oracle.md
```

Expected: no output. If unrelated existing whitespace in `backend/app/routers/assistant.py` appears, note it in final summary and do not hide it.

- [ ] **Step 5: Final manual acceptance**

Verify:
- `/oracle` requires login.
- First visit has no generated reading until city is provided.
- Shanghai draw returns a complete card.
- Cached reading survives page refresh.
- Date mismatch in Shanghai time offers a new draw without automatic API use.
- Existing `/intelligent-assistant` still streams.
- Admin-only pages remain admin-only.

- [ ] **Step 6: Commit docs**

Run:

```bash
git add docs/project_status.md README.md
git commit -m "docs: update weather oracle status"
```

## Self-Review

- Figma source and exact 78-card node mapping are included.
- Backend weather lookup, API response, LLM JSON cleanup, and fallback behavior are covered.
- Frontend page, cache behavior, Shanghai date handling, route wiring, and visual layout are covered.
- Existing assistant and admin flows have explicit regression checks.
- No open decisions remain for v1: city input is manual plus common city buttons, readings are cached in `localStorage`, and QWeather remains the weather source.
