# 온라인 쇼핑 최저가 검색 챗봇 Agent

이 브랜치는 test_3(GitHub Actions 최종확인)용입니다.

[![테스트 자동화](https://github.com/sssssungs/vibe-coding-w2/actions/workflows/test.yml/badge.svg)](https://github.com/sssssungs/vibe-coding-w2/actions/workflows/test.yml)

## 프로젝트 개요

**온라인 쇼핑 최저가 검색 챗봇 Agent**는 사용자가 상품명을 입력하면 여러 쇼핑몰의 가격을 자동으로 비교·분석하여 최적의 구매 선택을 도와주는 AI 챗봇입니다.

- FastAPI + Streamlit 기반의 웹 챗봇
- LangGraph + MCP(네이버/Exa 등) 연동
- Gemini LLM 활용 정보 파싱 및 검증
- PR/이슈 자동화(GitHub Actions)

---

## 주요 기능
- 실시간 상품 최저가 검색 및 가격 비교
- 다양한 쇼핑몰 정보 통합 제공
- 할인, 배송비, 구매링크 등 부가 정보 표시
- 자연어 기반 챗봇 인터페이스
- PR/이슈 자동 assign, label, comment, 리뷰 등 협업 자동화

---

## 폴더 구조
```
├── backend/         # FastAPI 백엔드
│   ├── app/         # API, Agent, Service 모듈
│   ├── main.py      # 엔트리포인트
│   ├── requirements.txt
│   └── tests/       # 테스트 코드
├── frontend/        # Streamlit 프론트엔드
│   ├── app.py
│   ├── requirements.txt
│   └── test_app.py
├── docs/            # 문서 및 와이어프레임
├── .github/         # GitHub Actions 워크플로우
├── .cursor/rules/   # 개발/운영 정책 및 PR/이슈 관리 룰
├── README.md
```

---

## 기술 스택
- **백엔드**: FastAPI, Python 3.11
- **프론트엔드**: Streamlit
- **AI/Agent**: LangGraph, Gemini LLM, MCP(네이버/Exa)
- **테스트**: Pytest, Unittest
- **CI/CD**: GitHub Actions

---

## 사용법
1. **백엔드 실행**
   ```bash
   cd backend
   pip install -r requirements.txt
   uvicorn main:app --reload
   ```
2. **프론트엔드 실행**
   ```bash
   cd frontend
   pip install -r requirements.txt
   streamlit run app.py
   ```
3. **테스트 실행**
   - 백엔드: `pytest` 또는 `python -m unittest discover`
   - 프론트엔드: `python -m unittest test_app.py`

---

## 기여 방법
- PR/이슈 생성 시 자동 assign, label, comment, 리뷰어 지정 등 자동화됨
- [CONTRIBUTING.md] 작성 예정
- 코드/문서/테스트 등 다양한 기여 환영

---

## 라이선스
- MIT License

---

## 배포/데모
- (예정) Streamlit Cloud, Vercel 등 배포 예정

---

## 문의
- GitHub Issues 활용 