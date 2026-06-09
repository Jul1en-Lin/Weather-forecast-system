# Dynamic Weather Tip Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Transform the static date-based daily weather tip card on the homepage to be dynamic and driven by LLM response matching real-time weather conditions of the selected city, with a graceful calendric fallback.

**Architecture:** We will add a `weather_tip` field to the `WeatherCardResponse` backend schema and instruct the LLM to output it. The frontend `OracleLeftSidebar` will display this tip when available, falling back to the existing 12-tip calendar modulo rotation when not.

**Tech Stack:** FastAPI, Pydantic, SQLAlchemy, pytest, Vue 3, TypeScript, Vite.

---

### Task 1: Backend Schemas Update

**Files:**
- Modify: `backend/app/schemas/assistant.py`

- [ ] **Step 1: Add the new schema types in `backend/app/schemas/assistant.py`**
  Add the `WeatherOracleTip` model and append the `weather_tip` field to `WeatherCardResponse`.

  Modify `backend/app/schemas/assistant.py`:
  ```python
  # Add this class above WeatherCardResponse
  class WeatherOracleTip(BaseModel):
      title: str
      advice: str

  # Inside WeatherCardResponse, add the weather_tip field:
  class WeatherCardResponse(BaseModel):
      # ... (existing fields)
      weather_tip: Optional[WeatherOracleTip] = None
  ```

- [ ] **Step 2: Run verification**
  Run: `cd backend && python3 -m pytest tests/test_weather_card.py`
  Expected: PASS (as the new field is optional and has a default value `None`).

- [ ] **Step 3: Commit**
  Run:
  ```bash
  git add backend/app/schemas/assistant.py
  git commit -m "feat(backend): add weather_tip to weather card response schemas"
  ```

---

### Task 2: Backend Logic, Prompt & Tests

**Files:**
- Modify: `backend/app/routers/assistant.py`
- Test & Modify: `backend/tests/test_weather_card.py`

- [ ] **Step 1: Write a failing test in `backend/tests/test_weather_card.py`**
  Modify `backend/tests/test_weather_card.py` to add a test asserting that `weather_tip` is correctly returned in the `/weather-card` endpoint response, and that it falls back to the day-of-month modulo fallback tip if the LLM output is empty or fails.

  Add the following test method to the test class in `backend/tests/test_weather_card.py`:
  ```python
  def test_weather_tip_generation_and_fallback(self):
      # Test fallback behavior (LLM response is empty or fails)
      response = self.client.post(
          "/api/v1/assistant/weather-card",
          json={"city": "北京"},
          headers=self.headers
      )
      self.assertEqual(response.status_code, 200)
      data = response.json()
      self.assertIn("weather_tip", data)
      self.assertIsNotNone(data["weather_tip"])
      self.assertIn("title", data["weather_tip"])
      self.assertIn("advice", data["weather_tip"])
  ```

- [ ] **Step 2: Run test to verify it fails**
  Run: `cd backend && python3 -m pytest tests/test_weather_card.py -k test_weather_tip_generation_and_fallback`
  Expected: FAIL (either `weather_tip` is missing or is `None`).

- [ ] **Step 3: Implement backend helper, prompt, and normalization in `backend/app/routers/assistant.py`**
  Modify `backend/app/routers/assistant.py`:
  
  1. Define a helper function to calculate the fallback tip:
     ```python
     def build_fallback_weather_tip() -> dict:
         from datetime import datetime
         day = datetime.now().day
         tips = [
             {"title": "紫外线提示", "advice": "夏季紫外线较强，外出建议涂抹防晒霜、配戴遮阳帽"},
             {"title": "防暑降温", "advice": "高温天气注意补充水分，避免长时间户外暴晒"},
             {"title": "雷雨天气", "advice": "雷雨天气避免在空旷地带停留，远离金属物体"},
             {"title": "台风预防", "advice": "台风来临前检查门窗，储备必要物资，关注预警信息"},
             {"title": "雾天出行", "advice": "大雾天气能见度低，驾车请减速慢行、开启雾灯"},
             {"title": "寒潮提醒", "advice": "寒潮来临注意添衣保暖，预防感冒和心血管疾病"},
             {"title": "空气质量", "advice": "关注空气质量指数，污染天气减少户外活动"},
             {"title": "干燥天气", "advice": "秋冬干燥季节注意补水保湿，预防静电和皮肤干裂"},
             {"title": "晨练建议", "advice": "晴好天气适宜户外运动，但避开高温时段"},
             {"title": "梅雨季节", "advice": "梅雨期间注意防潮除湿，衣物及时晾晒烘干"},
             {"title": "霜冻预警", "advice": "霜冻天气注意农作物保护，行车注意路面结冰"},
             {"title": "气压变化", "advice": "气压剧烈波动可能引起头痛不适，注意休息调节"},
         ]
         return tips[day % len(tips)]
     ```

  2. In `normalize_weather_oracle_model_data` (around lines 210-290), add parsing for `weather_tip`:
     ```python
     # Inside normalize_weather_oracle_model_data function, before returning:
     raw_tip = card_data.get("weather_tip") or card_data.get("weatherTip")
     weather_tip = dict(fallback["weather_tip"])
     if isinstance(raw_tip, dict):
         for key in ("title", "advice"):
             text = non_empty_text(raw_tip.get(key))
             if text:
                 weather_tip[key] = text

     # Return dictionary addition:
     return {
         # ... existing fields
         "weather_tip": weather_tip,
     }
     ```

  3. In `build_weather_oracle_prompt` (around line 298), update prompt to request `weather_tip`:
     ```python
     # Inside build_weather_oracle_prompt:
     return (
         "只输出 JSON，不要 markdown。"
         f"日期={date_key};天气={json.dumps(weather_payload, ensure_ascii=False)};"
         f"塔罗={json.dumps(card_payload, ensure_ascii=False)};"
         "生成 fortune={title,summary,lucky_color,lucky_number,good_for,avoid}、"
         "mood_guide={title,analysis,suggestions} 和 "
         "weather_tip={title,advice}（针对当前天气的防范与生活气象贴士，建议字数在30字以内。可以从常见的主题如'防暑降温、雷雨天气、台风预防、雾天出行、寒潮提醒、空气质量、干燥天气'中选择，也可以根据具体天气为用户定制一个）。"
     )
     ```

  4. In `generate_weather_card` (around line 693), add `weather_tip` to `fallback` and `response_payload`:
     ```python
     # Inside fallback dict definition:
     fallback = {
         # ... existing fields
         "weather_tip": build_fallback_weather_tip(),
     }

     # Inside response_payload dict:
     response_payload = {
         # ... existing fields
         "weather_tip": fallback["weather_tip"],
     }

     # Inside model_payload dict (the one built from LLM card_data):
     model_payload = {
         # ... existing fields
         "weather_tip": normalized_card_data["weather_tip"],
     }
     ```

- [ ] **Step 4: Run test to verify it passes**
  Run: `cd backend && python3 -m pytest tests/test_weather_card.py`
  Expected: PASS

- [ ] **Step 5: Commit**
  Run:
  ```bash
  git add backend/app/routers/assistant.py backend/tests/test_weather_card.py
  git commit -m "feat(backend): implement LLM prompt & fallback for weather_tip"
  ```

---

### Task 3: Frontend Types Update

**Files:**
- Modify: `src/types/weatherOracle.ts`

- [ ] **Step 1: Add frontend interface for `WeatherOracleTip` and update `WeatherOracleReading`**
  Modify `src/types/weatherOracle.ts`:
  ```typescript
  // Add this interface
  export interface WeatherOracleTip {
    title: string
    advice: string
  }

  // Update WeatherOracleReading interface:
  export interface WeatherOracleReading {
    // ... existing fields
    weather_tip?: WeatherOracleTip
  }
  ```

- [ ] **Step 2: Commit**
  Run:
  ```bash
  git add src/types/weatherOracle.ts
  git commit -m "feat(frontend): add weather_tip interface to typescript types"
  ```

---

### Task 4: Frontend View Update

**Files:**
- Modify: `src/views/WeatherOracle.vue`

- [ ] **Step 1: Pass the dynamic tip to the left sidebar component**
  Modify `src/views/WeatherOracle.vue` near line 25:
  ```vue
  <!-- Before -->
  <OracleLeftSidebar />

  <!-- After -->
  <OracleLeftSidebar :weather-tip="reading?.weather_tip" />
  ```

- [ ] **Step 2: Commit**
  Run:
  ```bash
  git add src/views/WeatherOracle.vue
  git commit -m "feat(frontend): pass weather_tip prop to OracleLeftSidebar component"
  ```

---

### Task 5: Frontend Sidebar Component Update

**Files:**
- Modify: `src/components/oracle/OracleLeftSidebar.vue`

- [ ] **Step 1: Declare the prop and calculate computed tip**
  Modify `src/components/oracle/OracleLeftSidebar.vue` script section:
  ```typescript
  import { computed } from 'vue'
  import { useAuthStore } from '../../stores/auth'
  import type { WeatherOracleTip } from '../../types/weatherOracle' // Import type

  const authStore = useAuthStore()
  const isAdmin = computed(() => authStore.isAdmin)

  // Declare props
  const props = defineProps<{
    weatherTip?: WeatherOracleTip
  }>()

  const weatherTips = [
    // ... (keep the existing 12 tips as fallback list)
  ]

  // Calculate final tip to display: prop if available, otherwise date-based fallback
  const displayTip = computed(() => {
    if (props.weatherTip && props.weatherTip.title && props.weatherTip.advice) {
      return props.weatherTip
    }
    const day = new Date().getDate()
    return weatherTips[day % weatherTips.length]
  })
  ```

- [ ] **Step 2: Render using `displayTip`**
  Modify the template in `src/components/oracle/OracleLeftSidebar.vue` around lines 51-52:
  ```vue
  <!-- Before -->
  <strong class="moon-sign-title">{{ currentTip.title }}</strong>
  <p class="moon-sign-copy">{{ currentTip.advice }}</p>

  <!-- After -->
  <strong class="moon-sign-title">{{ displayTip.title }}</strong>
  <p class="moon-sign-copy">{{ displayTip.advice }}</p>
  ```

- [ ] **Step 3: Verify frontend typecheck and build**
  Run: `npm run build`
  Expected: Successful compilation without TypeScript errors.

- [ ] **Step 4: Commit**
  Run:
  ```bash
  git add src/components/oracle/OracleLeftSidebar.vue
  git commit -m "feat(frontend): bind dynamic tip to sidebar UI with fallback support"
  ```
