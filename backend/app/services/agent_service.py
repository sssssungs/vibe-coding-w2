from backend.app.agents.langgraph_agent import search_with_agent

def search_product(query: str, session_id: str) -> dict:
    # 실제 검색 에이전트 호출
    agent_result = search_with_agent(query)
    # agent_result는 {"answer": ...} 형태
    return {
        "task_id": f"task_{session_id}",
        "status": "complete",
        "message": agent_result.get("answer", "검색 결과가 없습니다.")
    } 