import scrapy
from scrapy import Selector

class QuotesSpider(scrapy.Spider):
    """Example crawler: scrapes quotes.toscrape.com."""

    name = "quotes"
    allowed_domains = ["quotes.toscrape.com"]

    custom_settings = {
        "DOWNLOAD_DELAY": 0.25,
        "ITEM_PIPELINES": {
        "crawlers.pipelines.QuotesPipeline": 300
    }
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0 Safari/537.36",
    }


    def build_url(self,page):
        return f"https://quotes.toscrape.com/page/{page}/"
    async def start(self):
        # Optional: set "args": {"tag": "love"} in crawlers.json to scrape one tag only
        page = getattr(self, "page", 1)
        url = self.build_url(page=page)

        yield scrapy.Request(
            url=url,
            method="GET",
            headers=self.headers,
            callback=self.parse,
            meta={"page":page}
        )

    def parse(self, response):
        selector = Selector(response)

        page = response.meta.get("page")
        data = [
            {"quote":div_tag.xpath("./span[@class='text']/text()").get(),
            "author_name":div_tag.xpath(".//small[@class='author']/text()").get(),
            "tags":div_tag.xpath(".//div[@class='tags']//a[@class='tag']/text()").getall()
            }
            for div_tag in selector.xpath("//div[@class='quote']")
        ]
        
        yield {"page":page, "data":data}

        next_page = selector.xpath("//li[@class='next']")
        if next_page:
            yield response.follow(
                self.build_url(page=page+1), 
                callback=self.parse,
                headers=self.headers,
                meta={"page":page+1})
        