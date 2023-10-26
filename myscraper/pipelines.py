# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import psycopg2
from myscraper.items import PageItem, UrlItem, LinkItem, TextItem, MarkdownItem


class MyscraperPipeline:
    def process_item(self, item, spider):
        return item

class DatabasePipeline:
    def open_spider(self, spider):

        self.connection = psycopg2.connect(database="crown_scraping", user="crown_scraping", password="xAK9q5IMnj1opUh3", host="192.168.1.10", port="5432")
        self.cursor = self.connection.cursor()

    def close_spider(self, spider):
        self.connection.close()

    def process_item(self, item, spider):
        if isinstance(item, PageItem):
            # For PageItem, we just insert and skip if already set.
            self.cursor.execute("""
                INSERT INTO page (pageId, domain, initial_date, initial_source_url) 
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (pageId) DO NOTHING;
            """, (item['pageId'], item['domain'], item['initial_date'], item['initial_source_url']))
        
        elif isinstance(item, UrlItem):
            # For UrlItem, we update everything.
            self.cursor.execute("""
                INSERT INTO url (URL, return_code, mime, pageId, initial_referrer, date_updated, protocol, subdomain, domain, path, query, fragment) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (URL) DO UPDATE SET
                    return_code = excluded.return_code,
                    mime = excluded.mime,
                    pageId = excluded.pageId,
                    initial_referrer = excluded.initial_referrer,
                    date_updated = excluded.date_updated,
                    protocol = excluded.protocol,
                    subdomain = excluded.subdomain,
                    domain = excluded.domain,
                    path = excluded.path,
                    query = excluded.query,
                    fragment = excluded.fragment;
            """, (item['URL'], item['return_code'], item['mime'], item['pageId'], item['initial_referrer'], item['date_updated'], item['protocol'], item['subdomain'], item['domain'], item['path'], item['query'], item['fragment']))
        
        elif isinstance(item, LinkItem):
            # For LinkItem, we have a composite key (PageId, link_num) and update everything.
            self.cursor.execute("""
                INSERT INTO link (pageId, link_num, from_domain, from_url, to_domain, to_url) 
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (pageId, link_num) DO UPDATE SET
                    from_domain = excluded.from_domain,
                    from_url = excluded.from_url,
                    to_domain = excluded.to_domain,
                    to_url = excluded.to_url;
            """, (item['pageId'], item['link_num'], item['from_domain'], item['from_url'], item['to_domain'], item['to_url']))
        
        elif isinstance(item, TextItem):
            # For TextItem, we update the content.
            self.cursor.execute("""
                INSERT INTO text (pageId, text_version) 
                VALUES (%s, %s)
                ON CONFLICT (pageId) DO UPDATE SET
                    text_version = excluded.text_version;
            """, (item['pageId'], item['text_version']))
        
        elif isinstance(item, MarkdownItem):
            # For MarkdownItem, we update the content.
            self.cursor.execute("""
                INSERT INTO markdown (pageId, markdown_version) 
                VALUES (%s, %s)
                ON CONFLICT (pageId) DO UPDATE SET
                    markdown_version = excluded.markdown_version;
            """, (item['pageId'], item['markdown_version']))

        self.connection.commit()
        return item
