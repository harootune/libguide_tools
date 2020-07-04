# stdlib
import urllib.parse as parse
from typing import List, Union

# third party
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http.response import Response

# local
from libguide_spiders.uiuc_library.spiders.base_libguide_spider import LibGuideSpider
from libguide_spiders.uiuc_library.items import FoundLink


class SVSpider(LibGuideSpider):
    """Extracts and stores vufind and sfx links from libguides. See README.md"""
    # Class variables
    name = 'sv-spider'
    rules = [
        Rule(LinkExtractor(restrict_css=('#s-lg-guide-tabs',), allow='\S*guides.library.illinois.edu\S*', deny='.*#.*'),
                           callback='parse_sv_links', follow=True),
    ]

    def __init__(self, start_urls: Union[List[str], str] = '', css: str = '', csv_path: str = '', *args, **kwargs):
        super().__init__(start_urls, csv_path, *args, **kwargs)

        # attributes #
        # public
        self.css = css

    def parse_sv_links(self, response: Response) -> FoundLink:
        """
        Yields BrokenLink items for broken links not caught by an error or exception and moves them through the
        broken_link_detector pipeline.

        :param response: A response produced by a Rule
        :return: A BrokenLink Item to be passed to the pipeline
        """
        title = response.css('title::text').get()

        if self.css:
            links = response.css(self.parse_config['css'])
        else:
            links = response

        links = links.xpath('./descendant::*[@href]')

        for link in links:
            if 'vufind' in link.attrib['href'] or 'sfx' in link.attrib['href']:
                link_obj = FoundLink()
                link_obj['a_origin'] = response.url
                link_obj['b_title'] = title
                link_obj['c_url'] = self.assemble_absolute_link(response.url, link.attrib['href'])
                link_obj['d_text'] = link.xpath('./text()').get()
                yield link_obj

    def parse_start_url(self, response: Response) -> FoundLink:
        """
        Passes the first response to parse_sv_links

        :param response: a scrapy Response object
        :yield: a FoundLink representing a
        """
        yield from self.parse_sv_links(response)

    def assemble_absolute_link(self, origin: str, path: str) -> str:
        """
        Checks if a link is absolute
        :param origin: the address of the page where an image src was linked from
        :param path: an image src
        :return: an absolute version of the link, if it is not already absolute
        """
        src_parts = parse.urlparse(path)
        if not src_parts.netloc:
            return parse.urljoin(origin, path)
        else:
            return path

