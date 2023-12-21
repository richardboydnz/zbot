from typing import Dict, NamedTuple, Optional
from scrapy.item import Item, Field  # type: ignore
from ..db.db_cache import DbCache
from ..db.db_store import DBMapping
from ..encode.hash import hash64
# from ..pipelines.downloads_pipe import DownloadsPipe
from ..db import Connection

html_table = """
CREATE TABLE html_dim (
    html_id INTEGER PRIMARY KEY AUTOINCREMENT,
    html_hash INTEGER,
    html_data TEXT NOT NULL,
    domain_id INTEGER,
    FOREIGN KEY(domain_id) REFERENCES domain_dim(domain_id),
    UNIQUE (html_hash, domain_id)
);
"""

class HtmlItem(Item):
    domain_name: Optional[str] = Field()
    domain_id: Optional[int] = Field()
    html_id: Optional[int] = Field()
    html_hash: Optional[int] = Field()
    html_data: str = Field()

field_mapping_html = {
    'domain_id': 'domain_id',
    'html_hash': 'html_hash',
    'html_data': 'html_data'
}

html_db_mapping = DBMapping(
    item_to_db=field_mapping_html,
    itemClass=HtmlItem,
    db_table='html_dim',
    key_field='html_hash',
    constraint='(html_hash, domain_id)',
    id_field='html_id'
)

def make_html(domain_name: str, html_data: str) -> HtmlItem:
    # You would typically calculate the hash of the HTML data here
    html_hash = hash64(html_data)
    return HtmlItem(
        domain_name=domain_name,
        html_hash=html_hash,
        html_data=html_data
    )

def HtmlDBCache(db: Connection) -> DbCache:
    return DbCache(db, html_db_mapping)


