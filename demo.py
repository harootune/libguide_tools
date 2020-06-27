# local
from libguide_spiders.spider_interface.interfaces import LibguideSpiderInterface


def main():
    extractor_config = {
        'restrict_css': ('#s-lg-guide-tabs',),
        'allow_domains': 'guides.library.illinois.edu',
        'deny': '.*#.*'
    }

    parse_config = {
        'css': '#s-lg-guide-main',
    }

    # Instantiate the interface
    interface = LibguideSpiderInterface('bl-spider',
                                        csv_path='custom_log.csv',
                                        extractor_config=extractor_config,
                                        parse_config=parse_config)

    # start a crawl
    interface.start_crawl(['https://guides.library.illinois.edu/arabspringworkshop'])


if __name__ == '__main__':
    main()

