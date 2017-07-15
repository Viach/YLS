"""        Application for scraping http://price.ua/catc839t14.html with Scrapy

    Usage: scrapy crawl price [OPTION]...
                                                            Default:
    Options:    -a price_range=<min-price>:<max-pice>       None
                -a model=<string>                           None
                -a output_format=[csv|sql]                  csv

    Example: scrapy crawl price -a price_range=9800:10000 -a output_format=sql -a model=Lenovo

"""
from scrapy import Spider, Request

from scrapy_price.items import ScrapyPriceItem


class PriceSpider(Spider):
    """ Spider for scrapping data from  http://price.ua/catc839t14.html """
    name = "price"
    allowed_domains = ["price.ua"]

    def __init__(self, model=None, price_range=None, output_format='csv', *args, **kwargs):
        super(PriceSpider, self).__init__(*args, **kwargs)
        self.model = model.lower() if model else None
        self.price_range_url = ''
        if price_range:
            self.price_range = [int(v) for v in price_range.split(':') if v.isdigit()]
            self.price_range_url = '?price[min]={}&price[max]={}'.format(self.price_range[0], self.price_range[-1])
        self.item_count = 0
        self.max_page = 0
        if output_format.lower() in {'csv', 'sql'}:
            self.output_format = output_format.lower()

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
        self.max_page = int(response.css('div.top-paginator span#top-paginator-max::text').extract_first())

        for item_obj in items_obj:
            item = ScrapyPriceItem()
            item['item_url'] = item_obj.css('div.photo-wrap a::attr(onmousedown)').extract_first().replace(
                'this.href=', '').strip('"')
            item['price'] = item_obj.css('div.price-wrap span.price::text').extract_first()
            if not item['price']:
                item['price'] = item_obj.css('div.price-wrap a.price::text').extract_first()
            item['price'] = item['price'].replace('\xa0', '').strip()
            item['name'] = item_obj.css('a.model-name::text').extract_first()
            if not item['name']:  # JS code. Item from other host
                item['name'] = item_obj.css('div.photo-wrap a::attr(title)').extract_first().replace('Купить ', '')
                item['item_photo'] = item_obj.css(
                    'div.photo-wrap img::attr(data-original)').extract_first()
                item['description'] = '!!! Warning! Item from other host!\n' + \
                                      item_obj.css('div.desc span.wrap-descr ::text').extract()[0]
                item['description'] = item['description'].replace('|', '\n')
            else:  # HTML code
                item['description'] = item_obj.css('div.desc div.characteristics div.item *::text').extract()
                item['description'] = [i.strip() for i in item['description']]
                item['description'] = ''.join([i if i else '\n' for i in item['description']])
                item['item_photo'] = item_obj.css(
                    'div.photo-wrap div.hidden.tooltip-content::attr(data-big-image-url)').extract_first()
            if item['item_url'].startswith('/main/gate'):
                item['item_url'] = 'http://price.ua' + item['item_url']
            print('start', item['name'], end='')
            if self.model and self.model not in item['name'].lower():
                print('and scipped')
                continue
            self.item_count += 1
            print(' and finished')
            yield item

        print('****** Scrapped {} page from {} pages. Collected {} items'.format(
            current_page, self.max_page, self.item_count))
        if current_page < self.max_page:
            next_page_url = 'http://price.ua/catc839t14/page{}.html'.format(current_page + 1) + self.price_range_url
            url = response.urljoin(next_page_url)
            yield Request(url, callback=self.parse)
        else:
            print('****** Collected {} items'.format(self.item_count))
