#!/usr/bin/env python
# coding: utf-8

# In[1]:



#알라딘 베스트셀러 링크수집
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
from bs4 import BeautifulSoup
book_page_urls = []
html= urlopen('https://www.aladin.co.kr/shop/common/wbest.aspx?BranchType=1')
bsObject = BeautifulSoup(html, "html.parser")
links = bsObject.find_all(class_="bo3")
i=1
for links_item in links:
    if i<=20:
        book_page_urls.append(links_item.get('href'))
    i+=1
#print(book_page_urls)

#알라딘 베스트셀러 내용수집
aladin_data=[]
rank=1
# 메타 정보로부터 필요한 정보를 추출합니다.메타 정보에 없는 저자 정보만 따로 가져왔습니다.   
for book_page_url in book_page_urls:
    
    html = urlopen(book_page_url)
    bsObject = BeautifulSoup(html, "html.parser")
    
    aisbn=bsObject.find('meta',{'property':'og:barcode'}).get('content')
    
    aname = bsObject.find('meta', {'property':'og:title'}).get('content')
    aauthor = bsObject.find('meta', {'property':'og:author'}).get('content')
    aimg = bsObject.find('meta', {'property':'og:image'}).get('content')
    alink = book_page_url
    aoriginalp = bsObject.find('div',{'class':'info_list'}).find('div',{'class':'Ritem'}).text
    asalep = bsObject.find('div',{'class':'info_list'}).find('span',{'class':'Ere_fs24'}).text
    aladin_data.append([rank,aisbn,aname,aauthor,aoriginalp,asalep,alink,aimg])
    
    #columns=['ISBN','krank','kname','kauthor','kprice','klink','kimg']
    #df =pd.DataFrame(kyobo_data,columns=columns)
 
    rank+=1
    
print(aladin_data)


# In[ ]:




