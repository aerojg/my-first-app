import FinanceDataReader as fdr
import ccxt
import requests
import feedparser
import urllib.parse
from datetime import datetime

def get_stock_data():
    """
    국내(KOSPI, KOSDAQ) 및 미국(S&P 500, NASDAQ, DJI) 지수 가져오기
    """
    try:
        # 국내 지수
        kospi = fdr.DataReader('KS11')
        kosdaq = fdr.DataReader('KQ11')
        
        # 미국 지수
        sp500 = fdr.DataReader('US500')
        nasdaq = fdr.DataReader('IXIC')
        dji = fdr.DataReader('DJI')
        
        def process_index(df):
            if df.empty: return None
            current = df.iloc[-1]['Close']
            prev = df.iloc[-2]['Close']
            change = current - prev
            change_pct = (change / prev) * 100
            return {
                'current': current,
                'change': change,
                'change_pct': change_pct
            }
        
        return {
            'KR': {
                'KOSPI': process_index(kospi),
                'KOSDAQ': process_index(kosdaq)
            },
            'US': {
                'S&P 500': process_index(sp500),
                'NASDAQ': process_index(nasdaq),
                'Dow Jones': process_index(dji)
            }
        }
    except Exception as e:
        print(f"Stock data error: {e}")
        return None

def get_crypto_data():
    """
    바이낸스 BTC/USDT, 빗썸 BTC/KRW 시세 및 김치 프리미엄 계산
    """
    try:
        # Exchange rate for Kimchi Premium calculation
        usd_krw_df = fdr.DataReader('USD/KRW')
        exchange_rate = usd_krw_df.iloc[-1]['Close'] if not usd_krw_df.empty else 1400.0
        
        binance = ccxt.binance()
        bithumb = ccxt.bithumb()
        
        binance_ticker = binance.fetch_ticker('BTC/USDT')
        bithumb_ticker = bithumb.fetch_ticker('BTC/KRW')
        
        binance_price_usd = binance_ticker['last']
        bithumb_price_krw = bithumb_ticker['last']
        
        # Binance price in KRW
        binance_price_krw = binance_price_usd * exchange_rate
        
        # Kimchi Premium (%)
        kimchi_premium = ((bithumb_price_krw - binance_price_krw) / binance_price_krw) * 100
        
        return {
            'binance_usd': binance_price_usd,
            'bithumb_krw': bithumb_price_krw,
            'exchange_rate': exchange_rate,
            'kimchi_premium': kimchi_premium
        }
    except Exception as e:
        print(f"Crypto data error: {e}")
        return None

def get_weather_data():
    """
    하남시, 충주시 날씨 정보 (최고/최저 온도, 강수 확률)
    """
    locations = {
        '하남시': {'lat': 37.5385, 'lon': 127.2161},
        '충주시': {'lat': 36.9912, 'lon': 127.9261}
    }
    
    weather_results = {}
    
    try:
        for name, coords in locations.items():
            url = f"https://api.open-meteo.com/v1/forecast?latitude={coords['lat']}&longitude={coords['lon']}&daily=temperature_2m_max,temperature_2m_min,precipitation_probability_max&timezone=Asia%2FSeoul&forecast_days=1"
            response = requests.get(url)
            data = response.json()
            
            if 'daily' in data:
                weather_results[name] = {
                    'max_temp': data['daily']['temperature_2m_max'][0],
                    'min_temp': data['daily']['temperature_2m_min'][0],
                    'precip_prob': data['daily']['precipitation_probability_max'][0]
                }
        return weather_results
    except Exception as e:
        print(f"Weather data error: {e}")
        return None

def get_trending_keywords():
    """
    한국 실시간 인기 검색어 5개와 관련 상세 설명 가져오기
    """
    try:
        # 1. 키워드 가져오기 (Signal.bz)
        url = "https://api.signal.bz/news/realtime"
        response = requests.get(url, timeout=5)
        data = response.json()
        
        trending = []
        if 'top10' in data:
            # 상위 5개만 처리
            for item in data['top10'][:5]:
                keyword = item['keyword']
                
                # 2. 각 키워드별 상세 설명 검색 (Google News RSS)
                description = "관련 소식을 가져오는 중입니다."
                try:
                    safe_keyword = urllib.parse.quote(keyword)
                    rss_url = f"https://news.google.com/rss/search?q={safe_keyword}&hl=ko&gl=KR&ceid=KR:ko"
                    feed = feedparser.parse(rss_url)
                    if feed.entries:
                        # 첫 번째 뉴스의 제목이나 요약을 설명으로 사용
                        description = feed.entries[0].title
                        # 제목에서 매체 이름 제거 (보통 ' - 매체명' 형식)
                        if ' - ' in description:
                            description = description.rsplit(' - ', 1)[0]
                except:
                    pass
                
                trending.append({
                    'rank': item['rank'],
                    'keyword': keyword,
                    'description': description
                })
        return trending
    except Exception as e:
        print(f"Trending keywords error: {e}")
        return []
