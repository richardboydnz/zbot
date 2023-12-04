from scrapy.item import Item, Field  # type: ignore
from typing import Optional

from myscraper.db.db_store import DBMapping, SimpleDbStore, connection


class LinkItem(Item):
    # Links Fact Table
    link_id: Optional[int] = Field()

    domain_id: Optional[int] = Field()
    domain_name: Optional[str] = Field()
    content_id: Optional[int] = Field()
    content_hash: Optional[int] = Field()
    target_url: Optional[str] = Field()
    target_url_id: Optional[int] = Field()
    link_text: str = Field()
    link_tag: str= Field()
    link_attr: str= Field()
    link_type: str= Field()
    is_internal: bool = Field()

link_table = """
CREATE TABLE link_fact (
    link_id SERIAL PRIMARY KEY,
    domain_id INTEGER REFERENCES domain_dim(domain_id),
    target_url_id INTEGER REFERENCES url_dim(url_id),
    content_id INTEGER REFERENCES content_dim(content_id),
    link_text TEXT,
    link_tag TEXT,
    link_attr TEXT,
    link_type TEXT,
    is_internal BOOLEAN
);
"""

field_mapping_links = {
    'domain_id': 'domain_id',
    'target_url_id': 'target_url_id',
    'content_id': 'content_id',
    'link_text': 'link_text',
    'link_tag': 'link_tag',
    'link_attr': 'link_attr',
    'link_type': 'link_type',
    'is_internal': 'is_internal',
    # 'domain_name' and 'target_url' are excluded if they are not stored in the database
}

links_db_mapping = DBMapping(
    item_to_db=field_mapping_links,
    itemClass=LinkItem,
    db_table='link_fact',
    key_field='',  # can not be queried with a secondary key
    id_field='link_id',  # Assuming 'fragment_id' is the unique key field
)

def LinkDBStore(db: connection) -> SimpleDbStore:
    return SimpleDbStore(db, links_db_mapping)