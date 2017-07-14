from scrapy import Spider
from scrapy.selector import Selector

from scrapy_price.items import ScrapyPriceItem


class PriceSpider(Spider):
    name = "price"

    allowed_domains = ["price.ua"]
    start_urls = [
        'http://price.ua/catc839t14.html',
    ]

    def parse(self, response):
        itemsObj = response.xpath("//div").css('.product-item').css('.view-list')
        items = []
        for itemObj in itemsObj:
            item = ScrapyPriceItem()
            item["name"] = itemObj.xpath('//div[@class="info-wrap"]').css('a.model-name')

            items.append(item)
        return items
