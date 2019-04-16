# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
import os
import csv
from datetime import datetime as dt
from scrapy.exceptions import DropItem
from sqlalchemy.orm import sessionmaker
from pResearch.models import Products, HInfo, db_connect, create_deals_table

# import logging
# import pymongo

class JustOnePerDayPipeline(object):
    path = os.curdir + '/cache'
    
    def __init__(self):
        self.seen_item = set()
        self.fname = self.path+ '/'+ dt.today().strftime('%Y%m%d') + '.csv'

    def open_spider(self, spider):
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        if os.path.isfile(self.fname):
            with open(self.fname, 'r') as f:
                self.seen_item.update([sku.strip() for sku in f])

    def close_spider(self, spider):
        with open(self.fname, 'w') as outf:
            writer = csv.writer(outf,  delimiter='\n')
            writer.writerow(list(self.seen_item))

    def process_item(self, item, spider):
        if item['sku'] in self.seen_item:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.seen_item.add(item['sku'])
            return item

class PresearchPipelinePgsqlDB(object):
    """Livingsocial pipeline for storing scraped items in the database"""

    def __init__(self):
        self.crawled_items = []
        """
        Initializes database connection and sessionmaker.
        Creates deals table.
        """
        engine = db_connect()
        create_deals_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        """Save deals in the database.

        This method is called for every item pipeline component.

        """
        # skip item if it has alredy been loaded
        if item['id'] in self.crawled_items:
            return item
        self.crawled_items.append(item['id'])
        prices_subitem = {k: item[k] for k in ('date', 'date_str', 'price', 'id', 'sells') if k in item}
        prices_subitem['id_product'] = prices_subitem.pop('id')
        session = self.Session()
        product = Products(**item)
        h_info = HInfo(**prices_subitem)
        try:
            session.merge(product)
            session.commit()
            session.add(h_info)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return item


class MongoPipeline(object):
    collection_name = 'mlProducts'
    time_serie_collection_name = 'mlSales'
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        #self.db[self.collection_name].insert_one(dict(item))
        key = {'sku':item['sku']}
        sales_info = {k: dict(item)[k] for k in ('qty_sold', 'sku')}
        self.db[self.collection_name].update(key, item, upsert=True)
        self.db[self.time_serie_collection_name].insert_one(sales_info)
        return item
