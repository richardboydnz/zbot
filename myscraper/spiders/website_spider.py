import datetime
import hashlib
import scrapy
from myscraper.items import PageItem, UrlItem, LinkItem, TextItem, MarkdownItem
from urllib.parse import urlparse
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

import logging

import html2text
from markdownify import markdownify as md

# domain = 'ballet.zavidan.info'
domain = 'www.graceremovals.co.nz'

class WebsiteSpider(CrawlSpider):
    name = 'website_spider'
    start_urls = ['https://' + domain]  # Replace with the website you want to scrape
    # start_urls = start_urls

    rules = (
        Rule(LinkExtractor(allow_domains=[domain]), callback='parse_page', follow=True),
    )

    def parse_page(self, response):
        logging.info(f"Scraping URL: {response.url}")
        # Extracting data for the PageItem
        page_item = PageItem()
        # Hash the content of the page to generate the pageId
        page_item['pageId'] = hashlib.sha256(response.body).hexdigest()
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
        link_extractor = LinkExtractor()

        # Use the link extractor to extract links from the response
        for link_num, link in enumerate(link_extractor.extract_links(response), start=1):
            link_item = LinkItem()
            link_item['pageId'] = page_item['pageId']
            link_item['link_num'] = link_num  # Assign the link_num from enumerate
            link_item['from_domain'] = page_item['domain']
            link_item['from_url'] = response.url
            link_item['to_domain'] = urlparse(link.url).netloc
            link_item['to_url'] = link.url
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

        # Extracting links for the LinkItem
        domain_link_extractor = LinkExtractor(allow_domains=[domain])

        # for link in response.css('a::attr(href)').extract():
        for link in domain_link_extractor.extract_links(response):
            yield scrapy.Request(link.url, callback=self.parse)
