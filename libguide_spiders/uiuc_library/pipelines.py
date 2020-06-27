# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# stdlib
import csv
import datetime
from pathlib import Path

# third_party
from scrapy.item import Item
from scrapy.exporters import CsvItemExporter

# local
from libguide_spiders.uiuc_library.spiders.base_libguide_spider import LibGuideSpider


class CSVOutput:
    """Handles csv writing throughout the spider's lifetime"""
    def __init__(self):
        self.__file = None
        self.__exporter = None

    def open_spider(self, spider: LibGuideSpider) -> None:
        """
        Opens up the .csv file

        :param spider: the current ATVspider instance
        :return: None
        """
        if spider.csv_path:
            filename = spider.csv_path
        else:
            filename = f'{spider.name}_{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.csv'
        filepath = Path(filename)

        self.__file = open(filepath, mode='wb')
        self.__exporter = CsvItemExporter(self.__file, include_headers_line=True,
                                          delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        self.__exporter.start_exporting()

    def process_item(self, item: Item, spider: LibGuideSpider) -> Item:
        """
        Writes a row to the .csv file based on information from an InvalidAltTextImage item

        :param item: an InvalidAltTextImage item
        :param spider: the current ATVSpider
        :return: an InvalidAltTextImage item item to be passed further down the pipeline
        """
        self.__exporter.export_item(item)
        return item

    def close_spider(self, spider: LibGuideSpider) -> None:
        """
        Closes the .csv file

        :param spider: the current ATVSpider instance
        :return: None
        """
        self.__exporter.finish_exporting()
        self.__file.close()


