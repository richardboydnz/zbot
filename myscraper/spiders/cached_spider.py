from scrapy.spiders import CrawlSpider , Rule # type: ignore
# from ..items.domain_item import DomainCache # type: ignore

from ..items.url_item import UrlCache # type: ignore


class CachedSpider(CrawlSpider):

    def __init__(self):
        super().__init__()
        self.create_url = UrlCache()
        # self.create_domain = DomainCache()