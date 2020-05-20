# coding=utf-8
import urllib
import urllib.parse
import urllib.request
# 启动爬虫
from datetime import time
from urllib import parse
import time

with open('classfirstmuseum.txt','r',encoding='UTF-8') as file_obj:
    lines = file_obj.readlines()  # 按行读取每一个博物馆的名称
cnt=0
for line in lines:
    line = line.strip()
    cnt+=1
    # 项目名是MuseumNews，不能变，爬虫名是autospd也不变，kword和timee分别是要爬取的特定博物馆名称和新闻的时间范围，自己随意定
    test_data = {'project': 'MuseumNews', 'spider': 'autospd','kword':line,'timee':'3'}
    test_data_urlencode = parse.urlencode(test_data).encode("utf-8")

    requrl = "http://39.98.107.127:6800/schedule.json"

    # 以下是post请求
    req = urllib.request.Request(url=requrl, data=test_data_urlencode)

    res_data = urllib.request.urlopen(req)
    res = res_data.read()  # res 是str类型
    print(res)
    time.sleep(180)
    if cnt % 10 == 0:
        time.sleep(500)
    input()

# 查看日志
# 以下是get请求
# myproject = "MuseumNews"
# requrl = "http://39.98.107.127:6800/listjobs.json?project=" + myproject
# req = urllib.request.Request(requrl)
#
# res_data = urllib.request.urlopen(req)
# res = res_data.read()
# print(res)