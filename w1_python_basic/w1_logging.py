########################################################################
### logging 있는 ETL 파이프라인 ###
# raw_data 폴더에 여러 파일이 있다.
# 이 파일들을 읽어 숫자를 2배로 만드는 작업을 수행하며 다음의 로그를 남긴다.

# 1. 작업 시작 시: INFO 로그
# 2. 파일을 찾을 수 없거나 열 수 없을 때: ERROR 로그
# 3. 데이터가 숫자가 아닐 때: WARNING 로그
########################################################################

import logging
from pathlib import Path

# 로깅 설정
logging.basicConfig(
    filename='logging_practice_data_pipeline.log',
    level=logging.INFO, # info 등급 이상의 로그만 기록
    format='%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
    # encoding='utf-8'      # <- 현재 인터프리터가 3.8이라 인식 못함
)

def process_data_generator(data_dir):
    p = Path(data_dir)
    logging.info("데이터 처리 파이프라인 시작.")
    
    for file_path in p.glob('*.txt'):
        try:
            with file_path.open("r", encoding="utf-8") as f:
                for line in f:
                    val = line.strip()  # 전처리
                    try:
                        yield float(val)*2
                    except ValueError:
                        logging.warning(f"[WARNING] 데이터가 숫자가 아닙니다: {val}, 파일: {file_path.name}")
        except Exception as e:
            logging.error(f"[ERROR] 파일 처리 중 오류 발생: {file_path.name} -> {e}")
    logging.info("데이터 처리 완료.")
    
# 실행 테스트
if __name__=="__main__":
    # 테스트용 임시폴더 생성
    test_dir = Path("raw_data")
    test_dir.mkdir(exist_ok=True)
    (test_dir / "sample.txt").write_text("10\n20\nabc\n40\n집", encoding="utf-8")
    
    results = process_data_generator(test_dir)
    for r in results:
        print(f"계산된 값: {r}")
        
    print("\n'logging_practice_data_pipeline.log' 파일과 비교하기")