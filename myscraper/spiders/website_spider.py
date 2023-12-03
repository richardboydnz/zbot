import datetime
from scrapy.http import Request, Response # type: ignore
from myscraper.items import CrawlItem, HtmlItem, DownloadItem
from myscraper.items.html_item import make_html
from myscraper.items.items import LinkItem
from myscraper.parsers.fragment_parser import Fragment_Parser
from myscraper.encode.hash import hash64
from myscraper.spiders.cached_spider import CachedSpider
from ..parsers.html_parser import get_fragments

class WebsiteSpider(CachedSpider):
    name: str = 'myscraper'


    def __init__(self, domain_name: str | None = None):
        super().__init__()
        self.domain_name : str = domain_name or 'ballet.zavidan.info'
        self.allowed_domains = [self.domain_name]
        self.start_urls: list[str] = [f'http://{self.domain_name}', f'https://{self.domain_name}']

        # self.domain_item = self.create_domain(self.allowed_domains[0])
        self.crawl_item = self.create_crawl_item()  # Creating CrawlItem

    def start_requests(self):
        yield Request(
            url=self.start_urls[0],
            method='HTML',
            callback=self.parse_crawl_meta,
            meta={'fragment': self.domain_name}
        )

        for url in self.start_urls:
            yield Request(url, callback=self.parse_item)

#--- Top level parsing function

    def parse_crawl_meta(self, response: Response):
        print("----Crawl Item  ",self.crawl_item)
        yield self.crawl_item  # Assuming this is a valid request

    def parse_item(self, response: Response):
        html_item = self.create_html_item(response)
        yield html_item
        yield self.create_download_item(response, html_item)

        for fragment, _ in get_fragments(response.text):
            content_type = fragment.name
            yield Request(
                url=response.url,
                method='HTML',
                callback=self.parse_fragment,
                meta={'fragment': str(fragment)},
                cb_kwargs={'html_hash': html_item['html_hash'], 'orig_response': response, 'content_type': content_type}
            )

    def parse_fragment(self, response: Response, **kwargs):
        parser = Fragment_Parser(self, response, **kwargs)
        yield from self.generate_requests( parser.parse_fragment() )

    def parse_head(self, response: Response):
        # Logic to handle HEAD request response
        pass

#--- helper functions

    def generate_requests(self, items):
        for item in items:
            # Check if the item is a LinkItem
            if isinstance(item, LinkItem):
                if item['link_type'] == 'webpage' and item['is_internal']:
                    yield Request(url=item['target_url'], method='GET')
                else:
                    yield Request(url=item['target_url'], method='HEAD')

            yield item
            

#--- item functions from responses

    def create_html_item(self, response: Response) -> HtmlItem:
        return make_html(domain_name=self.domain_name, html_data=response.text)

    def create_download_item(self, response: Response, html_item: HtmlItem) -> DownloadItem:
        headers = str(response.headers)
        return DownloadItem(
            domain_name=self.domain_name,
            url=response.url,
            html_hash=html_item['html_hash'],
            download_timestamp=datetime.datetime.now().isoformat(),
            http_status=response.status,
            headers=headers,
        )

    def create_crawl_item(self) -> CrawlItem:
        self.crawl_item = CrawlItem(domain_name=self.allowed_domains[0], crawl_timestamp=datetime.datetime.now().isoformat())
        return self.crawl_item

