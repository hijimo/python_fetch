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

base_download_path = '/users/jimo/downloads/pics/'
url = 'https://picsum.photos/'
w = 310
h = 155



detail_chucks=[]
max_detail_size =10
max_count = 60


headers = {
    # 'Access-Control-Request-Headers': 'range',
    # 'Access-Control-Request-Method':
    # 'GET',
    # 'Origin':
    # 'https://www.bilibili.com',
    # 'Referer':
    # 'https://www.bilibili.com/video/av39282049',
    'User-Agent':
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
}


def createPath(path):
    if os.path.exists(path) == False:
        os.makedirs(path)

def clearText(str):
    str = str.replace('/', '-')
    str = str.replace('【', '')
    str = str.replace('】', '')
    str = str.replace(' ', '')
    return str


def download_file(url, path, isVideo):
    down_res = requests.get(url=url)
    with open(path,"wb") as code:
        code.write(down_res.content)

                
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
def pullData(id =1 ):
    

    while (id < max_count):
        global detail_chucks
        path = base_download_path + str(w) + 'x' + str(h) + '/'
        if os.path.exists(path) == False:
            os.makedirs(path)
        file_path = path + str(id) + '.jpg'
        file_url = url + '/id/'+ str(id) + '/' +str(w) + '/' + str(h)

        print('正在拉取第' + str(id) + '个图片')
        download_file(file_url,file_path,False)
        id +=1

    
       
    
    






pullData(10)


# print('list', dd)
# download_list(dir_list)
# print('list', dir_list)


# print(soup.find_all('div', class_="crowd-type"))
# print(soup.find_all("a",string="健身人群")[0]["href"].split("/"))