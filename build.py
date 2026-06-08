#!/usr/bin/env python3
"""
news.json을 읽어 index.html 생성
"""
import json

with open("data/news.json", encoding="utf-8") as f:
    data = json.load(f)

items = data.get("items", [])
updated_date = data.get("updated_date", "")
updated_time = data.get("updated_time", "")
source_url = data.get("source_url", "")

# 뉴스 아이템 HTML 생성
if items:
    news_html = ""
    for i, item in enumerate(items, 1):
        title = item.get("title", "")
        link = item.get("link", source_url)
        news_html += f"""
        <li class="news-item" style="--i:{i}">
          <span class="num">{i:02d}</span>
          <a href="{link}" target="_blank" rel="noopener">{title}</a>
          <span class="arrow">↗</span>
        </li>"""
else:
    news_html = '<li class="news-item empty"><span class="num">--</span><span>오늘은 새소식이 없습니다</span></li>'

html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>원주시 새소식 브리핑</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@400;700&family=Noto+Sans+KR:wght@300;400;500&display=swap" rel="stylesheet" />
  <style>
    :root {{
      --bg: #0d0f14;
      --surface: #13161e;
      --border: #1e2330;
      --accent: #c8a96e;
      --accent2: #7eb8c9;
      --text: #e8e4dc;
      --muted: #6b7280;
      --hover-bg: #1a1e28;
    }}

    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

    body {{
      background: var(--bg);
      color: var(--text);
      font-family: 'Noto Sans KR', sans-serif;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      align-items: center;
      padding: 0 1rem 4rem;
    }}

    /* 상단 헤더 */
    header {{
      width: 100%;
      max-width: 720px;
      padding: 3.5rem 0 2rem;
      border-bottom: 1px solid var(--border);
      margin-bottom: 2.5rem;
    }}

    .city-label {{
      font-family: 'Noto Sans KR', sans-serif;
      font-weight: 300;
      font-size: 0.72rem;
      letter-spacing: 0.25em;
      color: var(--accent);
      text-transform: uppercase;
      margin-bottom: 0.9rem;
      display: flex;
      align-items: center;
      gap: 0.6rem;
    }}

    .city-label::before {{
      content: '';
      display: inline-block;
      width: 24px;
      height: 1px;
      background: var(--accent);
    }}

    h1 {{
      font-family: 'Noto Serif KR', serif;
      font-size: clamp(1.7rem, 5vw, 2.5rem);
      font-weight: 700;
      line-height: 1.25;
      letter-spacing: -0.02em;
      color: var(--text);
    }}

    h1 em {{
      font-style: normal;
      color: var(--accent);
    }}

    .meta {{
      margin-top: 1.2rem;
      display: flex;
      align-items: center;
      gap: 1.2rem;
      font-size: 0.78rem;
      color: var(--muted);
    }}

    .meta .dot {{
      width: 3px;
      height: 3px;
      border-radius: 50%;
      background: var(--border);
    }}

    .badge {{
      display: inline-flex;
      align-items: center;
      gap: 0.4rem;
      background: rgba(200,169,110,0.12);
      border: 1px solid rgba(200,169,110,0.25);
      color: var(--accent);
      font-size: 0.7rem;
      padding: 0.2rem 0.6rem;
      border-radius: 20px;
      letter-spacing: 0.05em;
    }}

    .badge::before {{
      content: '';
      width: 6px;
      height: 6px;
      border-radius: 50%;
      background: var(--accent);
      animation: pulse 2s infinite;
    }}

    @keyframes pulse {{
      0%, 100% {{ opacity: 1; }}
      50% {{ opacity: 0.3; }}
    }}

    /* 뉴스 리스트 */
    .news-list {{
      width: 100%;
      max-width: 720px;
      list-style: none;
    }}

    .news-item {{
      display: grid;
      grid-template-columns: 2.4rem 1fr 1.2rem;
      align-items: center;
      gap: 1rem;
      padding: 1.15rem 0.5rem;
      border-bottom: 1px solid var(--border);
      opacity: 0;
      transform: translateY(12px);
      animation: fadeUp 0.45s ease forwards;
      animation-delay: calc(var(--i) * 0.055s);
      transition: background 0.2s;
      border-radius: 4px;
    }}

    .news-item:hover {{
      background: var(--hover-bg);
      padding-left: 1rem;
    }}

    @keyframes fadeUp {{
      to {{ opacity: 1; transform: translateY(0); }}
    }}

    .num {{
      font-size: 0.68rem;
      font-weight: 500;
      color: var(--accent);
      font-variant-numeric: tabular-nums;
      letter-spacing: 0.05em;
    }}

    .news-item a {{
      color: var(--text);
      text-decoration: none;
      font-size: 0.93rem;
      line-height: 1.55;
      font-weight: 400;
      transition: color 0.2s;
    }}

    .news-item a:hover {{
      color: var(--accent2);
    }}

    .arrow {{
      font-size: 0.8rem;
      color: var(--border);
      transition: color 0.2s, transform 0.2s;
    }}

    .news-item:hover .arrow {{
      color: var(--accent2);
      transform: translate(2px, -2px);
    }}

    .news-item.empty a, .news-item.empty span:last-child {{
      color: var(--muted);
    }}

    /* 하단 */
    footer {{
      width: 100%;
      max-width: 720px;
      margin-top: 2.5rem;
      padding-top: 1.5rem;
      border-top: 1px solid var(--border);
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 0.8rem;
    }}

    footer a {{
      font-size: 0.75rem;
      color: var(--muted);
      text-decoration: none;
      transition: color 0.2s;
    }}

    footer a:hover {{ color: var(--accent); }}

    .footer-note {{
      font-size: 0.72rem;
      color: var(--muted);
    }}

    /* 장식 선 */
    .deco-line {{
      width: 100%;
      max-width: 720px;
      height: 3px;
      background: linear-gradient(90deg, var(--accent) 0%, var(--accent2) 60%, transparent 100%);
      margin-bottom: 0;
      border-radius: 2px;
    }}
  </style>
</head>
<body>
  <div class="deco-line"></div>
  <header>
    <p class="city-label">Wonju City · Daily Briefing</p>
    <h1>원주시 <em>새소식</em> 브리핑</h1>
    <div class="meta">
      <span>{updated_date}</span>
      <span class="dot"></span>
      <span>오전 {updated_time} 기준</span>
      <span class="dot"></span>
      <span class="badge">자동 업데이트</span>
    </div>
  </header>

  <ul class="news-list">
    {news_html}
  </ul>

  <footer>
    <a href="{source_url}" target="_blank" rel="noopener">🔗 원주시 새소식 원문 보기</a>
    <span class="footer-note">매일 오전 8시 자동 수집 · GitHub Actions</span>
  </footer>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("✅ index.html 생성 완료")
