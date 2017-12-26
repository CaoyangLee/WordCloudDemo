# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb


class CommentanalysisPipeline(object):

    def __init__(self):
        self.db = MySQLdb.connect(host='localhost',
                                  port=3306,
                                  user='root',
                                  passwd='20160101zz',  # 本地密码
                                  db='scrapy',
                                  charset='utf8')
        self.cursor = self.db.cursor()

    def process_item(self, item, spider):
        self.cursor.executemany('insert into Comment (content) VALUE (%s)', [item['content'], ])
        self.db.commit()
        print('插入数据库完成')
        return item
