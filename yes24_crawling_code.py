#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#yes24베스트셀러 코드
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
from bs4 import BeautifulSoup

html= urlopen('http://www.yes24.com/24/category/bestseller?CategoryNumber=117')
bsObject = BeautifulSoup(html, "html.parser")

link=[]
yes24=[]
rank=1
for tag in bsObject.find_all('p',{'class':'image'}):
    if rank<=20:
        tmp = tag.select('a')[0].get('href')
        ylink='http://www.yes24.com'+tmp
        link.append(ylink)
        yname=tag.find('img').get('alt')
        rank+=1

yes24_data=[]
rank=1
# 메타 정보로부터 필요한 정보를 추출합니다.메타 정보에 없는 저자 정보만 따로 가져왔습니다.   
for book_page_url in link:
    
    html = urlopen(book_page_url)
    bsObject = BeautifulSoup(html, "html.parser")
    
    yisbn=bsObject.find('tbody',{'class':'b_size'}).select('td')[2].text
    yname = bsObject.find('meta', {'property':'og:title'}).get('content')
    yauthor = bsObject.find('meta', {'name':'author'}).get('content')
    yimg = bsObject.find('em', {'class':'imgBdr'}).find('img').get('src')
    ylink = book_page_url
    yoriginalp = bsObject.find('div', {'class': 'gd_infoTb'}).find('em',{'class':'yes_m'}).text
    ysalep = bsObject.find('div', {'class': 'gd_infoTb'}).find('tr',{'class':'accentRow'}).find('em',{'class':'yes_m'}).text
    yes24_data.append([rank,yisbn,yname,yauthor,yoriginalp,ysalep,ylink,yimg])
    rank+=1
    #columns=['ISBN','krank','kname','kauthor','kprice','klink','kimg']
    #df =pd.DataFrame(kyobo_data,columns=columns)
print(yes24_data)

