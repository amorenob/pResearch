# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html



from sqlalchemy.orm import sessionmaker
from pResearch.models import Products, HInfo, db_connect, create_deals_table

# import logging
# import pymongo


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
