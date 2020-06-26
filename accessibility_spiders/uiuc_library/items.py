# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import scrapy


class InvalidAltTextImage(scrapy.Item):
    """Wraps information which helps locate an image with invalid alt text"""
    origin = scrapy.Field()
    page_title = scrapy.Field()
    src = scrapy.Field()

