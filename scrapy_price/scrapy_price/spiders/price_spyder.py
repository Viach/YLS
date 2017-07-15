from scrapy import Spider, Request

from scrapy_price.items import ScrapyPriceItem


class PriceSpider(Spider):
    name = "price"

    allowed_domains = ["price.ua"]
    start_urls = [
        'http://price.ua/catc839t14.html',

    ]

    def parse(self, response):
        itemsObj = response.xpath("//div[@id='list-grid']").css('div.product-item')
        current_page = int(response.css(
            'div.top-paginator.fright input#top-paginator-input::attr(value)').extract_first())
        max_page = int(response.css('div.top-paginator span#top-paginator-max::text').extract_first())

        items = []
        for itemObj in itemsObj:
            item = ScrapyPriceItem()
            item['name'] = itemObj.css('a.model-name::text').extract_first()
            print('start', item['name'], end='')
            item['price'] = itemObj.css('div.price-wrap span.price::text').extract_first()
            if not item['price']:
                item['price'] = itemObj.css('div.price-wrap a.price::text').extract_first()
            item['price'] = item['price'].replace('\xa0', '').strip()
            item['description'] = itemObj.css('div.desc div.characteristics div.item *::text').extract()
            item['description'] = [i.strip() for i in item['description']]
            item['description'] = ''.join([i if i else '\n' for i in item['description']])
            item['item_url'] = itemObj.css('div.photo-wrap a::attr(onmousedown)').extract_first()
            item['item_photo'] = itemObj.css(
                'div.photo-wrap div.hidden.tooltip-content::attr(data-big-image-url)').extract_first()
            items.append(item)
            print('finished')
            

        print('****** Scrapped {} from {} pages'.format(current_page, max_page))
        if current_page > max_page:
            next_page_url = 'http://price.ua/catc839t14/page{}.html'.format(current_page + 1)
            url = response.urljoin(next_page_url)
            yield Request(url, callback=self.parse)

        return items
