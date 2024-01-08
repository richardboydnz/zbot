from .api_result import api_result, api_url
from scrapy.http import HtmlResponse # type: ignore
import json

from myscraper.spiders.wp_spider import WPSpider
from . import settings_test
settings = vars(settings_test)

def test_result():
    page = api_result[0]
    body = json.dumps(page)
    response = HtmlResponse(url=api_url,status = 200,body=body, encoding='utf-8')
    spider = WPSpider.from_settings(settings)
    print('-----test_result spider: ',spider)
    # spider.init_crawl()
    for element in spider.parse_api_page( page):
        print('--------------',element)
