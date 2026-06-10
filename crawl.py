import json, urllib.request, xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta

KST = timezone(timedelta(hours=9))

def fetch_news():
    # 원주시 새소식 RSS 피드
    url = "https://www.wonju.go.kr/www/rss.do?key=211"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/rss+xml, application/xml, text/xml, */*",
    }
    
    req = urllib.request.Request(url, headers=headers)
    
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            xml_data = resp.read()
    except Exception as e:
        print(f"❌ RSS 실패: {e}")
        # RSS 실패시 기존 데이터 유지
        try:
            with open("data/news.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    
    root = ET.fromstring(xml_data)
    ns = {"dc": "http://purl.org/dc/elements/1.1/"}
    
    items = []
    for item in root.findall(".//item")[:10]:
        title = item.findtext("title", "").strip()
        link  = item.findtext("link",  "").strip()
        date  = item.findtext("pubDate", "").strip()
        items.append({"title": title, "link": link, "date": date})
    
    return items

def main():
    print("🔍 원주시 새소식 RSS 수집 시작...")
    items = fetch_news()
    
    now_kst = datetime.now(KST).strftime("%Y년 %m월 %d일 %p %I:%M").replace(
        "AM", "오전").replace("PM", "오후")
    
    result = {
        "updated": now_kst,
        "items": items
    }
    
    import os
    os.makedirs("data", exist_ok=True)
    
    with open("data/news.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 완료! {len(items)}건 수집 → data/news.json")
    print(f"   업데이트 시각: {now_kst}")

if __name__ == "__main__":
    main()
