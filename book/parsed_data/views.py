from django.shortcuts import render

from urllib.request import urlopen
from bs4 import BeautifulSoup
#from .models import CrwalingData
from django.http import HttpResponse
import time
from django.template import loader
from datetime import datetime

# 교보문고의 베스트셀러 웹페이지를 가져옵니다.
import json
import os




def main(request):
    context={}
    return render(request, 'parsed_data/main.html',context)






def kyobo(request):
    workDir = os.path.abspath('.')
    with open('parsed_data\kyobo.json', 'r', encoding='utf-8') as json_file:
        kyobo_data = json.load(json_file)

    return render(request, 'parsed_data/book.html', {'kyobo': kyobo_data})
            # columns=['ISBN','krank','kname','kauthor','kprice','klink','kimg']
            # df =pd.DataFrame(kyobo_data,columns=columns)


