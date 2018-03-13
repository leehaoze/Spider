# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JDPage(scrapy.Item):
    type = scrapy.Field()
    crawl_time = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()


class JDProductItem(scrapy.Item):
    type = scrapy.Field()
    crawl_time = scrapy.Field()
    url = scrapy.Field()
    product_id = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    store_name = scrapy.Field()
    store_id = scrapy.Field()
    store_url = scrapy.Field()
    product_info = scrapy.Field()
    good_rate = scrapy.Field()
    after_comment = scrapy.Field()
    good_comment = scrapy.Field()
    medium_comment = scrapy.Field()
    bad_comment = scrapy.Field()
    product_tags = scrapy.Field()

class CSDNArticle(scrapy.Item):
    title = scrapy.Field()
    author = scrapy.Field()
    url = scrapy.Field()
    content = scrapy.Field()

class CSDANews(scrapy.Item):
    title = scrapy.Field()
    descrption = scrapy.Field()
    url = scrapy.Field()
    content = scrapy.Field()
