from myscraper.db.db_cache import DBSingletonCache
from myscraper.db.db_store import DBMapping
from myscraper.items.item_cache import SingletonCache
from urllib.parse import urlparse
from typing import Optional
from scrapy.item import Item, Field  # type: ignore
from ..db import connection


url_table = """
CREATE TABLE url_dim (
    url_id SERIAL PRIMARY KEY,
    url VARCHAR(1024) NOT NULL,
    protocol VARCHAR(10),
    domain_id INTEGER REFERENCES domain_dim(domain_id),
    path TEXT,
    is_resource BOOLEAN,
    is_webpage BOOLEAN,
    resource_type VARCHAR(255),
    last_status_code INTEGER,
    file_extension VARCHAR(50),
    UNIQUE (url, domain_id)
);
"""


class UrlItem(Item):
    url_id: Optional[int] = Field()
    url: str = Field()
    protocol: str = Field()
    domain_name: Optional[str] = Field()  # Textual representation of the domain
    domain_id: Optional[int] = Field()  # Foreign key to the domain in the database
    path: str = Field()
    is_resource: bool = Field()
    is_webpage: bool = Field()
    resource_type: str = Field()
    last_status_code: int = Field()
    file_extension: str = Field()

field_mapping_url = {
    'url': 'url',
    'protocol': 'protocol',
    'domain_id': 'domain_id',  # Maps to the foreign key column in the database
    'path': 'path',
    'is_resource': 'is_resource',
    'is_webpage': 'is_webpage',
    'resource_type': 'resource_type',
    'last_status_code': 'last_status_code',
    'file_extension': 'file_extension'
}

url_db_mapping = DBMapping(
    item_to_db=field_mapping_url,
    itemClass=UrlItem,
    db_table='url_dim',
    key_field='url',
    id_field='url_id'
)

def make_url(url: str) -> UrlItem:
    # Parse the URL
    parsed_url = urlparse(url)
    protocol = parsed_url.scheme
    domain_name = parsed_url.netloc
    path = parsed_url.path

    path_segments = path.split('/')
    last_path_segment = path_segments[-1] # if path_segments else ''
    file_parts = last_path_segment.split('.')
    file_extension = file_parts[-1] if len(file_parts) > 1 else ''

    is_resource = file_extension != '' and file_extension not in ['html', 'htm', 'php', 'asp', 'aspx', 'jsp']
    is_webpage = not is_resource

    return UrlItem(
        url=url,
        protocol=protocol,
        domain_name=domain_name,
        path=path,
        is_resource=is_resource,
        is_webpage=is_webpage,
        resource_type='',
        last_status_code=0,
        file_extension=file_extension
    )

def UrlCache() -> SingletonCache:
    return SingletonCache(url_db_mapping.key_field, make_url)

# def UrlDBCache(db: connection) -> DBSingletonCache:
#     return DBSingletonCache(db, url_db_mapping, make_url)
