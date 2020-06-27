# stdlib
from typing import List, Union

# third party
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http.response import Response
from scrapy.http.request import Request
from twisted.python.failure import Failure
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError

# local
from libguide_spiders.uiuc_library.spiders.base_libguide_spider import LibGuideSpider
from libguide_spiders.uiuc_library.items import FoundLink


class BLSpider(LibGuideSpider):
    """Extracts and stores broken links from libguides. See README.md"""
    # Class variables
    name = 'bl-spider'
    custom_settings = LibGuideSpider.custom_settings.copy()
    custom_settings['HTTPERROR_ALLOW_ALL'] = True

    def __init__(self, start_urls: Union[List[str], str] = '', csv_path: str = '',
                 extractor_config: dict = None, parse_config: dict = None, *args, **kwargs):
        super().__init__(start_urls, csv_path, parse_config, *args, **kwargs)

        # create rules
        BLSpider.construct_follow_rule('', extractor_config)
        BLSpider.construct_broken_link_rule('request_associator', 'parse_broken_link', 'errback_broken_link',
                                            self.parse_config)
        self._compile_rules()

    def parse_broken_link(self, response: Response) -> FoundLink:
        """
        Yields FoundLink items to be processed in the pipeline

        :param response: A response produced by a Rule
        :return: A FoundLink Item to be passed to the pipeline
        """
        # Filter working links
        if response.status >= 400:
            link_obj = FoundLink()
            link_obj['a_origin'] = response.request.meta['origin']
            link_obj['b_title'] = response.request.meta['origin_title']
            link_obj['c_url'] = response.url
            link_obj['d_text'] = response.request.meta['link_text']
            yield link_obj

    def errback_broken_link(self, failure: Failure) -> FoundLink:  # Failure may not be the right typehint
        """
        Handles behavior for links which cause Twisted failures - which is most of the broken links this spider
        hopes to find

        :param failure: A Twisted failure raised by the Retry middleware
        :return: None
        """
        # Structure of this function heavily inspired by:
        # https://docs.scrapy.org/en/latest/topics/request-response.html#topics-request-response-ref-errbacks

        # If its a TCP or DNS error, short-circuit to the pipeline
        if failure.check(DNSLookupError, TCPTimedOutError):
            self.logger.info(f'Handled DNS/TCP related error. {failure.request.url}')
            request = failure.request
            dummy_response = Response(
                url=request.url,
                status=404,  # Kind of a lie
                request=request
            )
            yield from self.parse_broken_link(dummy_response)

        # If the client timed out, report that
        elif failure.check(TimeoutError):
            self.logger.info(f'Client timeout. {failure.request.url}')
            self.logger.error(repr(failure))

    def request_associator(self, request: Request, response: Response):
        """
        Persists the url of the page in which a link was found past the point that information would usually be
        destroyed by hiding it in the resulting request's meta dictionary

        :param request: The Request object currently passed to the Rule's LinkExtractor
        :param response: The Response object which produced request
        :return: the same request as input
        """
        title = response.css('title::text').get()

        request.meta['origin'] = response.url
        request.meta['origin_title'] = title

        return request

    @classmethod
    def construct_broken_link_rule(cls, process_request: str, callback: str, errback: str, parse_config: dict) -> None:
        print('GOT TO BROKEN LINK CONSTRUCTOR')
        if parse_config:
            if 'css' in parse_config:
                bl_extractor = LinkExtractor(restrict_css=(parse_config['css'],))
            elif 'xpath' in parse_config:
                bl_extractor = LinkExtractor(restrict_xpaths=(parse_config['xpath'],))
            else:
                bl_extractor = LinkExtractor()
        else:
            bl_extractor = LinkExtractor()

        print(f'PROCESS REQUEST: {process_request}')
        print(f'CALLBACK: {callback}')
        print(f'ERRBACK: {errback}')
        bl_rule = Rule(bl_extractor, process_request=process_request, callback=callback, errback=errback, follow=False)

        if cls.rules:
            cls.rules += (bl_rule,)
        else:
            cls.rules = (bl_rule,)


        # Rule(LinkExtractor(restrict_xpaths=('//*[@id="s-lg-guide-main"]',)),
        #                    process_request='request_associator',
        #                    callback='parse_broken_link',
        #                    errback='errback_broken_link',
        #                    follow=False)