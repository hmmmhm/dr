import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# 1. API 키 설정
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

# 2. 시스템 프롬프트 (초기 역할 설정)
system_prompt = """
너는 전문 의료 챗봇이야. 사용자의 증상을 듣고, MSD 매뉴얼 기반의 의학 정보를 바탕으로 아래 기준에 따라 대답해.

1. 확정 진단 대신 가능한 질환만 제시하고, "추정", "가능성 있음" 등의 표현 사용
2. 추가 정보 수집을 위해 반드시 3~5개의 질문을 할 것 (나이, 증상 기간, 통증 강도 등)
3. 응급하거나 위험할 가능성이 있으면 병원 방문을 강력히 권장할 것
4. MSD 매뉴얼 이외의 출처는 사용하지 말 것

대답할 때는 다음 형식으로 해줘:
- **가능성 있는 질환 간략히 언급**
- **추가 질문 제시**
- **병원 방문 필요 여부에 대한 조언**
"""

# 3. 세션 초기화 (chat 세션과 메시지 이력)
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[
        {"role": "user", "parts": [system_prompt]}
    ])
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. 기존 대화 출력
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 5. 사용자 입력 처리
if user_input := st.chat_input("증상을 입력해 주세요 (예: 기침이 심하고 열이 나요)"):
    # 사용자 메시지 표시
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Gemini 응답 요청 (멀티턴)
    response = st.session_state.chat.send_message(user_input)
    assistant_reply = response.text

    # 응답 저장 및 표시
    st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
    with st.chat_message("assistant"):
        st.markdown(assistant_reply)
