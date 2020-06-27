# stdlib
from typing import List, Union

# third party
from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor


class AccessibilitySpider(CrawlSpider):
    """A basic spider that other accessibility spiders inherit from. Defines a common interface expected by the
    spider_interfaces package.

    DO NOT INSTANTIATE THIS SPIDER DIRECTLY"""
    custom_settings = {
         'ITEM_PIPELINES': {
             'accessibility_spiders.uiuc_library.pipelines.CSVOutput': 300,
             'accessibility_spiders.uiuc_library.pipelines.DBOutput': 500,
             'accessibility_spiders.uiuc_library.pipelines.ListOutput': 700
         }
    }

    def __init__(self, start_urls: Union[List[str], str], csv: bool, db: bool, list_output: bool,
                 csv_path: str, db_path: str, output_target: list, parse_config: dict, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # get our start urls
        try:
            self.start_urls = start_urls.split(',')
        except AttributeError:
            self.start_urls = start_urls

        # Pipeline-related attributes
        self.csv = csv
        self.db = db
        self.list_output = list_output
        self.csv_path = csv_path
        self.db_path = db_path
        self.output_target = output_target
        self.parse_config = parse_config

    @classmethod
    def construct_follow_rule(cls, callback: str, **kwargs) -> None:
        follow_extractor = LinkExtractor(**kwargs)
        follow_rule = Rule(follow_extractor, callback=callback, follow=True)  # TODO: add support for other Rule parameters?

        if cls.rules:
            cls.rules += (follow_rule,)
        else:
            cls.rules = (follow_rule,)



