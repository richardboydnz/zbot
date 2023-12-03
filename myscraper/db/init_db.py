from typing import Dict, Any
import psycopg2

from ..items.domain_item import domain_table
from ..items.crawl_item import crawl_table
from ..items.url_item import url_table
from ..items.html_item import html_table
from ..items.download_item import download_table
from psycopg2.extensions import connection



drop_sql = """
-- drop facts
DROP TABLE IF EXISTS html_content_bridge;
-- DROP TABLE IF EXISTS link_fact;
DROP TABLE IF EXISTS download_fact;
-- drop dimensions
-- DROP TABLE IF EXISTS content_dim;
DROP TABLE IF EXISTS html_dim;
DROP TABLE IF EXISTS url_dim;
DROP TABLE IF EXISTS crawl_dim;
-- drop util (used by dimensions)
DROP TABLE IF EXISTS domain_dim;
"""


def get_db(db_settings: Dict[str,Any]) -> connection:
    return psycopg2.connect(**db_settings)

def close_db(conn:connection):
    conn.close()

def create_db(db:connection):
    cursor = db.cursor()
    cursor.execute(drop_sql)
    cursor.execute(domain_table)
    cursor.execute(crawl_table)
    cursor.execute(url_table)
    cursor.execute(html_table)
    cursor.execute(download_table)
    db.commit()


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
    