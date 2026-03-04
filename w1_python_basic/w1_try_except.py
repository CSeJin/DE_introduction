####################################################
### 불량 데이터 필터링 파이프라인 ###
# data_files 폴더 안에 여러 텍스트 파일이 있다.
# 각 파일에는 숫자 데이터가 들어있는데, 가끔 숫자가 아닌 글자가 섞여 있거나 0이 포함되어 계산(100 / 숫자)을 방해한다.

## 목표 ##
# 1. pathlib으로 파일을 하나씩 찾기
# 2. Generator를 사용해 파일의 숫자를 하나씩 가져와 100 / 숫자를 계산
# 3. try-except를 사용해 글자가 있는 경우와 0인 경우를 각각 다르게 처리
####################################################

from pathlib import Path

# 환경설정: 파일 생성
def setup_dirty_data():
    data_dir = Path("dirty_data")
    data_dir.mkdir(exist_ok=True)
    
    content = ["10", "20", "0", "abc", "50"]
    file_path = data_dir / "raw_data.txt"
    with file_path.open("w") as f:
        for item in content:
            f.write(f"{item}\n")
    f.close()
    return data_dir

# 예외처리 제너레이터
def safe_calculator_generator(directory):
    p = Path(directory)
    for file in p.glob("**/*.txt"):
        try:
            with file.open("r", encoding="utf-8") as f:
                for line in f:
                    val = line.strip()
                    try:
                        val = int(val)
                        yield 100 / val
                    except ZeroDivisionError:
                        print(f"[Error] 0으로 나눌 수 없습니다: {val}")
                        continue
                    except ValueError:
                        print(f"[Error] 숫자가 아닙니다: {val}")
                        continue
        except FileNotFoundError as e:
            print(e)

if __name__=="__main__":
    data_directory = setup_dirty_data()
    for res in safe_calculator_generator(data_directory):
        print(f"계산 결과: {res}")