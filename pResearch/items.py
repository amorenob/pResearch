# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PresearchItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    date = scrapy.Field()
    date_str = scrapy.Field()
    sub = scrapy.Field()
    name = scrapy.Field()
    brand = scrapy.Field()
    price = scrapy.Field()
    image_link = scrapy.Field()
    product_link = scrapy.Field()
    id = scrapy.Field()
    sells = scrapy.Field()
    location = scrapy.Field()
    pass


