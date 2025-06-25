import streamlit as st
import requests

st.set_page_config(page_title="온라인 쇼핑 최저가 챗봇")
st.title("온라인 쇼핑 최저가 챗봇")

# 세션 상태로 메시지 기록 관리
if 'messages' not in st.session_state:
    st.session_state['messages'] = []

# 사용자 입력창
user_input = st.text_input("상품명을 입력하세요:")

# FastAPI 백엔드 URL
API_URL = "http://localhost:8000/search"

# 입력이 있으면 메시지 기록에 추가 및 API 호출
if user_input:
    st.session_state['messages'].append({"role": "user", "content": user_input})
    with st.spinner('검색 중입니다...'):
        try:
            response = requests.post(API_URL, json={"query": user_input, "session_id": "test_session"})
            if response.status_code == 200:
                data = response.json()
                # 가격 비교 결과 리스트 표시
                if "products" in data:
                    products = data["products"]
                    result_str = "\n".join([
                        f"{p['shop_name']}: {p['total_price']}원 (할인: {p['discount_rate']}%, 배송비: {p['shipping_cost']}원) [구매링크]({p['purchase_url']})"
                        for p in products
                    ])
                    bot_msg = f"검색 결과:\n{result_str}"
                else:
                    bot_msg = data.get("message", "검색 결과를 불러왔습니다.")
            else:
                bot_msg = f"검색 중 오류가 발생했습니다. (status: {response.status_code})"
        except Exception as e:
            bot_msg = f"에러: {e}"
            st.error(bot_msg)
    st.session_state['messages'].append({"role": "bot", "content": bot_msg})

# 메시지 표시 영역
for msg in st.session_state['messages']:
    if msg["role"] == "user":
        st.markdown(f"**사용자:** {msg['content']}")
    else:
        st.markdown(f"**챗봇:** {msg['content']}") 