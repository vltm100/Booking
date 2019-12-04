#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#알라딘 베스트셀러 수집
yes24_data=[]
rank=1
# 메타 정보로부터 필요한 정보를 추출합니다.메타 정보에 없는 저자 정보만 따로 가져왔습니다.   
for book_page_url in book_page_urls:
    
    html = urlopen(book_page_url)
    bsObject = BeautifulSoup(html, "html.parser")
    
    aisbn=bsObject.find('meta',{'property':'og:barcode'}).get('content')
    
    #aname = bsObject.find('meta', {'property':'og:title'}).get('content')
    #aauthor = bsObject.find('meta', {'name':'author'}).get('content')
    #aimg = bsObject.find('em', {'class':'imgBdr'}).find('img').get('src')
    #alink = book_page_url
    aoriginalp = bsObject.find('div',{'class':'info_list'}).find('div',{'class':'Ritem'}).text
    #asalep = bsObject.find('div', {'class': 'gd_infoTb'}).find('tr',{'class':'accentRow'}).find('em',{'class':'yes_m'}).text
    #aes24_data.append([rank,yisbn,yname,yauthor,yoriginalp,ysalep,ylink,yimg])
    rank+=1
    #columns=['ISBN','krank','kname','kauthor','kprice','klink','kimg']
    #df =pd.DataFrame(kyobo_data,columns=columns)
    print(aisbn, aoriginalp)

