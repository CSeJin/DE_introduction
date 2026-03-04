##############################################################################################
### AI 테크 뉴스 ETL 파이프라인 구축 ###

## 요구사항 ##

# [환경 및 경로] pathlib 활용
# - 프로젝트 루트 폴더에 ai_news_results라는 폴더를 자동으로 생성
# - 결과 파일은 해당 폴더 안에 final_ai_report.json으로 저장

# [로그 기록] logging 활용
# - 로그 등급은 INFO 이상으로 설정(버전 이슈 방지를 위해 encoding 인자는 제외 권장)
# - 최소 3개 지점(수집 시작, 키워드 매칭 발견, 저장 완료)에서 로그를 남기기

# [데이터 수집] requests 활용
# - API 주소: https://hn.algolia.com/api/v1/search?query=AI (Hacker News의 AI 검색 결과 API)
# - 네트워크 에러나 HTTP 에러(404, 500 등) 발생 시 프로그램이 멈추지 않도록 예외 처리

# [데이터 변환] Generator & JSON
# 전체 뉴스 목록 중 제목(title)에 "AI" 또는 "Artificial Intelligence"가 포함된 기사만 필터링하는 제너레이터 함수 생성
# .get() 메서드를 사용하여 제목이나 URL 데이터가 없는 경우에 대비

# [데이터 적재] json.dump
# 필터링된 결과를 indent=4으로 가독성 있게 저장
##############################################################################################

import requests
import json
import logging
from pathlib import Path


# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s: %(message)s'
)

# 웹 API에서 데이터 수집하는 함수
def extract_news():
    url = f"https://hn.algolia.com/api/v1/search?query=AI"
    try:
        response = requests.get(url, timeout=5)
        
        # 성공 확인
        response.raise_for_status()
        
        # json으로 반환
        return(response.json())
    except requests.exceptions.HTTPError as e:
        logging.error(f"http 오류 발생, 요청 코드: {response.status_code}, {e}")
        return([])
    except Exception as e:
        logging.error(f"데이터 수집 중 기타 오류 발생: {e}")
        return([])


# AI 기사 필터링 제너레이터 함수 생성
def transform_news(news_data):
    news_list = news_data.get("hits", [])
    # 제목에 포함될 내용 배열 선언
    keywords = ['AI', 'Artificial Intelligence']
    try:
        for article in news_list:
            title = article.get("title")
            url = article.get("url", "주소 없음")
            author = article.get("author", "unknown")
            
            # 제목 없는 기사는 건너뛰기
            if not title: pass
            
            if any(kw.lower() in title.lower() for kw in keywords):
                yield {
                    "title": title[:30] + "...",
                    "url": url,
                    "author": author
                }
    except Exception as e:
        logging.error(f"제목 필터링 중 오류 발생: {e}")
    
    logging.info("뉴스 필터링 성공")
        

# 필터링한 뉴스를 파일로 저장
def load_news(filtered_data):
    output_dir = Path("ai_new_results")
    output_dir.mkdir(exist_ok=True)
    save_path = output_dir / 'final_ai_report.json'
    
    final_data = list(filtered_data)
    try:
        with save_path.open("w", encoding='utf-8') as f:
            json.dump(final_data, f, indent=4, ensure_ascii=False)
        
        logging.info("파일 저장 성공")
        logging.info(f"총 {len(final_data)}개의 관련 뉴스를 찾았습니다.")
    except Exception as e:
        logging.error(f"파일 저장 중 오류 발생: {e}")


# 실행
if __name__=="__main__":
    logging.info("AI 관련 뉴스 수집 프로그램 시작")
    
    # Extract
    raw_news = extract_news()
    # print(type(raw_news))
    if raw_news:
        # Transform
        filtered_news_list = transform_news(raw_news)
        # Load
        load_news(filtered_news_list)