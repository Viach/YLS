# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv
from scrapy_price import settings


def save_data_to_csv(item):
    writer = csv.writer(open(settings.csv_file_path, 'a'), lineterminator='\n')
    writer.writerow([item[key] for key in item.keys()])


class ScrapyPricePipeline(object):

    def __init__(self):
        pass

    def process_item(self, item, spider):
        save_data_to_csv(item)
        return item
