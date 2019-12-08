# 교보 최종
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
from bs4 import BeautifulSoup
import json

# 교보문고의 베스트셀러 웹페이지를 가져옵니다.

html = urlopen('http://www.kyobobook.co.kr/bestSellerNew/bestseller.laf?orderClick=d79')
bsObject = BeautifulSoup(html, "html.parser")

tmp = 1
# 책의 상세 웹페이지 주소를 추출하여 리스트에 저장합니다.
book_page_urls = []
for cover in bsObject.find_all('div', {'class': 'detail'}):
    if tmp <= 20:
        link = cover.select('a')[0].get('href')
        book_page_urls.append(link)
    tmp += 1
kyobo_data = []
book_list = []
rank = 1

# 메타 정보로부터 필요한 정보를 추출합니다.메타 정보에 없는 저자 정보만 따로 가져왔습니다.
for index, book_page_url in enumerate(book_page_urls):
    # kyobo_data=[]
    html = urlopen(book_page_url)
    bsObject = BeautifulSoup(html, "html.parser")

    kisbn = bsObject.find('span', {'title': 'ISBN-13'}).text
    kname = bsObject.find('meta', {'property': 'rb:itemName'}).get('content')
    kauthor = bsObject.select('span.name a')[0].text
    kimg = bsObject.find('meta', {'property': 'rb:itemImage'}).get('content')
    klink = bsObject.find('meta', {'property': 'rb:itemUrl'}).get('content')
    koriginalp = bsObject.find('meta', {'property': 'rb:originalPrice'}).get('content')
    ksalep = bsObject.find('meta', {'property': 'rb:salePrice'}).get('content')

    # yes24에서 찾기
    k_yes24_search = "http://www.yes24.com/searchcorner/Search?query=" + kisbn
    # print(k_yes24_search)
    html2 = urlopen(k_yes24_search)
    bsObject2 = BeautifulSoup(html2, "html.parser")
    k_yes24 = bsObject2.find('p', {'class': 'goods_price'}).find('strong').text
    tmp = bsObject2.find('td', {'class': 'goods_img'}).select('a')[0].get('href')
    k_yes24_link = 'http://www.yes24.com' + tmp
    # yes24 중고에서 찾기
    k_yes24_used = ''
    k_yes24_used_link = ''
    k_yes24_used = bsObject2.find('em', {'class': 'act_txt002'})
    if k_yes24_used != None:
        k_yes24_used = bsObject2.find('em', {'class': 'act_txt002'}).text
        k_yes24_used_link = bsObject2.find('p', {'class': 'used_info'}).find('a').get('href')
    # print(k_yes24,k_yes24_link,k_yes24_used, k_yes24_used_link)
    else:
        k_yes24_used='-'
        k_yes24_used_link=''
    # 알라딘에서 찾기
    k_aladin_search = "https://www.aladin.co.kr/search/wsearchresult.aspx?SearchTarget=All&SearchWord=" + kisbn
    # print(k_aladin_search)
    html2 = urlopen(k_aladin_search)
    bsObject2 = BeautifulSoup(html2, "html.parser")
    k_aladin = bsObject2.find('span', {'class': 'ss_p2'}).text
    k_aladin_link = bsObject2.find('div', {'class': 'ss_book_list'}).find('a', {'class': 'bo3'}).get('href')

    # 알라딘 중고에서 찾기
    k_aladin_search = "https://www.aladin.co.kr/search/wsearchresult.aspx?SearchTarget=Used&KeyWord=" + kisbn
    # print("주소다주소: ",k_aladin_search)
    html2 = urlopen(k_aladin_search)
    bsObject2 = BeautifulSoup(html2, "html.parser")
    k_aladin_used = ''
    k_aladin_used_link = bsObject2.find('div', {'class': 'ss_book_list'})
    # 중고책에 자료가 있으면
    if k_aladin_used_link != None:

        # k_aladin_used_link2=bsObject2.find('div', {'class':'ss_line5'}).find('img').get('src')
        # 중고가격 가져오기 가장 위에 정보로
        flag = False
        temp = bsObject2.find_all(class_="bo_used")
        for item in temp:
            # if item.text[-1]=='원':

            if flag:
                k_aladin_used = item.text
                if k_aladin_used[-1] == '원':
                    k_aladin_used_link = 'http://www.aladin.co.kr' + item.get('href')
                    break
                else:
                    k_aladin_used = '-'
                    k_aladin_used_link = ''
                    break

            if item.text[0] == '판':
                flag = True


        else:
            k_aladin_used = '-'
            k_aladin_used_link = ''
        # k_aladin_used=bsObject2.find('a', {'class':'bo_used'}).text#새책으로나옴

    # print( k_aladin_used_link)
    # print(k_aladin, k_aladin_link, k_aladin_used, k_aladin_used_link)

    kyobo_data.append([rank, kisbn, kname, kauthor, koriginalp, ksalep, klink
                          , k_yes24, k_yes24_link, k_yes24_used, k_yes24_used_link
                          , k_aladin, k_aladin_link, k_aladin_used, k_aladin_used_link])
    json_book_data = {
        "title": kname,
        "isbn": kisbn,
        "author": kauthor,
        "img": kimg,
        "link": klink,
        "originalp": koriginalp,
        "salep": ksalep,
        "rank": rank,
        "k_yes24": k_yes24,
        "k_yes24_link": k_yes24_link,
        "k_yes24_used": k_yes24_used,
        "k_yes24_used_link": k_yes24_used_link,
        "k_aladin": k_aladin,
        "k_aladin_link": k_aladin_link,
        "k_aladin_used": k_aladin_used,
        "k_aladin_used_link": k_aladin_used_link

    }
    rank += 1
    book_list.append(json_book_data)
    with open("kyobo.json", 'w', encoding='utf-8') as json_file:
        json.dump(book_list, json_file, ensure_ascii=False, indent="\t")

