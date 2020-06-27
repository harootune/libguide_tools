# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import scrapy


class FoundLink(scrapy.Item):
    """Wraps information related to links scraped from a crawled guide page"""
    a_origin = scrapy.Field()
    b_title = scrapy.Field()
    c_url = scrapy.Field()
    d_text = scrapy.Field()
