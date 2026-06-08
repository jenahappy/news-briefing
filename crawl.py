#!/usr/bin/env python3
"""
원주시 새소식 크롤러
매일 오전 8시 GitHub Actions 실행
"""

import json
import os
import re
from datetime import datetime, timezone, timedelta
import urllib.request
from html.parser import HTMLParser

URL = "https://www.wonju.go.kr/www/selectBbsNttList.do?bbsNo=1&key=211&"
OUTPUT_FILE = "data/news.json"
MAX_ITEMS = 10

KST = timezone(timedelta(hours=9))


class WonjuNewsParser(HTMLParser):
    """원주시 전자정부 프레임워크 게시판 파서"""

    def __init__(self):
        super().__init__()
        self.items = []
        self.current = {}
        self.in_td = False
        self.in_subject = False
        self.in_link = False
        self.capture_text = False
        self.td_count = 0
        self.in_tbody = False
        self.link_href = ""
        self.buffer = ""

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        cls = attrs_dict.get("class", "")
        href = attrs_dict.get("href", "")

        if tag == "tbody":
            self.in_tbody = True

        if self.in_tbody and tag == "tr":
            self.current = {}
            self.td_count = 0

        if self.in_tbody and tag == "td":
            self.in_td = True
            self.td_count += 1
            self.buffer = ""

        # 제목 링크 감지: subject/title 클래스 또는 nttSj 패턴
        if tag == "a" and self.in_td:
            if any(k in cls for k in ["subject", "title", "nttSj"]) or (
                "selectBbsNttView" in href or "nttNo" in href
            ):
                self.in_link = True
                self.link_href = href
                self.buffer = ""

        # td 내부 a 태그에서 제목 찾기 (클래스 없는 경우)
        if tag == "a" and self.in_td and self.td_count == 2:
            self.in_link = True
            self.link_href = href
            self.buffer = ""

    def handle_data(self, data):
        text = data.strip()
        if not text:
            return
        if self.in_link:
            self.buffer += text
        elif self.in_td and self.td_count == 1 and not self.current.get("num"):
            if text.isdigit():
                self.current["num"] = text

    def handle_endtag(self, tag):
        if tag == "a" and self.in_link:
            self.in_link = False
            title = self.buffer.strip()
            # 불필요한 공백/개행 정리
            title = re.sub(r"\s+", " ", title)
            if title and len(title) > 2:
                self.current["title"] = title
                if self.link_href:
                    base = "https://www.wonju.go.kr"
                    href = self.link_href
                    if href.startswith("/"):
                        self.current["link"] = base + href
                    elif href.startswith("http"):
                        self.current["link"] = href
                    else:
                        self.current["link"] = base + "/" + href
            self.buffer = ""

        if tag == "td":
            self.in_td = False

        if tag == "tr" and self.in_tbody:
            if self.current.get("title"):
                self.items.append(self.current)
            self.current = {}
            self.td_count = 0

        if tag == "tbody":
            self.in_tbody = False


def fetch_news():
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "ko-KR,ko;q=0.9",
        "Referer": "https://www.wonju.go.kr/",
    }

    req = urllib.request.Request(URL, headers=headers)
    with urllib.request.urlopen(req, timeout=15) as resp:
        raw = resp.read()
        # 인코딩 자동 감지
        try:
            html = raw.decode("utf-8")
        except UnicodeDecodeError:
            html = raw.decode("euc-kr", errors="replace")
    return html


def parse_news(html):
    parser = WonjuNewsParser()
    parser.feed(html)
    items = parser.items[:MAX_ITEMS]

    # 제목만 없는 경우 fallback: <a> 전체에서 추출
    if not items:
        # fallback: 정규식으로 게시판 링크+제목 추출
        pattern = re.compile(
            r'<a[^>]+href="([^"]*(?:selectBbsNttView|nttNo)[^"]*)"[^>]*>\s*([^<]{4,80})\s*</a>',
            re.IGNORECASE,
        )
        base = "https://www.wonju.go.kr"
        for i, m in enumerate(pattern.finditer(html)):
            href, title = m.group(1), m.group(2).strip()
            title = re.sub(r"\s+", " ", title)
            if len(title) > 3:
                link = base + href if href.startswith("/") else href
                items.append({"num": str(i + 1), "title": title, "link": link})
            if len(items) >= MAX_ITEMS:
                break

    return items


def save_json(items):
    now = datetime.now(KST)
    data = {
        "updated_at": now.strftime("%Y-%m-%d %H:%M:%S"),
        "updated_date": now.strftime("%Y년 %m월 %d일"),
        "updated_time": now.strftime("%H:%M"),
        "source_url": URL,
        "items": items,
    }
    os.makedirs("data", exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"✅ {len(items)}개 저장 완료 → {OUTPUT_FILE}")
    for i, item in enumerate(items, 1):
        print(f"  {i:2}. {item['title']}")


if __name__ == "__main__":
    print(f"🔍 원주시 새소식 크롤링 시작...")
    html = fetch_news()
    items = parse_news(html)
    if not items:
        print("⚠️ 항목을 찾지 못했습니다. 페이지 구조를 확인하세요.")
        # 빈 데이터라도 저장 (페이지가 유지되도록)
        items = []
    save_json(items)
