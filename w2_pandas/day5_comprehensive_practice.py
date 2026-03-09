import pandas as pd
import numpy as np
import random
from faker import Faker # python 3.14.3에서 실행 안됨

# 더미 데이터 생성 준비
fake = Faker('ko_KR')
Faker.seed(42)
np.random.seed(42)

# mess data 생성 ########################
raw_data_list = []
for _ in range(100):
    raw_data_list.append({
        'title': random.choice([' [속보] ', " ", ""]) + fake.sentence(nb_words=3),   # 공백 有 제목
        'author': random.choice([fake.name(), np.nan]),   # 결측치 포함
        'views': str(random.randint(0, 500)) + random.choice(['회', "", " view"]),  # 단위 유무
        'reg_date': fake.date_between(start_date='-30d', end_date='today').strftime('%Y-%m-%d')
    })

df = pd.DataFrame(raw_data_list)

# 중복 데이터 삽입
df = pd.concat([df, df.iloc[:5]], ignore_index=True)
########################################

# 데이터 확인
print("------------ 원본 데이터 ------------------")
print(df.head())
print("------------------------------------------")

# data cleaning #########################
# 1. 공백, 중복 제거
df['title'] = df['title'].str.strip()
df = df.drop_duplicates()

# 2. 결측치 처리
df['author'] = df['author'].fillna('unknown')
df = df.dropna(subset=['title'])

# 3. 숫자로 변환
df['views'] = df['views'].str.extract('(\d+)').astype(int)

# 4. 날짜 타입 변환
df['reg_date'] = pd.to_datetime(df['reg_date'])
########################################

# feature engineering ##################
# 1. 등급 생성
conditions = [
    (df['views'] < 100),
    (df['views'] < 300),
    (df['views'] >= 300)
]
grade_list = ['Gold', 'Silver', 'Bronze']
df['grade'] = np.select(
    conditions, grade_list, default='Standard'
)

# 2. 요일 정보 추가
df['weekday'] = df['reg_date'].dt.day_name()

# 3. 주말여부 추가
df['is_weekend'] = df['reg_date'].dt.weekday >= 5

print("------------ 정제 데이터 ------------------")
print(df.head())
print("------------------------------------------")
#########################################

# filtering ##############################
# 1. 월요일, 화요일에 올라온 gold 등급 뉴스만 추출
mon_tue_report = df.loc[
    (df['weekday'].isin(['Monday', 'Tuesday'])) & (df['grade'] == 'Gold'),
    ['title', 'author', 'views', 'weekday']
]
print("------ 월요일, 화요일에 올라온 gold 등급 뉴스 ------")
print(mon_tue_report)

# 2. 속보만 추출
newsflash = df.loc[
    df['title'].str.contains('[속보]'),
    ['title', 'author', 'views', 'weekday']
]
##########################################

# statistics #############################
# 등급별 평균 조회수와 기사 개수 요약
summary = df.groupby('grade')['views'].agg(['count', 'mean']).round(1)
print("------ 등급별 평균 조회수와 기사 개수 ------")
print(summary)
##########################################

# 저장
df.to_csv('w2_news_report_practice.csv', index=False, encoding='utf-8-sig')