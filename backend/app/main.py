from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.routers import auth, assistant
from app.config import settings

# 自动建表（开发阶段）
Base.metadata.create_all(bind=engine)

app = FastAPI(title="气象智能助手 API", version="1.0.0")

# CORS
origins = [origin.strip() for origin in settings.allowed_origins.split(",")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 路由注册
app.include_router(auth.router)
app.include_router(assistant.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}
