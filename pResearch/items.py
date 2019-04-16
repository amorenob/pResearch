# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PresearchItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    sub = scrapy.Field()
    name = scrapy.Field()
    brand = scrapy.Field()
    price = scrapy.Field()
    product_link = scrapy.Field()
    sku = scrapy.Field()
    qty_sold = scrapy.Field()
    location = scrapy.Field()
    pass



