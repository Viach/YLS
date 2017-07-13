import requests
import html2text
from bs4 import BeautifulSoup


class Soup:
    """ Class Soup - scrapper for site """

    def __init__(self, args):
        self.args = [param.split('=') for param in args]
        self.args = {arg[0]: arg[-1].lower() for arg in self.args if arg[0] != arg[-1]}
        if self.args.get('--price-range', False):
            price_range = self.args['--price-range'].split(':')
            self.args['--price-range'] = [int(price) for price in price_range if price.isdigit()]
        self.url = 'http://price.ua/catc839t14.html'
        self.page = 1  # Number of current page.
        self.item_list = []  # List with result

    def get_url(self, page):
        """ Ruturn url for next scrape. """
        if page > 1:
            self.url = 'http://price.ua/catc839t14/page{}.html'.format(page)
        return self.url

    def get_item_detail(self, item):
        """ Return data for every item in scrape list """
        price = item.find('div', {'class': 'price-wrap'})
        price = price.text.replace('\xa0', '')
        price = ''.join([i for i in price if i.isdigit()])
        price_min, price_max = self.args['--price-range']
        if price_min and price_max and price.isdigit() and price_max <= int(price) <= price_min:
            return None

        name = item.find('a', {'class': {'model-name', }}).text
        name_contains = self.args.get('--name-contains', False)
        if name_contains and name_contains not in name.lower():
            return None

        """ Open url for every item and scrape detailed data"""
        item_url = item.find('a', {'class': {'full-desc', }}).attrs['onmousedown'].partition('=')[-1]
        item_url = requests.get(item_url.strip('"')).content
        item_full = BeautifulSoup(item_url, "html.parser")
        description = str(item_full.find('div', {'class': 'full-desc', }))
        description = html2text.html2text(description).replace('(javascript:void\\', '').replace('[](0\\);)', '')
        item_photos = item_full.find('div', {'id': 'scrollable-gallery-photo'})
        item_photos = item_photos.find_all('img')
        item_photos = [item_photo.get_attribute_list('data-original')[0] for item_photo in item_photos]
        return name, price, description, item_url, item_photos

    def get_item_list(self):
        r = requests.get(self.get_url(self.page))
        if r.status_code != 200:
            return 'Error'
        bs = BeautifulSoup(r.content, "html.parser")
        items = bs.find_all('div', {'class': {'product-item', 'view-list '}})
        max_page = int(bs.find('span', {'id': 'top-paginator-max'}).text)
        for item in items:
            item_detail = self.get_item_detail(item)
            if item_detail:
                self.item_list.append(item_detail)
        print('Scanned {} page of {} pages (max pages for scan: {})'.format(self.page, max_page,
                                                                            self.args['--max-pages']))
        if self.page < max_page and self.page < int(self.args['--max-pages']):
            self.page += 1
            self.get_item_list()

        return self.item_list
