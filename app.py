import streamlit as st
import time

# 1. 웹페이지 기본 설정
st.set_page_config(page_title="AI 주석 리스크 스크리너", layout="wide")
st.title("🔍 공시이용자를 위한 AI 주석 리스크 스크리너")
st.markdown("**재무제표 본문 숫자**와 **외계어 같은 주석**을 대조하여 숨은 폭탄(Off-Balance Risk)을 찾아냅니다.")
st.divider()

# 2. 좌우 단 나누기 (UI 구성)
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📊 1. 기초 재무 체력 입력 (단위: 억원)")
    st.caption("DART 재무상태표 및 손익계산서에서 숫자를 입력하세요.")
    
    # 6대 필수 계정 입력칸
    c1, c2 = st.columns(2)
    with c1:
        equity = st.number_input("1. 자기자본", min_value=0, value=0, step=100)
        cash = st.number_input("2. 현금 및 현금성자산", min_value=0, value=0, step=100)
        borrowings = st.number_input("3. 차입금 총계 (단기+장기)", min_value=0, value=0, step=100)
    with c2:
        liabilities = st.number_input("4. 부채총계", min_value=0, value=0, step=100)
        revenue = st.number_input("5. 총 매출액", min_value=0, value=0, step=100)
        op_income = st.number_input("6. 영업이익", value=0, step=100)

with col2:
    st.subheader("📝 2. 주석 텍스트 복붙")
    st.caption("DART 사업보고서에서 관련 주석을 그대로 복사해 붙여넣으세요.")
    
    related_party_text = st.text_area("특수관계자 거래 주석", height=150, placeholder="특수관계자 매출, 대여금 등 주석 원문 복붙...")
    contingent_text = st.text_area("우발부채 및 약정사항 주석", height=150, placeholder="지급보증, 소송, 금융약정 등 주석 원문 복붙...")

st.divider()

# 3. 추가 정밀 분석을 위한 자율 입력칸 (방법 3 로직)
st.subheader("💡 3. AI 추가 정밀진단 (선택사항)")
st.caption("AI가 1차 진단 후 요구한 추가 계정명과 금액이 있다면 아래에 기입하고 다시 분석을 돌리세요.")
c3, c4 = st.columns(2)
with c3:
    extra_account_name = st.text_input("추가 계정명 (예: 외화단기차입금)")
with c4:
    extra_account_value = st.number_input("금액 (억원)", value=0, step=100)

# 4. 분석 실행 버튼
if st.button("🚀 AI 리스크 스코어링 실행", use_container_width=True):
    
    # 에러 방지 로직 (값이 없을 때)
    if not related_party_text and not contingent_text:
        st.error("주석 텍스트를 최소 1개 이상 입력해야 분석이 가능합니다.")
    elif equity == 0 or revenue == 0:
        st.warning("경고: 자기자본과 매출액이 0이면 정확한 비율 산출이 어렵습니다. 그래도 진행합니다.")
    
    # 5. 결과 출력부 (AI 분석 로직)
    else:
        with st.spinner('AI가 수십 페이지의 주석을 해체하고 숫자를 크로스체크 중입니다...'):
            time.sleep(2) # LLM API 통신을 가정하여 2초 대기
            
            st.success("✅ 분석 완료!")
            
            # --- 실전에서는 이 아래 텍스트들을 LLM(OpenAI/Gemini API) 호출 결과로 대체함 ---
            
            # 탭으로 깔끔하게 결과 분류
            tab1, tab2, tab3, tab4 = st.tabs(["📊 1차 스크리닝", "💡 정밀진단 제안", "🛡️ 헤지(Hedge) 분석", "👶 주린이 요약 (3줄)"])
            
            with tab1:
                st.markdown("### 🔍 우발채무 및 특관자 전이 리스크: **[ 상 / 중 / 하 ]**")
                st.markdown(f"입력된 자기자본 {equity}억원, 현금 {cash}억원 대비 주석에서 추출된 뇌관을 분석한 결과입니다.")
                st.info("(여기에 AI가 6대 숫자와 주석을 비교한 팩트 기반 스코어링 결과가 출력됨)")
                
            with tab2:
                st.markdown("### ⚠️ 추가 확인이 필요한 재무 데이터")
                st.markdown("현재 주석 텍스트만으로는 완벽한 리스크 계산이 불가능합니다. DART에서 아래 숫자를 찾아 **[3. AI 추가 정밀진단]** 칸에 넣고 다시 돌려주세요.")
                st.warning("1. **[파생상품부채]**: 환율 약정에 대한 헷지 여부 파악 목적\n2. **[종속기업투자주식 손상차손]**: 특관자 대여금 부실화 파악 목적")
                
            with tab3:
                st.markdown("### 🛡️ 기업의 방어 수단 검증")
                st.success("기업이 환리스크나 소송에 대비해 [통화선도 계약]이나 [보상보험]에 가입했는지 여부를 파악합니다. 만약 관련 주석이 없다면 완전 무방비 상태일 수 있습니다.")
                
            with tab4:
                st.markdown("### 🚨 일반 투자자용 3대 주의사항")
                st.error("""
                1. **(쉬운 비유 1)**: 회사가 대신 갚아주기로 한 남의 빚이 회사 전 재산의 절반입니다.
                2. **(쉬운 비유 2)**: 계열사끼리 물건을 사고팔면서 덩치만 키웠지, 진짜 외부에서 벌어온 돈은 적습니다.
                3. **(쉬운 비유 3)**: 당장 내일 은행이 대출 연장을 안 해주면, 금고에 있는 현금으로 절대 못 막습니다.
                """)
