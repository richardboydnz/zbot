
from myscraper.spiders.website_spider import WebsiteSpider


class WPSpider(WebsiteSpider):
    name: str = 'wpscraper'


    def init_crawl(self):
        scan_api()


        super().init_crawl()

    def parse_pages_api(self, response):
        # Load the JSON response
        data = json.loads(response.text)

        # Yield each page as a simple JSON item
        for page in data:
            yield {
                'id': page['id'],
                'title': page['title']['rendered'],
                # Add other fields as needed
            }

        # Determine if there are more pages to fetch
        total_pages = int(response.headers.get('X-WP-TotalPages', 0))
        current_page = int(response.url.split('page=')[1].split('&')[0])
        if current_page < total_pages:
            next_page = current_page + 1
            next_page_url = f'http://example.com/wp-json/wp/v2/pages?per_page=10&page={next_page}&orderby=id&order=asc'
            yield scrapy.Request(next_page_url, callback=self.parse_pages_api)
