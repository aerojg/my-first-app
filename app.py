import streamlit as st
from data_fetcher import get_stock_data, get_crypto_data, get_weather_data, get_trending_keywords
from news_scraper import get_ai_news, get_ai_trends
import pandas as pd

# 페이지 설정
st.set_page_config(page_title="비트와 가든, 굿모닝 리포트", layout="wide")

# 커스텀 CSS (프리미엄 및 고대비 디자인)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700;900&family=Outfit:wght@700;900&display=swap');
    
    body {
        font-family: 'Noto Sans KR', sans-serif;
    }
    
    /* Global Typography & High Contrast */
    h1, h2, h3, h4, h5, h6, span, p, label, .stMetric div {
        color: #1a1a1a !important;
    }
    
    .stApp {
        background-color: #f4f7f4;
    }
    
    .title-text {
        font-family: 'Outfit', sans-serif;
        color: #1b5e20 !important;
        font-weight: 900;
        text-align: center;
        padding: 15px 0 5px 0;
        font-size: 3rem;
        letter-spacing: -2.5px;
        white-space: nowrap;
    }
    
    /* Dashboard Headers */
    .section-header {
        font-size: 1.5rem !important;
        font-weight: 800 !important;
        color: #2e7d32 !important;
        margin-bottom: 10px !important;
        margin-top: 5px !important;
        border-left: 5px solid #2e7d32;
        padding-left: 10px;
    }
    
    /* Card Styles */
    .stCard, [data-testid="stVerticalBlock"] > div:has(div.stMetric) {
        background-color: #ffffff !important;
        padding: 18px !important;
        border-radius: 16px !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.06) !important;
        border: 1px solid #e0e0e0 !important;
        margin-bottom: 15px !important;
    }
    
    /* Metric Styling */
    [data-testid="stMetricLabel"] {
        font-size: 1.05rem !important;
        font-weight: 600 !important;
        color: #444 !important;
    }
    [data-testid="stMetricValue"] {
        font-size: 1.7rem !important;
        font-weight: 900 !important;
        color: #000 !important;
        letter-spacing: -0.5px;
    }
    
    /* Trending Card (실시간 잇슈) */
    .trending-card {
        background-color: #fffaf0 !important;
        border-top: 6px solid #fb8c00 !important;
        padding: 15px !important;
        border-radius: 16px !important;
        border: 1px solid #ffe0b2 !important;
        margin-bottom: 15px !important;
    }
    .trending-item {
        display: flex;
        align-items: center;
        margin-bottom: 4px;
    }
    .rank-num {
        font-weight: 900;
        color: #ef6c00;
        width: 25px;
        font-size: 1.1rem;
    }
    .keyword-text {
        font-weight: 800;
        color: #222;
        font-size: 1.1rem;
    }
    .trending-desc {
        padding-left: 25px;
        color: #555;
        font-size: 0.92rem;
        line-height: 1.25;
        margin-bottom: 10px;
    }
    
    /* News & Trends (Left Column) */
    .news-box {
        background-color: #ffffff;
        padding: 18px;
        border-radius: 16px;
        border: 1px solid #e0e0e0;
        border-top: 6px solid #1976d2;
        margin-bottom: 15px;
    }
    .trend-box {
        background-color: #e3f2fd;
        padding: 18px;
        border-radius: 16px;
        border: 1px solid #bbdefb;
        border-left: 6px solid #0d47a1;
        margin-bottom: 15px;
    }
    .news-title {
        font-size: 1.15rem !important;
        font-weight: 700 !important;
        color: #111 !important;
        margin-bottom: 6px;
        line-height: 1.3;
    }
    .news-link {
        color: #1976d2 !important;
        text-decoration: none;
        font-weight: 700;
        font-size: 0.9rem;
    }
    
    /* Weather Card */
    .weather-box {
        background-color: #ffffff;
        padding: 18px;
        border-radius: 16px;
        border: 1px solid #e0e0e0;
        border-top: 6px solid #388e3c;
        margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 class='title-text'>🌿 비트와 가든, 굿모닝 리포트 ☀️</h1>", unsafe_allow_html=True)

# 자료검색 시점 표시 (상단)
now = pd.Timestamp.now()
days = ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일']
day_of_week = days[now.weekday()]
search_time = now.strftime('%y.%m.%d %H:%M') + f" {day_of_week}"

st.markdown(f"""
    <div style="text-align: center; color: #444; margin-top: -20px; margin-bottom: 30px; font-size: 1.1rem; font-weight: 500;">
        자료검색 시점: {search_time}
    </div>
""", unsafe_allow_html=True)

# 데이터 로딩
with st.spinner('데이터를 가져오는 중...'):
    stock_data = get_stock_data()
    crypto_data = get_crypto_data()
    weather_data = get_weather_data()
    ai_news = get_ai_news()
    ai_trends = get_ai_trends()
    trending_keywords = get_trending_keywords()

col1, col2 = st.columns(2)

# 왼쪽 컬럼: 날씨 및 AI 최신 뉴스
with col1:
    st.markdown('<div class="section-header">🌦️ 오늘의 날씨</div>', unsafe_allow_html=True)
    if weather_data:
        w_cols = st.columns(len(weather_data))
        for i, (loc, data) in enumerate(weather_data.items()):
            with w_cols[i]:
                st.markdown(f"""
                <div class="weather-box">
                    <h3 style="margin-top:0; color:#1b5e20; font-size:1.3rem;">{loc}</h3>
                    <p style="font-size:1.05rem; margin-bottom:5px;">🌡️ <b>최고:</b> <span style="color:#d32f2f;">{data['max_temp']}°C</span></p>
                    <p style="font-size:1.05rem; margin-bottom:5px;">❄️ <b>최저:</b> <span style="color:#1976d2;">{data['min_temp']}°C</span></p>
                    <p style="font-size:1.05rem; margin-bottom:0;">💧 <b>강수:</b> {data['precip_prob']}%</p>
                </div>
                """, unsafe_allow_html=True)
    
    # 인공지능 동향 (거시적 관점)
    st.markdown('<div class="section-header">🌐 인공지능 동향</div>', unsafe_allow_html=True)
    if ai_trends:
        st.markdown('<div class="trend-box">', unsafe_allow_html=True)
        st.markdown("<div style='font-weight:700; color:#0d47a1; margin-bottom:10px; font-size:1.1rem;'>📍 최근 AI 산업의 거시적 변화와 전망</div>", unsafe_allow_html=True)
        for trend in ai_trends:
            st.markdown(f"""
                <div style="margin-bottom:10px; padding-left:10px; border-left:3px solid #1976d2;">
                    <div class="news-title" style="font-size:1.05rem;">{trend['title']}</div>
                    <a href="{trend['link']}" class="news-link" target="_blank">자세히 보기 ➔</a>
                </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # 인공지능 주요뉴스
    st.markdown('<div class="section-header">📰 인공지능 주요뉴스</div>', unsafe_allow_html=True)
    if ai_news:
        st.markdown('<div class="news-box">', unsafe_allow_html=True)
        for news in ai_news:
            st.markdown(f"""
                <div style="margin-bottom:12px; border-bottom:1px solid #eee; padding-bottom:8px;">
                    <div class="news-title">{news['title']}</div>
                    <a href="{news['link']}" class="news-link" target="_blank">기사 읽기 ➔</a>
                </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# 오른쪽 컬럼: 인기 검색어, 미국/국내 증시, 비트코인 비교
with col2:
    # 실시간 잇슈 (상단 배치)
    st.markdown('<div class="section-header">🔥 실시간 잇슈</div>', unsafe_allow_html=True)
    if trending_keywords:
        st.markdown('<div class="trending-card">', unsafe_allow_html=True)
        for i, item in enumerate(trending_keywords[:5]):
            st.markdown(f"""
                <div style="margin-bottom: 6px;">
                    <div class="trending-item">
                        <span class="rank-num">{item['rank']}</span>
                        <span class="keyword-text">{item['keyword']}</span>
                    </div>
                    <div class="trending-desc">
                        {item['description']}
                    </div>
                </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.write("실시간 이슈 정보를 불러올 수 없습니다.")

    # 증시 현황
    st.markdown('<div class="section-header">📈 글로벌 증시 현황</div>', unsafe_allow_html=True)
    if stock_data:
        # 미국 & 국내 증시를 같은 공간에 효율적으로 배치
        if 'US' in stock_data:
            u_cols = st.columns(3)
            with u_cols[0]: st.metric("S&P 500", f"{stock_data['US']['S&P 500']['current']:,.2f}", f"{stock_data['US']['S&P 500']['change_pct']:+.2f}%")
            with u_cols[1]: st.metric("NASDAQ", f"{stock_data['US']['NASDAQ']['current']:,.2f}", f"{stock_data['US']['NASDAQ']['change_pct']:+.2f}%")
            with u_cols[2]: st.metric("Dow Jones", f"{stock_data['US']['Dow Jones']['current']:,.2f}", f"{stock_data['US']['Dow Jones']['change_pct']:+.2f}%")
        
        if 'KR' in stock_data:
            k_cols = st.columns(3)
            with k_cols[0]: st.metric("KOSPI", f"{stock_data['KR']['KOSPI']['current']:,.2f}", f"{stock_data['KR']['KOSPI']['change_pct']:+.2f}%")
            with k_cols[1]: st.metric("KOSDAQ", f"{stock_data['KR']['KOSDAQ']['current']:,.2f}", f"{stock_data['KR']['KOSDAQ']['change_pct']:+.2f}%")

    # 가상화폐
    st.markdown('<div class="section-header">₿ Bitcoin & Premium</div>', unsafe_allow_html=True)
    if crypto_data:
        st.markdown('<div class="stCard" style="padding:15px !important; margin-bottom:0 !important;">', unsafe_allow_html=True)
        c_cols = st.columns(2)
        with c_cols[0]:
            st.metric("Binance (USD)", f"{crypto_data['binance_usd']:,.2f}")
        with c_cols[1]:
            st.metric("Bithumb (KRW)", f"{crypto_data['bithumb_krw']:,.0f}")
        
        kp = crypto_data['kimchi_premium']
        kp_color = "#d32f2f" if kp > 0 else "#1976d2"
        st.markdown(f"""
            <div style="text-align: center; margin-top: 8px; padding: 12px; background: #f1f8e9; border-radius: 12px; border: 1.5px solid #c8e6c9;">
                <div style="font-size: 1.1rem; font-weight: 700; color: #333;">Kimchi Premium: <span style="color: {kp_color}; font-size: 1.4rem; font-weight: 900;">{kp:+.2f}%</span></div>
                <div style="font-size: 0.85rem; color: #666; margin-top: 2px;">환율: 1 USD = {crypto_data['exchange_rate']:,.2f} KRW</div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# 하단 공백
st.markdown("<div style='margin-bottom: 50px;'></div>", unsafe_allow_html=True)
