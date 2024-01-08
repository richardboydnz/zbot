
import datetime
import json
from typing import Any, Dict, List
from myscraper.items.download_item import DownloadItem
from myscraper.items.html_item import HtmlItem, make_html
from myscraper.spiders.website_spider import WebsiteSpider
from scrapy.http import Request, Response # type: ignore
from myscraper.types.api_page import Pages, Page

class WPSpider(WebsiteSpider):
    name: str = 'wpscraper'

    def apply_settings(self, settings: Dict[str, Any]):
        super().apply_settings(settings)
        self.api_url = self.domain_name + '/wp-json/wp/v2/pages'
        return self

    def init_crawl(self):
        yield from self.start_wordpress_api()

    def start_wordpress_api(self):
        yield Request(
            url=f"{self.api_url}?per_page=10&page=1&orderby=id&order=asc",
            callback=self.parse_api_pages,
            errback=self.parse_error
        )

    def parse_api_pages(self, response: Response):
        # Load the JSON response
        data: Pages = response.json()

        total_pages = int(response.headers.get('X-WP-TotalPages', 0))
        current_page = int(response.url.split("page=")[-1].split("&")[0])
        if current_page < total_pages:
            next_page = current_page + 1
            next_page_url = f"{self.base_url}?per_page=10&page={next_page}&orderby=id&order=asc"
            yield Request(
                url=next_page_url,
                callback=self.parse_api_pages,
                errback=self.parse_error
            )

        # Yield each page as a simple JSON item
        for page in data:
            yield from self.parse_api_page(page)

    def parse_api_page(self, page: Page):
        content = page['content']['rendered']
        html_item = self.create_html_from_api_page(page)
        yield html_item
        download_item = self.create_download_from_api_page( page,html_item['html_hash'])
        yield download_item
        content_type = "pagecontent" 
        yield self.make_fragment_req(download_item['url'], html_item['html_hash'], content, content_type, "[]")
#---

    def create_html_from_api_page(self, page: Page) -> HtmlItem:
        return make_html(domain_name=self.domain_name, html_data=page['content']['rendered'])

    def create_download_from_api_page(self, page: Page, html_hash:int) -> DownloadItem:
        page_url = f"{self.api_url}/{page['guid']}"
        headers = get_headers(page)
        return DownloadItem(
            domain_name=self.domain_name,
            url=page_url,
            html_hash=html_hash,
            download_timestamp=datetime.datetime.now().isoformat(),
            http_status=200,
            headers=headers,
        )

def get_headers(page: Page):
    # Create a copy of the page and remove 'content'
    modified_page = page.copy()
    # modified_page.pop('content', None)  # Removes 'content', does nothing if 'content' is not a key
    return json.dumps(modified_page)
