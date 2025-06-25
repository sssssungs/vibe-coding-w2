from fastapi import APIRouter, Request
from pydantic import BaseModel
from backend.app.services.agent_service import search_product

router = APIRouter()

class SearchRequest(BaseModel):
    query: str
    session_id: str

class SearchResponse(BaseModel):
    task_id: str
    status: str
    message: str

@router.post("/search")
async def search(request: Request):
    data = await request.json()
    query = data.get("query")
    session_id = data.get("session_id")
    # 실제 검색 로직 호출
    result = search_product(query, session_id)
    return result 