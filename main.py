import requests
from bs4 import BeautifulSoup
import re
import time
import telegram
import html

data = ""
pre_data = ""

my_token = "Place Telegram bot token key"

bot = telegram.Bot(token = my_token)
channel = 'Your Channel ID'

while True:
    xml_data = requests.get("http://cooln.net/rss?bo_table=jirum").text #xml 파일 받아옴
    parsing = BeautifulSoup(xml_data, "lxml-xml") #정렬
    xml_title = parsing.find_all("title") #title 찾기
    xml_link = parsing.find_all("link") #link 찾기
    title_resub = re.sub('<.+?>', '', str(xml_title[1]))  # 타이틀에서 html 태그 제거 (=제목 추출)
    link_resub = re.findall("\d+", str(xml_link[1]))[0]  # 링크에서 숫자만 뽑기(=글번호 추출)
    data = link_resub #글번호를 data에 넣음, 안 이래도 될것 같은데 혹시나 싶어서 하였음
    if data > pre_data: #당연히 if문, 이전데이터와 비교하여 다를경우 작동
        tele_msg = title_resub+"\nhttp://cooln.net/bbs/jirum/"+link_resub #텔레로 보낼 메시지
        unescaped_msg = html.unescape(tele_msg) #HTML Unescape
        print(unescaped_msg) #미리보기
        bot.sendMessage(chat_id=channel, text=unescaped_msg) #텔레로 메시지 보냄
    pre_data = data #이전데이터내용에 현 데이터를 넣음, while문이 1회 작동되면 1회차 데이터가 저장되며 2회차 작동때 데이터 비교가 가능
    time.sleep(10) #10초 대기
