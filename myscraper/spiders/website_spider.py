import datetime
import logging
from scrapy.http import Request, Response # type: ignore
from myscraper.db import init_db
from myscraper.db.db_store import KeyedDbStore # type: ignore
from myscraper.items import CrawlItem, HtmlItem, DownloadItem, LinkItem
from myscraper.items.html_content_item import HtmlContentItem
from myscraper.items.html_item import HtmlDBCache, make_html
from myscraper.items.url_item import get_url_item
from myscraper.parsers.fragment_parser import Fragment_Parser
from myscraper.encode.hash import hash64
from myscraper.spiders.cached_spider import CachedSpider
from ..parsers.html_parser import get_fragments
from scrapy.spidermiddlewares.httperror import HttpError  # type: ignore
from ..items.url_item import build_url, fragment_separator, normalise_url
from scrapy.exceptions import IgnoreRequest # type: ignore
from psycopg2.extensions import connection
from ..items.html_item import html_db_mapping


check_resources = False

class WebsiteSpider(CachedSpider):
    name: str = 'myscraper'
    handle_httpstatus_all = True

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        # spider = super().from_crawler(crawler, *args, **kwargs)

        # Extract settings from the crawler
        db_settings = crawler.settings.getdict('DB_SETTINGS')
        db = init_db.get_db(db_settings)  # Modify the get_db method to accept settings

        if crawler.settings.get('CLEAR_DB'):
            init_db.create_db(db)

        domain_name = crawler.settings.get('CRAWL_DOMAIN', 'ballet.zavidan.info')

        # Create the database connection using settings

        # Return an instance of the pipeline class with the db connection
        return cls(db, domain_name)

    def __init__(self, db: connection, domain_name: str):
        super().__init__()
        # self.html_store = HtmlDBCache(self.db)
        self.domain_name = domain_name
        # self.html_store = KeyedDbStore[int](self.db, html_db_mapping)


        # self.domain_name : str = domain_name or 'crownrelo-co-nz.archive.zavidan.nz'
        # self.domain_name : str = domain_name or 'www.graceremovals.co.nz'
        # self.domain_name : str = domain_name or 'ballet.zavidan.info'
        # self.domain_name : str = domain_name or 'www.crownrelo.co.nz'
        
        self.allowed_domains = [domain_name]
        self.start_urls: list[str] = [f'http://{self.domain_name}']#, f'https://{self.domain_name}']

        # self.domain_item = self.create_domain(self.allowed_domains[0])
        self.crawl_item = self.create_crawl_item()  # Creating CrawlItem

    def start_requests(self):
        yield make_request(
            url=self.start_urls[0],
            method='INIT',
            callback=self.parse_crawl_meta
            
        )


#--- Top level parsing function

    def parse_crawl_meta(self, response: Response):
        logging.debug("----Crawl Item  ",self.crawl_item)
        yield self.crawl_item  # Assuming this is a valid request
        for url in self.start_urls:
            request = make_request(url, callback=self.parse_item, errback=self.parse_error)
            logging.debug(f"----init request  {request}")

            yield request


    def parse_item(self, response: Response):
        logging.debug(f'parse item {response}')
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
        # print()
        # print('####', response.status, html_hash, content_hash, path)
        if response.status == 200:
            parser = Fragment_Parser(self, response, **kwargs )
            yield from self.generate_requests( parser.parse_fragment() )
        else:
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
            # Check if the item is a LinkItem
            if isinstance(item, LinkItem):
                url_item = get_url_item(item['target_url'])
                if item['link_type'] == 'webpage' and \
                        url_item['file_extension'].lower() not in self.webpage_extensions:
                    # item['is_webpage'] = False
                    item['link_type'] = "non-webpage"
                else:
                    # item['is_webpage'] = True
                    pass
                # print('----- link ', LinkItem)
                if url_item['protocol'] not in ['http', 'https']:
                    pass

                elif item['link_type'] == 'webpage' and item['is_internal']:
                    if '?' in item['target_url']:
                    # If there is a query in the URL, use HEAD method
                        yield make_request(url=item['target_url'], method='HEAD', 
                                    callback=self.parse_head,
                                    errback=self.parse_error)
                    else:
                        yield make_request(url=item['target_url'], method='GET',
                                    callback=self.parse_item,
                                    errback=self.parse_error)

                else:
                    if check_resources:
                        yield make_request(url=item['target_url'], method='HEAD',
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


def make_request(url, **kwargs):
    return Request(url, **kwargs)