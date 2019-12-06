

#from django.shortcuts import render

from datetime import datetime
from urllib.request import urlopen
from bs4 import BeautifulSoup
#from .models import CrwalingData
import json
#from django.http import HttpResponse
import time
from django.template import loader
from datetime import datetime

import os


# 교보문고의 베스트셀러 웹페이지를 가져옵니다.



kyobo_data = []
book=[]
context={}


def main():

    html = urlopen('http://www.kyobobook.co.kr/bestSellerNew/bestseller.laf?orderClick=d79')
    bsObject = BeautifulSoup(html, "html.parser")

    # 책의 상세 웹페이지 주소를 추출하여 리스트에 저장합니다.
    book_page_urls = []
    book_list=[]
    tmp=0
    for cover in bsObject.find_all('div', {'class': 'detail'}):
        if tmp<=10:
            link = cover.select('a')[0].get('href')
            book_page_urls.append(link)
        tmp+=1


    rank = 1

    # 메타 정보로부터 필요한 정보를 추출합니다.메타 정보에 없는 저자 정보만 따로 가져왔습니다.
    for index, book_page_url in enumerate(book_page_urls):

        html = urlopen(book_page_url)
        bsObject = BeautifulSoup(html, "html.parser")

        kisbn = bsObject.find('span', {'title': 'ISBN-13'}).text
        kname = bsObject.find('meta', {'property': 'rb:itemName'}).get('content')
        kauthor = bsObject.select('span.name a')[0].text
        kimg = bsObject.find('meta', {'property': 'rb:itemImage'}).get('content')
        klink = bsObject.find('meta', {'property': 'rb:itemUrl'}).get('content')
        koriginalp = bsObject.find('meta', {'property': 'rb:originalPrice'}).get('content')
        ksalep = bsObject.find('meta', {'property': 'rb:salePrice'}).get('content')
        rank += 1
        json_book_data = {
            "title": kname,
            "isbn": kisbn,
            "author": kauthor,
            "img": kimg,
            "link": klink,
            "originalp": koriginalp,
            "salep": ksalep,
            "rank": rank
        }
        book_list.append(json_book_data)
        with open("kyobo.json", 'w', encoding='utf-8') as json_file:
            json.dump(book_list, json_file,ensure_ascii=False, indent="\t")
       

    # 새 데이터 삽입

if __name__ == '__main__':
    main()
