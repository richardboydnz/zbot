from scrapy.http import HtmlResponse  # type: ignore
import logging

from myscraper.db import init_db
from myscraper.items.content_item import ContentDBCache

class HandleHtmlFragmentRequest:
    def __init__(self, db: init_db.connection):
        self.db = db
        self.content_store = ContentDBCache(self.db)

    @classmethod
    def from_crawler(cls, crawler):
        # Extract settings from the crawler
        db_settings = crawler.settings.getdict('DB_SETTINGS')

        # Create the database connection using settings
        db = init_db.get_db(db_settings)  # Modify the get_db method to accept settings

        # Return an instance of the pipeline class with the db connection
        return cls(db)

    def spider_opened(self, spider):
        self.spider = spider

    def close_spider(self, spider):
        # Close the database cursor when the spider closes
        init_db.close_db(self.db)

    def process_request(self, request, spider):
        # print(f'---- Request ---, request {request}')

        # Check if the request contains a fragment
        fragment = request.meta.get('fragment')
        if fragment:
            # Check if the fragment already exists in the database
            if self.fragment_exists_in_db(fragment):
                logging.debug(f'Fragment already exists in DB, skipping: {fragment}')
                return HtmlResponse(url=request.url, status=204)  # No content status

            # Process the fragment
            return HtmlResponse(
                url=request.url,
                body=fragment.encode('utf-8'),
                encoding='utf-8',
                request=request
            )

        return None  # Return None for other requests

    def fragment_exists_in_db(self, fragment):
        # Implement the logic to check if the fragment exists in the database
        # For example, query the database using self.db_cache and check if the fragment is present
        # Return True if exists, False otherwise
        return False

    def process_exception(self, request, exception, spider):
        if isinstance(exception, TCPTimedOutError):
            return spider.handle_download_error(request, exception)

        # You can add more exception types here if needed

    def handle_timeout(self, request, exception, spider):
        # Handle the timeout error
        spider.logger.error(f'TCP Timeout error occurred for {request.url}: {exception}')
        # You can also call a method of the spider here if you want
        return None  # Or you could return a response or a request
