import psycopg2
from scrapy.exceptions import IgnoreRequest # type: ignore


class SkipDuplicateMiddleware:
    def __init__(self, db_settings):
        self.connection = psycopg2.connect(
            dbname=db_settings['dbname'],
            user=db_settings['user'],
            password=db_settings['password'],
            host=db_settings['host'],
            port=db_settings['port']
        )
        self.cursor = self.connection.cursor()

    @classmethod
    def from_crawler(cls, crawler):
        db_settings = crawler.settings.getdict("DB_SETTINGS")
        return cls(db_settings)

    def process_request(self, request, spider):
        self.cursor.execute("SELECT return_code FROM url WHERE URL = %s AND return_code = 200", (request.url,))
        if self.cursor.fetchone():
            spider.logger.info(f"Skipping already crawled URL: {request.url}")
            raise IgnoreRequest(f"Skipping already crawled URL: {request.url}")  # This will skip the request

    def close_spider(self, spider):
        self.cursor.close()
        self.connection.close()

