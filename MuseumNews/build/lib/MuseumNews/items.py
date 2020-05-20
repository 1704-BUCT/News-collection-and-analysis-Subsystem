# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MuseumnewsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    url = scrapy.Field()
    releasetime = scrapy.Field()
    extract = scrapy.Field()
    imgurl = scrapy.Field()
    # imgpath =scrapy.Field()
    # large_imgs = scrapy.Field()
    content = scrapy.Field()
    sign = scrapy.Field()
    nature = scrapy.Field()
    pass
