import streamlit as st
import pandas as pd
import numpy as np
import os
from sklearn.linear_model import LinearRegression

# 1. 파일 경로 설정
current_folder = os.path.dirname(__file__)
csv_path = os.path.join(current_folder, "past_quotes.csv")

if os.path.exists(csv_path):
    df = pd.read_csv(csv_path, encoding='cp949') # 혹은 utf-8-sig
    
    # 2. AI 학습 (과목 추가: 자재등급, 확장여부)
    X = df[['평수', '방개수', '자재등급', '확장여부']]
    y = df['공사비']
    model = LinearRegression().fit(X, y)
    
    # --- 웹 화면 꾸미기 ---
    st.title("💎 프리미엄 AI 인테리어 견적기")
    st.sidebar.header("📋 세부 현장 정보")
    
    size = st.sidebar.slider("평수", 5, 100, 25)
    rooms = st.sidebar.selectbox("방 개수", [1, 2, 3, 4, 5])
    
    # 추가된 항목들
    grade_name = st.sidebar.radio("자재 등급", ["일반", "중급", "고급"])
    # 글자를 숫자로 변환 (일반=1, 중급=2, 고급=3)
    grade_map = {"일반": 1, "중급": 2, "고급": 3}
    grade = grade_map[grade_name]
    
    ext_name = st.sidebar.checkbox("베란다 확장 여부")
    # 체크박스(True/False)를 숫자(1/0)로 변환
    is_ext = 1 if ext_name else 0
    
    if st.button("정밀 견적 산출하기"):
        # 4개의 정보를 모두 넣어서 예측!
        pred = model.predict([[size, rooms, grade, is_ext]])
        st.success(f"현장 조건을 분석한 결과, 예상 견적은 **{pred[0]:.0f}만원**입니다!")
        st.info(f"💡 분석 정보: {grade_name} 자재 / {'확장형' if is_ext else '비확장형'}")

else:
    st.error("엑셀 파일을 먼저 확인해 주세요!")
    # 가중치 확인용 코드 (모델 학습 코드 아래에 넣어보세요)
# 평수, 방개수, 자재등급, 확장여부 순서대로 중요도가 출력됩니다.
st.write("📈 AI가 분석한 항목별 영향력:", model.coef_)