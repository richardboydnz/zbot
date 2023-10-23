import datetime
import hashlib
import scrapy
from myscraper.items import PageItem, UrlItem, LinkItem, TextItem, MarkdownItem
from urllib.parse import urlparse

import html2text
from markdownify import markdownify as md

class WebsiteSpider(scrapy.Spider):
    name = 'website_spider'
    start_urls = ['http://ballet.zavidan.info/']  # Replace with the website you want to scrape

    def parse(self, response):
        # Extracting data for the PageItem
        page_item = PageItem()
        page_item['pageId'] = hashlib.sha256(response.url.encode()).hexdigest()
        page_item['domain'] = urlparse(response.url).netloc
        page_item['initial_date'] = datetime.datetime.now()
        page_item['initial_source_url'] = response.url
        yield page_item

        # Extracting data for the UrlItem
        url_item = UrlItem()
        parsed_url = urlparse(response.url)
        url_item['URL'] = response.url
        url_item['return_code'] = response.status
        url_item['mime'] = response.headers.get('Content-Type').decode('utf-8')
        url_item['pageId'] = page_item['pageId']
        url_item['initial_referrer'] = response.request.headers.get('Referer', None)
        url_item['date_updated'] = datetime.datetime.now()
        url_item['protocol'] = parsed_url.scheme
        url_item['subdomain'] = parsed_url.hostname.split('.')[0] if len(parsed_url.hostname.split('.')) > 2 else None
        url_item['domain'] = parsed_url.netloc
        url_item['path'] = parsed_url.path
        url_item['query'] = parsed_url.query
        url_item['fragment'] = parsed_url.fragment
        yield url_item

        # Extracting links for the LinkItem
        for link in response.css('a::attr(href)').extract():
            link_item = LinkItem()
            link_item['pageId'] = page_item['pageId']
            link_item['from_domain'] = page_item['domain']
            link_item['from_url'] = response.url
            link_item['to_domain'] = urlparse(link).netloc
            link_item['to_url'] = link
            yield link_item

        # Extracting data for TextItem and MarkdownItem (assuming a function to convert HTML to Markdown)
        text_item = TextItem()
        text_item['pageId'] = page_item['pageId']
        text_item['text_version'] = html2text.html2text(response.text)
        yield text_item

        markdown_item = MarkdownItem()
        markdown_item['pageId'] = page_item['pageId']
        markdown_item['markdown_version'] = md(response.text)
        yield markdown_item

        # Follow links to scrape other pages
        for link in response.css('a::attr(href)').extract():
            yield scrapy.Request(link, callback=self.parse)
