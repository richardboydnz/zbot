from typing import Optional
from scrapy.item import Item, Field # type: ignore

from myscraper.encode.hash import Hash64
from ..db.db_store import DBMapping
from ..db.db_cache import DbCache
from ..db import Connection

content_table = """
CREATE TABLE content_dim (
    content_id INTEGER PRIMARY KEY AUTOINCREMENT,
    content_hash INTEGER,
    content_text TEXT NOT NULL,
    content_type TEXT,
    plain_text TEXT,
    plain_hash INTEGER,
    domain_id INTEGER,
    fragment_hash INTEGER,
    fragment_text TEXT NOT NULL,
    FOREIGN KEY(domain_id) REFERENCES domain_dim(domain_id),
    UNIQUE (content_hash, domain_id)
);
"""
#     content_type VARCHAR(50) CHECK (content_type IN ('page', 'header', 'footer', 'aside', 'nav')),


class ContentItem(Item):
    content_id: Optional[int] = Field()
    domain_name: Optional[str] = Field()
    domain_id: Optional[int] = Field()

    fragment_hash: Hash64 = Field()
    fragment_text: str = Field()
    content_text: str = Field()
    content_hash: Optional[Hash64] = Field()
    content_type: str = Field()
    plain_text: str = Field()
    plain_hash: Optional[Hash64] = Field()

field_mapping_content = {
    'domain_id': 'domain_id',
    'fragment_hash': 'fragment_hash',
    'fragment_text': 'fragment_text',
    'content_text': 'content_text',
    'content_hash': 'content_hash',
    'content_type': 'content_type',
    'plain_text': 'plain_text',
    'plain_hash': 'plain_hash'
}

content_db_mapping = DBMapping(
    item_to_db=field_mapping_content,
    itemClass=ContentItem,
    db_table='content_dim',
    key_field='content_hash',
    constraint='(content_hash, domain_id)',
    id_field='content_id'
)

def ContentDBCache(db: Connection) -> DbCache:
    return DbCache(db, content_db_mapping)
