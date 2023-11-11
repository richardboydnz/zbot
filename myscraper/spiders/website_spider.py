import datetime
import hashlib
from myscraper.items import ContentItem, CrawlItem, DomainItem, DownloadItem, HtmlContentItem, HtmlItem, LinkItem
from urllib.parse import urlparse
from scrapy.linkextractors import LinkExtractor # type: ignore
from scrapy.spiders import CrawlSpider, Rule # type: ignore
from scrapy import Request # type: ignore


import logging

import html2text

import hashlib
from bs4 import BeautifulSoup
from myscraper.utils.parse_links import gen_css_links
from ..utils.markdown import soup_to_markdown as md 
from ..utils.util import hash64 

from itertools import chain

flatten = chain.from_iterable

# domain = 'ballet.zavidan.info'
domain = 'www.graceremovals.co.nz'



class WebsiteSpider(CrawlSpider):
    name = 'website_spider'
    allowed_domains = ['example.com']

    start_urls = ['https://' + domain]  # Replace with the website you want to scrape
    # start_urls = start_urls

    rules = (
        Rule(LinkExtractor(allow_domains=[domain]), callback='parse_page', follow=True),
    )


    def __init__(self):
        super().__init__()
        self.cache = {}

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
            yield Request(url, meta={'crawl_item': self.crawl_item, 'domain_item': self.domain_item})

    def parse_item(self, response):
        # This function gets the HTML item, yields the HtmlItem,
        # and passes the html_hash to the gen_downloadItem function
        html_item = self.create_html_item(response)
        yield html_item
        yield from self.gen_downloadItem(response, html_item)

        content_fragments = self.find_content_fragments(response.body)
        yield from flatten(self.gen_content_item(fragment, html_item) 
                           for fragment in content_fragments)


    def create_html_item(self, response):
        # This method creates an HtmlItem
        html_data = response.text
        html_hash = int(hashlib.sha256(html_data.encode('utf-8')).hexdigest(), 16) % 10**8
        return HtmlItem(
            domain=response.url.split('/')[2],
            domain_id=None,  # This should be set according to your domain logic
            html_hash=html_hash,
            html_data=html_data
        )

    def gen_downloadItem(self, response, html_item:HtmlItem):
        # This method yields a DownloadItem
        headers = str(response.headers)
        yield DownloadItem(
            domain=html_item.domain,
            url=response.url,
            html_hash=html_item.html_hash,
            download_timestamp=datetime.datetime.now().isoformat(),
            http_status=response.status,
            headers=headers,
            crawl_id=None  # This should be set according to your crawl logic
        )

    def find_content_fragments(self, content):
        # Placeholder: Your logic to split content into fragments
        return [content[i:i+1000] for i in range(0, len(content), 1000)]

    def gen_content_item(self, fragment, html_item:HtmlItem):

        content_text = md(fragment)
        plain_text = md(fragment)

        content_hash = hash64(content_text)
        plain_hash = hash64(plain_text)

        # Check if this content has already been processed
        if content_hash in self.cache.contentItem:
            return
        
        content_item = ContentItem()

        yield content_item

        association_item = HtmlContentItem()
        association_item['html_hash'] = html_item.html_hash
        association_item['content_hash'] = content_hash
        yield association_item

        # Flatten nested iterators for link items
        link_items = (self.create_link_item(link, content_item) 
                      for link in self.find_links(fragment))
        yield from flatten(link_items)


    def gen_links(self, soup, content_item):
        # Process href tags for navigable links
        for tag in soup.find_all(href=True):
            url_item = self.url_cache.get_url_item(tag['href'], content_item.domain)
            link_item = LinkItem(
                domain=url_item.domain,
                from_content_hash=content_item.content_hash,
                to_url=tag['href'],
                link_text=tag.get_text(),
                link_attr='href',
                link_tag=tag.name,
                internal=url_item.domain == content_item.domain,
            )
            yield link_item

        # Process src tags for resources
        for tag in soup.find_all(src=True):
            url_item = self.url_cache.get_url_item(tag['src'], content_item.domain)
            link_item = LinkItem(
                domain=url_item.domain,
                from_content_hash=content_item.content_hash,
                to_url=tag['src'],
                link_text='',  # src tags often don't have text; could use alt attribute for images
                link_attr='src',
                link_tag=tag.name,
                internal=url_item.domain == content_item.domain,
            )
            yield link_item
            if not link_item.internal:
                yield Request(url=tag['src'], method='HEAD')  # HEAD request for external resources

    def parse_css_file(self, response, content_item):
        css_content = response.text
        for link_item in gen_css_links(css_content, content_item):
            yield link_item

    def gen_requests(self, item_generator):
        parse_callbacks = {'webpage': self.parse_html_file, 'style': self.parse_css_file}

        for item in item_generator:
            if item['link_type'] in parse_callbacks and item['domain'] in self.allowed_domains:
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

        soup = BeautifulSoup(response.body, 'html.parser')


        # Yield a DownloadItem first
        download_item = self.create_download_item(response, soup)

        # Flatten nested iterators for content items
        content_fragments = self.find_content_fragments(response.body)
        yield from flatten(self.create_content_item(fragment, download_item) 
                           for fragment in content_fragments)

    def create_download_item(self, response, soup):
        download_item = DownloadItem()
        download_item['url'] = response.url
        download_item['content'] = response.body
        yield download_item
        

    def create_link_item(self, link, content_item):

        link_item = LinkItem()
        link_item['link_id'] = hashlib.sha256(link['href'].encode('utf-8')).hexdigest()
        link_item['from_content'] = content_item.content_id
        link_item['to_url'] = link['href']
        link_item['link_text'] = link.get_text(strip=True)
        link_item['crawl_timestamp'] = datetime.utcnow().isoformat()
        link_item['pageId'] = content_item['pageId']
        link_item['link_num'] = content_item  # Assign the link_num from enumerate
        link_item['from_domain'] = content_item['domain']
        link_item['to_domain'] = urlparse(link.url).netloc
        link_item['to_url'] = link.url
        
        yield link_item

