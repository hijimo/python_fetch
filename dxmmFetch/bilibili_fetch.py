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

html_tpl = '<html><head><meta charset="utf-8" /></head><body>___content</body></html>'
wx_app_secret = '228545803ee809e9b50968487d90a27c'

wx_title = '傻缺搞笑'
wx_title_index = 0
base_download_path = '/users/jimo/downloads/'
# columnId='3284317633650361633'

# keyword = '国外趣味视频集锦，看完觉得整个世界都是那么欢乐'
keyword = '笑'

headers = {
    # 'Access-Control-Request-Headers': 'range',
    'app-os': 'IOS',
        'app-mc': '45ff4adfe045996bb720ac646b6a766d4c41d4c9',
        'app-mt': 'iPhone_iOS12.3.1',
        'Referer': 'https://mama.dxy.com',
        'Cookie': 'DXY_TRACE_ID=fTrtH7OUYAUzoC8LIzZz363n6jJrbxvq; route=ae6f4780d05f62342b430de7d1a8c0cc; DXY_CHD_SESSION=eyJhIjoxMjIxNzgyNDEyLCJ0IjoxNTkzNzQyNTc3LCJuIjoiaFRFYXZia09lSElkc0J4MCIsImQiOiJ7XCJhdHRyaWJ1dGVzXCI6e1wic3NvXCI6XCJkeHlfMzJ2eGI2MzdcIixcInZcIjo2NSxcIm1JZFwiOjM0MjEzMjY1OTY0MzM1NjIwOTV9LFwiaWRcIjozNDE3OTkwNjM3MzUyOTg0ODE4LFwidXNlcm5hbWVcIjpcIuermeS9j--8geWIq-i3kVwiLFwibWFya3NcIjoxNjAyLFwibW9tXCI6MjAyMDA2MjZ9IiwicyI6IjJmZjQwNWI2ZmFkNWE4MjNiMmViYjgwMmRjMmViYmZlOGYxNjBkYzkifQ==; CHD_TRACE_ID=3422062801073349540',
        'User-Agent	Mozilla/5.0 (iPhone; CPU iPhone OS 12_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 dxyapp_name/gaia dxyapp_ac/7c1d8e0a-a463-4428-b270-37410df888ae dxyapp_version/4.7.2 dxyapp_system_version/12.3.1 dxyapp_client_id/45ff4adfe045996bb720ac646b6a766d4c41d4c9 dxyapp_sid/D1B7AE8B-AA67-4ED2-9B7D-93DFCF3B9C5E': 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 dxyapp_name/gaia dxyapp_ac/7c1d8e0a-a463-4428-b270-37410df888ae dxyapp_version/4.7.2 dxyapp_system_version/12.3.1 dxyapp_client_id/45ff4adfe045996bb720ac646b6a766d4c41d4c9 dxyapp_sid/D1B7AE8B-AA67-4ED2-9B7D-93DFCF3B9C5E',
        'app-ac': '7c1d8e0a-a463-4428-b270-37410df888ae',
        'DXY-AUTH-TOKEN': 'TGT-410365-s447PV3u016SvnzeJSY5doedWvE4bf2kN2g-50',
        'app-os-version': '12.3.1'
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

def createPath(path):
    if os.path.exists(path) == False:
        os.makedirs(path)

def clearText(str):
    str = str.replace('/', '-')
    str = str.replace('【', '')
    str = str.replace('】', '')
    str = str.replace(' ', '')
    return str
def download_list(dir_list):
    for dirc in dir_list:
        title = dirc['title']
        path = base_download_path +'丁香妈妈大学/' + title + '/'
        catalogId = dirc['categoryId']
        # 生成主文件夹
        createPath(path)

        for column in dirc['columnList']:
            columnId = column['columnId']
            title2 = column['columnName']
            path2 = path   + title2 + '/'
            createPath(path2)

            # 拉取课程列表
            course_list = bilibiliParser.fetchDirLv2(catalogId,columnId)
            print("course_list.count",len(course_list))
            if (len(course_list) == 0):
                course_list = bilibiliParser.fetchDirLv24(catalogId,columnId)
            # print(title2, course_list)
            for course in course_list:
                course_name = clearText(course['title'])
                course_path = path2 + course_name + '/'
                print(course_path)
                # 生成课程文件夹
                createPath(course_path)
                # 拉取课程详情
                course_content = bilibiliParser.fetchContent(course['id'],columnId)
                # 开始写入 html文件
                html_path = course_path + clearText(course_content['title']) + '.html'
                html_content = html_tpl.replace('___content',course_content['body'])
                f = open(html_path, 'w')
                # f.write(html_content.encode('utf-8').decode('unicode_escape'))
                f.write(html_content)
                f.close()
                # 下载资源
                resource = course_content['resource']
                if (resource!= ""):
                    download_path = course_path + clearText(course_name) + '.m4a'
                    download_file(resource,download_path, False)
            # print('file', filen_path)
            # print('url', url)
            # #开始下载资源
            # download_file(url, filen_path, True)


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


dir_list = bilibiliParser.fetchDirLv1()

download_list(dir_list)
# print('list', dir_list)

# url = 'http://upos-hz-mirrorkodou.acgvideo.com/upgcxcode/78/22/69032278/69032278-1-6.mp4?e=ig8euxZM2rNcNbuVhwdVtWuVhwdVNEVEuCIv29hEn0l5QK==&deadline=1546157628&gen=playurl&nbs=1&oi=3080682485&os=kodou&platform=html5&trid=9a288cc91da7443699092ba914dff955&uipk=5&upsig=b31bf438a09693cb19c446166bb916eb'

# download_file(url, path)
