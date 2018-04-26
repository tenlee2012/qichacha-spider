# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


import pymongo


class MongodbPipeline(object):

    def __init__(self, mongodb_uri, mongodb_db, mongodb_user, mongodb_pass, mongodb_coll):
        self.mongodb_uri = mongodb_uri
        self.mongodb_db = mongodb_db
        self.mongodb_user = mongodb_user
        self.mongodb_pass = mongodb_pass
        self.collection_name = mongodb_coll
        self.client = None
        self.db = None

    @classmethod
    def from_crawler(cls, crawler):
        """
         创建Item Pipeline对象是回调改类方法，通常在该方法中通过crawler.settings读取配置，创建
        :param crawler:
        :return:
        """
        mongodb_config = crawler.settings.get('MONGODB_CONFIG')
        return cls(
            mongodb_uri=mongodb_config.get('uri'),
            mongodb_db=mongodb_config.get('database', 'crawler'),
            mongodb_user=mongodb_config.get('user'),
            mongodb_pass=mongodb_config.get('password'),
            mongodb_coll=mongodb_config.get('collection'),
        )

    def open_spider(self, spider):
        """
        Spider打开时（处理数据前）回调改方法，通常在完成数据处理之前完成某些初始化工作，如链接数据库
        :param spider:
        :return:
        """
        self.client = pymongo.MongoClient(self.mongodb_uri)
        self.db = self.client[self.mongodb_db]
        self.db.authenticate(name=self.mongodb_user, password=self.mongodb_pass)
        # 创建索引
        self.db[self.collection_name].create_index([('uid', 1)], unique=True, name='unique_uid')
        self.db[self.collection_name].create_index([('name', pymongo.TEXT)], name='text_name')

    def close_spider(self, spider):
        """
        Spider关闭（处理数据后）回调改方法，通常用于完成清理工作
        :param spider:
        :return:
        """
        self.client.close()

    def process_item(self, item, spider):
        """
        数据处理
        :param item:
        :param spider:
        :return:
        """
        self.db[self.collection_name].update({'uid': item['uid']}, dict(item), True)
        return item
