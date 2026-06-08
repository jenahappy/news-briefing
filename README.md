# 📰 원주시 새소식 브리핑

원주시 홈페이지의 새소식을 매일 오전 8시에 자동으로 수집하여 정리하는 페이지입니다.

🔗 **라이브 페이지**: `https://jenahappy.github.io/news-briefing/`

## 동작 방식

```
매일 08:00 KST
    ↓
GitHub Actions 실행
    ↓
crawl.py → 원주시 새소식 10개 수집 → data/news.json 저장
    ↓
build.py → news.json 읽어 index.html 생성
    ↓
git commit & push → GitHub Pages 자동 배포
```

## 파일 구조

```
news-briefing/
├── .github/
│   └── workflows/
│       └── daily-news.yml   # 스케줄 자동화
├── data/
│   └── news.json            # 수집된 뉴스 데이터
├── crawl.py                 # 크롤러
├── build.py                 # HTML 빌더
├── index.html               # 결과 페이지 (자동 생성)
└── README.md
```

## GitHub Pages 설정

1. 저장소 → Settings → Pages
2. Source: `Deploy from a branch`
3. Branch: `main` / `/(root)`
4. Save

## 수동 실행

Actions 탭 → `원주시 새소식 업데이트` → `Run workflow`
