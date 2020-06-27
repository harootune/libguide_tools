# local
from accessibility_spiders.spider_interface.interfaces import AccessibilitySpiderInterface


def main():
    extractor_config = {
        'restrict_xpaths': ('//*[@id="bs-navbar-header"]',),
        'allow_domains': 'library.illinois.edu',
        'deny': '.*#.*'
    }

    # parse_config = {
    #     'css': '#content',
    # }

    # Instantiate the interface
    interface = AccessibilitySpiderInterface('atv-spider',
                                             csv=True,
                                             csv_path='custom_log_2.csv',
                                             extractor_config=extractor_config,
                                             list_output=False)
                                             # parse_config=parse_config)

    # start a crawl
    interface.start_crawl(['https://www.library.illinois.edu/',
                           'https://www.library.illinois.edu/ihx/',
                           'https://www.library.illinois.edu/funkaces/',
                           'https://www.library.illinois.edu/arx/',
                           'https://www.library.illinois.edu/chx/',
                           'https://www.library.illinois.edu/mainstacks/'])

    # retrieve output
    print(interface.get_output())

    # clear output up till now
    interface.clear_output()

    # demonstrate output is clear
    interface.get_output()


if __name__ == '__main__':
    main()

