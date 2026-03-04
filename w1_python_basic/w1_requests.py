##############################################################
### 날씨 데이터 수집 및 로컬 저장 ###
# 날씨 API(Open-Meteo)에서 서울의 현재 날씨 데이터를 가져온다.

# Extract: requests를 이용해 JSON 데이터를 get
# Transform: 전체 데이터 중 현재 온도와 시간만 추출
# Load: 추출한 데이터를 pathlib을 사용하여 weather_data/seoul_weather.json 파일로 저장
##############################################################

import requests
import json
import logging
from pathlib import Path

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# 날씨 데이터 가져오기 & 저장
def fetch_and_save_weather():
    # 서울 날씨 API 주소
    url = "https://api.open-meteo.com/v1/forecast?latitude=37.5665&longitude=126.9780&current_weather=true"
    
    # 저장할 폴더(weather_data)
    output_dir = Path("weather_data")
    output_dir.mkdir(exist_ok=True)
    save_path = output_dir / "seoul_weather.json"
    
    try:
        logging.info("프로그램 시작")
        
        # 데이터 요청
        response = requests.get(url)
        # http 상태 코드가 성공인지 확인
        response.raise_for_status()
        # json 데이터를 딕셔너리로 변환
        data = response.json()
        
        # 현재 온도, 시간 추출
        current_weather = data.get("current_weather")
        weather_info = {
            "time": current_weather.get("time"),
            "temperature": current_weather.get("temperature")
        }
        
        # 파일로 저장
        with save_path.open("w", encoding="utf-8") as f:
            json.dump(weather_info, f, indent=4)
        logging.info("날씨 정보 파일 저장 성공")
    
    except requests.exceptions.HTTPError as e:
        logging.error(f"HTTP 오류: {e}")
    except Exception as e:
        logging.error(f"기타 오류 발생: {e}")
    finally:
        logging.info("프로그램 종료")
        
# 실행
if __name__=="__main__":
    fetch_and_save_weather()