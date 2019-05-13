# -*- coding: utf-8 -*-
import bs4, requests, re, zipfile, io, sys
from urllib.request import urlopen
import urllib.request
import pymysql
import time
import json
import telegram
import datetime
from difflib import SequenceMatcher
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from telegram import ReplyKeyboardMarkup
import urllib.parse
import pyfiglet


_headers_get = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
}

#### Global ####
#Tags to search
tags = []
#Time to waint betewen request tag
time_tag = 600
#Ratio equal tag and email
ratio = 0.620


#### DB Config ####
host="xxxx.xxxx.us-east-1.rds.amazonaws.com"
port=3306
dbname="xxxxx"
user="xxxxx"
password="xxxxxx"

#Example schema table
'''
CREATE TABLE `domains` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `link` varchar(250) COLLATE utf8_bin NOT NULL,
  `emails` blob,
  `created_at` timestamp NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
'''


#### Telegram Config #### [Optional]
telegram_on = False
TOKEN = 'xxxxx:xxxx-xxx'
mi_canal = xxxxxx


def addslashes(s):
    return s.replace("'", '"')


def getDomains(tags,conn):
    if telegram_on:
        mi_bot = telegram.Bot(token=TOKEN)
        mi_bot_updater = Updater(mi_bot.token)

    urls = []
    array_d = []
    result = requests.get("https://whoisds.com/newly-registered-domains",headers=_headers_get)
    c = result.content
    soup = bs4.BeautifulSoup(c, "html.parser")
    table = soup.find("table", {"class":"table-bordered"})
    tr = soup.findAll('tr')[1]
    a = tr.find('a')
    link = str(a['href'])

    with conn.cursor() as cur:
        exist = cur.execute('select link from domains where link = "%s" LIMIT 1' % (link))
        if exist==0:
            r = requests.get(link,headers=_headers_get, stream=True)
            zfile = zipfile.ZipFile(io.BytesIO(r.content))
            for finfo in zfile.infolist():
                ifile = zfile.open(finfo)
                urls = ifile.readlines()
                for url_value in urls:
                    for tag in tags:
                        domain = url_value.strip().decode("utf-8")
                        if (float(ratio) <= float(SequenceMatcher(None, domain, tag).ratio())):
                            if domain not in array_d:
                                array_d.append(domain)

            print("-------")
            print(link)
            print(array_d)
            emails_json = addslashes(str(json.dumps(array_d)))
            cur.execute("insert into domains (link, emails) values('%s', '%s')" % (link,emails_json))
            conn.commit()
            if telegram_on:
                try:
                    mi_bot.sendMessage(chat_id=mi_canal, text="--------"+datetime.datetime.now().strftime("%H:%M %d/%m/%y")+"---------")
                    mi_bot.sendMessage(chat_id=mi_canal, text=("%s" % str(link)))
                    mi_bot.sendMessage(chat_id=mi_canal, text=("%s" % str(array_d)))
                except Exception as e:
                    pass

    return True

def main():
    ascii_banner = pyfiglet.figlet_format("DomainWhisper")
    print("\n"+ascii_banner)
    conn = pymysql.connect(host, user=user,port=port,passwd=password, db=dbname)
    try:
        tags_sys = str(sys.argv[1])
        if tags_sys:
            tags.clear()
            tags_ = str(tags_sys)
            tags_ = tags_.split(",")
            for value in tags_:
                tags.append(value)

    except Exception as e:
        pass

    while True:
        print(datetime.datetime.now().strftime("%H:%M %d/%m/%y"))
        print("Tags: %s" % str(tags))
        # Search
        getDomains(tags,conn)
        time.sleep(time_tag)

if __name__ == "__main__":
    main()
