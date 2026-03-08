###################################################################################
### ai 뉴스 데이터 전처리 ###
# 원본 데이터 생성
# 공백 제거: news_title 양옆에 붙은 불필요한 공백을 제거
# 중복 제거: 제목 공백 제거 후 발생한 동일한 행들을 하나만 남기기
# 결측치 채우기: author_name이 비어있으면 '익명'으로 채우기
# 불량 데이터 삭제: news_title 자체가 비어있는 데이터는 분석 가치가 없으므로 삭제
# 타입 변환: view_count의 '비공개' 등 글자를 0으로 바꾸고 정수형으로 변환
# 날짜 표준화: reg_date를 Pandas가 인식할 수 있는 날짜 타입으로 변경
# 안전하게 저장: 인덱스를 제외하고, 엑셀에서도 한글이 안 깨지는 인코딩으로 저장
###################################################################################

import pandas as pd
import numpy as np

# 원본 데이터 생성
df = pd.DataFrame({
    'news_title': [' AI 기초 ', 'AI 기초', '데이터 과학', None],
    'view_count': ['150', '150', '비공개', '30'],
    'author_name': ['James', 'James', np.nan, 'Unknown'],
    'reg_date': ['2026-03-01', '2026-03-01', '2026-03-05', '2026-03-07']
})

# 공백 제거
df['news_title'] = df['news_title'].str.strip()
# 중복 제거
df = df.drop_duplicates()
# 결측치 채우기
df['author_name'] = df['author_name'].fillna('익명')
# 불량 데이터 삭제
df = df.dropna(subset=['news_title'])
# 타입 변환
df['view_count'] = pd.to_numeric(df['view_count'], errors='coerce')
df['view_count'] = df['view_count'].fillna(0).astype(int)
# 날짜 표준화
df['reg_date'] = pd.to_datetime(df['reg_date'])
# 안전하게 저장
df.to_csv('cleaned_report.csv', index=False, encoding='utf-8-sig')

print(df.info())
print(df.head(3))