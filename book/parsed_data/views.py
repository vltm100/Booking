from django.shortcuts import render

from urllib.request import urlopen
from bs4 import BeautifulSoup
from .models import CrwalingData
from django.http import HttpResponse
import time
from django.template import loader
from datetime import datetime

# 교보문고의 베스트셀러 웹페이지를 가져옵니다.



def select(request):


    # 절대 경로 지정 - 현재 소스파일 폴더로 지정되어 있음
    workDir = os.path.abspath('.')

    # 현재 날짜 가져오기
    thetime = datetime.now().strftime('%Y-%m-%d')

    # 현재 날짜 + .json 해서 "현재날짜.json" 파일 가져오기
    filename = str(thetime + ".json")

    # json 파일 읽어오기
    with open(filename, 'r', encoding='utf-8') as json_file:
        text_list = json.load(json_file)
        book_list = text_list
    '''
    읽어들인 데이터 형식
    [
        {
            "serial" : ...,
            "title" : "...",
            "contents" : "...",
        },
        {
            ...
        },
        ...
    ]
    '''
    # 읽어온 json 파일 출력
    for book in book_list:
        print(book['serial'])
        print(book['title'])
        print(book['contents'])
        print()


def main(request):
    context={}
    return render(request, 'parsed_data/NewFile1.html',context)


kyobo_data = []
book=[]
context={}


def kyobo_book(request):

    html = urlopen('http://www.kyobobook.co.kr/bestSellerNew/bestseller.laf?orderClick=d79')
    bsObject = BeautifulSoup(html, "html.parser")

    # 책의 상세 웹페이지 주소를 추출하여 리스트에 저장합니다.
    book_page_urls = []
    tmp=1
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
        json_book_date_ = {
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
        with open(filename, 'w', encoding='utf-8') as json_file:
            text_list = json.dump(book_list, json_file, indent="\t")
        '''kyobo_data.append({
            "title":kname,
            "isbn":kisbn,
            "author":kauthor,
            "img":kimg,
            "link":klink,
            "originalp":koriginalp,
            "salep":ksalep,
            "rank": rank
        })

    context={
        'kyobo':kyobo_data
    }'''



    # 새 데이터 삽입




    return render(request, 'parsed_data/book.html', context)
            # columns=['ISBN','krank','kname','kauthor','kprice','klink','kimg']
            # df =pd.DataFrame(kyobo_data,columns=columns)


