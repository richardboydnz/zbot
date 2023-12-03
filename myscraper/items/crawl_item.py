from scrapy.item import Item, Field  # type: ignore
from ..db import connection

crawl_table = """
CREATE TABLE crawl_dim (
    crawl_id SERIAL PRIMARY KEY,
    domain_id INTEGER REFERENCES domain_dim(domain_id),
    crawl_timestamp TIMESTAMP
);
"""

# crawl_hash BIGINT,
# endtime
#     UNIQUE (crawl_hash, domain_id)


class CrawlItem(Item):
    crawl_id = Field()
    domain_id = Field()
    domain_name = Field()
    crawl_timestamp = Field()

field_mapping_crawl = {
    'domain_id': 'domain_id',
    'crawl_timestamp': 'crawl_timestamp'
}

from myscraper.db.db_store import DBMapping

crawl_db_mapping = DBMapping(
    item_to_db=field_mapping_crawl,
    itemClass=CrawlItem,
    db_table='crawl_dim',  # Replace with your actual table name
    key_field='crawl_id',  # Assuming 'crawl_id' is the unique key field
    id_field='crawl_id'  # Assuming 'crawl_id' is also the ID field in the table
)

from myscraper.db.db_store import SimpleDbStore

def CrawlDBStore(db: connection) -> SimpleDbStore:
    return SimpleDbStore(db, crawl_db_mapping)
