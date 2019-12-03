from django.shortcuts import render

from urllib.request import urlopen
from bs4 import BeautifulSoup
from .models import CrwalingData
from django.http import HttpResponse
import time
from django.template import loader
# 교보문고의 베스트셀러 웹페이지를 가져옵니다.



def select(request):
    return HttpResponse("sdfjlaejf;ljel")


def main(request):
    context={}
    return render(request, 'parsed_data/NewFile1.html',context)


kyobo_data = []




def kyobo_book(request):

    html = urlopen('http://www.kyobobook.co.kr/bestSellerNew/bestseller.laf?orderClick=d79')
    bsObject = BeautifulSoup(html, "html.parser")

    # 책의 상세 웹페이지 주소를 추출하여 리스트에 저장합니다.
    book_page_urls = []
    for cover in bsObject.find_all('div', {'class': 'detail'}):
        link = cover.select('a')[0].get('href')
        book_page_urls.append(link)
    context={}

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
        kyobo_data.append([rank, kisbn, kname, kauthor, koriginalp, ksalep, klink, kimg])
        rank += 1
    return render(request, 'parsed_data/book.html', {'books': kyobo_data})
            # columns=['ISBN','krank','kname','kauthor','kprice','klink','kimg']
            # df =pd.DataFrame(kyobo_data,columns=columns)


