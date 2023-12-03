
from scrapy import Item
from myscraper.db.db_cache import DBSingletonCache

from myscraper.items import UrlItem
from myscraper.items.url_item import make_url, url_db_mapping, U

from ..items import UrlCache
from ..db import init_db # type: ignore

from ..items import DownloadItem, HtmlItem, CrawlItem
from ..items import DomainDBCache, UrlDBCache, HtmlDBCache, DownloadDBStore, CrawlDBStore

# from myscraper.db.db_store import SimpleDbStore, DBMapping
# from scrapy import Item # type: ignore


class UrlPipe:

    def __init__(self, db):
        # Initialize the pipeline with the database connection
        self.db = db
        self.domains = DomainDBCache(self.db)
        self.url_cache = DBSingletonCache(db, url_db_mapping, self.make_db_url_item)
        self.urls = UrlDBCache(self.db)
        self.domain_name = ""
        self.domain_id = 0

    @classmethod
    def from_crawler(cls, crawler):
        # Extract settings from the crawler
        db_settings = crawler.settings.getdict('DB_SETTINGS')

        # Create the database connection using settings
        db = init_db.get_db(db_settings)  # Modify the get_db method to accept settings
        init_db.create_db(db)

        # Return an instance of the pipeline class with the db connection
        return cls(db)

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        # Close the database cursor when the spider closes
        init_db.close_db(self.db)

    def make_db_url_item(self, url: str) -> UrlItem:
        url_item = make_url(url)
        url_item["domain_id"] = self.domains.get_id(url_item["domain_name"])
        return url_item
    
    def process_item(self, item: Item, spider):
        # Process items based on their type
        try:
            if isinstance(item, CrawlItem):
                self.init_domain(item)

            item["domain_id"] = self.domain_id

            url = item.get("url")
            if url:
                # check cache
                # create new item
                # store
                url_item = self.url_cache.fetch_item(url)

                domain_name = item.get("domain_name")
                if domain_name:
                    item["domain_id"] = 

                return self.process_download_item(item)
            elif isinstance(item, HtmlItem):
                return self.process_html_item(item)
            elif isinstance(item, CrawlItem):
                return self.process_crawl_item(item)      
            return item
        except Exception as e:
            # Rollback transaction in case of error
            self.db.rollback()
            spider.logger.error(f"Error processing item: {e}")
            raise
        finally:
            # This block executes regardless of whether an exception occurred
            # Commit transaction only if no exceptions were raised
            if not self.db.closed:
                print('!!! commit', item)
                self.db.commit()


    def process_download_item(self, item: DownloadItem):
        # Process a DownloadItem (e.g., store it in the database)
        item['domain_id'] = self.domains.get_id(item['domain_name'])
        item['url_id'] = self.urls.get_id(item['url'])
        item['html_id'] = self.html_store.get_id(item['html_hash'])
        item['crawl_id'] = self.crawl_id

        self.download_store.store_item(item)
        return None

    def process_html_item(self, item: HtmlItem):
        item['domain_id'] = self.domains.get_id(item['domain_name'])
        # Process an HtmlItem (e.g., store it in the database)
        self.html_store.store_item(item)
        return None

    def process_crawl_item(self, item: CrawlItem):
        item['domain_id'] = self.domains.get_id(item['domain_name'])
        item = self.crawl_store.store_item(item)
        self.crawl = item
        self.crawl_id = item['crawl_id']
        return None

    def init_domain(self, item: CrawlItem):
        self.domain_name = item["domain_name"]
        domain_item = self.domains.fetch_item(self.domain_name)
        self.domain_id = domain_item["domain_id"]
