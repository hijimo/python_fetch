# -*- coding: utf-8 -*-
# @Author: jimo
# @Date:   2018-12-30 13:12:38
# @Last Modified by:   jimo
# @Last Modified time: 2019-03-16 16:38:58
from contextlib import closing
import time
from multiprocessing import Queue
import requests
import hashlib
import threading
import _thread
import os
import json
from bilibili_html_parse import bilibiliParser





detail_chucks=[]
max_detail_size =10
max_count = 1000000


basic_path = os.getcwd() + '/downloads/'



def createPath(path):
    if os.path.exists(path) == False:
        os.makedirs(path)

def clearText(str):
    str = str.replace('/', '-')
    str = str.replace('【', '')
    str = str.replace('】', '')
    str = str.replace(' ', '')
    return str

def writeFile(path,content):
    print(path)
    
    f = open(path, 'w')
    f.write(json.dumps(content))
    f.close()

def writeDetailFile( content ):
    detail_path =basic_path + 'details/'
    createPath(detail_path)
    page_no = len(os.listdir(detail_path))
    path = detail_path + str(page_no) + '.json'
    writeFile(path,content)


def next(id):
    if (id < max_count):
        pullData(id + 1)
def pullData(id =1, ):
    

    while (id < max_count):
        global detail_chucks
        doc = bilibiliParser.fetchHtml(url='http://www.boohee.com/shiwu/' + str(id))
        soup = bilibiliParser.parse_html(doc)
        code = bilibiliParser.getCodeInHtml(soup)
        print('正在拉取第' + str(id) + '个文件', code)
        if (code):
            detail = bilibiliParser.fetchDirLv2(code)
            detail_chucks.append(detail)
            if (len(detail_chucks) >= max_detail_size * 20):
                writeDetailFile(detail_chucks)
                detail_chucks =[]
        id +=1

    
       
    
    






pullData(1)


# print('list', dd)
# download_list(dir_list)
# print('list', dir_list)


# print(soup.find_all('div', class_="crowd-type"))
# print(soup.find_all("a",string="健身人群")[0]["href"].split("/"))