# -*- coding: utf-8 -*-

import csv
import sqlite3

from os import path
from scrapy_price import settings


class ScrapyPricePipeline(object):
    def __init__(self):
        self.conn = None
        self.sql_filename = settings.sql_file_path
        self.csv_filename = settings.csv_file_path

    def process_item(self, item, spider):
        self.save_sql(item) if spider.output_format == 'sql' else self.save_csv(item)
        return item

    def open_spider(self, spider):
        if spider.output_format == 'sql':
            if path.exists(self.sql_filename):
                self.conn = sqlite3.connect(self.sql_filename)
            else:
                self.conn = self.create_table()

    def close_spider(self, spider):
        if self.conn is not None:
            self.conn.commit()
            self.conn.close()
            self.conn = None

    def create_table(self):
        conn = sqlite3.connect(self.sql_filename)
        conn.execute("""CREATE TABLE price_ua
                     (id  INTEGER PRIMARY KEY AUTOINCREMENT,
                     name CHAR(250), 
                     price REAL, 
                     description TEXT,
                     item_url CHAR(250),
                     item_photo CHAR(250) 
                     )""")
        conn.commit()
        return conn

    def save_sql(self, item):
        try:
            self.conn.execute(
                "insert into price_ua ('name', 'price', 'description', 'item_url', 'item_photo') values(?,?,?,?,?)",
                (item['name'],
                 item['price'],
                 item['description'],
                 item['item_url'],
                 item['item_photo']))
        except BaseException as e:
            print('Failed to insert item: ' + item['name'], e)

    def save_csv(self, item):
        with open(settings.csv_file_path, 'a') as csv_output:
            writer = csv.writer(csv_output, lineterminator='\n')
            writer.writerow([item[key] for key in ('name', 'price', 'description', 'item_url', 'item_photo')])
