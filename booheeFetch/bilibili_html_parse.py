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
        'Host': 'food.boohee.com',
        'Cookie': 'sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2299087142%22%2C%22%24device_id%22%3A%221727f735e1e4be-022c7c4bffdf46-645e7c07-304500-1727f735e1fc09%22%2C%22props%22%3A%7B%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%2C%22first_id%22%3A%2217322079a09121a-03c1d838292a308-645e7c04-304500-17322079a0a13e2%22%7D',
        'User-Agent':'boohee/ios',
        
        'Token': '9c7ABZH8s6QsUMFQrx8f8Bu2x8Aai3Tq',
        
}
# test_url ='https://www.bilibili.com/'
class bilibiliParser(object):
  def __init__():
    print('init')

  def fetchDirLv1(page,keyword):
    api = 'https://food.boohee.com/fb/v1/search'
    params = {
      'user_favorite_food': 1,
      'page_from':'record_diet',
      'page': page,
      'q':keyword,
    }
    h = copy.copy(headers)


    ret = requests.get(api, headers=h, params=params)
    
    return json.loads(ret.text)

# https://food.boohee.com/fb/v2/foods/fd8d94c3/detail?tenant=null&platform=app
  def fetchDirLv2(code):
    api = 'https://food.boohee.com/fb/v2/foods/'+ str(code)+'/detail'
    # api = 'https://food.boohee.com/fb/v1/foods/'+str(code)
    params = {
      'tenant': 'null',
      'platform': 'app'
    }
    h = copy.copy(headers)
    ret = requests.get(api, headers=h, params=params)
    return json.loads(ret.text)

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
  	# url = 'http://www.boohee.com/shiwu/' + str(id)
    ret = requests.get(url)
    return ret.text
  def parse_html(html_doc):
  	return BeautifulSoup(html_doc, 'html.parser')
  
  def getCodeInHtml(soup):
    doms = soup.find_all("a",string="健身人群")
    if (len(doms)>0):
      ary =  doms[0]["href"].split("/")
      return ary[len(ary)-1]
    return ''

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



