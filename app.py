import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 페이지 설정
st.set_page_config(page_title="Sales Dashboard", layout="wide")
st.title("📊 Sales Dashboard")

# 2. 데이터 불러오기 및 전처리
@st.cache_data
def load_data():
    # 같은 폴더의 Sales.xlsx 파일 내 supermarket_sales_test 시트를 불러옵니다.
    df = pd.read_excel("Sales.xlsx", sheet_name="supermarket_sales_test")
    # 결측치 제거
    df = df.dropna()
    return df

try:
    df = load_data()

    # 3. 사이드바 - 지점(Branch) 선택
    st.sidebar.header("필터 설정")
    branches = sorted(df["Branch"].unique())
    selected_branch = st.sidebar.selectbox("지점(Branch)을 선택하세요:", branches)

    # 선택된 지점으로 데이터 필터링
    filtered_df = df[df["Branch"] == selected_branch]

    # 4. KPI Metrics 표시
    total_sales = filtered_df["Total"].sum()
    avg_sales = filtered_df["Total"].mean()
    avg_rating = filtered_df["Rating"].mean()

    st.subheader(f"📍 {selected_branch} 지점 주요 요약")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(label="총 매출 (Total Sales)", value=f"${total_sales:,.2f}")
    with col2:
        st.metric(label="평균 매출 (Average Sales)", value=f"${avg_sales:,.2f}")
    with col3:
        st.metric(label="평균 평점 (Average Rating)", value=f"{avg_rating:.2f} / 10")

    st.markdown("---")

    # 5. 상품 카테고리별 평균 매출 막대그래프
    st.subheader("🛍️ 상품 카테고리(Product line)별 평균 매출")
    
    # 카테고리별 평균 매출 계산
    category_sales = (
        filtered_df.groupby("Product line")["Total"]
        .mean()
        .reset_index()
        .sort_values(by="Total", ascending=False)
    )

    # Plotly를 이용한 막대그래프 시각화
    fig = px.bar(
        category_sales,
        x="Product line",
        y="Total",
        labels={"Total": "평균 매출 ($)", "Product line": "상품 카테고리"},
        text_auto=".2s",
        color="Total",
        color_continuous_scale="Viridis"
    )
    
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"데이터를 불러오는 중 오류가 발생했습니다. 'Sales.xlsx' 파일과 시트명을 확인해 주세요.\n오류 내용: {e}")
