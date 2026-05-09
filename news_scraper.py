import feedparser
import urllib.parse

def get_ai_news():
    """
    구글 뉴스 RSS에서 AI 관련 최신 뉴스 5개 수집
    """
    query = urllib.parse.quote("인공지능 AI")
    # RSS URL for Google News
    rss_url = f"https://news.google.com/rss/search?q={query}&hl=ko&gl=KR&ceid=KR:ko"
    
    try:
        feed = feedparser.parse(rss_url)
        news_items = []
        
        # 상위 5개 항목만 추출
        for entry in feed.entries[:5]:
            news_items.append({
                'title': entry.title,
                'link': entry.link,
                'published': entry.published
            })
            
        return news_items
    except Exception as e:
        print(f"News scraper error: {e}")
        return []

def get_ai_trends():
    """
    구글 뉴스 RSS에서 인공지능 트렌드/전망 관련 뉴스 수집
    """
    query = urllib.parse.quote("인공지능 트렌드 전망 미래")
    rss_url = f"https://news.google.com/rss/search?q={query}&hl=ko&gl=KR&ceid=KR:ko"
    
    try:
        feed = feedparser.parse(rss_url)
        trend_items = []
        
        # 상위 3개 항목만 추출 (요약용)
        for entry in feed.entries[:3]:
            trend_items.append({
                'title': entry.title,
                'link': entry.link,
                'summary': entry.summary if 'summary' in entry else ""
            })
            
        return trend_items
    except Exception as e:
        print(f"Trend scraper error: {e}")
        return []
