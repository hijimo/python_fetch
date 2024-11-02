# -*- coding: utf-8 -*-
#!/bin/env python

# @Author: jimo
# @Date:   2018-12-30 10:51:37
# @Last Modified by:   jimo
# @Last Modified time: 2019-01-14 19:35:07
# 如果报证书错误， python3.6以上用户进入 mac->应用程序->python3.x-> Install Certificates.command

import requests

from bs4 import BeautifulSoup

import re
import json
import copy


# test_url = 'https://mama.dxy.com/japi/platform/201720020?columnId=3284317633650361633'
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
# test_url ='https://www.bilibili.com/'
class bilibiliParser(object):
  def __init__():
    print('init')

  def fetchDirLv1(columnId):
    api = 'https://mama.dxy.com/japi/platform/201720001'
    params = {
      'asc': 1,
      'columnId': columnId,
    }
    h = copy.copy(headers)


    ret = requests.get(api, headers=h, params=params)
    
    return json.loads(ret.text)['results']['items']

  def fetchDirLv2(catalogId, columnId):
    api = 'https://mama.dxy.com/japi/platform/201720002'
    params = {
      'catalogId': catalogId,
      'columnId': columnId,
      'catalogMode': 1
    }
    h = copy.copy(headers)
    ret = requests.get(api, headers=h, params=params)
    
    return json.loads(ret.text)['results']['items']
  def fetchContent(id, columnId):
    api = 'https://mama.dxy.com/japi/platform/200920023'
    params = {
      'id': id,
      'columnId': columnId,
      
    }
    h = copy.copy(headers)
    ret = requests.get(api, headers=h, params=params)
    return json.loads(ret.text)['results']['item']


  def fetchHtml(url):
  	
    h = copy.copy(headers)
    # h['Upgrade-Insecure-Requests'] = 1
    h['Accept-Language'] = 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2'
    # h['Cookie'] = 'LIVE_BUVID=AUTO2315407326899386; stardustvideo=1; CURRENT_FNVAL=16; buvid3=B777F5F3-1243-409A-8684-1DAB8FF32A2A19602infoc; rpdid=iwxiipkmlqdospwmkixqw; fts=1540740910; UM_distinctid=166bb534ecb6d7-03c28767212c73-346a7808-fa000-166bb534ecc48; _uuid=E2846997-B64D-16D9-0873-B8F45B9CD78609333infoc; sid=cynikqad; finger=14bc3c4e; CURRENT_QUALITY=64; flash_player_gray=false; BANGUMI_SS_25739_REC=250472; BANGUMI_SS_25681_REC=250623; bp_t_offset_161660186=203130976482611657; DedeUserID=161660186; DedeUserID__ckMd5=cf312c2c07371111; SESSDATA=c486ee73%2C1548743510%2C12f368c1; bili_jct=44859482995b0e7dc27fc0cd8bf0196f; _dfcaptcha=201bb57f912216fc36de36da1249a14d'
  	
    ret = requests.get(url, headers=h)

    # print('ret', ret.text)
    return ret.text
  	# return ret.text

  def parse_html(html_doc):
  	return BeautifulSoup(html_doc, 'html.parser')

  def parserVideoUrlByHtml(soup):
    
    scripts = soup.find_all('script', string=re.compile("__playinfo__"))
    video_info = ''

    if len(scripts) > 0:
    	script = scripts[0].contents[0]
    	json_str = script[20:len(script)]
    	video_info = json.loads(json_str)
    	for key in video_info:
    		print('*** key %s , value: %s',key, 'a')
    if 'durl' in video_info:
      return video_info['durl'][0]['url']
    if 'data' in video_info:
      return video_info['data']['durl'][0]['url']
    # if 'data' in video_info:
      # return video_info['data']['dash']['video'][0]['baseUrl']


  def parsePlayUrlResponse(ret):
    response_text = ret.text
    return json.loads(response_text)['durl'][0]['url']

  def getVideoUrlByAid(aid):
    api = 'https://api.bilibili.com/playurl'
    id = str(aid)
    params = {
      'aid': id,
      'page': 1,
      'platform': 'html5',
      'quality': 1,
      'vtype': 'mp4',
      'type': 'json'
    }
    h = copy.copy(headers)
    h['Referer'] = 'https://space.bilibili.com/' + id + '/'
    h['Host'] = 'api.bilibili.com'
    h['Cookie'] = 'CURRENT_FNVAL=16; sid=c53doy2g; buvid3=14EFECE2-9938-447F-A390-590B26BAFA2481651infoc'

    ret = requests.get(api, headers=h, params=params)
    return bilibiliParser.parsePlayUrlResponse(ret)
    
    # api = 'https://www.bilibili.com/video/av' + str(aid)
    # html_doc = bilibiliParser.fetchHtml(api)
    # return bilibiliParser.parserVideoUrlByHtml(bilibiliParser.parse_html(html_doc))

  # def parseVideInfoByHtml(soup):
    
  #   scripts = soup.find_all('script', string=re.compile("__INITIAL_STATE__"))
  #   video_info = ''
  #   if len(scripts) > 0:
  #   	script = scripts[0].contents[0]
  #   	json_str = script[25:len(script) - 122]
  #   	video_info = json.loads(json_str)
  #   	video_info['url'] = bilibiliParser.parserVideoUrlByHtml(soup)
  #   	# for key in video_info:
  #   	# 	print('*** key %s , value: %s',key, 'a')	

  #   return video_info



# print(bilibiliParser.fetchVideoList('171671943', keyword='真香'))
# html_doc = bilibiliParser.fetchHtml(test_url)
# soup = bilibiliParser.parse_html(html_doc)
# video = bilibiliParser.parseVideInfoByHtml(soup)



