# stdlib
from urllib import parse
from typing import List, Union

# third party
from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor


class LibGuideSpider(CrawlSpider):
    """The base class for all LibGuide-oriented spiders in this application. No effect when run."""
    # Class variables
    custom_settings = {
        'ITEM_PIPELINES': {
                           'libguide_spiders.uiuc_library.pipelines.CSVOutput': 500,
                        },
    }

    def __init__(self, start_urls: Union[List[str], str], csv_path: str, parse_config: dict, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # get our start urls
        try:
            self.start_urls = start_urls.split(',')
        except AttributeError:
            self.start_urls = start_urls

        # Pipeline-related attributes
        self.csv_path = csv_path
        self.parse_config = parse_config

    @classmethod
    def construct_follow_rule(cls, callback: str, extractor_config: dict) -> None:
        if extractor_config:
            follow_extractor = LinkExtractor(**extractor_config)
        else:
            follow_extractor = LinkExtractor()


        follow_rule = Rule(follow_extractor,
                           callback=callback if callback else None,
                           follow=True)  # TODO: add support for other Rule parameters?

        if cls.rules:
            cls.rules += (follow_rule,)
        else:
            cls.rules = (follow_rule,)

