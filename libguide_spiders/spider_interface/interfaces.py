# Structure of these interfaces heavily inspired by the following thread;
# https://stackoverflow.com/questions/31662797/getting-scrapy-project-settings-when-script-is-outside-of-root-directory

# stdlib
import os
from typing import List

# third party
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


class LibguideSpiderInterface(object):
    """Provides a simple interface for interacting with ann accessibility spider outside of the scrapy project
    directory"""

    def __init__(self, spider_name: str, csv_path: str = '', extractor_config: dict = None, parse_config: dict = None):
        # environ
        # This ensures that the interface an be used outside of the scrapy project root directory
        settings_path = 'libguide_spiders.uiuc_library.settings'
        os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_path)

        # internal process
        self.__process = CrawlerProcess(get_project_settings())

        # attributes
        self.spider_name = spider_name

        ## Pipeline related attributes
        self.csv_path = csv_path

        ## Spider config related attributes
        self.extractor_config = extractor_config
        self.parse_config = parse_config

    def start_crawl(self, start_urls = List[str]) -> None:
        self.__process.crawl(self.spider_name,
                             start_urls=start_urls,
                             csv_path=self.csv_path,
                             extractor_config=self.extractor_config,
                             parse_config=self.parse_config,)
        self.__process.start()
