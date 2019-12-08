# yes24베스트셀러 코드 최종
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
html = urlopen('http://www.yes24.com/24/category/bestseller')
bsObject = BeautifulSoup(html, "html.parser")

link = []
yes24 = []
temp = 1
book_list = []
for tag in bsObject.find_all('p', {'class': 'image'}):
    if temp <= 20:
        tmp = tag.select('a')[0].get('href')
        ylink = 'http://www.yes24.com' + tmp
        link.append(ylink)
        yname = tag.find('img').get('alt')
        temp += 1

yes24_data = []
rank = 1
# 메타 정보로부터 필요한 정보를 추출합니다.메타 정보에 없는 저자 정보만 따로 가져왔습니다.
for book_page_url in link:

    html = urlopen(book_page_url)
    bsObject = BeautifulSoup(html, "html.parser")

    yisbn = bsObject.find('tbody', {'class': 'b_size'}).select('td')[2].text
    yname = bsObject.find('meta', {'property': 'og:title'}).get('content')
    yauthor = bsObject.find('meta', {'name': 'author'}).get('content')
    yimg = bsObject.find('em', {'class': 'imgBdr'}).find('img').get('src')
    ylink = book_page_url
    yoriginalp = bsObject.find('div', {'class': 'gd_infoTb'}).find('em', {'class': 'yes_m'}).text
    ysalep = bsObject.find('div', {'class': 'gd_infoTb'}).find('tr', {'class': 'accentRow'}).find('em', {
        'class': 'yes_m'}).text
    # yes24_data.append([rank,yisbn,yname,yauthor,yoriginalp,ysalep,ylink,yimg])
    # print(yisbn)
    # columns=['ISBN','krank','kname','kauthor','kprice','klink','kimg']
    # df =pd.DataFrame(kyobo_data,columns=columns)
    # 교보에서 찾기
    y_kyobo_search = "https://search.kyobobook.co.kr/web/search?vPstrKeyWord=" + yisbn
    html2 = urlopen(y_kyobo_search)
    bsObject2 = BeautifulSoup(html2, "html.parser")
    # print(y_kyobo_search)

    y_kyobo = bsObject2.find('div', {'class': 'sell_price'}).find('strong').text
    y_kyobo_link = bsObject2.find('div', {'class': 'cover'}).find('a').get('href')

    # yes24 중고에서 찾기
    y_yes24_search = "http://www.yes24.com/searchcorner/Search?query=" + yisbn
    # print(y_yes24_search)

    html2 = urlopen(y_yes24_search)
    bsObject2 = BeautifulSoup(html2, "html.parser")
    y_yes24 = bsObject2.find('p', {'class': 'goods_price'}).find('strong').text
    y_yes24_used = ''
    y_yes24_used_link = ''
    y_yes24_used = bsObject2.find('em', {'class': 'act_txt002'})
    if y_yes24_used != None:
        y_yes24_used = bsObject2.find('em', {'class': 'act_txt002'}).text
        y_yes24_used_link = bsObject2.find('p', {'class': 'used_info'}).find('a').get('href')

    else:
        y_yes24_used = '-'
        y_yes24_used_link = ''
    # 알라딘에서 찾기
    y_aladin_search = "https://www.aladin.co.kr/search/wsearchresult.aspx?SearchTarget=All&SearchWord=" + yisbn
    # print(y_aladin_search)
    html2 = urlopen(y_aladin_search)
    bsObject2 = BeautifulSoup(html2, "html.parser")
    y_aladin = bsObject2.find('span', {'class': 'ss_p2'}).text
    y_aladin_link = bsObject2.find('div', {'class': 'ss_book_list'}).find('a', {'class': 'bo3'}).get('href')

    # 알라딘 중고에서 찾기
    y_aladin_search = "https://www.aladin.co.kr/search/wsearchresult.aspx?SearchTarget=Used&KeyWord=" + yisbn
    # print("주소다주소: ",y_aladin_search)
    html2 = urlopen(y_aladin_search)
    bsObject2 = BeautifulSoup(html2, "html.parser")
    y_aladin_used = ''
    y_aladin_used_link = bsObject2.find('div', {'class': 'ss_book_list'})
    # 중고책에 자료가 있으면
    if y_aladin_used_link != None:

        # k_aladin_used_link2=bsObject2.find('div', {'class':'ss_line5'}).find('img').get('src')
        # 중고가격 가져오기 가장 위에 정보로
        flag = False
        temp = bsObject2.find_all(class_="bo_used")
        for item in temp:
            # if item.text[-1]=='원':

            if flag:
                y_aladin_used = item.text
                if y_aladin_used[-1] == '원':
                    y_aladin_used_link = 'http://www.aladin.co.kr' + item.get('href')
                    break
                else:
                    y_aladin_used = '-'
                    y_aladin_used_link = ''
                    flag= False

            if item.text[0] == '판':
                flag = True


    else:
        y_aladin_used = '-'
        y_aladin_used_link = ''

    yes24_data.append([rank, yisbn, yname, yauthor, yoriginalp, ysalep, ylink
                          , y_kyobo, y_kyobo_link, y_yes24, y_yes24_used, y_yes24_used_link
                          , y_aladin, y_aladin_link, y_aladin_used, y_aladin_used_link])
    print([rank, yisbn, yname, yauthor, yoriginalp, ysalep, ylink
              , y_kyobo, y_kyobo_link, y_yes24, y_yes24_used, y_yes24_used_link
              , y_aladin, y_aladin_link, y_aladin_used, y_aladin_used_link])
    json_book_data = {
        "title": yname,
        "isbn": yisbn,
        "author": yauthor,
        "img": yimg,
        "link": ylink,
        "originalp": yoriginalp,
        "salep": ysalep,
        "rank": rank,
        "y_kyobo": y_kyobo,
        "y_kyobo_link": y_kyobo_link,
        "y_yes24": y_yes24,
        "y_yes24_used": y_yes24_used,
        "y_yes24_used_link": y_yes24_used_link,
        "y_aladin": y_aladin,
        "y_aladin_link": y_aladin_link,
        "y_aladin_used": y_aladin_used,
        "y_aladin_used_link": y_aladin_used_link

    }
    rank += 1
    book_list.append(json_book_data)
    with open("yes24.json", 'w', encoding='utf-8') as json_file:
        json.dump(book_list, json_file, ensure_ascii=False, indent="\t")


# print(yes24_data)