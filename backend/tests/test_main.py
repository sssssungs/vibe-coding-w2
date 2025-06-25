import pytest
from fastapi.testclient import TestClient
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_search():
    payload = {"query": "아이폰 15 케이스", "session_id": "user_123"}
    response = client.post("/search", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "processing"
    assert "task_id" in data
    assert "message" in data 