# Scrapy settings for myscraper project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "myscraper"

LOG_LEVEL = 'INFO'

PG_DB_SETTINGS = {
    'database': 'crown_scraping',
    'user': 'crown_scraping',
    'password': 'xAK9q5IMnj1opUh3',
    'host': '192.168.1.10',
    'port': '5432'
}

SQLITE_DB_SETTINGS = {
    'database' : 'crawl.db'
}

DB_SETTINGS = SQLITE_DB_SETTINGS

CLEAR_DB = False

# CRAWL_DOMAIN = 'crownrelo-co-nz.archive.zavidan.nz'
        # self.domain_name : str = domain_name or 'crownrelo-co-nz.archive.zavidan.nz'
        # self.domain_name : str = domain_name or 'www.graceremovals.co.nz'
CRAWL_DOMAIN : str = 'ballet.zavidan.info'
        # self.domain_name : str = domain_name or 'www.crownrelo.co.nz'

SPIDER_MODULES = ["myscraper.spiders"]
NEWSPIDER_MODULE = "myscraper.spiders"

REDIRECT_ENABLED = False
FOLLOW_RESOURCES = False

ITEM_PIPELINES = {
   'myscraper.pipelines.downloads_pipe.DownloadsPipe': 300,
}

DOWNLOADER_MIDDLEWARES = {
    'myscraper.middlewares.html_response.HandleHtmlFragmentRequest': 10,  # Adjust the path and priority as needed
}

# DOWNLOADER_MIDDLEWARES = {
#     'myscraper.middlewares.skip_duplicate_middleware.SkipDuplicateMiddleware': 100,
#     # ... other middlewares ...
# }


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "myscraper (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    "myscraper.middlewares.MyscraperSpiderMiddleware": 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    "myscraper.middlewares.MyscraperDownloaderMiddleware": 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    "myscraper.pipelines.MyscraperPipeline": 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"



# Enable AutoThrottle to automatically adjust the scraping speed based on the server's response times and load.
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 0.3  # Initial delay (in seconds) between requests.
AUTOTHROTTLE_MAX_DELAY = 1  # Maximum delay (in seconds) between requests.

# Introduce a delay between consecutive requests.
DOWNLOAD_DELAY = 0.3  # Delay (in seconds) between consecutive requests.

# Limit the number of concurrent requests.
CONCURRENT_REQUESTS = 3

# Disable cookies as some sites might track requests using cookies.
COOKIES_ENABLED = False

# Respect robots.txt. This is a good practice, but it doesn't reduce the chances of getting blocked.
ROBOTSTXT_OBEY = True

# Limit the depth of your crawl if you don't need to scrape all the pages.
DEPTH_LIMIT = 0

# Set a limit on the response size to avoid downloading large files.
DOWNLOAD_MAXSIZE = 10485760  # 10 MB

# Retry middleware settings.
RETRY_TIMES = 0  # Number of times a request should be retried.
RETRY_HTTP_CODES = [500, 502, 503, 504, 408]  # HTTP codes that should trigger a retry.

# If you don't want to rotate user agents, set a default user agent.
USER_AGENT = "ZBot/1.1 (Zavidan link checker)"
