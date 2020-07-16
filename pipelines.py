# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient

class BookparserPipeline:
    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.mongo_base = self.client.books

    def process_item(self, item, spider):
        price_new = item['price_new']
        collection = self.mongo_base[spider.name]
        collection.insert_one(item)

        def price_discount_processing(self, price_new):
                if price_new:
                    item['price_new'] = int(item['price_new'])
                else:
                    item['price_new'] = None

        return item
    def __del__(self):
        self.client.close()