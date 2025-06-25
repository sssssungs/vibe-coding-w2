import unittest
import os
from unittest.mock import patch
from backend.app.agents import langgraph_agent
from backend.app.agents.langgraph_agent import exa_search

class TestLanggraphAgent(unittest.TestCase):
    def test_duckduckgo_search(self):
        result = langgraph_agent.duckduckgo_search("아이폰 15 케이스")
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)

    @patch("backend.app.agents.langgraph_agent.genai.GenerativeModel")
    def test_gemini_summarize(self, mock_model):
        # Gemini API 키가 없을 때 에러 반환
        with patch.dict(os.environ, {"GEMINI_API_KEY": ""}):
            result = langgraph_agent.gemini_summarize("테스트 프롬프트")
            self.assertIn("에러", result)
        # 정상 동작 mock
        mock_instance = mock_model.return_value
        mock_instance.generate_content.return_value.text = "요약 결과"
        with patch.dict(os.environ, {"GEMINI_API_KEY": "dummy_key"}):
            result = langgraph_agent.gemini_summarize("테스트 프롬프트")
            self.assertEqual(result, "요약 결과")

    @patch("backend.app.agents.langgraph_agent.gemini_summarize")
    @patch("backend.app.agents.langgraph_agent.duckduckgo_search")
    def test_search_with_agent(self, mock_ddg, mock_gemini):
        mock_ddg.return_value = "검색결과1 - url1"
        mock_gemini.return_value = "최저가 요약"
        result = langgraph_agent.search_with_agent("아이폰 15 케이스")
        self.assertIn("answer", result)
        self.assertEqual(result["answer"], "최저가 요약")

    @patch.dict(os.environ, {"EXA_API_KEY": "dummy"})
    @patch("exa_py.Exa")
    def test_exa_search(self, mock_exa):
        class DummyResult:
            def __init__(self, title, url):
                self.title = title
                self.url = url
        class DummyResults:
            results = [DummyResult("상품1", "http://a.com"), DummyResult("상품2", "http://b.com")]
        mock_exa.return_value.search.return_value = DummyResults()
        from importlib import reload
        import backend.app.agents.langgraph_agent as agent_mod
        reload(agent_mod)
        result = agent_mod.exa_search("아이폰 15 케이스")
        self.assertIn("상품1", result)
        self.assertIn("상품2", result)

if __name__ == "__main__":
    unittest.main() 