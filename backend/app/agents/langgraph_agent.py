# from langgraph.prebuilt import create_react_agent
from duckduckgo_search import DDGS
from duckduckgo_search.exceptions import DuckDuckGoSearchException
import os
import google.generativeai as genai
from exa_py import Exa
import re

# DuckDuckGo Tool 함수 정의
def duckduckgo_search(query: str) -> str:
    """DuckDuckGo에서 상품명 등 쿼리로 검색 결과를 가져옵니다."""
    try:
        results = DDGS().text(query, max_results=3)
    except DuckDuckGoSearchException as e:
        return f"DuckDuckGo 검색 중 에러 발생: {str(e)}"
    if not results:
        return "검색 결과가 없습니다."
    return "\n".join([f"{r['title']} - {r['href']}" for r in results])

# Exa Tool 함수 정의
def exa_search(query: str) -> str:
    """Exa에서 상품명 등 쿼리로 검색 결과(본문 하이라이트 포함)를 가져옵니다."""
    api_key = os.environ.get("EXA_API_KEY")
    if not api_key:
        return "[에러] Exa API 키가 설정되어 있지 않습니다."
    exa = Exa(api_key)
    highlights_options = {
        "num_sentences": 20,  # 최대한 길게
        "highlights_per_url": 2
    }
    shopping_domains = [
        "coupang.com", "gmarket.co.kr", "11st.co.kr", "auction.co.kr", "ssg.com", "wemakeprice.com", "interpark.com", "naver.com", "amazon.com", "ebay.com", "aliexpress.com"
    ]
    search_query = f"{query} 가격 구매 최저가 할인 세일 원 ₩ KRW $ USD 총액 배송비"
    try:
        results = exa.search_and_contents(
            search_query,
            highlights=highlights_options,
            num_results=20,
            use_autoprompt=True,
            include_domains=shopping_domains
        )
    except Exception as e:
        return f"Exa 검색 중 에러 발생: {str(e)}"
    if not results or not results.results:
        return "검색 결과가 없습니다."
    sorted_results = sorted(
        results.results,
        key=lambda r: getattr(r, 'published_date', None) or "",
        reverse=True
    )
    shop_min_price = {}
    # 가격 패턴 강화 (원, ₩, KRW, $, USD, 총액, 할인, 세일 등)
    price_pattern = re.compile(r"([0-9]{1,3}(?:,[0-9]{3})+|[0-9]+) ?(원|₩|KRW|\$|USD|￦|달러|불|엔|유로|총액|할인|세일)?")
    for r in sorted_results:
        url = r.url
        domain = url.split("/")[2].replace("www.","")
        highlight = '\n'.join(r.highlights) if hasattr(r, 'highlights') and r.highlights else ''
        price_matches = price_pattern.findall(highlight + ' ' + r.title)
        price_values = []
        for p, unit in price_matches:
            p_clean = re.sub(r'[^0-9]', '', p)
            if p_clean.isdigit():
                price_values.append(int(p_clean))
        min_price = min(price_values) if price_values else None
        if domain in shop_min_price:
            if min_price is not None and shop_min_price[domain]['min_price'] is not None and min_price >= shop_min_price[domain]['min_price']:
                continue
            if min_price is None and shop_min_price[domain]['min_price'] is not None:
                continue
        shop_min_price[domain] = {
            'title': r.title,
            'url': url,
            'highlight': highlight,
            'min_price': min_price,
            'published_date': getattr(r, 'published_date', None) or ""
        }
    final_results = sorted(shop_min_price.values(), key=lambda x: x['published_date'], reverse=True)
    final_results = sorted(final_results, key=lambda x: (x['min_price'] is None, x['min_price'] if x['min_price'] is not None else 999999999))
    lines = []
    for item in final_results:
        if item['min_price'] is not None:
            price_str = f"{item['min_price']}원"
        else:
            price_str = "링크에서 가격 확인"
        lines.append(f"{item['title']} - {item['url']}\n가격: {price_str}\n{item['highlight']}")
    return "\n\n".join(lines)

# Gemini LLM 요약 함수 (공식 API, 동기 wrapper)
def gemini_summarize(prompt: str) -> str:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return "[에러] Gemini API 키가 설정되어 있지 않습니다."
    genai.configure(api_key=api_key)
    try:
        model = genai.GenerativeModel("gemini-2.5-flash-preview-05-20")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"[에러] Gemini 호출 실패: {str(e)}"

def search_with_agent(query: str) -> dict:
    search_result = exa_search(query)
    prompt = f"""너는 온라인 쇼핑 최저가 비교 챗봇이야.\n아래는 사용자가 \"{query}\"로 Exa에서 검색한 실제 쇼핑몰/가격/상품 정보야.\n\n{search_result}\n\n아래 조건을 반드시 지켜서 표로 정리해줘.\n- 각 행에는 [쇼핑몰명 | 상품명(간단 요약) | 최저가 | 배송비 | 총액 | 구매링크]를 포함해.\n- 반드시 가격(최저가) 정보를 표에 포함해.\n- 가격, 배송비, 총액, 구매링크가 명확하지 않으면 '링크에서 가격 확인'으로 표시해.\n- 광고/홍보성 문구, 위키/뉴스/리뷰/공식정보 등 실제 구매와 무관한 정보는 빼고, 실제 구매 가능한 쇼핑몰 정보만 남겨.\n- 한 쇼핑몰에서는 가장 저렴한 금액의 링크 하나만 표에 포함해.\n- 최신 검색 결과가 표 상단에 오도록 정렬해.\n- 아래 예시처럼 가격을 꼭 표에 넣어줘.\n\n[예시]\n| 쇼핑몰명 | 상품명 | 최저가 | 배송비 | 총액 | 구매링크 |\n|---|---|---|---|---|---|\n| coupang | 닌텐도 스위치 | 298000원 | 3000원 | 301000원 | https://coupang.com/xxx |\n| gmarket | 닌텐도 스위치 | 링크에서 가격 확인 | 정보 없음 | 링크에서 가격 확인 | https://gmarket.co.kr/xxx |\n\n- 마지막에 한 줄로 '최저가 요약'을 한국어로 알려줘."""
    answer = gemini_summarize(prompt)
    return {"answer": answer} 