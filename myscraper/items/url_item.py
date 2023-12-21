import re
from myscraper.db.db_cache import DbGeneratorCache
from myscraper.db.db_store import DBMapping
from myscraper.items.item_cache import GeneratorCache
from urllib.parse import urlparse
from typing import Optional, Tuple
from scrapy.item import Item, Field  # type: ignore

url_table = """
CREATE TABLE url_dim (
    url_id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT NOT NULL,
    protocol TEXT,
    domain_id INTEGER,
    path TEXT,
    is_resource BOOLEAN,
    is_webpage BOOLEAN,
    resource_type TEXT,
    last_status_code INTEGER,
    file_extension TEXT,
    FOREIGN KEY(domain_id) REFERENCES domain_dim(domain_id),
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
    constraint='(url, domain_id)',
    id_field='url_id'
)

def norm_url( url:str, response = None) -> Tuple[str, str]:
    if response is not None:
        url = response.urljoin( url )
    url_item = get_url_item(url)
    return url_item.get('domain_name', ''), build_url(url_item)

fragment_separator = "??"

def get_url_item(url: str) -> UrlItem:
    # Parse the URL
    url = url.split('#')[0]
    url = url.split(fragment_separator)[0]

    parsed_url = urlparse(url)
    protocol = parsed_url.scheme
    netloc = parsed_url.netloc
    netloc_parts = netloc.split(':')
    domain_name = netloc_parts.pop(0)
    port = int(netloc_parts[0]) if netloc_parts else 80
    port_str = str(port)
    path = parsed_url.path
    normalized_path = re.sub(r'/+', '/', path)


    path_segments = path.split('/')
    last_path_segment = path_segments[-1] # if path_segments else ''
    file_parts = last_path_segment.split('.')
    file_extension = file_parts[-1] if len(file_parts) > 1 else ''

    is_resource = file_extension != '' and file_extension not in ['html', 'htm', 'php', 'asp', 'aspx', 'jsp']
    is_webpage = not is_resource

    # does not include port
    url_item = UrlItem(
        url=url,
        protocol=protocol, 
        domain_name=domain_name,
        path=normalized_path,
        is_resource=is_resource,
        is_webpage=is_webpage,
        resource_type='',
        last_status_code=0,
        file_extension=file_extension
    )
    norm_url = build_url(url_item)
    url_item['url'] = norm_url
    return url_item

def build_url( u: UrlItem) -> str:
    return u['protocol'] + '://' + u['domain_name'] + u['path']

def UrlCache() -> GeneratorCache:
    assert url_db_mapping.key_field is not None
    return GeneratorCache(url_db_mapping.key_field, get_url_item)

