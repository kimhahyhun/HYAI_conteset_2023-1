import os
import requests
from bs4 import BeautifulSoup
import time

# 웹 페이지의 소스코드를 가져오기
URL = 'https://www.google.com/search?q=%EB%AC%BC%EB%B3%91+%EC%9D%B4%EB%AF%B8%EC%A7%80&rlz=1C5CHFA_enKR1058KR1058&sxsrf=APwXEdchlYCnCSj1qLItkB75kHFaJUGLUg1686730702823&source=lnms&tbm=isch&sa=X&ved=2ahUKEwiQlf7CqcL_AhXUMN4KHep9A3gQ0pQJegQIAxAC&biw=1440&bih=703&dpr=2'

response = requests.get(URL)
content = response.content
soup = BeautifulSoup(content, 'html.parser')

# 웹 페이지에서 모든 이미지 태그(<img>)를 찾기
img_tags = soup.find_all('img')

# 이미지 URL을 저장할 디렉터리 생성
SAVE_DIR = './saved_images'
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

i = 0

path = SAVE_DIR

# 이미지 태그에서 이미지 URL을 추출하고 이미지 저장하기
for img in img_tags:
    img_url = img.get('src')
    if not img_url.startswith('http'):
        img_url = URL + img_url
    response = requests.get(img_url, stream=True)
    t = time.time()
    # 이미지 파일을 저장할 경로 지정
    filename = f"{path}/{t}{i}.jpg"
    i+= 1
    

    # 이미지 파일을 저장
    with open(filename, 'wb') as file_out:

        for chunk in response.iter_content(chunk_size=8192):
            file_out.write(chunk)