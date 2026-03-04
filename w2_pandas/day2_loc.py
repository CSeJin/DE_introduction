import pandas as pd

data = {
    'title': ['AI의 미래', 'Python 기초', 'OpenAI 신기술', 'Deep Learning', '데이터 엔지니어링', 'AI 윤리 가이드'],
    'author': ['CareerCoach', 'unknown', 'CareerCoach', 'Gemini', 'unknown', 'CareerCoach'],
    'hits': [150, 45, 300, 80, 120, 30],
    'date': ['2026-03-01', '2026-03-02', '2026-03-02', '2026-03-03', '2026-03-04', '2026-03-04']
}

df = pd.DataFrame(data)
# 날짜 컬럼을 진짜 '날짜 타입'으로 변경 (중요!)
df['date'] = pd.to_datetime(df['date'])