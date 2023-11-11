from scrapy.item import Item, Field  # type: ignore
from typing import Optional

class CrawlItem(Item):
    crawl_id = Field()
    domain_id = Field()
    domain_name = Field()
    start_time = Field()
    end_time = Field()
    # Add other relevant fields

class DomainItem(Item):
    domain_id = Field()
    domain_name = Field()

class UrlItem(Item):
    url: str = Field()
    protocol: str = Field()
    domain: str = Field()
    path: str = Field()
    is_resource: bool = Field()
    is_webpage: bool = Field()
    resource_type: str = Field()
    last_status_code: int = Field()
    file_extension: str = Field()

class DownloadItem(Item):
    # Downloads Fact Table
    domain: Optional[str] = Field()
    domain_id: Optional[int] = Field()
    url: Optional[str] = Field()
    url_id: Optional[int] = Field()
    html_hash: Optional[int] = Field()
    download_timestamp: str = Field()
    http_status: int = Field()
    headers: str = Field()
    crawl_id: Optional[int] = Field()

class HtmlItem(Item):
    # Raw HTML Dimension Table (requires explicit creation)
    domain: Optional[str] = Field()
    domain_id: Optional[int] = Field()
    html_hash: Optional[int] = Field()
    html_data: str = Field()

class HtmlContentItem(Item):
    # HTML-Content Association Bridge Table
    domain: Optional[str] = Field()
    domain_id: Optional[int] = Field()
    html_id: Optional[int] = Field()
    html_hash: Optional[int] = Field()
    content_id: Optional[int] = Field()
    content_hash: Optional[int] = Field()
    content_path: str = Field()

class ContentItem(Item):
    # Content Dimension Table (requires explicit creation)
    domain: Optional[str] = Field()
    domain_id: Optional[int] = Field()
    content_hash: Optional[int] = Field()
    content_text: str = Field()
    content_type: str = Field()
    plain_text: str = Field()
    plain_text_hash: Optional[int] = Field()

class LinkItem(Item):
    # Links Fact Table
    domain: Optional[str] = Field()
    domain_id: Optional[int] = Field()
    from_content_id: Optional[int] = Field()
    from_content_hash: Optional[int] = Field()
    to_url: Optional[str] = Field()
    to_url_id: Optional[int] = Field()
    link_text: str = Field()
    link_tag: str= Field()
    link_attr: str= Field()
    is_internal: bool = Field()

