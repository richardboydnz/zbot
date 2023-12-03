from typing import Optional
from myscraper.db.db_cache import DBSingletonCache
from myscraper.db.db_store import DBMapping
from myscraper.items.item_cache import SingletonCache 
from scrapy.item import Item, Field  # type: ignore
from ..db import connection

domain_table = """
CREATE TABLE domain_dim (
    domain_id SERIAL PRIMARY KEY,
    domain_name VARCHAR(255) NOT NULL
);
"""

class DomainItem(Item):
    domain_id = Field()
    domain_name = Field()

domain_field_mapping = {
    'domain_name': 'domain_name',
}

domain_db_mapping = DBMapping(
    item_to_db=domain_field_mapping,
    itemClass=DomainItem,
    db_table='domain_dim',
    key_field='domain_name',
    id_field='domain_id'
)

def make_domain(key: str) -> Optional[DomainItem]:
    return DomainItem(domain_name=key)

def DomainCache() -> SingletonCache:
    key_field = 'domain_name'  # Assuming 'domain_name' is the key field for DomainItem
    return SingletonCache(key_field, make_domain)


def DomainDBCache(db: connection) -> DBSingletonCache:
    return DBSingletonCache(db, domain_db_mapping, make_domain)

# You'll need to define `create_gen_func_url` and `create_gen_func_domain`
# These are the generator functions that create a new UrlItem or DomainItem if not found in the database.
