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
        itemsObj = response.xpath("//div[@id='list-grid']").css('div.product-item')
        items = []
        for itemObj in itemsObj:
            item = ScrapyPriceItem()
            item['name'] = itemObj.css('a.model-name::text').extract_first()
            item['price'] = itemObj.css('div.price-wrap span.price::text').extract_first().replace('\xa0', '').strip()
            item['description'] = itemObj.css('div.desc div.characteristics div.item *::text').extract()
            item['description'] = [i.strip() for i in item['description']]
            item['description'] = ''.join([i if i else '\n' for i in item['description']])
            item['item_url'] = itemObj.css('div.photo-wrap a::attr(onmousedown)').extract_first()
            item['item_photo'] = itemObj.css(
                'div.photo-wrap div.hidden.tooltip-content::attr(data-big-image-url)').extract_first()

            items.append(item)
        print(items)
        return items
