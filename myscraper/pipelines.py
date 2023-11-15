# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import psycopg2
from .items import ContentItem, DownloadItem, LinkItem, HtmlContentItem
from urllib.parse import urlparse


class MyscraperPipeline:
    def process_item(self, item, spider):
        return item

import psycopg2

class DatabasePipeline:
    def __init__(self):
        # Cache for dimensions
        self.crawl_id
        self.cache = {
            'crawl_id': None,
            'domains': {},
            'urls': {},
            'content_hashes': {}
        }

    def open_spider(self, spider):
        self.connection = psycopg2.connect(database="crown_scraping", user="crown_scraping", password="xAK9q5IMnj1opUh3", host="192.168.1.10", port="5432")
        self.cursor = self.connection.cursor()

        # Initialize a new crawl record and cache the crawl_id
        self.cursor.execute("INSERT INTO dim_crawl_id (crawl_timestamp) VALUES (NOW()) RETURNING crawl_id;")
        self.crawl_id = self.cursor.fetchone()[0]

    def close_spider(self, spider):
        self.connection.close()

    def get_dim_domain(self, domain_name):
        if domain_name in self.cache['domains']:
            return self.cache['domains'][domain_name]

        self.cursor.execute("SELECT domain_id FROM dim_domains WHERE domain_name = %s", (domain_name,))
        result = self.cursor.fetchone()

        if result is None:
            self.cursor.execute("INSERT INTO dim_domains (domain_name) VALUES (%s) RETURNING domain_id;", (domain_name,))
            domain_id = self.cursor.fetchone()[0]
        else:
            domain_id = result[0]

        self.cache['domains'][domain_name] = domain_id
        return domain_id

    def get_dim_url(self, url):
        if url in self.cache['urls']:
            return self.cache['urls'][url]

        self.cursor.execute("SELECT url_id FROM dim_urls WHERE url = %s", (url,))
        result = self.cursor.fetchone()

        if result is None:
            domain_name = urlparse(url).netloc  # using urlparse for better handling of URLs
            domain_id = self.get_dim_domain(domain_name)
            self.cursor.execute("INSERT INTO dim_urls (url, domain_id) VALUES (%s, %s) RETURNING url_id;", (url, domain_id))
            url_id = self.cursor.fetchone()[0]
        else:
            url_id = result[0]

        self.cache['urls'][url] = url_id
        return url_id

    def get_dim_content(self, content_hash):
        if content_hash in self.cache['content_hashes']:
            return self.cache['content_hashes'][content_hash]

        self.cursor.execute("SELECT content_id FROM dim_content WHERE content_hash = %s", (content_hash,))
        result = self.cursor.fetchone()

        if result is None:
            self.cursor.execute("""
                INSERT INTO dim_content (content_hash)
                VALUES (%s) RETURNING content_id;
            """, (content_hash,))
            content_id = self.cursor.fetchone()[0]
        else:
            content_id = result[0]

        self.cache['content_hashes'][content_hash] = content_id
        return content_id

    def create_dim_content(self, content_hash, raw_html_id, text_id, markdown_id):
        content_id = self.get_dim_content(content_hash)

        if raw_html_id is not None or text_id is not None or markdown_id is not None:
            self.cursor.execute("""
                UPDATE dim_content
                SET raw_html_id = COALESCE(%s, raw_html_id),
                    text_id = COALESCE(%s, text_id),
                    markdown_id = COALESCE(%s, markdown_id)
                WHERE content_id = %s;
            """, (raw_html_id, text_id, markdown_id, content_id))

        return content_id


    def process_item(self, item, spider):
        # DownloadsItem
        if isinstance(item, DownloadItem):
            domain_id = self.get_dim_domain(item['domain_name'])
            url_id = self.get_dim_url(item['url'])
            # Insert into fact_downloads
            self.cursor.execute("""
                INSERT INTO fact_downloads (download_timestamp, http_status, headers, url_id, domain_id, crawl_id)
                VALUES (%s, %s, %s, %s, %s, %s);
            """, (item['download_timestamp'], item['http_status'], item['headers'], url_id, domain_id, self.crawl_id))

        # ContentItem
    # ContentItem
        elif isinstance(item, ContentItem):
            # Insert raw_html, text, and markdown data
            self.cursor.execute("INSERT INTO dim_raw_html (raw_html_data) VALUES (%s) RETURNING raw_html_id;", (item['raw_html_data'],))
            raw_html_id = self.cursor.fetchone()[0]

            self.cursor.execute("INSERT INTO dim_text (text_data) VALUES (%s) RETURNING text_id;", (item['text_data'],))
            text_id = self.cursor.fetchone()[0]

            self.cursor.execute("INSERT INTO dim_markdown (markdown_data) VALUES (%s) RETURNING markdown_id;", (item['markdown_data'],))
            markdown_id = self.cursor.fetchone()[0]

            # Create or update dim_content
            content_id = self.create_dim_content(item['content_hash'], raw_html_id, text_id, markdown_id)


        # LinksItem
        elif isinstance(item, LinkItem):
            fragment_id = self.get_dim_content(item['fragment_hash'], None, None, None)
            to_url_id = self.get_dim_url(item['to_url'])
            # Insert into fact_links
            self.cursor.execute("""
                INSERT INTO fact_links (fragment_id, to_url_id, link_text, crawl_id)
                VALUES (%s, %s, %s, %s);
            """, (fragment_id, to_url_id, item['link_text'], self.crawl_id))

        # HtmlContentBridgeItem
        elif isinstance(item, HtmlContentItem):
            page_content_id = self.get_dim_content(item['page_content_hash'], None, None, None)
            fragment_content_id = self.get_dim_content(item['fragment_content_hash'], None, None, None)
            # Insert into page_fragment_association
            self.cursor.execute("""
                INSERT INTO page_fragment_association (page_content_id, fragment_content_id)
                VALUES (%s, %s);
            """, (page_content_id, fragment_content_id))

        self.connection.commit()
        return item
