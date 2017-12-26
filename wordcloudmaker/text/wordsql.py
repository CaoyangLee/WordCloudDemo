# !/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb
from wordcloudmaker import files


class Comment():

    def create_txt(self):
        files.create_file('fanghua.txt')

    def connect(self):
        self.db = MySQLdb.connect(host='localhost',
                                  port=3306,
                                  user='root',
                                  passwd='20160101zz',
                                  db='scrapy',
                                  charset='utf8')
        self.cursor = self.db.cursor()

    def close(self):
        # 关闭数据库连接
        self.cursor.close()
        self.db.close()

    def query(self):
        with open('fanghua.txt', 'w', encoding='utf-8') as f:
            self.cursor.execute('select * from Comment')
            for (id, content) in self.cursor.fetchall():
                print('content=%s' % content)
                f.write(content + '\n')
        print('write file success')

    def do(self):
        self.create_txt()
        self.connect()
        self.query()
        self.close()


a = Comment()
a.do()
