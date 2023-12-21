
BOT_NAME = "testscraper"

LOG_LEVEL = 'INFO'

CRAWL_DOMAIN : str = 'ballet.zavidan.info'

PG_DB_SETTINGS = {
    'database': 'crown_scraping_test',
    'user': 'crown_scraping',
    'password': 'xAK9q5IMnj1opUh3',
    'host': '192.168.1.10',
    'port': '5432'
}

SQLITE_DB_SETTINGS = {
    'database' : 'test.db'
}

DB_SETTINGS = SQLITE_DB_SETTINGS

CLEAR_DB = True
REDIRECT_ENABLED = False
FOLLOW_RESOURCES = False
