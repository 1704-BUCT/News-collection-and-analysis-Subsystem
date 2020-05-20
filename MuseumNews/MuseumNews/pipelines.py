# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import codecs
import json

from scrapy.exceptions import DropItem
from scrapy.http import Request
from logging import log
import pymysql
from scrapy.pipelines.images import ImagesPipeline

from MuseumNews import settings
class MuseumnewsPipeline(object):
    def process_item(self, item, spider):
        return item

class DBspiderpipeline(object):
    def __init__(self):
        self.connect = pymysql.connect(
            host = settings.MYSQL_HOST,
            port = 3306,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            charset='utf8',
            use_unicode=True
        )
        self.cursor=self.connect.cursor()

    def process_item(self,item,spider):
        title = item['title']
        try:
            self.cursor.execute(
                "select title from news where title = '{}' ".format(title)
            )
            repetiton = self.cursor.fetchone()
            if repetiton:
                pass
            else:
                for each in item['sign']: #遍历该项的每一个标签值
                    # print("sign:", each)
                    if each!=",":
                        self.cursor.execute(  #并将其标签值和对应的标题存储在nrm表中
                            "insert into nmr(title,sign) values ('{}','{}')".format(
                                pymysql.escape_string(item['title']), pymysql.escape_string(each)
                            )
                        )
                self.connect.commit() #提交
                signn =  item['sign'] #保存该项的标签值
                sign_ = [] #存储新的标签值
                for each in signn:
                    sign_.append(each) #将标签值添加到新的存储列表中
                sign_ = ''.join(sign_) #将标签值转化为字符串格式
                self.cursor.execute(   #向news表中添加数据
                    "insert into news(nature,title,author,url,sign,content,extract,releasetime,imgurl) values ('{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(
                        str(item['nature']), pymysql.escape_string(item['title']),
                        pymysql.escape_string(item['author']), pymysql.escape_string(item['url']),
                        sign_, pymysql.escape_string(item['content']),
                        pymysql.escape_string(item['extract']), pymysql.escape_string(item['releasetime']),
                        pymysql.escape_string(item['imgurl'])
                    )
                )
                self.connect.commit()
        except Exception as error:
            log(error)

#
# class ImgDownloadPipeline(ImagesPipeline):
#     default_headers = {
#         'referer': '',
#         'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.54 Safari/536.5',
#     }
#
#     def get_media_requests(self, item, info):
#         for image_url in item['imgurl']:
#             self.default_headers['referer'] = image_url
#             yield Request(image_url, headers=self.default_headers)
#
#     def item_completed(self, results, item, info):
#         image_paths = [x['path'] for ok, x in results if ok]
#         if not image_paths:
#             item['imgpath'] = ""
#             return item
#         image_paths="".join(image_paths)
#         image_paths="E:/SoftwareProject/STORE_IMAGE/"+image_paths
#         item['imgpath'] = pymysql.escape_string(image_paths)
#         return item

