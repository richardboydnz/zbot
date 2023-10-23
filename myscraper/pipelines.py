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
        self.connection = psycopg2.connect(database="myscraperdb", user="your_user", password="your_password", host="localhost", port="5432")
        self.cursor = self.connection.cursor()

    def close_spider(self, spider):
        self.connection.close()

    def process_item(self, item, spider):
        if isinstance(item, PageItem):
            self.cursor.execute("INSERT INTO page (pageId, domain, initial_date, initial_source_url) VALUES (%s, %s, %s, %s)", 
                                (item['pageId'], item['domain'], item['initial_date'], item['initial_source_url']))
        
        elif isinstance(item, UrlItem):
            self.cursor.execute("INSERT INTO url (URL, return_code, mime, pageId, initial_referrer, date_updated, protocol, subdomain, domain, path, query, fragment) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", 
                                (item['URL'], item['return_code'], item['mime'], item['pageId'], item['initial_referrer'], item['date_updated'], item['protocol'], item['subdomain'], item['domain'], item['path'], item['query'], item['fragment']))
        
        elif isinstance(item, LinkItem):
            self.cursor.execute("INSERT INTO link (pageId, from_domain, from_url, to_domain, to_url) VALUES (%s, %s, %s, %s, %s)", 
                                (item['pageId'], item['from_domain'], item['from_url'], item['to_domain'], item['to_url']))
        
        elif isinstance(item, TextItem):
            self.cursor.execute("INSERT INTO text (pageId, text_version) VALUES (%s, %s)", 
                                (item['pageId'], item['text_version']))
        
        elif isinstance(item, MarkdownItem):
            self.cursor.execute("INSERT INTO markdown (pageId, markdown_version) VALUES (%s, %s)", 
                                (item['pageId'], item['markdown_version']))

        self.connection.commit()
        return item
