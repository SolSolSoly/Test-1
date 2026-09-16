import streamlit as st
import google.generativeai as genai

# 1. 제미나이 API 연동
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
# 속도가 빠르고 무료 할당량이 넉넉한 gemini-1.5-flash 모델 적용
model = genai.GenerativeModel("gemini-1.5-flash")

st.set_page_config(page_title="AI 주석 리스크 스크리너", layout="wide")
st.title("🔍 공시이용자를 위한 AI 주석 리스크 스크리너 (Powered by Gemini)")
st.divider()

col1, col2 = st.columns([1, 1])

# UI: 6대 필수 계정 입력칸
with col1:
    st.subheader("📊 1. 기초 재무 체력 입력 (단위: 억원)")
    c1, c2 = st.columns(2)
    with c1:
        equity = st.number_input("1. 자기자본", min_value=0, value=300, step=100)
        cash = st.number_input("2. 현금 및 현금성자산", min_value=0, value=150, step=100)
        borrowings = st.number_input("3. 차입금 총계", min_value=0, value=100, step=100)
    with c2:
        liabilities = st.number_input("4. 부채총계", min_value=0, value=200, step=100)
        revenue = st.number_input("5. 총 매출액", min_value=0, value=500, step=100)
        op_income = st.number_input("6. 영업이익", value=50, step=10)

# UI: 주석 입력칸
with col2:
    st.subheader("📝 2. 주석 텍스트 복붙")
    related_party_text = st.text_area("특수관계자 거래 주석", height=150)
    contingent_text = st.text_area("우발부채 및 약정사항 주석", height=150)

st.divider()

st.subheader("💡 3. AI 추가 정밀진단 (선택사항)")
c3, c4 = st.columns(2)
with c3:
    extra_account_name = st.text_input("추가 계정명 (AI가 1차 진단 후 요구한 항목)")
with c4:
    extra_account_value = st.number_input("금액 (억원)", value=0, step=10)

# 분석 실행 버튼
if st.button("🚀 AI 리스크 스코어링 실행", use_container_width=True):
    if not related_party_text and not contingent_text:
        st.error("주석 텍스트를 최소 1개 이상 입력해주세요.")
    else:
        with st.spinner('제미나이가 주석 데이터를 정밀 분석 중입니다...'):
            # 프롬프트 조립
            prompt = f"""
당신은 최고 수준의 기업회계 전문가입니다. 
제공된 [기초 재무 데이터]와 [주석 텍스트]를 교차 검증하여 회사의 '장부 외 숨은 리스크(Off-Balance Risk)'를 스코어링하세요.

반드시 아래 4가지 항목으로 구분하여 가독성 좋은 마크다운 형식으로 작성하세요:

### 1. 🔍 1차 리스크 스코어링
- 우발채무 및 특관자 전이 리스크를 [상 / 중 / 하]로 명확히 판정.
- 주석에서 추출한 주요 뇌관(보증액, 소송액, 풋옵션, 내부매출 비중 등)을 명시하고, 입력된 자기자본/현금/매출과 비교하여 논리적 위험성을 진단.

### 2. 💡 AI 추가 정밀진단 제안
- 현재 주석 텍스트만으로는 부족하여 공시이용자가 DART에서 추가로 확인해야 할 [재무 계정 2가지]를 추천하고 이유를 서술.

### 3. 🛡️ 기업의 방어 수단(Hedge) 점검
- 회사가 이 리스크(환율 변동, 소송 등)를 막기 위해 취했을 가능성이 높은 헤지 수단(파생상품 계약 등)을 제시하고, 재무상태표의 어떤 계정을 봐야 하는지 설명.

### 4. 👶 주린이용 3줄 번역 요약
- 회계 지식이 없는 일반 개인투자자가 한눈에 이해할 수 있도록 쉬운 비유를 들어 3줄로 요약.

---
[입력된 데이터]
- 자기자본: {equity}억원
- 현금 및 현금성자산: {cash}억원
- 차입금 총계: {borrowings}억원
- 부채총계: {liabilities}억원
- 총 매출액: {revenue}억원
- 영업이익: {op_income}억원
- 추가 기입 데이터: {extra_account_name} ({extra_account_value}억원)

[주석 원문]
1. 특수관계자 주석:
{related_party_text}

2. 우발부채 및 약정 주석:
{contingent_text}
"""
            try:
                # 제미나이 호출
                response = model.generate_content(prompt)
                
                st.success("✅ 제미나이 진단 완료!")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"제미나이 호출 중 에러가 발생했습니다: {e}")
