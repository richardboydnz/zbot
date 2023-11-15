from scrapy.spiders import CrawlSpider , Rule # type: ignore
from myscraper.items.domains import DomainCache # type: ignore

from myscraper.items.urls import URLCache # type: ignore


class CachedSpider(CrawlSpider):

    def __init__(self):
        super().__init__()
        self.urls = URLCache()
        self.domains = DomainCache()