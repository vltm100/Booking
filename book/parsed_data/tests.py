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







def main():

    with open('kyobo_json/kyobo.json', 'r', encoding='utf-8') as json_file:
        kyobo_data = json.load(json_file)

    for book in kyobo_data:
        print(book['title'])
    context={
        'kyobo':kyobo_data
    }


if __name__ == '__main__':
    main()


