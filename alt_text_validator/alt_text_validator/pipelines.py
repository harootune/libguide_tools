# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import csv
import datetime

from .spiders.alt_text_validation_spider import ATVSpider
from .items import InvalidAltTextImage


class CSVOutput:
    """Handles csv writing throughout the spider's lifetime"""
    def __init__(self):
        self.file = None
        self.writer = None

    def open_spider(self, spider: ATVSpider) -> None:
        """
        Opens up the .csv file

        :param spider: the current ATVspider instance
        :return: None
        """
        filename = f'invalid_alt_text_crawl_{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.csv'

        self.file = open(filename, mode='w', newline='')
        self.writer = csv.writer(self.file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        self.writer.writerow(['origin', 'page_title', 'src'])

    def process_item(self, item: InvalidAltTextImage, spider: ATVSpider) -> InvalidAltTextImage:
        """
        Writes a row to the .csv file based on information from an InvalidAltTextImage item

        :param item: an InvalidAltTextImage item
        :param spider: the current ATVSpider
        :return: an InvalidAltTextImage item item to be passed further down the pipeline
        """
        self.writer.writerow([item['origin'], item['page_title'], item['src']])
        return item

    def close_spider(self, spider: ATVSpider) -> None:
        """
        Closes the .csv file

        :param spider: the current ATVSpider instance
        :return: None
        """
        self.file.close()
