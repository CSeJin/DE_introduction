######################################################################
### ai 뉴스 리포트 지표 고도화: 분석용 데이터셋 생성 ###
# 조회수 등급(grade) 생성: view_count의 값에 따라 산정
# - 0~100 미만: Bronze
# - 100~200 미만: Silver
# - 200 이상: Gold
# 제목 요약(summary) 생성: 제목이 15자보다 길면 앞의 15자만 남기고 뒤에 "..." 붙이기.
# 요일 정보(day_of_week) 추출: 기사가 작성된 날짜의 요일 이름(예: Monday)을 새 컬럼에 저장
# 긴급 기사(is_urgent) 여부: 제목에 "신기술" 또는 "긴급"이라는 단어가 포함되어 있으면 True, 아니면 False.
######################################################################

import pandas as pd
import numpy as np

# 실습용 cleand data
data = {
    'title': ['AI 신기술 발표', '파이썬 기초 강의', '긴급: 데이터 유출 사고', '딥러닝의 미래', '현대 AI 윤리: OpenAI의 AI윤리부서 해체'],
    'view_count': [250, 80, 400, 150, 120],
    'reg_date': pd.to_datetime(['2026-03-01', '2026-03-02', '2026-03-03', '2026-03-04', '2026-03-05'])
}
df = pd.DataFrame(data)

# 조회수 등급
conditions = [
    (df['view_count'] < 100),
    (df['view_count'] < 200),
    (df['view_count'] >= 200)
]
grade_name = ['Bronze', 'Silver', 'Gold']
df['grade'] = np.select(conditions, grade_name, default='unknown')

# 제목 요약 생성
df['summary'] = df['title'].apply(lambda x: x[:15]+'...' if len(x)> 15 else x)

# 요일 정보 생성
df['day_of_week'] = df['reg_date'].dt.day_name()

# 긴급 기사 여부
df['is_argent'] = df['title'].str.contains('신기술|긴급')

print(df)

###############
# 문제 1: 등급별 평균 조회수를 구하라.
grade_avg = df.groupby('grade')['view_count'].mean()
print(grade_avg)

# 문제 2: 요일별 게시된 기사의 개수와 총 조회수를 구하라.
weekday_report = df.groupby('day_of_week')['view_count'].agg(['count','sum'])
print(weekday_report)

# 문제 3: 요일별 인기 지표를 생성하라.
weekly_popularity_report = df.groupby('day_of_week')['view_count'].agg(['mean', 'max'])
print(weekly_popularity_report)