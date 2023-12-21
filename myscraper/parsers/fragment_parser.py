import logging
import re
from bs4 import BeautifulSoup, Tag
# from scrapy.http import Request, Response # type: ignore
from myscraper.items import ContentItem, CrawlItem, DownloadItem, HtmlContentItem, HtmlItem, LinkItem

from myscraper.encode.hash import Hash64
from scrapy.http import HtmlResponse  # type: ignore

from myscraper.items.url_item import norm_url # type: ignore

from ..spiders.cached_spider import CachedSpider  # type: ignore
from ..items import LinkItem
from ..encode.markdown import soup_to_markdown as md_soup, markdown 
from myscraper.encode.hash import hash64, Hash64 
from scrapy.crawler import Crawler  # type: ignore
from ..items.url_item import fragment_separator

url_patterns = [
    ('a', 'href', 'webpage'),
    ('img', 'src', 'resource'),
    ('audio', 'src', 'resource'),
    ('video', 'src', 'resource'),
    ('source', 'src', 'resource'),
    ('script', 'src', 'scripts'),
    ('link', 'href', 'style'), # can sometimes be other things
    ('area', 'href', 'webpage'),
    ('embed', 'src', 'resource'),
    ('iframe', 'src', 'resource'),
    ('input', 'src', 'resource'),
    ('form', 'action', 'other_url'),
    ('object', 'data', 'resource'),
    ('html', 'manifest', 'other_url'),
    ('svg', 'xlink:href', 'webpage'),
]

# Note: For the 'input' tag, an additional filter is provided for type 'image'.
# For SVG elements, a namespace filter is used to correctly identify elements with xlink:href.

class Fragment_Parser:

    # def __init__(self, spider:CachedSpider, response: HtmlResponse, html_hash: Hash64, path: str, content_type='html', **kwargs) -> None:
    def __init__(self, spider:CachedSpider, response: HtmlResponse, content_type, **kwargs) -> None:
        self.create_url = spider.create_url
        # self.html_hash = html_hash
        # self.path = path
        self.response = response
        self.url = response.url.split(fragment_separator)[0] # take off html_hash and any other # string 
        self.url_item = self.create_url(self.url)
        self.domain_name = self.url_item['domain_name']
        self.content_type = content_type
        self.fragment_text: str = response.text
        self.content_hash=hash64(self.fragment_text)

        self.soup = BeautifulSoup(self.fragment_text, features="lxml")

    def parse_fragment(self):
        self.content_item = self.create_content_item()
        logging.info('yield content item')
        # print('yeild content item')
        yield self.content_item        
        yield from self.gen_link_items()

    def create_content_item(self) -> ContentItem:
        fragment_text = self.response.text
        content_text = markdown(fragment_text)
        plain_text = markdown(fragment_text, links=False)

        return ContentItem(
            content_hash=self.content_hash,  # Or hash64(response.text) if you want to use the fragment_hash
            domain_name=self.domain_name,
            fragment_text= fragment_text,
            fragment_hash=self.content_hash,
            content_text=content_text,
            content_type=self.content_type,
            ## temporarily use fragment_text !!!
            plain_text=plain_text,
            plain_hash=hash64(plain_text)
        )
            
    def gen_link_items(self):
        for tag_type, attr, link_type in url_patterns:
            for tag in self.soup.find_all(tag_type, **{attr: True}):
                yield self.create_link_from_attr(tag, attr, link_type)

        for tag in self.soup.find_all('style'):
            css_content = tag.string or ''
            yield from self.gen_css_links(css_content, 'style', '')

        for tag in self.soup.find_all(style=True):
            inline_style = tag['style']
            yield from self.gen_css_links(inline_style, 'inline', 'style')


    def gen_css_links(self, css_content, link_tag, link_attr):
        css_url_pattern = re.compile(r'url\((.*?)\)') # !!! untested
        css_import_pattern = re.compile(r'@import\s+["\']?(.*?)["\']?;') # !!! untested

        for url_match in css_url_pattern.finditer(css_content):
            url = url_match.group(1).strip('\'"')
            yield self.create_css_link_item(url, 'resource', link_tag, link_attr)
        
        for import_match in css_import_pattern.finditer(css_content):
            url = import_match.group(1)
            yield self.create_css_link_item(url, 'style', link_tag, link_attr)


    def create_css_link_item(self, url_raw: str, link_type: str, link_tag: str, link_attr: str) -> LinkItem:
        domain_name, target_url = norm_url(url_raw, self.response )

        return LinkItem(
            domain_name=self.domain_name,
            content_hash=self.content_hash,
            target_url=target_url,
            target_url_raw = url_raw,
            link_text='',
            link_type=link_type,
            link_tag=link_tag,
            link_attr=link_attr,
            is_internal= domain_name == self.domain_name
        )
    
    def create_link_from_attr(self, bs_tag:Tag, attr:str, link_type:str):
        url_raw = get_url_attr(bs_tag,attr)
        domain_name, target_url = norm_url(url_raw, self.response )
        # target_url_item = self.create_url(target_url)
        return LinkItem(
            domain_name=self.domain_name,
            content_hash=self.content_hash,
            target_url=target_url,
            target_url_raw = url_raw,
            link_text=md_soup(bs_tag),
            link_tag=bs_tag.name,
            link_attr=attr,
            link_type=link_type,
            is_internal= domain_name == self.domain_name
        )

# if __name__ == "__main__":
#     # Example usage
#     from .html_snippets import test_html_content 

#     soup = BeautifulSoup(test_html_content, 'html.parser')
#     domain = 'example.com'  # The domain of the content
#     for link_item in gen_link_items(soup, domain):
#         # Process each LinkItem
#         pass

def get_url_attr(tag:Tag, attr:str) -> str:
    attribute: str | list[str] | None = tag.get(attr, '')
    if isinstance(attribute, list):
        # Join the list into a single string, separated by spaces
        logging.error('should only be a single URL in attribute')
        return attribute[0]
    if attribute is None:
        logging.error('attribute should contain URL')
        return ""
    return attribute
