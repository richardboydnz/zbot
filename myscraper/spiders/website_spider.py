import datetime
import logging
from typing import Iterator, List, Optional
from scrapy.http import Request, Response # type: ignore
from myscraper.db import init_db
from myscraper.db.db_store import KeyedDbStore # type: ignore
from myscraper.items import CrawlItem, HtmlItem, DownloadItem, LinkItem
from myscraper.items.html_content_item import HtmlContentItem
from myscraper.items.html_item import HtmlDBCache, make_html
from myscraper.items.url_item import get_url_item
from myscraper.middlewares.html_response import CUSTOM_SUCCESS
from myscraper.parsers.fragment_parser import Fragment_Parser
from myscraper.encode.hash import hash64
from myscraper.spiders.cached_spider import CachedSpider
from ..parsers.html_parser import get_fragments
from scrapy.spidermiddlewares.httperror import HttpError  # type: ignore
from ..items.url_item import build_url, fragment_separator, norm_url
from scrapy.exceptions import IgnoreRequest # type: ignore
from ..db import Connection
from ..items.html_item import html_db_mapping



class WebsiteSpider(CachedSpider):
    name: str = 'myscraper'
    handle_httpstatus_all = True
    handle_httpstatus_list = range(200, 600)  # Handle all status codes from 200 to 599
    start_urls: List[str]

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        # Call the base implementation first to get the spider object
        spider = super().from_crawler(crawler, *args, **kwargs)

        settings = crawler.settings

        db_settings = settings.getdict('DB_SETTINGS')
        spider.db = init_db.get_db(db_settings)  # Modify the get_db method to accept settings

        if settings.get('CLEAR_DB'):
            init_db.create_db(spider.db)

        spider.follow_resources = settings.get('FOLLOW_RESOURCES', False)
        spider.domain_name = settings.get('CRAWL_DOMAIN', 'ballet.zavidan.info')

       
        spider.allowed_domains = [spider.domain_name]
        spider.start_urls = [f'http://{spider.domain_name}']
        #, f'https://{spider.domain_name}']

        # self.domain_item = self.create_domain(self.allowed_domains[0])
        spider.crawl_item = spider.create_crawl_item()  # Creating CrawlItem
        # Extract settings from the crawler


        # Return the spider instance
        return spider
    
    # def __init__(self):
    #     super().__init__()
    #     # self.html_store = HtmlDBCache(self.db)
    #     self.domain_name = domain_name
    #     self.follow_resources = follow_resources
    #     # self.html_store = KeyedDbStore[int](self.db, html_db_mapping)


        
    #     self.allowed_domains = [domain_name]
    #     self.start_urls: list[str] = [f'http://{self.domain_name}']#, f'https://{self.domain_name}']

    #     # self.domain_item = self.create_domain(self.allowed_domains[0])
    #     self.crawl_item = self.create_crawl_item()  # Creating CrawlItem

    # @classmethod
    # def from_crawler(cls, crawler, *args, **kwargs):
    #     # spider = super().from_crawler(crawler, *args, **kwargs)

    #     # Extract settings from the crawler
    #     db_settings = crawler.settings.getdict('DB_SETTINGS')
    #     db = init_db.get_db(db_settings)  # Modify the get_db method to accept settings

    #     if crawler.settings.get('CLEAR_DB'):
    #         init_db.create_db(db)

    #     follow_resources = crawler.settings.get('FOLLOW_RESOURCES', False)

    #     domain_name = crawler.settings.get('CRAWL_DOMAIN', 'ballet.zavidan.info')

    #     # Create the database connection using settings

    #     # Return an instance of the pipeline class with the db connection
    #     return cls( domain_name, follow_resources)

    # def __init__(self) -> None:
    #     super().__init__()
    #     settings = self.crawler.settings

    #     db_settings = settings.getdict('DB_SETTINGS')
    #     self.db = init_db.get_db(db_settings)  # Modify the get_db method to accept settings

    #     if settings.get('CLEAR_DB'):
    #         init_db.create_db(self.db)

    #     self.follow_resources = settings.get('FOLLOW_RESOURCES', False)
    #     self.domain_name = settings.get('CRAWL_DOMAIN', 'ballet.zavidan.info')

    #     # Set the instance variables from settings

    #     # self.html_store = HtmlDBCache(self.db)

    #     # self.html_store = KeyedDbStore[int](self.db, html_db_mapping)


        
    #     self.allowed_domains = [self.domain_name]
    #     self.start_urls: list[str] = [f'http://{self.domain_name}']#, f'https://{self.domain_name}']

    #     # self.domain_item = self.create_domain(self.allowed_domains[0])
    #     self.crawl_item = self.create_crawl_item()  # Creating CrawlItem

    def start_requests(self) -> Iterator[Request]:
        # Just create the crawl item
        yield make_request(
            url=self.start_urls[0],
            method='INIT',
            callback=self.parse_crawl_meta
        )


#--- Top level parsing function

    def parse_crawl_meta(self, response: Response):
        logging.info("----Crawl Item  ",self.crawl_item)
        yield self.crawl_item  # Assuming this is a valid request

        yield from self.init_crawl()

    def init_crawl(self):
        for url in self.start_urls:
            request = make_request(url, callback=self.parse_item, errback=self.parse_error)
            logging.debug(f"----init request  {request}")

            yield request


    def parse_item(self, response: Response):
        logging.debug(f'parse item {response}')
        if response.status in [300, 301, 302, 303, 307, 308]:
            yield from self.parse_redirect(response)
            return
        if response.status != 200:
            yield self.create_empty_download_item(response)
            return
        
        html_item = self.create_html_item(response)
        yield html_item
        yield self.create_download_item(response, html_item)

        for content_bs, path in get_fragments(response.text):
            logging.debug(f'parse fragment {path}')
            content_type = content_bs.name
            content_text = str(content_bs)
            content_hash=hash64(content_text)
            path_str = str(path)
            # print('------make fragment request', content_type)

            yield make_request(
                url=f'{response.url}{fragment_separator}{str(content_hash)}',
                method='HTML',
                callback=self.parse_fragment,
                errback=self.parse_error,
                meta={ 'content': content_text, 'content_hash': content_hash},
                cb_kwargs={'html_hash': html_item['html_hash'], 'content_hash': content_hash, 'path': path_str, 'content_type': content_type, 'orig_response': response  }
            )

    def parse_fragment(self, response: Response, html_hash, content_hash, path, **kwargs):
        logging.info(f'------ parse_fragment {response}')
        print(f'------ parse_fragment {response}')

        # print()
        # print('####', response.status, html_hash, content_hash, path)
        if response.status == CUSTOM_SUCCESS:
            parser = Fragment_Parser(self, response, **kwargs )
            yield from self.generate_requests( parser.parse_fragment() )
        else: # CUSTOM_EXISTS
            logging.info(f'Fragment already exists in DB, skipping: {content_hash}')
            # print(f'Fragment already exists in DB, skipping: {content_hash}')


        association_item = HtmlContentItem(
            domain_name=self.domain_name,
            html_hash=html_hash,
            content_hash=content_hash,
            path=path
        )
        yield association_item

    def parse_head(self, response: Response):
        logging.debug(f'------ parse_head {response}')

        # print('### HEAD ', response)
        yield self.create_empty_download_item(response)
        # Logic to handle HEAD request response
        pass

    def parse_error(self, failure):
        if failure.check(IgnoreRequest):
            return
        # This method handles all types of errors
        logging.error(f'################### {failure}')
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

    def parse_redirect(self, response: Response):
        headers = str(response.headers)
        redirect_url=response.headers['Location'].decode('utf-8')
        _, rd_url = norm_url(redirect_url, response)
        logging.info(f'--- REDIRECT to {rd_url}')

        yield DownloadItem(
            domain_name = self.domain_name,
            url=response.url,
            html_hash=None,
            download_timestamp=datetime.datetime.now().isoformat(),
            http_status=response.status,
            headers=headers,
            redirect_url = rd_url
        )

        request = self.create_request(rd_url, 'webpage')
        if request:
            yield request

#--- helper functions
    webpage_extensions = [
        '', 'htm', 'html', 'php', 
        'asp', 'aspx', 'jsp', 'cgi', 
        'shtml', 'xhtml', 'cfm', 'pl', 
        'php3', 'php4', 'php5', 'phtml', 
        'rhtml', 'jspx'
    ]

    def generate_requests(self, items):
        for item in items:
            if isinstance(item, LinkItem):
                request = self.create_request(item['target_url'], item['link_type'])
                if request:
                    yield request

            yield item

            
    def create_request(self, url: str, link_type: str) -> Optional[Request]:
        url_item = get_url_item(url)
        head_request = False

        if url_item['protocol'] not in ['http', 'https']:
            return None

        if url_item['domain_name'] != self.domain_name:
            head_request = True
        
        if link_type != 'webpage':
            head_request = True

        if url_item['file_extension'].lower() not in self.webpage_extensions:
            head_request = True

        # is_webpage = link_type == 'webpage' and url_item['file_extension'].lower() in self.webpage_extensions

        if '?' in url:
            head_request = True

        if not head_request:
            return Request(url=url, method='GET', callback=self.parse_item, errback=self.parse_error)
        elif self.follow_resources:
            return Request(url=url, method='HEAD', callback=self.parse_head, errback=self.parse_error)

        return None

 
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


def make_request(url, **kwargs):
    return Request(url, **kwargs)