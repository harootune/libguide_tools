# third party
from scrapy_dynamic_spiders.wranglers import SpiderWrangler
from scrapy.utils.project import get_project_settings

# local
from libguide_spiders.uiuc_library.spiders.broken_link_spider import BLSpider
from libguide_spiders.uiuc_library.spiders.sfx_vufind_spider import SVSpider
from libguide_spiders.spider_interface.interfaces import LibguideSpiderInterface


def main():
    wrangler = SpiderWrangler(get_project_settings(), gen_spiders=False, spidercls=BLSpider)

    # start a crawl
    wrangler.start_crawl(start_urls='https://guides.library.illinois.edu/arabspringworkshop', csv_path='../demo.csv')


if __name__ == '__main__':
    main()

