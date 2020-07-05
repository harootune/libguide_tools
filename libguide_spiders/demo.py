# third party
from scrapy_dynamic_spiders.wranglers import SpiderWrangler
from scrapy.utils.project import get_project_settings

# local
from libguide_spiders.uiuc_library.spiders.broken_link_spider import BLSpider
from libguide_spiders.uiuc_library.spiders.sfx_vufind_spider import SVSpider


def main():
    wrangler = SpiderWrangler(get_project_settings(), gen_spiders=False, spidercls=SVSpider)

    # start a crawl
    wrangler.start_crawl(csv_path='demo_sv.csv',
                         from_file='guides.csv')


if __name__ == '__main__':
    main()

