import requests
from bs4 import BeautifulSoup

# 웹사이트 접속(AI 뉴스만 검색)
url = "https://news.google.com/search?q=ai&hl=ko&gl=KR&ceid=KR%3Ako"
response = requests.get(url)
html = response.text

# BeautifulSoup 객체 생성
soup = BeautifulSoup(html, 'html.parser')

a_tag = soup.find('a')

# 뉴스 파트 추출
contents = soup.select('a.JtKRv')

print(f"뉴스 개수: {len(contents)}개\n")

# 텍스트(제목) 추출
for i, title in enumerate(contents[:5], 1):
    print(f"{i}. {title.text}")