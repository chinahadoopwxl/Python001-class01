# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

dbInfo = {
    'host' : 'localhost',
    'port' : 3306,
    'user' : 'root',
    'password' : 'root',
    'db' : 'maoyan',
    'charset' : 'utf8'
}

class SpidersPipeline:
    def __init__(self):
        self.host = dbInfo['host']
        self.port = dbInfo['port']
        self.user = dbInfo['user']
        self.password = dbInfo['password']
        self.db = dbInfo['db']
        self.charset = dbInfo['charset']
    
    def process_item(self, item, spider):
        conn = pymysql.connect(
            host = self.host,
            port = self.port,
            user = self.user,
            password = self.password,
            db = self.db,
            charset = self.charset
        )
        cur = conn.cursor()

        movie_name = item['movie_name']
        movie_type = item['movie_type']
        movie_time = item['movie_time']
        insert_sql = """
            insert into movie(movie_name, movie_type, movie_time)
            VALUES (%s, %s, %s)
        """
        try:
            cur.execute(insert_sql, (movie_name, movie_type, movie_time))
            cur.close()
            conn.commit()
        except:
            conn.rollback()
        finally:
            conn.close()
        return item