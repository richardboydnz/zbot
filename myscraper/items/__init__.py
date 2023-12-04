from scrapy.item import Item, Field  # type: ignore
from typing import Optional

from myscraper.encode.hash import Hash64 

from .items import get_class
from .domain_item import DomainItem, DomainCache,DomainDBCache
from .url_item import UrlItem, UrlCache
from .html_item import HtmlItem, HtmlDBCache
from .download_item import DownloadItem, DownloadDBStore
from .crawl_item import CrawlItem, CrawlDBStore
from .content_item import ContentItem, ContentDBCache
from .html_content_item import HtmlContentItem, HtmlContentDBStore
from .link_item import LinkItem, LinkDBStore