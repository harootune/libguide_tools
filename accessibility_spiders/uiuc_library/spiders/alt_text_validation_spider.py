# stdlib
import re
from typing import List, Union
from urllib import parse

# third party
from scrapy.http.response import Response

# local
from accessibility_spiders.uiuc_library.spiders.base_accessibility_spider import AccessibilitySpider
from accessibility_spiders.uiuc_library.items import InvalidAltTextImage


class ATVSpider(AccessibilitySpider):
    """Detects and reports missing image alt-text"""
    name = 'atv-spider'

    # TODO: CLI support for the boolean parameters
    def __init__(self, start_urls: Union[List[str], str] = '', csv: bool = False, db: bool = False,
                 list_output: bool = False, csv_path: str = '', db_path: str = '', output_target: list = None,
                 extractor_config: dict = None, parse_config: dict = None):

        # parent constructor
        super().__init__(start_urls, csv, db, list_output, csv_path, db_path, output_target, parse_config)

        # assemble and compile our rules
        ATVSpider.construct_follow_rule('parse_invalid_images', **extractor_config)
        super()._compile_rules()

    def parse_invalid_images(self, response: Response) -> InvalidAltTextImage:
        """
        Parses an http response for images with missing or invalid alt text and yields items describing them
        to the pipeline

        :param response: a scrapy Response object
        :yield: an item representing an invalid image
        """
        title = response.css('title::text').get()

        # TODO: figure out how to handle case where both css and xpath are present
        # Narrow down our search to user-specified selection
        if self.parse_config:
            if 'css' in self.parse_config:
                imgs = response.css(self.parse_config['css']).xpath('./descendant::img')
            elif 'xpath' in self.parse_config:
                imgs = response.xpath(self.parse_config['xpath']).xpath('./descendant::img')
            else:
                imgs = response.xpath('//img')
        else:
            imgs = response.xpath('//img')

        # filter for images with invalid alt text
        invalid_imgs = []
        for img in imgs:
            if 'alt' not in img.attrib:
                invalid_imgs.append(img)
            elif re.fullmatch('\s*', img.attrib['alt']):
                invalid_imgs.append(img)

        # make objects
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
        yield from self.parse_invalid_images(response)

    def assemble_absolute_link(self, origin: str, src: str) -> str:
        """
        Checks if a link is absolute, and returns an absolute version if it is not already absolute.

        :param origin: the address of the page where an image src was linked from
        :param src: an image src
        :return: an absolute version of the link, if it is not already absolute
        """
        src_parts = parse.urlparse(src)
        if not src_parts.netloc:
            return parse.urljoin(origin, src)
        else:
            return src
