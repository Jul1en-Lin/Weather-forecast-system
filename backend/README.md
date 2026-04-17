# 气象智能助手后端

## 启动

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## 环境变量

复制 `.env` 并填写真实值：
- `DATABASE_URL`: MySQL 连接串
- `KIMI_API_KEY` / `DEEPSEEK_API_KEY` / `MINIMAX_API_KEY`: LLM API Key
- `TAVILY_API_KEY`: 天气搜索工具 Key
- `ALLOWED_ORIGINS`: 前端地址，默认 `http://localhost:5173`

## API 文档

启动后访问：http://localhost:8000/docs
