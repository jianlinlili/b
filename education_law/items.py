# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class EducationLawItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    PublishingUnits = scrapy.Field()  # 发布单位
    ArticleUrl = scrapy.Field()  # 文章来源网站
    PublishTime = scrapy.Field()  # 文章发布时间
    Title = scrapy.Field()  # 标题

    CrawlTime = scrapy.Field()  # 爬取时间
    Area = scrapy.Field()  # 地区
    Content = scrapy.Field()  # 文章的类容
    Classification = scrapy.Field() # 分类
    Heat = scrapy.Field()  # 热度*
    Annex = scrapy.Field()  # 附件*

    pass
