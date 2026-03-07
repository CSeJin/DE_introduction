import pandas as pd

data = {
    'title': ['AI의 미래', 'Python 기초', 'OpenAI 신기술', 'Deep Learning', '데이터 엔지니어링', 'AI 윤리 가이드'],
    'author': ['CareerCoach', 'unknown', 'CareerCoach', 'Gemini', 'unknown', 'CareerCoach'],
    'hits': [150, 45, 300, 80, 120, 30],
    'date': ['2026-03-01', '2026-03-02', '2026-03-02', '2026-03-03', '2026-03-04', '2026-03-04']
}

df = pd.DataFrame(data)
df['date'] = pd.to_datetime(df['date'])

# 조회수(hits)가 50회 이상이고 작성자(author)가 'unknown'이 아닌 기사들의 제목(title)과 날짜(date)만 추출
filtered_data = df.loc[(df.hits>=50) & (df.author != 'unknown'), ['title', 'date']]
print(filtered_data)
