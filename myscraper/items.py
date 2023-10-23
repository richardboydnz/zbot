# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class PageItem(scrapy.Item):
    pageId = scrapy.Field()
    domain = scrapy.Field()
    initial_date = scrapy.Field()
    initial_source_url = scrapy.Field()

class UrlItem(scrapy.Item):
    URL = scrapy.Field()
    return_code = scrapy.Field()
    mime = scrapy.Field()
    pageId = scrapy.Field()
    initial_referrer = scrapy.Field()
    date_updated = scrapy.Field()
    protocol = scrapy.Field()
    subdomain = scrapy.Field()
    domain = scrapy.Field()
    path = scrapy.Field()
    query = scrapy.Field()
    fragment = scrapy.Field()

class LinkItem(scrapy.Item):
    pageId = scrapy.Field()
    from_domain = scrapy.Field()
    from_url = scrapy.Field()
    to_domain = scrapy.Field()
    to_url = scrapy.Field()

class TextItem(scrapy.Item):
    pageId = scrapy.Field()
    text_version = scrapy.Field()

class MarkdownItem(scrapy.Item):
    pageId = scrapy.Field()
    markdown_version = scrapy.Field()
