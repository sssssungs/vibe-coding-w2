from fastapi import FastAPI
from datetime import datetime
from backend.app.api.routes.chat import router as chat_router

app = FastAPI()

@app.get("/")
def root():
    return {"message": "온라인 쇼핑 최저가 검색 챗봇 API"}

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

app.include_router(chat_router) 