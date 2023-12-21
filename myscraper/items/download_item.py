from types import NoneType
from scrapy.item import Item, Field  # type: ignore
from typing import Optional, Type

from myscraper.db.db_store import DBMapping, SimpleDbStore
from myscraper.db import Connection

download_table = """
CREATE TABLE download_fact (
    download_id INTEGER PRIMARY KEY AUTOINCREMENT,
    domain_id INTEGER,
    url_id INTEGER,
    redirect_url_id INTEGER,
    html_id INTEGER,
    download_timestamp TEXT NOT NULL,
    http_status INTEGER,
    headers TEXT,
    crawl_id INTEGER,
    FOREIGN KEY(domain_id) REFERENCES domain_dim(domain_id),
    FOREIGN KEY(url_id) REFERENCES url_dim(url_id),
    FOREIGN KEY(redirect_url_id) REFERENCES url_dim(url_id),
    FOREIGN KEY(html_id) REFERENCES html_dim(html_id),
    FOREIGN KEY(crawl_id) REFERENCES crawl_dim(crawl_id),
    UNIQUE (crawl_id, url_id)
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
    redirect_url: Optional[str] = Field()
    redirect_url_id: Optional[int] = Field()


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
    key_field=None,  # can not be queried with a secondary key
    constraint='(crawl_id, url_id)',
    id_field='download_id'
)

def DownloadDBStore(db: Connection) -> SimpleDbStore:
    return SimpleDbStore(db, downloads_db_mapping)

