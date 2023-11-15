import datetime
import hashlib

from myscraper.items import ContentItem, CrawlItem, DomainItem, DownloadItem, HtmlContentItem, HtmlItem, LinkItem
from urllib.parse import urlparse
# from scrapy.linkextractors import LinkExtractor # type: ignore
from scrapy.http import Request # type: ignore
from scrapy.http import Response


import hashlib
from bs4 import BeautifulSoup
from .cached_spider import CachedSpider
from myscraper.utils.parse_links import Fragment_Parser
from myscraper.utils.urls import URLCache
from myscraper.utils.util import hash64, Hash64 
from ..utils.fragments import get_fragments

from itertools import chain

flatten = chain.from_iterable

domain = 'ballet.zavidan.info'
# domain = 'www.graceremovals.co.nz'



class WebsiteSpider(CachedSpider):
    name = 'website_spider'
    allowed_domains = [domain]

    start_urls = ['https://' + domain]  # Replace with the website you want to scrape
    # start_urls = start_urls

    # rules = (
    #     Rule(LinkExtractor(allow_domains=[domain]), callback='parse_page', follow=True),
    # )


    def __init__(self):
        super().__init__()

    def start_requests(self):

        self.domain = self.allowed_domains[0]
        # Initialize DomainItem
        self.domain_item = DomainItem(
            domain_name=self.allowed_domains[0]
        )

        # Initialize CrawlItem
        self.crawl_item = CrawlItem(
            domain_name=self.allowed_domains[0],
            start_time=datetime.datetime.now()
        )

        for url in self.start_urls:
            yield Request(url, callback=self.parse_item)

    def parse_item(self, response: Response):
        # This function gets the HTML item, yields the HtmlItem,
        # and passes the html_hash to the gen_downloadItem function
        html_item = self.create_html_item(response)
        yield html_item
        yield self.create_downloadItem(response, html_item)



        for fragment, _ in get_fragments(response.text):
            # Creating a new HtmlResponse object for each fragment
            # Directly calling the callback method
            content_type = fragment.name
            yield Request(
                url=response.url,
                method='HTML',
                callback=self.parse_fragment,
                meta={'fragment': str(fragment)},  #.encode('utf-8')},
                cb_kwargs={'html_hash': html_item['html_hash'],
                           'orig_response': response,
                           'content_type': content_type}
            )
            # yield from self.parse_fragment(fragment)

        # fragments = self.find_fragments(response.text)
        # for fragment in fragments:
        #     yield Request(
        #         url=response.url, # Ensures nothing new is downloaded
        #         callback=self.parse_fragment,
        #         cb_kwargs={'fragment': fragment},
        #         dont_filter=True  # Ensures the request is not filtered
        #     )

    def parse_fragment(self, response, **kwargs):
        parser = Fragment_Parser(self, response, **kwargs)
        yield from parser.parse_fragment()
        # fragment = response.text
        # content_item = self.create_content_item(response, html_hash, content_type)
        # content_hash = content_item['fragment_hash']

        # yield content_item        

        # association_item = HtmlContentItem()
        # association_item['html_hash'] = html_hash
        # association_item['content_hash'] = content_hash
        # yield association_item

        # yield from self.gen_links(response, content_item)

        # # for link in self.find_links(fragment):
        # #     yield from self.create_link_item(link, content_item) 


    def gen_fragments(self, html):
        for fragment in get_fragments(html):
            yield fragment

    def create_html_item(self, response:Response):
        # This method creates an HtmlItem
        html_data = response.text
        html_hash = hash64(html_data)
        return HtmlItem(
            domain=self.url_cache.get_url_item(response.url)['domain'],
            html_hash=html_hash,
            html_data=html_data
        )

    def create_downloadItem(self, response, html_item:HtmlItem) -> DownloadItem:
        # This method yields a DownloadItem
        headers = str(response.headers)
        return DownloadItem(
            domain=html_item['domain'],
            url=response.url,
            html_hash=html_item['html_hash'],
            download_timestamp=datetime.datetime.now().isoformat(),
            http_status=response.status,
            headers=headers,
            crawl_id=None  # This should be set according to your crawl logic
        )

    def find_fragments(self, content):
        # Placeholder: Your logic to split content into fragments
        return [content[i:i+1000] for i in range(0, len(content), 1000)]



    # def gen_links(self, response: Response, content_item: ContentItem):
    #     soup = BeautifulSoup(content_item['fragment_text'])
    #     # Process href tags for navigable links
    #     for tag in soup.find_all(href=True):
    #         url = response.urljoin( tag['href'] )
    #         url_item = self.url_cache.get_url_item(url)
    #         link_item = LinkItem(
    #             domain=url_item['domain'],
    #             fragment_hash=content_item['content_hash'],
    #             to_url=url,
    #             link_text=tag.get_text(),
    #             link_attr='href',
    #             link_tag=tag.name,
    #             is_internal=url_item['domain'] == content_item['domain'],
    #         )
    #         yield link_item
    #         # print( 'from: ', content_item['domain'], ' to: ', url_item['domain'] , ' ===================================')
    #         if link_item['is_internal']:
    #             yield Request(url=url, method='GET')  # GET request for external resources
    #         else:
    #             yield Request(url=url, method='HEAD')  # HEAD request for external resources



    #     # Process src tags for resources
    #     for tag in soup.find_all(src=True):
    #         url = response.urljoin( tag['src'] )
    #         url_item = self.url_cache.get_url_item(url)
    #         link_item = LinkItem(
    #             domain=url_item['domain'],
    #             fragment_hash=content_item['content_hash'],
    #             to_url=url,
    #             link_text='',  # src tags often don't have text; could use alt attribute for images
    #             link_attr='src',
    #             link_tag=tag.name,
    #             is_internal=url_item['domain'] == content_item['domain'],
    #         )
    #         yield link_item
    #         yield Request(url=url, method='HEAD')  # query existance of all linked resources

    # def parse_css_file(self, response, content_item):
    #     css_content = response.text
    #     for link_item in gen_css_links(css_content, content_item):
    #         yield link_item

    def gen_requests(self, item_generator):
        parse_callbacks = {'webpage': self.parse_html_file, 'style': self.parse_css_file}

        for item in item_generator:
            if isinstance(item, LinkItem):
                if item['link_type'] in parse_callbacks and item['domain'] in self.domain:
                    # Create a full download and parse request
                    yield Request(item['to_url'], callback=parse_callbacks[item['link_type']])
                else:
                    # Create a HEAD request for existence check
                    yield Request(item['to_url'], method='HEAD', callback=self.check_existence)
            # Pass through all items
            yield item

    def check_existence(self, response):
        # Logic to handle HEAD request response
        pass
#---------------------------
    def parse(self, response):
        # ... initial parsing logic ...

        soup = BeautifulSoup(response.text, 'html.parser')


        # Yield a DownloadItem first
        download_item = self.create_download_item(response, soup)

        # Flatten nested iterators for content items
        content_fragments = self.find_fragments(response.text)
        yield from flatten(self.create_content_item(fragment, download_item) 
                           for fragment in content_fragments)

    def create_download_item(self, response, soup):
        download_item = DownloadItem()
        download_item['url'] = response.url
        download_item['content'] = response.text
        yield download_item
        

    def create_link_item(self, link, content_item):

        link_item = LinkItem()
        link_item['link_id'] = hashlib.sha256(link['href'].encode('utf-8')).hexdigest()
        link_item['from_content'] = content_item['content_id']
        link_item['to_url'] = link['href']
        link_item['link_text'] = link.get_text(strip=True)
        link_item['crawl_timestamp'] = datetime.utcnow().isoformat()
        link_item['pageId'] = content_item['pageId']
        link_item['link_num'] = content_item  # Assign the link_num from enumerate
        link_item['from_domain'] = content_item['domain']
        link_item['to_domain'] = urlparse(link.url).netloc
        link_item['to_url'] = link.url
        
        yield link_item

