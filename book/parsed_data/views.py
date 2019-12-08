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
    workDir = os.path.abspath('.')
    return render(request, 'parsed_data/main.html')


def yes24(request):
    workDir = os.path.abspath('.')
    #with open('parsed_data/yes24_json/yes24.json', 'r', encoding='utf-8') as json_file:
        #yes24_data = json.load(json_file)
    with open('parsed_data/crawlingTojson/yes24.json', 'r', encoding='utf-8') as json_file:
        yes24_data = json.load(json_file)

    return render(request, 'parsed_data/yes24.html', {'yes24': yes24_data})


def kyobo(request):
    workDir = os.path.abspath('.')
    #with open('parsed_data/kyobo_json/kyobo.json', 'r', encoding='utf-8') as json_file:
       # kyobo_data = json.load(json_file)
    with open('parsed_data/crawlingTojson/kyobo.json', 'r', encoding='utf-8') as json_file:
        kyobo_data = json.load(json_file)

    return render(request, 'parsed_data/kyobo.html', {'kyobo': kyobo_data})


def aladin(request):
    workDir = os.path.abspath('.')
    #with open('parsed_data/aladin_json/aladin.json', 'r', encoding='utf-8') as json_file:
       # aladin_data = json.load(json_file)
    with open('parsed_data/crawlingTojson/aladin.json', 'r', encoding='utf-8') as json_file:
        aladin_data = json.load(json_file)

    return render(request, 'parsed_data/aladin.html', {'aladin': aladin_data})
