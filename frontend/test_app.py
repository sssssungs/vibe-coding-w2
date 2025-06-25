import unittest
import os

class TestStreamlitApp(unittest.TestCase):
    def test_app_file_exists(self):
        # app.py 파일이 존재하는지 확인
        self.assertTrue(os.path.exists('frontend/app.py'))

    def test_app_contains_title(self):
        # app.py에 챗봇 타이틀이 포함되어 있는지 확인
        with open('frontend/app.py', 'r', encoding='utf-8') as f:
            content = f.read()
        self.assertIn('온라인 쇼핑 최저가 챗봇', content)

    def test_app_contains_input(self):
        # app.py에 입력창 코드가 포함되어 있는지 확인
        with open('frontend/app.py', 'r', encoding='utf-8') as f:
            content = f.read()
        self.assertIn('st.text_input', content)

    def test_app_contains_session_state(self):
        with open('frontend/app.py', 'r', encoding='utf-8') as f:
            content = f.read()
        self.assertIn('st.session_state', content)

    def test_app_contains_message_display(self):
        with open('frontend/app.py', 'r', encoding='utf-8') as f:
            content = f.read()
        self.assertIn('st.markdown', content)

    def test_app_contains_requests(self):
        with open('frontend/app.py', 'r', encoding='utf-8') as f:
            content = f.read()
        self.assertIn('requests.post', content)

    def test_app_contains_spinner(self):
        with open('frontend/app.py', 'r', encoding='utf-8') as f:
            content = f.read()
        self.assertIn('st.spinner', content)

    def test_app_contains_result_list(self):
        with open('frontend/app.py', 'r', encoding='utf-8') as f:
            content = f.read()
        self.assertIn('products', content)
        self.assertIn('result_str', content)

    def test_app_contains_error_ui(self):
        with open('frontend/app.py', 'r', encoding='utf-8') as f:
            content = f.read()
        self.assertIn('st.error', content)

if __name__ == "__main__":
    unittest.main() 