from scrapy.item import Item, Field  # type: ignore
from typing import Optional

from myscraper.db.db_store import DBMapping, SimpleDbStore
from myscraper.encode.hash import Hash64
from ..db import connection

html_content_table = """
CREATE TABLE html_content_bridge (
    bridge_id SERIAL PRIMARY KEY,
    domain_id INTEGER REFERENCES domain_dim(domain_id),
    html_id INTEGER REFERENCES html_dim(html_id),
    content_id INTEGER,
    path TEXT NOT NULL,
    UNIQUE(domain_id, html_id, content_id)
);
"""



field_mapping_html_content = {
    'domain_id': 'domain_id',
    'html_id': 'html_id',
    'content_id': 'content_id',
    'path': 'path',
    # 'domain_name' is excluded if it's not stored in the database
}

class HtmlContentItem(Item):
    # HTML-Content Association Bridge Table
    bridge_id: Optional[int] = Field()
    domain_name: Optional[str] = Field()
    domain_id: Optional[int] = Field()
    html_id: Optional[int] = Field()
    html_hash: Optional[int] = Field()
    content_id: Optional[int] = Field()
    content_hash: Hash64 = Field()
    path: str = Field()
    
html_content_db_mapping = DBMapping(
    item_to_db=field_mapping_html_content,
    itemClass=HtmlContentItem,
    db_table='html_content_bridge',
    key_field='',  # No secondary key
    id_field='bridge_id'
)

def HtmlContentDBStore(db: connection) -> SimpleDbStore:
    return SimpleDbStore(db, html_content_db_mapping)
