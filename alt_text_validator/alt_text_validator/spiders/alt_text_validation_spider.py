import re

from urllib import parse
from scrapy.http.response import Response
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from ..items import InvalidAltTextImage


class ATVSpider(CrawlSpider):
    """Detects and reports missing image alt-text"""
    name = 'atv-spider'
    rules = (
        Rule(LinkExtractor(restrict_xpaths=('//*[@id="bs-navbar-header"]',),
                           allow_domains='library.illinois.edu', deny='.*#.*'),
             follow=True, callback='parse_missing_alt_text'),
    )
    custom_settings = {
         'ITEM_PIPELINES': {'alt_text_validator.pipelines.CSVOutput': 300, }
    }

    def __init__(self, start_points: str = '', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = start_points.split(',')

    def parse_missing_alt_text(self, response: Response) -> InvalidAltTextImage:
        """
        :param response: a scrapy Response object
        :yield: an invalid img
        """
        title = response.css('title::text').get()
        imgs = response.css('#content').xpath('./descendant::img')

        invalid_imgs = []
        for img in imgs:
            try:
                if re.fullmatch('\s*', img.attrib['alt']):
                    invalid_imgs.append(img)
            except KeyError as e:
                invalid_imgs.append(img)

        for img in invalid_imgs:
            invalid_img_obj = InvalidAltTextImage()
            invalid_img_obj['origin'] = response.url
            invalid_img_obj['page_title'] = title
            invalid_img_obj['src'] = self.assemble_absolute_link(response.url, img.attrib['src'])
            yield invalid_img_obj

    def parse_start_url(self, response: Response) -> InvalidAltTextImage:
        """
        Passes the first response to parse_missing_alt_text

        :param response: a scrapy Response object
        :yield: an invalid img
        """
        yield from self.parse_missing_alt_text(response)

    @staticmethod
    def assemble_absolute_link(origin: str, src: str) -> str:
        """
        Checks if a link is absolute
        :param origin: the address of the page where an image src was linked from
        :param src: an image src
        :return: an absolute version of the link, if it is not already absolute
        """
        src_parts = parse.urlparse(src)
        if not src_parts.netloc:
            return parse.urljoin(origin, src)
        else:
            return src
