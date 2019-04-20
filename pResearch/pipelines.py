# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
import os
from datetime import datetime as dt
from scrapy.exceptions import DropItem
from sqlalchemy.orm import sessionmaker
from pResearch.models import Products, HInfo, db_connect, create_deals_table

# import logging

class ItemFilterPipeline(object):
    """ Pipeline for filtering items by 
    """
    def process_item(self, item, spider):
        if item['qty_sold'] < 20 or (item['qty_sold'] * item['price']) < 500000:
            raise DropItem("Item do not pass the criteria: {0}".format(item))
        else:
            return item

class JustOnePerWeekPipeline(object):
    """Pipeline for keeping a weekly cache file of seen items"""
    path = os.curdir + '/cache'
    
    def __init__(self):
        self.seen_item = set()
        self.fname = '_'.join(['seen', dt.today().strftime('%Y%m'), "w", self.week_of_month()])
        self.file = None

    def week_of_month(self):
        """ Returns the week of the month for the specified date.
        """
        day_of_month = dt.today().day
        return str((day_of_month - 1) // 7 + 1)
    
    def open_spider(self, spider):
        """ Update seen items set from file
        """
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        file_name =  '_'.join(['seen', dt.today().strftime('%Y%m'), "w", self.week_of_month()])
        self.file = open(os.path.join(self.path, file_name), 'a+')
        self.file.seek(0)
        self.seen_item.update(x.rstrip() for x in self.file)


    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        if item['sku'] in self.seen_item:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.seen_item.add(item['sku'])
            self.file.write(item['sku'] + os.linesep)
            return item

class PresearchPipelinePgsqlDB(object):
    """Pipeline for storing scraped items in the  Pgsql database"""

    def __init__(self):
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
