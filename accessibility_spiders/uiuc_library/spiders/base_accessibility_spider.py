# stdlib
from typing import List

# third party
from scrapy.spiders import CrawlSpider
from scrapy.item import Item


class AccessibilitySpider(CrawlSpider):
    """A basic spider that other accessibility spiders inherit from. Defines a common interface expected by the
    spider_interfaces package"""
    name = 'acc-spider'

    def __init__(self, start_urls: List[str] = '', csv_path: str = '', output: List[Item] = None,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = start_urls
        self.csv_path = csv_path
        self.output = output

