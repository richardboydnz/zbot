import datetime
from scrapy.http import Request, Response # type: ignore
from myscraper.items import CrawlItem, HtmlItem, DownloadItem, LinkItem
from myscraper.items.html_item import make_html
from myscraper.items.url_item import make_url
from myscraper.parsers.fragment_parser import Fragment_Parser
from myscraper.encode.hash import hash64
from myscraper.spiders.cached_spider import CachedSpider
from ..parsers.html_parser import get_fragments
from scrapy.spidermiddlewares.httperror import HttpError  # type: ignore


class WebsiteSpider(CachedSpider):
    name: str = 'myscraper'
    handle_httpstatus_all = True


    def __init__(self, domain_name: str | None = None):
        super().__init__()
        # init_db.create_db(db)

        self.domain_name : str = domain_name or 'www.graceremovals.co.nz'
        # self.domain_name : str = domain_name or 'ballet.zavidan.info'
        self.allowed_domains = [self.domain_name]
        self.start_urls: list[str] = [f'http://{self.domain_name}', f'https://{self.domain_name}']

        # self.domain_item = self.create_domain(self.allowed_domains[0])
        self.crawl_item = self.create_crawl_item()  # Creating CrawlItem

    def start_requests(self):
        yield Request(
            url=self.start_urls[0],
            method='HTML',
            callback=self.parse_crawl_meta,
            errback=self.parse_error,
            meta={'fragment': self.domain_name}
        )

        for url in self.start_urls:
            yield Request(url, callback=self.parse_item, errback=self.parse_error)

#--- Top level parsing function

    def parse_crawl_meta(self, response: Response):
        print("----Crawl Item  ",self.crawl_item)
        yield self.crawl_item  # Assuming this is a valid request

    def parse_item(self, response: Response):
        if response.status != 200:
            yield self.create_empty_download_item(response)
            return
        
        html_item = self.create_html_item(response)
        yield html_item
        yield self.create_download_item(response, html_item)

        for fragment, path in get_fragments(response.text):
            content_type = fragment.name
            fragment_text = str(fragment)
            fragment_hash=hash64(fragment_text)
            path_str = str(path)
            # print('------make fragment request', content_type)

            yield Request(
                url=f'{response.url}??{str(fragment_hash)}',
                method='HTML',
                callback=self.parse_fragment,
                errback=self.parse_error,
                meta={'fragment': fragment_text},
                cb_kwargs={'html_hash': html_item['html_hash'], 'orig_response': response, 'content_type': content_type, 'path': path_str}
            )

    def parse_fragment(self, response: Response, **kwargs):
        parser = Fragment_Parser(self, response, **kwargs)
        yield from self.generate_requests( parser.parse_fragment() )

    def parse_head(self, response: Response):
        # print('### HEAD ', response)
        yield self.create_empty_download_item(response)
        # Logic to handle HEAD request response
        pass

    def parse_error(self, failure):
        # This method handles all types of errors
        request = failure.request
        if failure.check(HttpError):
            yield self.create_empty_download_item(failure.value.response)
        else:
            yield DownloadItem(
                domain_name=self.domain_name,
                url=request.url,
                html_hash=0,
                download_timestamp=datetime.datetime.now().isoformat(),
                http_status=400,
                headers=str(failure)
            )

#--- helper functions

    def generate_requests(self, items):
        for item in items:
            # Check if the item is a LinkItem
            if isinstance(item, LinkItem):
                url_item = make_url(item['target_url'])
                # print('----- link ', LinkItem)
                if url_item['protocol'] not in ['http', 'https']:
                    pass
                elif '?' in item['target_url']:
                    # If there is a query in the URL, use HEAD method
                    yield Request(url=item['target_url'], method='HEAD', 
                                callback=self.parse_head,
                                errback=self.parse_error)
                elif item['link_type'] == 'webpage' and item['is_internal']:
                    yield Request(url=item['target_url'], method='GET',
                                callback=self.parse_item,
                                errback=self.parse_error)

                else:
                    yield Request(url=item['target_url'], method='HEAD',
                                callback=self.parse_head,
                                errback=self.parse_error)


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

    def create_empty_download_item(self, response: Response) -> DownloadItem:
        headers = str(response.headers)
        return DownloadItem(
            domain_name=self.domain_name,
            url=response.url,
            html_hash=None,
            download_timestamp=datetime.datetime.now().isoformat(),
            http_status=response.status,
            headers=headers,
        )


    def create_crawl_item(self) -> CrawlItem:
        self.crawl_item = CrawlItem(domain_name=self.allowed_domains[0], crawl_timestamp=datetime.datetime.now().isoformat())
        return self.crawl_item

