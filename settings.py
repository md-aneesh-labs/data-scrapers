"""Shared Scrapy settings for all crawlers.

Individual crawlers can override any of these via `custom_settings` on the spider.
"""

BOT_NAME = "data_scrapers"

SPIDER_MODULES = ["crawlers"]
NEWSPIDER_MODULE = "crawlers"

ROBOTSTXT_OBEY = True

CONCURRENT_REQUESTS_PER_DOMAIN = 8
DOWNLOAD_DELAY = 0.5
AUTOTHROTTLE_ENABLED = True

DEFAULT_REQUEST_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en",
}

FEED_EXPORT_ENCODING = "utf-8"
LOG_LEVEL = "INFO"
