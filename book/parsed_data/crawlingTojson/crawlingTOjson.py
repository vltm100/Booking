import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
from bs4 import BeautifulSoup
from time import sleep
import json

def aladin():
    book_page_urls = []
    html = urlopen('https://www.aladin.co.kr/shop/common/wbest.aspx?BranchType=1')
    bsObject = BeautifulSoup(html, "html.parser")
    links = bsObject.find_all(class_="bo3")
    i = 1
    for links_item in links:
        if i <= 20:
            book_page_urls.append(links_item.get('href'))
        i += 1
    aladin_data = []
    book_list = []
    rank = 1
    # 메타 정보로부터 필요한 정보를 추출합니다.메타 정보에 없는 저자 정보만 따로 가져왔습니다.
    for book_page_url in book_page_urls:

        html = urlopen(book_page_url)
        bsObject = BeautifulSoup(html, "html.parser")

        aisbn = bsObject.find('meta', {'property': 'og:barcode'}).get('content')

        aname = bsObject.find('meta', {'property': 'og:title'}).get('content')
        aauthor = bsObject.find('meta', {'property': 'og:author'}).get('content')
        aimg = bsObject.find('meta', {'property': 'og:image'}).get('content')
        alink = book_page_url
        aoriginalp = bsObject.find('div', {'class': 'info_list'}).find('div', {'class': 'Ritem'}).text
        asalep = bsObject.find('div', {'class': 'info_list'}).find('span', {'class': 'Ere_fs24'}).text
        aladin_data.append([rank, aisbn, aname, aauthor, aoriginalp, asalep, alink, aimg])

        # columns=['ISBN','krank','kname','kauthor','kprice','klink','kimg']
        # df =pd.DataFrame(kyobo_data,columns=columns)

        # 교보에서 찾기
        a_kyobo_search = "https://search.kyobobook.co.kr/web/search?vPstrKeyWord=" + aisbn
        html2 = urlopen(a_kyobo_search)
        bsObject2 = BeautifulSoup(html2, "html.parser")
        # print(a_kyobo_search)

        a_kyobo = bsObject2.find('div', {'class': 'sell_price'}).find('strong').text
        a_kyobo_link = bsObject2.find('div', {'class': 'cover'}).find('a').get('href')

        # print(rank ," : ",a_kyobo,a_kyobo_link)

        # yes24에서 찾기
        a_yes24_search = "http://www.yes24.com/searchcorner/Search?query=" + aisbn
        # print(a_yes24_search)
        html2 = urlopen(a_yes24_search)
        bsObject2 = BeautifulSoup(html2, "html.parser")
        a_yes24 = bsObject2.find('p', {'class': 'goods_price'}).find('strong').text
        tmp = bsObject2.find('td', {'class': 'goods_img'}).select('a')[0].get('href')
        a_yes24_link = 'http://www.yes24.com' + tmp

        # yes24 중고에서 찾기
        a_yes24_used = ''
        a_yes24_used_link = ''
        a_yes24_used = bsObject2.find('em', {'class': 'act_txt002'})
        if a_yes24_used != None:
            a_yes24_used = bsObject2.find('em', {'class': 'act_txt002'}).text
            a_yes24_used_link = bsObject2.find('p', {'class': 'used_info'}).find('a').get('href')
        # print(rank,":",a_yes24,a_yes24_link,a_yes24_used, a_yes24_used_link)
        else:
            a_yes24_used = '-'
            a_yes24_used_link = ''

        # 알라딘 중고에서 찾기
        a_aladin_search = "https://www.aladin.co.kr/search/wsearchresult.aspx?SearchTarget=Used&KeyWord=" + aisbn
        # print("주소다주소: ",a_aladin_search)
        html2 = urlopen(a_aladin_search)
        bsObject2 = BeautifulSoup(html2, "html.parser")

        a_aladin_used = ''
        a_aladin_used_link = bsObject2.find('div', {'class': 'ss_book_list'})
        # 중고책에 자료가 있으면
        if a_aladin_used_link != None:

            # k_aladin_used_link2=bsObject2.find('div', {'class':'ss_line5'}).find('img').get('src')
            # 중고가격 가져오기 가장 위에 정보로
            flag = False
            temp = bsObject2.find_all(class_="bo_used")
            for item in temp:
                # if item.text[-1]=='원':

                if flag:
                    a_aladin_used = item.text
                    if a_aladin_used[-1] == '원':
                        a_aladin_used_link = 'http://www.aladin.co.kr' + item.get('href')
                        break
                    else:
                        a_aladin_used = '-'
                        a_aladin_used_link = ''
                        flag = False

                if item.text[0] == '판':
                    flag = True


        else:
            a_aladin_used = '-'
            a_aladin_used_link = ''
        # aladin_data에 모든 정보 저장
        aladin_data.append([rank, aisbn, aname, aauthor, aoriginalp, asalep, alink
                               , a_kyobo, a_kyobo_link, a_yes24, a_yes24_link
                               , a_yes24_used, a_yes24_used_link, a_aladin_used, a_aladin_used_link])
        json_book_data = {
            "title": aname,
            "isbn": aisbn,
            "author": aauthor,
            "img": aimg,
            "link": alink,
            "originalp": aoriginalp,
            "salep": asalep,
            "rank": rank,
            "a_kyobo": a_kyobo,
            "a_kyobo_link": a_kyobo_link,
            "a_yes24": a_yes24,
            "a_yes24_link": a_yes24_link,
            "a_yes24_used": a_yes24_used,
            "a_yes24_used_link": a_yes24_used_link,
            "a_aladin_used": a_aladin_used,
            "a_aladin_used_link": a_aladin_used_link

        }
        rank += 1
        book_list.append(json_book_data)
        with open("aladin.json", 'w', encoding='utf-8') as json_file:
            json.dump(book_list, json_file, ensure_ascii=False, indent="\t")


def kyobo():
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
            k_yes24_used = '-'
            k_yes24_used_link = ''
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
                        flag=False

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


#######################################3










# yes24베스트셀러 코드 최종
def yes24():
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



def main():
    while True:
        sleep(86400) #24시간
        kyobo()
        aladin()
        yes24()


if __name__ == '__main__':
    main()