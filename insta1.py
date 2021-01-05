from urllib.request import urlopen
from urllib.parse import quote_plus # ASCII code로 변환
from bs4 import BeautifulSoup
from selenium import webdriver # javascript 때문
from selenium.webdriver.common.keys import Keys 
import time

# https://www.instagram.com/explore/tags/%ED%8C%8C%EC%9D%B4%EC%8D%AC/
# 뒤에는 검색내용이 ASCII code로 변환된 것 
url1 = 'https://www.instagram.com/explore/tags/'
url2 = input('검색할 해시태그를 입력하세요 : ') 
url = url1 + quote_plus(url2)

cnt = int(input('원하는 이미지의 개수 : '))

driver = webdriver.Chrome()
driver.get("https://instagram.com")
time.sleep(3) # 웹 페이지 로드를 보장하기 위해 3초 쉬기

# 인스타그램 로그인 필요 
nick = input("인스타그램 ID : ")
pw = input("인스타그램 PW : ")
driver.find_element_by_name("username").send_keys(nick) # chrome에서 [F12] -> name 찾기
driver.find_element_by_name("password").send_keys(pw)
driver.find_element_by_name("password").send_keys(Keys.RETURN)

# 나중에 하기
time.sleep(3)
driver.find_element_by_css_selector(".sqdOP.yWX7d.y3zKF").click() # chrome에서 [F12] -> class 이름 찾기
time.sleep(3)
driver.find_element_by_css_selector(".aOOlW.HoLwm").click()

driver.get(url)
time.sleep(3)

html = driver.page_source # selenium 사용하기 때문에 urlopen X
bsOb = BeautifulSoup(html, "html.parser")

insta = bsOb.select('.v1Nh3.kIKUG._bz0w')

t = open(url2 + ".txt", "a")
n = 1
for i in insta : 
    # 사진의 주소 저장
    addr = 'https://isntagram.com' + i.a['href']
    t.write(url2 + str(n) + " :: " + addr + "\n")
    
    # 사진 저장
    imgUrl = i.select_one('.KL4Bh').img['src'] # KL4Bh의 class 안에 img 태그의 src 부분만 가져옴 
    with urlopen(imgUrl) as f :
        with open('./img/' + url2 + str(n) + '.jpg', 'wb') as h : 
            img = f.read()
            h.write(img)
    if n == cnt :
        break
    n += 1

t.close()
driver.close()