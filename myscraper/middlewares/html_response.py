from scrapy.http import HtmlResponse, Response  # type: ignore
from scrapy.exceptions import IgnoreRequest # type: ignore

import logging

from myscraper.db import init_db
from myscraper.items.content_item import ContentDBCache
from myscraper.items.html_item import HtmlDBCache

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
        try:
            if request.method == "GET":
                logging.debug(f'pass on {request}')

                return None
            if request.method == "INIT":
                return Response(
                    url=request.url,
                    body=b"",
                    request=request
                )
            elif request.method == "HTML":
                content_hash = request.meta.get('content_hash')
                if content_hash: # crawl or fragment
                    logging.info(f'pass on {content_hash}')

                    # Check if the fragment already exists in the database
                    content_id = self.content_store.get_id(content_hash)
                    content = request.meta.get('content')

                    status = 200 if content_id is None else 201

                    # Process the fragment
                    return HtmlResponse(
                        url=request.url,
                        status=status,
                        body=content.encode('utf-8'),
                        encoding='utf-8',
                        request=request,
                    )
                
            logging.debug(f'pass on {request}')
            return None
        except IgnoreRequest as e:
            raise
        except Exception as e:
            self.db.rollback()
            spider.logger.error('########################################')

            spider.logger.error(f"Error while processing request: {request}")
            spider.logger.error(e)
            raise
        finally:
            if not self.db.closed:
                self.db.commit()

        return None  # Return None for other requests

    # def fragment_exists_in_db(self, fragment):
    #     # Implement the logic to check if the fragment exists in the database
    #     # For example, query the database using self.db_cache and check if the fragment is present
    #     # Return True if exists, False otherwise
    #     return False

    # def process_exception(self, request, exception, spider):
    #     spider.logger.error(f'Exception occured while processing {request.url}: {exception}')
    #     return None

        # You can add more exception types here if needed

    def handle_timeout(self, request, exception, spider):
        # Handle the timeout error
        spider.logger.error(f'TCP Timeout error occurred for {request.url}: {exception}')
        # You can also call a method of the spider here if you want
        return None  # Or you could return a response or a request
