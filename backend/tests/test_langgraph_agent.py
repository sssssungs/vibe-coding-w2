import sys
import os
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../app/agents')))
from langgraph_agent import search_with_agent

def test_search_with_agent_basic():
    query = "노트북 충전기 최저가"
    result = search_with_agent(query)
    assert isinstance(result, dict)
    assert "answer" in result
    assert isinstance(result["answer"], str)
    assert len(result["answer"]) > 0 