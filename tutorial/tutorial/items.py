# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

# Item 是保存爬取到的数据的容器；其使用方法和python字典类似
import scrapy


class TutorialItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class CnnItem(scrapy.Item):
    
    title = scrapy.Field() # 标题
    # link = scrapy.Field()
    content = scrapy.Field() # 内容地址
    author = scrapy.Field() # 作者
    update_time = scrapy.Field() # 发布时间
    url = scrapy.Field() # 网址
    types = scrapy.Field() # 类别
    pic = scrapy.Field() # 图片url
    cover_rate = scrapy.Field() # 覆盖率
    totalLett = scrapy.Field() # 单词数目

