# Structure of these interfaces heavily inspired by the following thread;
# https://stackoverflow.com/questions/31662797/getting-scrapy-project-settings-when-script-is-outside-of-root-directory

# stdlib
import os
from typing import List

# third party
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


class AccessibilitySpiderInterface(object):
    """Provides a simple interface for interacting with ann accessibility spider outside of the scrapy project
    directory"""

    def __init__(self, spider_name: str, csv_path: str = ''):
        # environ
        # This ensures that the interface an be used outside of the scrapy project root directory
        settings_path = 'accessibility_spiders.uiuc_library.settings'
        os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_path)

        # attributes
        self.__spider_name = spider_name
        self.__csv_path = csv_path
        self.__process = CrawlerProcess(get_project_settings())
        self.__output = []

    def start_crawl(self, start_urls = List[str]) -> None:
        self.__process.crawl(self.__spider_name, start_urls=start_urls,
                             csv_path=self.__csv_path,
                             output=self.__output)
        self.__process.start()

    def get_output(self):
        return self.__output

    def clear_output(self):
        self.__output = []
