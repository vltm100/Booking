#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import requests
from bs4 import BeautifulSoup
from django.db import models
from urllib.request import urlopen
from bs4 import BeautifulSoup
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "book.settings")
import django



# 교보문고의 베스트셀러 웹페이지를 가져옵니다.





# 책의 상세 웹페이지 주소를 추출하여 리스트에 저장합니다.

html = urlopen('http://www.kyobobook.co.kr/bestSellerNew/bestseller.laf?orderClick=d79')
bsObject = BeautifulSoup(html, "html.parser")

book_page_urls = []
for cover in bsObject.find_all('div', {'class':'detail'}):
    link = cover.select('a')[0].get('href')
    book_page_urls.append(link)

kyobo_data = [[0 for col in range(20)] for row in range(8)]

rank=1
index=0
# 메타 정보로부터 필요한 정보를 추출합니다.메타 정보에 없는 저자 정보만 따로 가져왔습니다.
for index, book_page_url in enumerate(book_page_urls):

    html = urlopen(book_page_url)
    bsObject = BeautifulSoup(html, "html.parser")

    kisbn=bsObject.find('span',{'title':'ISBN-13'}).text
    kname = bsObject.find('meta', {'property':'rb:itemName'}).get('content')
    kauthor = bsObject.select('span.name a')[0].text
    kimg = bsObject.find('meta', {'property':'rb:itemImage'}).get('content')
    klink = bsObject.find('meta', {'property':'rb:itemUrl'}).get('content')
    koriginalp = bsObject.find('meta', {'property': 'rb:originalPrice'}).get('content')
    ksalep = bsObject.find('meta', {'property':'rb:salePrice'}).get('content')
    kyobo_data[index]=[rank,kisbn,kname,kauthor,koriginalp,ksalep,klink,kimg]
    rank+=1



print(kyobo_data[0][0])


