# -*- coding: utf-8 -*-
import re
import time
import scrapy
from MuseumNews.items import MuseumnewsItem
from aip import AipNlp
from datetime import datetime
from scrapy.http import Request
import requests
from lxml import etree
import json

""" 你的 APPID AK SK """
APP_ID = '19552748'
API_KEY = 'fU8uuvwNlyj1kNnTjBRzGsMy'
SECRET_KEY = 'z0pfdOslGFFX1fipmcum1rDZHmnNBLl4'

client = AipNlp(APP_ID, API_KEY, SECRET_KEY)

nid = 1
startPage = 1
cnt = 0


# URL="http://news.baidu.com/ns?word=%E5%8D%9A%E7%89%A9%E9%A6%86&pn={page}&cl=2&ct=0&tn=newsdy&rn=40&ie=utf-8"

class Startspider(scrapy.Spider):
    # headers = {
    #     # 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    #     "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.8.1.7) Gecko/20070914 Firefox/2.0.0.7",
    #     'Connection': 'close',
    # }
    URL = 'https://www.baidu.com/s?rtt=1&bsst=1&cl=2&tn=news&word=博物馆'
    name = 'autospd'
    allowed_domains = ['baidu.com']
    page = startPage
    start_urls = [URL]
    end = False
    flag = set()
    dt = datetime.strftime(datetime.now(), "%Y-%m-%d")
    timee = 365

    # print(dt)
    def __init__(self, kword=None, timee=0, *args, **kwargs):  # 传参的实现
        super(Startspider, self).__init__(*args, **kwargs)
        # self.URL = self.URL.format(kword)
        # self.start_urls = [self.URL]
        self.start_urls = ['https://www.baidu.com/s?rtt=1&bsst=1&cl=2&tn=news&word=%s'%kword]
        self.timee = timee
        # print(self.URL)

    def get_emotion(self, data):  # 情感分析
        #定义百度API情感分析的token值和URL值
        token = '24.6c35da63430c9d1bab6e33974e304937.2592000.1590290924.282335-19580524'
        url = 'https://aip.baidubce.com/rpc/2.0/nlp/v1/sentiment_classify?charset=UTF-8&access_token={}'.format(
            token)

        # 将text按照lenth长度分为不同的几段
        def cut_text(text, lenth):
            textArr = re.findall('.{' + str(lenth) + '}', text)
            textArr.append(text[(len(textArr) * lenth):])
            return textArr

        # 百度情感分析API的上限是2048字节，因此判断文章字节数小于2048，则直接调用
        if (len(data.encode()) < 2048):
            # print(data)
            new_each = {
                'text': data
            }
            new_each = json.dumps(new_each) #利用URL请求百度情感分析API
            res = requests.post(url, data=new_each)
            # print("content: ", res.content)
            res_text = res.text #保存分析得到的结果，以string格式保存
            result = res_text.find('items') #查找得到的结果中是否有items这一项
            positive = 1
            if (result != -1):
                json_data = json.loads(res.text)
                negative = (json_data['items'][0]['negative_prob']) #得到消极指数值
                positive = (json_data['items'][0]['positive_prob']) #得到积极指数值
                # print(positive)
                if (positive > negative):  # 如果积极大于消极，则返回2
                    return 2
                elif (positive == negative):
                    return 1
                else:
                    return 0
            else:
                return 1
        else:
            data = cut_text(data, 1500)
            # print(data)
            sum_positive = 0.0
            sum_negative = 0.0
            for each in data:
                # print(each)
                new_each = {
                    'text': each  #将文本数据保存在变量new_each中
                }
                new_each = json.dumps(new_each)
                res = requests.post(url, data=new_each)
                # print("content: ", res.content)
                res_text = res.text
                result = res_text.find('items')
                if (result != -1):
                    json_data = json.loads(res.text)
                    positive = (json_data['items'][0]['positive_prob'])
                    negative = (json_data['items'][0]['negative_prob'])
                    sum_positive = sum_positive + positive
                    sum_negative = sum_negative + negative
                    # print(positive)
            # print("res:", sum / count)
            if (sum_positive > sum_negative):
                return 2
            elif (sum_positive == sum_negative):
                return 1
            else:
                return 0

    def parse(self, response):
        res = response.xpath('//div[@class="result"]')
        for each in res:
            title = each.xpath('./h3/a//text()').extract()  # 要用相对地址
            title = ''.join(title)
            title = title.replace('\n', '').replace('\r', '').replace(' ', '')
            if title in self.flag:  # 避免重复爬取
                continue
            self.flag.add(title)
            ans = [i.strip() for i in each.xpath('.//div//p[@class="c-author"]/text()').extract() if i.strip()][
                0].split()
            author = ans[0]
            ptime = ''.join(ans[1])
            if ptime.find('年') != -1:
                ptime = ptime.replace('年', '-').replace('月', '-').replace('日', '')
            else:
                ptime = self.dt
            tt = datetime.strptime(ptime, "%Y-%m-%d")
            mt = datetime.strptime(self.dt, "%Y-%m-%d")
            # print(bt)
            # print(tt)
            print(self.timee)
            if (mt - tt).days < int(self.timee):
                url = each.xpath('h3[@class="c-title"]/a/@href').extract()[0]

                introduct = each.xpath('.//div[@class="c-span18 c-span-last"]/text()').extract()
                introduct = ''.join(introduct)
                if introduct == '':
                    introduct = each.xpath('.//h3[@class="c-title"]/following-sibling::*[1]/text()').extract()
                    introduct = ''.join(introduct)
                introduct = introduct.replace('\n', '').replace('\r', '').replace(' ', '')

                # img_url = each.xpath('.//img[@class="c-img c-img6"]//@src').extract_first()

                item = MuseumnewsItem()
                item['title'] = title
                item['url'] = url
                item['author'] = author
                item['releasetime'] = ptime
                item['extract'] = introduct

                # yield scrapy.Request(item["url"], callback=self.parse_detail(), meta={"item": item})
                # if img_url:
                #     item['imgurl'] = img_url
                # else:  # 没有图片就忽略item['img']
                #     # item['imgurl'] = ""
                #     item['imgurl'] = ""
                r = requests.get(url)
                e = etree.HTML(r.text)
                all_p = e.xpath('//div[@class="article-content"]//p')
                content = []
                for c in all_p:
                    info = c.xpath('string(.)')
                    content.append(info)
                content_str = ''.join(content)
                item['content'] = content_str

                img_url = e.xpath('//div[@class="article-content"]//img//@src')
                if img_url:
                    img_url = img_url[0]
                if img_url:
                    item['imgurl'] = img_url
                else:  # 没有图片就忽略item['img']
                    # item['imgurl'] = ""
                    item['imgurl'] = ""

                with open('C:\museum.txt') as file_obj:
                    lines = file_obj.readlines()  #按行读取每一个博物馆的名称

                for line in lines:
                    if line[0] == '#':
                        lines.remove(line)
                sign = []  # 定义标签存储变量
                for line in lines:  # 遍历所有博物馆的名称
                    result1 = content_str.find(line.strip())  # 在新闻内容中查找是否有该博物馆名称
                    if (result1 != -1):  # 如果结果不等于-1，则添加
                        sign.append(line.strip())
                        sign.append(",")
                    result2 = title.find(line.strip())  # 在新闻标题中查找
                    if (result2 != -1 and result1 == -1):  # 如果存在，添加
                        sign.append(line.strip())
                        sign.append(",")
                # for x in sign:
                # print(x)
                # sign=''.join(sign) #将其添加至该新闻的标签值中
                item['sign'] = sign  # 保存该新闻的标签值
                item['nature'] = self.get_emotion(content_str)  # 保存该新闻的性质（正向、负向、中间）值

                if item['title'] != "" and item['url'] != "" and item['author'] != "" and item['author'] != "三秦网"and item['author'] != "德州新闻网" and item['releasetime'] != "" and item['extract'] != "" and item['content'] != "":
                    # item['nid'] = nid
                    # nid = nid + 1
                    yield item

        next_url = response.xpath("//a[text()='下一页>']//@href").extract_first()
        if next_url:
            time.sleep(5)
            next_url = response.urljoin(next_url)
            yield Request(next_url, callback=self.parse, dont_filter=True, headers={'Connection':'close'})