# local
from accessibility_spiders.spider_interface.interfaces import AccessibilitySpiderInterface


def main():
    # Instantiate the interface
    interface = AccessibilitySpiderInterface('atv-spider', csv_path='custom_log.csv')

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

