from scrapy.spiders import CrawlSpider , Rule # type: ignore

from myscraper.utils.urls import URLCache # type: ignore


class CachedSpider(CrawlSpider):

    def __init__(self):
        super().__init__()
        self.url_cache = URLCache()