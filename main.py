import requests
from bs4 import BeautifulSoup
import re
import time
import telegram
import html
import pymongo

#set url
url = "http://cooln.net/rss?bo_table=jirum"

#set telegram
my_token = "Place Telegram bot token key"
bot = telegram.Bot(token = my_token)
channel = 'Your Channel ID'

#set mongodb
connection = pymongo.MongoClient('localhost', 27017)
db = connection.cooln
jirum = db.jirum

def check_new_data():
    xml_data = requests.get(url).text
    parsing = BeautifulSoup(xml_data, "lxml-xml")
    xml_link = parsing.find_all("link")
    link_resub = re.findall("\d+", str(xml_link[1]))[0]
    return link_resub

def get_new_data(xml_data, n):
    parsing = BeautifulSoup(xml_data, "lxml-xml")
    xml_title = parsing.find_all("title")
    xml_link = parsing.find_all("link")
    title_resub = html.unescape(re.sub('<.+?>', '', str(xml_title[n])))
    link_resub = re.findall("\d+", str(xml_link[n]))[0]
    data = {"time" : int(time.time()),"title" : title_resub, "link" : link_resub, "deleted" : False}
    return data

def check_title(url):
    r = jirum.find({"link" : url})
    return r

def compre(old, new):
    if old == new:
        return False
    elif old > new:
        return False
    elif old < new:
        return True
    elif None:
        return True
    else:
        return None


print(db)
print(jirum)
xml_data = requests.get(url).text
for i in range(1, 26):
    jirum.insert_one(get_new_data(xml_data, i))

while True:
    oldnnew = compre(jirum.find_one()['link'], check_new_data())
    if oldnnew == True:
        jirum.insert_one(get_new_data(xml_data, 1))
        for i in check_title(check_new_data()):
            title = i['title']
        link = jirum.find_one()['link']
        msg = title+"\nhttp://cooln.net/bbs/jirum/"+link
        unescaped_msg = html.unescape(msg)
        bot.sendMessage(chat_id=channel, text=unescaped_msg)
        print(unescaped_msg)
