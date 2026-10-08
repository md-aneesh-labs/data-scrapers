import json

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


def main():
    with open("crawlers.json") as f:
        crawlers = json.load(f)

    process = CrawlerProcess(get_project_settings())

    for crawler in crawlers:
        if crawler["enabled"]:
            process.crawl(crawler["name"], **crawler.get("args", {}))

    process.start()


if __name__ == "__main__":
    main()
