# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import csv
import re

class BibleCrawlerPipeline(object):
    def process_item(self, item, spider):
        for key, value in item.items():
            item[key] = re.sub(r"([\t\n\r])", "", value).strip()
        return item

class SaveScrapedVerses(object):
    """
    Saving the data
    """
    def open_spider(self, spider):
        try:
            filename = spider.custom_settings['filename']
        except TypeError:
            filename = 'bible'
        
        self.file = open(f'data/{filename}.csv', encoding='utf-8', mode='w+')
        self.filewriter = csv.DictWriter(self.file, fieldnames=['book', 'verse', 'version'], delimiter=';', quotechar='"', lineterminator="\n")
        self.filewriter.writeheader()

    def close_spider(self,spider):
        self.file.close()

    def process_item(self, item, spider):
        self.filewriter.writerow(item)
        return item