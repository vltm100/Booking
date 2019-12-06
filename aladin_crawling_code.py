#알라딘 베스트셀러 수집
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
    
#교보에서 찾기
    a_kyobo_search="https://search.kyobobook.co.kr/web/search?vPstrKeyWord="+aisbn
    html2 = urlopen(a_kyobo_search)
    bsObject2 = BeautifulSoup(html2, "html.parser")
    #print(a_kyobo_search)
    
    a_kyobo=bsObject2.find('div',{'class':'sell_price'}).find('strong').text
    a_kyobo_link=bsObject2.find('div',{'class':'cover'}).find('a').get('href')
    
    #print(rank ," : ",a_kyobo,a_kyobo_link)
    
#yes24에서 찾기
    a_yes24_search="http://www.yes24.com/searchcorner/Search?query="+aisbn
    #print(a_yes24_search)
    html2 = urlopen(a_yes24_search)
    bsObject2 = BeautifulSoup(html2, "html.parser")
    a_yes24= bsObject2.find('p', {'class':'goods_price'}).find('strong').text
    tmp=bsObject2.find('td', {'class':'goods_img'}).select('a')[0].get('href')
    a_yes24_link= 'http://www.yes24.com'+tmp
    
#yes24 중고에서 찾기
    a_yes24_used=''
    a_yes24_used_link=''
    a_yes24_used=bsObject2.find('em', {'class':'act_txt002'})
    if a_yes24_used!=None:
        a_yes24_used=bsObject2.find('em', {'class':'act_txt002'}).text
        a_yes24_used_link=bsObject2.find('p',{'class':'used_info'}).find('a').get('href')
    #print(rank,":",a_yes24,a_yes24_link,a_yes24_used, a_yes24_used_link)
    
#알라딘 중고에서 찾기
    a_aladin_search="https://www.aladin.co.kr/search/wsearchresult.aspx?SearchTarget=Used&KeyWord="+aisbn
    #print("주소다주소: ",a_aladin_search)
    html2 = urlopen(a_aladin_search)
    bsObject2 = BeautifulSoup(html2, "html.parser")
    a_aladin_used=''
    a_aladin_used_link=bsObject2.find('div', {'class':'ss_book_list'})
    #중고책에 자료가 있으면
    if a_aladin_used_link!=None:
        
        #k_aladin_used_link2=bsObject2.find('div', {'class':'ss_line5'}).find('img').get('src')
        #중고가격 가져오기 가장 위에 정보로
        flag=False
        temp=bsObject2.find_all('a',{'class':'bo_used'})
        for item in temp:
            if flag:
                a_aladin_used=item.text
                a_aladin_used_link='aladin.co.kr'+item.get('href')
                break
            if item.text[0]=='판':
                flag=True
        #print(rank,":",a_aladin_used, a_aladin_used_link)

#aladin_data에 모든 정보 저장
    aladin_data.append([rank,aisbn,aname,aauthor,aoriginalp,asalep,alink
                      ,a_kyobo, a_kyobo_link, a_yes24, a_yes24_link
                      ,a_yes24_used, a_yes24_used_link, a_aladin_used, a_aladin_used_link])
    #print(rank,aisbn,aname,aauthor,aoriginalp,asalep,alink
    #                  ,a_kyobo, a_kyobo_link, a_yes24, a_yes24_link
    #                  ,a_yes24_used, a_yes24_used_link, a_aladin_used, a_aladin_used_link)
    rank+=1
    
#print(aladin_data)
