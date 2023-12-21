import logging
import pytest
from myscraper.db.init_db import get_db, create_db
from myscraper.db.db_cache import DbGeneratorCache
from myscraper.items.domain_item import DomainDBCache, make_domain, domain_db_mapping   # Replace with your actual module and objects
from myscraper.items.url_item import UrlItem, build_url, get_url_item, url_db_mapping  # Replace with the actual path
from .settings_test import DB_SETTINGS
# Assuming 'connection' is a mockable database connection object
# and 'make_db_url_item' is a function that creates a UrlItem from a database entry


@pytest.fixture
def db():
    db =  get_db(DB_SETTINGS)
    create_db(db)
    return db



@pytest.fixture
def domain_db_generator_cache(db):
    return DbGeneratorCache[str](db, domain_db_mapping, make_domain)

@pytest.fixture
def make_db_url_item(domain_db_generator_cache):
    def f(url):

        print('------------------ make_db_url_item', url)
        url_item = get_url_item(url)
        print(f'--- url_item {url_item}')

        url_item["domain_id"] = domain_db_generator_cache.get_id(url_item["domain_name"])
        print(f'--- domain id {url_item["domain_id"]}')
        return url_item
    return f

@pytest.fixture
def url_db_generator_cache( db, domain_db_generator_cache, make_db_url_item):
    return DbGeneratorCache[str](db, url_db_mapping, make_db_url_item)



@pytest.fixture
def sample_url_item():
    return UrlItem(
        url="http://example.com/index.html",
        domain_name="example.com",
        protocol="http",
        path="/index.html",
        is_resource=False,
        is_webpage=True,
        resource_type="",
        last_status_code=200,
        file_extension=""
    )

def test_store_and_fetch_url(url_db_generator_cache, sample_url_item, make_db_url_item):
    # Test storing a URL and then fetching it
    url = build_url(sample_url_item)
    url_item = make_db_url_item(url)
    print('URL_ITEM', url_item)
    url_db_generator_cache.store_item(url_item)
    print('URL_CACHE', url_db_generator_cache.cache)
    fetched_item = url_db_generator_cache.fetch_item(sample_url_item['url'])
    print('FETCHED', fetched_item)
    assert build_url(fetched_item) == url

def test_fetch_nonexistent_url(url_db_generator_cache):
    # Test fetching a URL that does not exist
    fetched_item = url_db_generator_cache.fetch_item("http://nonexistent.com")
    assert fetched_item is None

def test_store_invalid_url(url_db_generator_cache):
    # Test storing an invalid URL (invalid data type, missing fields, etc.)
    invalid_url_item = UrlItem(url="not a valid url")
    with pytest.raises(Exception):  # Replace with specific exception if applicable
        url_db_generator_cache.store_item(invalid_url_item)

# Additional tests can be added for other edge cases and functionalities
