from scrapy import Spider, Request

from scrapy_price.items import ScrapyPriceItem


class PriceSpider(Spider):
    name = "price"
    allowed_domains = ["price.ua"]

    def __init__(self, model=None, price_range='10000:20000', *args, **kwargs):
        super(PriceSpider, self).__init__(*args, **kwargs)
        self.model = model.lower() if model else None
        self.price_range_url = ''
        self.price_range = [int(v) for v in price_range.split(':') if v.isdigit()]
        self.price_range_url = '?price[min]={}&price[max]={}'.format(self.price_range[0], self.price_range[-1])

    def start_requests(self):
        urls = [
            'http://price.ua/catc839t14.html' + self.price_range_url,
        ]
        for url in urls:
            yield Request(url=url, callback=self.parse)

    def parse(self, response):
        items_obj = response.xpath("//div[@id='list-grid']").css('div.product-item')
        current_page = int(response.css(
            'div.top-paginator.fright input#top-paginator-input::attr(value)').extract_first())
        max_page = int(response.css('div.top-paginator span#top-paginator-max::text').extract_first())
        item_count = 0

        for item_obj in items_obj:
            item = ScrapyPriceItem()
            item['name'] = item_obj.css('a.model-name::text').extract_first()
            if self.model not in item['name'].lower():
                print('scipped', item['name'])
                continue
            print('start', item['name'], end='')
            item['price'] = item_obj.css('div.price-wrap span.price::text').extract_first()
            if not item['price']:
                item['price'] = item_obj.css('div.price-wrap a.price::text').extract_first()
            item['price'] = item['price'].replace('\xa0', '').strip()
            item['description'] = item_obj.css('div.desc div.characteristics div.item *::text').extract()
            item['description'] = [i.strip() for i in item['description']]
            item['description'] = ''.join([i if i else '\n' for i in item['description']]).encode()
            item['item_url'] = item_obj.css('div.photo-wrap a::attr(onmousedown)').extract_first().replace(
                'this.href=', '').strip('"')
            item['item_photo'] = item_obj.css(
                'div.photo-wrap div.hidden.tooltip-content::attr(data-big-image-url)').extract_first()
            item_count += 1
            print(' and finished')
            yield item

        print('****** Scrapped {} from {} pages'.format(current_page, max_page))
        if current_page > max_page:
            next_page_url = 'http://price.ua/catc839t14/page{}.html'.format(current_page + 1) + self.price_range_url
            url = response.urljoin(next_page_url)
            yield Request(url, callback=self.parse)
        print('****** Collected {} items'.format(item_count))