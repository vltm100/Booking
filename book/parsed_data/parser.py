import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "book.settings")
import django
django.setup()
from book.parsed_data.models import BookData
from urllib.request import urlopen
from bs4 import BeautifulSoup


# 교보문고의 베스트셀러 웹페이지를 가져옵니다.




def parse_book():
# 책의 상세 웹페이지 주소를 추출하여 리스트에 저장합니다.
    html = urlopen('http://www.kyobobook.co.kr/bestSellerNew/bestseller.laf?orderClick=d79')
    bsObject = BeautifulSoup(html, "html.parser")
    book_page_urls = []
    for cover in bsObject.find_all('div', {'class':'detail'}):
        link = cover.select('a')[0].get('href')
        book_page_urls.append(link)

    parse_book_detail(book_page_urls)


# 메타 정보로부터 필요한 정보를 추출합니다.메타 정보에 없는 저자 정보만 따로 가져왔습니다.

def parse_book_detail(book_page_urls):
    result=[]
    for index, book_page_url in enumerate(book_page_urls):
        html = urlopen(book_page_url)
        bsObject = BeautifulSoup(html, "html.parser")
        title = bsObject.find('meta', {'property': 'rb:itemName'}).get('content')
        author = bsObject.select('span.name a')[0].text
        image = bsObject.find('meta', {'property': 'rb:itemImage'}).get('content')
        url = bsObject.find('meta', {'property': 'rb:itemUrl'}).get('content')
        originalPrice = bsObject.find('meta', {'property': 'rb:originalPrice'}).get('content')
        salePrice = bsObject.find('meta', {'property': 'rb:salePrice'}).get('content')
        print(title)
        item_obj={
            'title':title,
            'author':author,
            'image':image,
            'url':url,
            'originalPrice':originalPrice,
            'salePrice':salePrice,
        }
        result.append(item_obj)

        return item_obj





def add_new_items(crawled_items):
    last_inserted_items = BookData.objects.last()
    if last_inserted_items is None:
        last_inserted_specific_id = ""
    else:
        last_inserted_specific_id = getattr(last_inserted_items, 'title')
    items_to_insert_into_db = []
    for item in crawled_items:
         if  item['title'] == last_inserted_specific_id:
            break
         items_to_insert_into_db.append(item)
    items_to_insert_into_db.reverse()


    for item in items_to_insert_into_db:
        print("new item added!! : " + item['title'])
        BookData(title=item['title'],
                  author=item['author'],
                  image=item['image'],
                 url=item['url'],
                 originalPrice=item['originalPrice'],
                 salePrice=item['salePrice']).save()


if __name__ == '__main__':
    add_new_items(parse_book())




