# ######################################################################
# 에러 로그 추출기
# logs 폴더 내에 수십 개의 .txt 파일이 있다. 이 파일 안에서 "ERROR"이 포함된 줄을 출력하라.
#
# 목표
# - pathlib을 사용해 특정 폴더 내의 모든 .txt 찾기
# - Generator를 사용하여 파일을 한 줄씩 읽으며 "ERROR"가 포함된 줄만 yield 하기 <-메모리 낭비 방지
# ######################################################################

from pathlib import Path

# 환경 설정: 실습을 위해 가짜 로그 폴더와 파일 생성
def setup_logs():
    log_dir = Path("data_logs")
    log_dir.mkdir(exist_ok=True)
    
    # 임의 텍스트 파일 3개 생성
    for i in range(3):
        file_path = log_dir / f"log_{i}.txt"
        with file_path.open("w", encoding="utf-8") as f:
            f.write(f"INFO: 시스템 가동 중... {i}\n")
            f.write(f"ERROR: 크리티컬 에러 발생! 코드: {i*100}\n")
            f.write(f"DEBUG: 데이터 정합성 체크 완료 {i}\n")
    print(f"{log_dir} 폴더에 실습용 로그 파일 생성이 완료되었습니다.\n")
    return log_dir

# 에러 로그만 한 줄씩 뽑아주는 generator 생성
def error_log_generator(directory_path):
    p = Path(directory_path)
    
    for file_path in p.glob("*.txt"):
        with file_path.open("r", encoding="utf-8") as f:
            # line 안에 "ERROR" 발견 시 yield를 사용해 반환
            yield from (line.strip() for line in f if "ERROR" in line)

# 실행
if __name__ == "__main__":
    # 환경 구축
    log_folder = setup_logs()
    
    # 제너레이터 생성
    errors = error_log_generator(log_folder)
    
    print("--- 로그 분석 시작 ---")
    # 제너레이터는 반복문(for)에 넣었을 때 비로소 하나씩 값을 꺼내옵니다.
    for error in errors:
        print(f"발견된 에러: {error.strip()}")


