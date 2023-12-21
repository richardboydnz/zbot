import pytest
from unittest.mock import Mock
from myscraper.db.init_db import get_db, create_db
from myscraper.db.db_cache import DbGeneratorCache
from myscraper.items.domain_item import DomainItem, DomainDBCache, domain_db_mapping, make_domain  # Replace with actual imports
from .settings_test import DB_SETTINGS

# Mock Database Connection

@pytest.fixture
def db():
    db =  get_db(DB_SETTINGS)
    create_db(db)
    return db

@pytest.fixture
def mock_db_connection(db):
    # Mock the database connection here
    return db

# Fixture for DomainDBCache
@pytest.fixture
def domain_db_cache(mock_db_connection):
    # return DomainDBCache(mock_db_connection)
    return DbGeneratorCache[str](mock_db_connection, domain_db_mapping, make_domain)

# Fixture for sample DomainItem
@pytest.fixture
def sample_domain_item():
    return DomainItem(domain_name="example.com")

# Test the creation of a DomainItem
def test_domain_item_creation(sample_domain_item):
    assert sample_domain_item['domain_name'] == "example.com"

# Test storing and fetching a domain item
def test_store_and_fetch_domain(domain_db_cache, sample_domain_item):

    # Store the domain item
    domain_db_cache.store_item(sample_domain_item)

    # Fetch the domain item
    fetched_item = domain_db_cache.fetch_item("example.com")
    assert fetched_item == sample_domain_item

# Test fetching a non-existent domain item
def test_fetch_nonexistent_domain(domain_db_cache):

    fetched_item = domain_db_cache.fetch_item("nonexistent.com")
    assert fetched_item is None

# Additional tests can be added for other edge cases and functionalities
