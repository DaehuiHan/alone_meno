import requests
from bs4 import BeautifulSoup

url = 'https://movie.naver.com/movie/bi/mi/basic.nhn?code=171539'

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get(url,headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')

# FIXME: 1. 보통은 이렇게 하면 나오지만 html에 나와있는 메타태그 순서랑 파이썬에서 나와있는 순서랑 다르기 때문이다.
# 그렇게 때문에 괄호안에 번호를 바꾸면서 찾을 수 있지만 다른 방법이 있다.
title = soup.select_one('head > meta:nth-child(3)')
print(title)

# FIXME: 2. meta라고 쓰고 대괄호 안에 이것과 속성이 같은걸 가져와라 라는 뜻
og_title = soup.select_one('meta[property="og:title"]')['content']
og_image = soup.select_one('meta[property="og:image"]')['content']
og_description = soup.select_one('meta[property="og:description"]')['content']

print(og_title, og_image, og_description)