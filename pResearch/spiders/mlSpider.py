# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime as dt
import re
from pResearch.items import PresearchItem
import logging

class MlibreSpider(scrapy.Spider):
    name = "mlibreSpider"

    #processed_item = set()
    #allowed_domains = ["www.mercadolibre.com"]
    #start_urls = ['http://www.mercadolibre.com/']
    def start_requests(self):
        #update categories
        url = 'https://www.mercadolibre.com.co/categories.html'
        yield scrapy.Request(url=url, callback=self.parse_urls)

    def parse_urls(self, response):
        urls = response.css('span.ch-g1-3 a::attr(href)').extract()
        for url in urls:
            print("Crawling url: {0}".format(url))
            yield scrapy.Request(url=url+"_BestSellers_YES", callback=self.parse)


    def parse(self, response):
        products = response.css('li.results-item.article.stack')
        #self.processed_item = self.processed_item.union(products)

        for product in products:
            sku = product.css('div.rowItem::attr(id)').extract_first()
            name = product.css('span.main-title::text').extract_first().strip()
            price = int(product.css('span.price__fraction::text').extract_first().replace('.', ''))
            sale_info = product.css('div.item__condition::text').extract_first().strip()
            product_link = product.css('a.item__info-title::attr(href)').extract_first()
            sub = response.url.split('/')[3]
            #print(product_id, name, price, sells, sub)
            #Filters
            #Not yiel item if it was allready processed
            #if product_id in self.processed_item:
            #    continue

            sells_search = re.findall("([0-9]*) vendidos", sale_info)
            qty_sold = int(sells_search[0]) if sells_search else 0
            # Filter products by sales
            if qty_sold < 20 or (qty_sold * price) < 500000:
                continue
            location_search = re.findall("vendidos - (.*)", sale_info)
            location = location_search[0] if location_search else ''
            item = PresearchItem()
            item['sub'] = sub
            item['name'] = name
            item['brand'] = ''
            item['price'] = price
            item['qty_sold'] = qty_sold
            item['location'] = location
            item['product_link'] = product_link
            item['sku'] = sku
            yield item
        #next_page = response.css('li.pagination__next a::attr(href)').extract_first()
        next_page = response.xpath('//a[@class="andes-pagination__link" and  span="Siguiente"]/@href').extract_first()
        
        #logging.debug('Items processed:     '+str(len(self.processed_item)))
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def get_category_links(self):

        pass

