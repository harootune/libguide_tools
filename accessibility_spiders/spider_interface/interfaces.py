# Structure of these interfaces heavily inspired by the following thread;
# https://stackoverflow.com/questions/31662797/getting-scrapy-project-settings-when-script-is-outside-of-root-directory

# stdlib
import os
import warnings
from typing import List

# third party
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


class AccessibilitySpiderInterface(object):
    """Provides a simple interface for interacting with ann accessibility spider outside of the scrapy project
    directory"""

    def __init__(self, spider_name: str, csv: bool = False, db: bool = False, list_output: bool = True,
                 csv_path: str = '', db_path: str = '', extractor_config: dict = None, parse_config: dict = None):
        # environ
        # This ensures that the interface an be used outside of the scrapy project root directory
        settings_path = 'accessibility_spiders.uiuc_library.settings'
        os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_path)

        # internal process
        self.__process = CrawlerProcess(get_project_settings())

        # attributes
        self.spider_name = spider_name

        ## Pipeline related attributes
        self.csv = csv
        self.db = db
        self.list_output = list_output
        self.csv_path = csv_path
        self.db_path = db_path
        self.output_target = [] if list_output else None

        ## Spider config related attributes
        self.extractor_config = extractor_config
        self.parse_config = parse_config

    def start_crawl(self, start_urls = List[str]) -> None:
        self.__process.crawl(self.spider_name,
                             start_urls=start_urls,
                             csv=self.csv,
                             db=self.db,
                             list_output=self.list_output,
                             csv_path=self.csv_path,
                             db_path=self.db_path,
                             output_target=self.output_target,
                             extractor_config=self.extractor_config,
                             parse_config=self.parse_config,)
        self.__process.start()

    def get_output(self):
        if self.list_output:
            return self.output_target
        else:
            warnings.warn('AccessibilitySpiderInterface instance has list output disabled')

    def clear_output(self):
        if self.list_output:
            self.output_target.clear()
        else:
            warnings.warn('AccessibilitySpiderInterface instance has list output disabled')
