from typing import Optional
from myscraper.db.db_cache import DbGeneratorCache
from myscraper.db.db_store import DBMapping
from myscraper.items.item_cache import GeneratorCache 
from scrapy.item import Item, Field  # type: ignore
from ..db import Connection

domain_table = """
CREATE TABLE domain_dim (
    domain_id INTEGER PRIMARY KEY AUTOINCREMENT,
    domain_name TEXT NOT NULL,
    UNIQUE (domain_name)
);
"""

class DomainItem(Item):
    domain_id: Optional[int] = Field()
    domain_name: str = Field()

domain_field_mapping = {
    'domain_name': 'domain_name',
}

domain_db_mapping = DBMapping(
    item_to_db=domain_field_mapping,
    itemClass=DomainItem,
    db_table='domain_dim',
    key_field='domain_name',
    constraint='(domain_name)',
    id_field='domain_id'
)

def make_domain(key: str) -> Optional[DomainItem]:
    return DomainItem(domain_name=key)

def DomainCache() -> GeneratorCache:
    assert domain_db_mapping.key_field is not None
    return GeneratorCache(domain_db_mapping.key_field, make_domain)


def DomainDBCache(db: Connection) -> DbGeneratorCache:
    return DbGeneratorCache(db, domain_db_mapping, make_domain)

# You'll need to define `create_gen_func_url` and `create_gen_func_domain`
# These are the generator functions that create a new UrlItem or DomainItem if not found in the database.
