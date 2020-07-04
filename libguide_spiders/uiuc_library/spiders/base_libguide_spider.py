# stdlib
from typing import List, Union

# third party
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class LibGuideSpider(CrawlSpider):
    """The base class for all LibGuide-oriented spiders in this application. No effect when run."""
    # Class variables
    custom_settings = {
        'ITEM_PIPELINES': {
                           'libguide_spiders.uiuc_library.pipelines.CSVOutput': 500,
                        },
    }

    def __init__(self, start_urls: Union[List[str], str], csv_path: str, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # get our start urls
        try:
            self.start_urls = start_urls.split(',')
        except AttributeError:
            self.start_urls = start_urls
        print(self.start_urls)

        # Pipeline-related attributes
        self.csv_path = csv_path

