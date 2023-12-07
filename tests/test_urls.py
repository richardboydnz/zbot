import pytest
from myscraper.db import init_db
from myscraper.db.db_cache import DbGeneratorCache
from myscraper.items.domain_item import DomainDBCache   # Replace with your actual module and objects
from myscraper.items.url_item import UrlItem, build_url, get_url_item, url_db_mapping  # Replace with the actual path

# Assuming 'connection' is a mockable database connection object
# and 'make_db_url_item' is a function that creates a UrlItem from a database entry
DB_SETTINGS = {
    'database': 'crown_scraping',
    'user': 'crown_scraping',
    'password': 'xAK9q5IMnj1opUh3',
    'host': '192.168.1.10',
    'port': '5432'
}

db = init_db.get_db(DB_SETTINGS)
domains = DomainDBCache(db)
def make_db_url_item(url):
    print('------------------ make_db_url_item', url)
    url_item = get_url_item(url)
    url_item["domain_id"] = domains.get_id(url_item["domain_name"])
    return url_item

@pytest.fixture
def db_generator_cache():
    return DbGeneratorCache(db, url_db_mapping, make_db_url_item)



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

def test_store_and_fetch_url(db_generator_cache, sample_url_item):
    # Test storing a URL and then fetching it
    url = build_url(sample_url_item)
    url_item = make_db_url_item(url)
    print('URL_ITEM', url_item)
    db_generator_cache.store_item(url_item)
    print('URL_CACHE', db_generator_cache.cache)
    fetched_item = db_generator_cache.fetch_item(sample_url_item['url'])
    print('FETCHED', fetched_item)
    assert build_url(fetched_item) == url

def test_fetch_nonexistent_url(db_generator_cache):
    # Test fetching a URL that does not exist
    fetched_item = db_generator_cache.fetch_item("http://nonexistent.com")
    assert fetched_item is None

def test_store_invalid_url(db_generator_cache):
    # Test storing an invalid URL (invalid data type, missing fields, etc.)
    invalid_url_item = UrlItem(url="not a valid url")
    with pytest.raises(Exception):  # Replace with specific exception if applicable
        db_generator_cache.store_item(invalid_url_item)

# Additional tests can be added for other edge cases and functionalities
