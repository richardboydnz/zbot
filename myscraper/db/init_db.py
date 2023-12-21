from typing import Dict, Any

from ..items.domain_item import domain_table
from ..items.crawl_item import crawl_table
from ..items.url_item import url_table
from ..items.html_item import html_table
from ..items.content_item import content_table
from ..items.html_content_item import html_content_table
from ..items.download_item import download_table
from ..items.link_item import link_table
# from sqlite3 import Connection
from .sqlite_mock import Connection


drop_sql = """
-- drop facts
DROP TABLE IF EXISTS html_content_bridge;
DROP TABLE IF EXISTS link_fact;
DROP TABLE IF EXISTS download_fact;
-- drop dimensions
DROP TABLE IF EXISTS content_dim;
DROP TABLE IF EXISTS html_dim;
DROP TABLE IF EXISTS url_dim;
DROP TABLE IF EXISTS crawl_dim;
-- drop util (used by dimensions)
DROP TABLE IF EXISTS domain_dim;
"""


def get_db(db_settings: Dict[str,Any]) -> Connection:
    return Connection(db_settings)

def close_db(conn:Connection):
    conn.close()


def create_db(db:Connection):
    print('---------- Create DB')
    with db.cursor() as cursor:
        # cursor.executes(drop_sql)
        cursor.executescript(drop_sql)
        cursor.execute(domain_table)

        cursor.execute(crawl_table)
        cursor.execute(url_table)
        cursor.execute(html_table)
        cursor.execute(content_table)
        
        cursor.execute(html_content_table)
        cursor.execute(download_table)
        cursor.execute(link_table)


# from dbutils.pooled_db import PooledDB

# def get_db(db_settings: Dict[str,Any]) -> connection:
#     pool = PooledDB(
#     creator=psycopg2,  # Database module
#     maxconnections=6,  # Max connections
#     **db_settings         # Additional connection parameters
#     )
#     return pool

# def close_db(pool):
#     pool.close()
    