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
global wx_app_secret
global wx_title
global wx_title_index

wx_app_secret = '228545803ee809e9b50968487d90a27c'

wx_title = '傻缺搞笑'
wx_title_index = 0
base_download_path = '/users/jimo/downloads/'
userId = '30417070'

# keyword = '国外趣味视频集锦，看完觉得整个世界都是那么欢乐'
keyword = '笑'

headers = {
    # 'Access-Control-Request-Headers': 'range',
    'Access-Control-Request-Method':
    'GET',
    'Origin':
    'https://www.bilibili.com',
    'Referer':
    'https://www.bilibili.com/video/av39282049',
    'User-Agent':
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
}


def download_file(url, path, isVideo):

    with closing(requests.get(url, stream=True, headers=headers)) as r:
        chunk_size = 1024 * 100
        content_size = int(r.headers['content-length'])
        if os.path.exists(path) and os.path.getsize(path) >= content_size:
            print('已下载')
            return
        with open(path, "wb") as f:
            # p = ProgressData(size = content_size, unit='Kb', block=chunk_size, file_name=path)
            print('downloading...', path)
            for chunk in r.iter_content(chunk_size=chunk_size):
                f.write(chunk)

                # p.output()
            print('下载完成, 开始转码')
            if (isVideo == True):
                t = threading.Thread(target=recodec_video, args=(path,))
                t.start()


def clearText(str):
    str = str.replace('【', '')
    str = str.replace('】', '')
    str = str.replace(' ', '')
    return str


def download_list(file_list):
    for file in file_list:
        title = clearText(file['title'])
        url = bilibiliParser.getVideoUrlByAid(file['aid'])
        path = base_download_path + userId + '/' + str(file['aid']) + '/'
        filen_path = path + title + '.mp4'
        pic_url = 'https:' + file['pic']
        pic_path = path + title + '.jpg'
        json_path = path + title + '.txt'
        if os.path.exists(path) == False:
            os.makedirs(path)
        # 开始写入 封面图
        download_file(pic_url, pic_path, False)
        # 开始写入 json文件说明
        f = open(json_path, 'w')
        f.write(json.dumps(file).encode('utf-8').decode('unicode_escape'))
        f.close()
        print('file', filen_path)
        print('url', url)
        #开始下载视频
        download_file(url, filen_path, True)


def postWx(file_path):
    global wx_app_secret
    global wx_title
    global wx_title_index

    if os.path.exists(file_path) == True:
        print('file exists')
        api = 'https://api.weixin.qq.com/cgi-bin/material/add_material?access_token=' + wx_app_secret + '&type=video'
        _t = wx_title + str(wx_title_index)
        data = {'description': {'title': _t, 'introduction': _t}}

        files = {'media': ('name', open(file_path, 'rb'))}
        
        r = requests.post(api, data=data, files=files)
        wx_title_index += 1
        print('wx msg', r)


def recodec_video(file_path):

    tpl = 'ffmpeg -i {} -i {} -i {} -filter_complex "overlay[tmp];[tmp]overlay=main_w-overlay_w-10:10" -c:v libx264 -c:a copy {}'
    # tpl = 'ffmpeg -i {} -i {} -i {} -filter_complex "overlay[tmp];[tmp]overlay=main_w-overlay_w-10:10" -c:v libx264 -c:a copy -ss 00:00:15 -t 00:03:30 {}'
    # tpl = 'ffmpeg -i {} -i {} -i {} -filter_complex "overlay=10:10[tmp];[tmp]overlay=main_w-overlay_w-10:main_h-overlay_h-10" -b:v 128k -s 640x480 -r 20 -ss 00:00:10 -t 00:03:30 {}'

    # 左上角
    # 	10:10
    # 右上角
    # 	main_w-overlay_w-10:10
    # 左下角
    # 	10:main_h-overlay_h-10
    # 右下角
    # main_w-overlay_w-10 : main_h-overlay_h-10

    wm1 = os.path.abspath('wm.png')
    wm2 = os.path.abspath('wm2.png')
    wm3 = os.path.abspath('wm3.png')
    out = file_path + '_out.mp4'
    print('start codec ', file_path)
    sh = tpl.format(file_path, wm3, wm1, out)
    # sh = tpl.format(file_path, wm2, wm1, out)
    os.system(sh)
    postWx(file_path)


video_list = bilibiliParser.fetchVideoList(userId, keyword=keyword)

download_list(video_list)
# print('list', video_list)

# url = 'http://upos-hz-mirrorkodou.acgvideo.com/upgcxcode/78/22/69032278/69032278-1-6.mp4?e=ig8euxZM2rNcNbuVhwdVtWuVhwdVNEVEuCIv29hEn0l5QK==&deadline=1546157628&gen=playurl&nbs=1&oi=3080682485&os=kodou&platform=html5&trid=9a288cc91da7443699092ba914dff955&uipk=5&upsig=b31bf438a09693cb19c446166bb916eb'

# download_file(url, path)
