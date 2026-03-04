import pandas as pd
from pathlib import Path

# 파일 경로 설정
file_path = Path('../w1_python_basic/ai_news_results/final_ai_report.json')

# 데이터 불러오기
if file_path.exists():
	df = pd.read_json(file_path)
	
	# 데이터 살펴보기
	print(df.head(), "\n")
	# 데이터 요약 정보
	print(df.info(), "\n")
 
else:
	print("파일을 찾을 수 없습니다.")
