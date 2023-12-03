from scrapy.item import Item, Field  # type: ignore
from typing import Optional

from myscraper.db.db_store import DBMapping, SimpleDbStore
from ..db import connection


download_table = """
CREATE TABLE download_fact (
    download_id SERIAL PRIMARY KEY,
    domain_id INTEGER REFERENCES domain_dim(domain_id),   -- Foreign key to domain_dim
    url_id INTEGER REFERENCES url_dim(url_id),            -- Foreign key to url_dim
    html_id INTEGER,                                    -- New column for html_hash
    download_timestamp TIMESTAMP NOT NULL,                -- Timestamp of the download
    http_status INTEGER,                                  -- HTTP status code
    headers TEXT,                                         -- HTTP headers as text
    crawl_id INTEGER REFERENCES crawl_dim(crawl_id)       -- Foreign key to crawl_dim
);
"""

class DownloadItem(Item):
    # Downloads Fact Table
    domain_name: Optional[str] = Field()
    domain_id: Optional[int] = Field()
    download_id: Optional[int] = Field()
    url: Optional[str] = Field()
    url_id: Optional[int] = Field()
    html_hash: Optional[int] = Field()
    html_id: Optional[int] = Field()
    download_timestamp: str = Field()
    http_status: int = Field()
    headers: str = Field()
    crawl_id: Optional[int] = Field()

field_mapping_downloads = {
    'domain_id': 'domain_id',
    'url_id': 'url_id',
    'html_id': 'html_id',
    'download_timestamp': 'download_timestamp',
    'http_status': 'http_status',
    'headers': 'headers',
    'crawl_id': 'crawl_id',
    # 'domain_name' and 'url' are excluded if they are not stored in the database
}

downloads_db_mapping = DBMapping(
    item_to_db=field_mapping_downloads,
    itemClass=DownloadItem,
    db_table='download_fact',
    key_field='url_id',  # Assuming 'url_id' is the unique key field
    id_field='download_id'
)

def DownloadDBStore(db: connection) -> SimpleDbStore:
    return SimpleDbStore(db, downloads_db_mapping)

