import re
from bs4 import BeautifulSoup, Tag
from scrapy.http import Request, Response # type: ignore
from myscraper.items import ContentItem, CrawlItem, DomainItem, DownloadItem, HtmlContentItem, HtmlItem, LinkItem
from myscraper.spiders.cached_spider import CachedSpider

from myscraper.encode.hash import Hash64
from scrapy.http import HtmlResponse 
from ..items import LinkItem
from ..encode.markdown import soup_to_markdown as md_soup, markdown 
from myscraper.encode.hash import hash64, Hash64 
from myscraper.spiders.cached_spider import CachedSpider

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

    def __init__(self, spider:CachedSpider, response: HtmlResponse, html_hash: Hash64, content_type='html', **kwargs) -> None:
        self.url_cache = spider.urls
        self.html_hash = html_hash
        self.response = response
        self.url = response.url
        url_item = self.url_cache.get_item(self.url)
        self.domain = url_item['domain']
        self.content_type = content_type
        self.fragment_text: str = response.text
        self.fragment_hash=hash64(self.fragment_text)

        self.soup = BeautifulSoup(self.fragment_text)

    def parse_fragment(self):
        fragment = self.response.text
        content_item = self.create_content_item()

        yield content_item        

        association_item = HtmlContentItem(
            domain=self.domain,
            html_hash=self.html_hash,
            fragment_hash=self.fragment_hash
        )
        yield association_item

        yield from self.gen_link_items()

    def create_content_item(self) -> ContentItem:
        fragment_text = self.response.text
        content_text = markdown(fragment_text)
        plain_text = markdown(fragment_text, links=False)

        return ContentItem(
            domain=self.url_cache.get_item(self.response.url)['domain'],
            fragment_text= fragment_text,
            fragment_hash=hash64(fragment_text),
            content_text=content_text,
            ## temporarily use fragment_text !!!
            content_hash=hash64(fragment_text),  # Or hash64(response.text) if you want to use the fragment_hash
            plain_text=plain_text,
            plain_hash=hash64(plain_text)
        )
            
    def gen_link_items(self):
        for tag_type, attr, link_type in url_patterns:
            for tag in self.soup.find_all(tag_type, **{attr: True}):
                link = self.create_link_from_attr(tag, attr, link_type)
                if (link_type == 'webpage') and link['is_internal']:
                    yield Request(url=link['to_url'], method='GET')  # GET request for external resources
                else:
                    yield Request(url=link['to_url'], method='HEAD')  # HEAD request for external resources

    # for tag in soup.find_all('style'):
    #     css_content = tag.string or ''
    #     yield from gen_css_links(css_content, content_item, 'style', '')

    # for tag in soup.find_all(style=True):
    #     inline_style = tag['style']
    #     yield from gen_css_links(inline_style, content_item, 'inline', 'style')


    def gen_css_links(css_content, content_item, link_tag, link_attr):
        css_url_pattern = re.compile(r'url\((.*?)\)')
        css_import_pattern = re.compile(r'@import\s+["\']?(.*?)["\']?;')

        for url_match in css_url_pattern.finditer(css_content):
            yield LinkItem(
                domain=content_item['domain'],
                from_content_raw_hash=content_item['content_raw_hash'],
                to_url=url_match.group(1),
                link_type='resources',
                link_tag=link_tag,
                link_attr=link_attr,
                internal=content_item['domain'] in url_match.group(1)
            )
        
        for import_match in css_import_pattern.finditer(css_content):
            yield LinkItem(
                domain=content_item['domain'],
                from_content_raw_hash=content_item['content_raw_hash'],
                to_url=import_match.group(1),
                link_type='styles',
                link_tag=link_tag,
                link_attr=link_attr,
                internal=content_item['domain'] in import_match.group(1)
            )

    def create_link_from_attr(self, bs_tag:BeautifulSoup, attr:str, link_type:str):
        to_url = self.response.urljoin( bs_tag[attr] )
        to_url_item = self.url_cache.get_item(to_url)

        return LinkItem(
            domain=self.domain,
            fragment_hash=self.fragment_hash,
            to_url=to_url,
            link_text=md_soup(bs_tag),
            link_tag=bs_tag.name,
            link_attr=attr,
            link_type=link_type,
            is_internal= to_url_item['domain'] == self.domain
        )

# if __name__ == "__main__":
#     # Example usage
#     from .html_snippets import test_html_content 

#     soup = BeautifulSoup(test_html_content, 'html.parser')
#     domain = 'example.com'  # The domain of the content
#     for link_item in gen_link_items(soup, domain):
#         # Process each LinkItem
#         pass
