import requests
import html2text
from bs4 import BeautifulSoup


class Soup:
    """ Class Soup - scrapper for site """

    def __init__(self, args):
        self.args = [param.split('=') for param in args]
        self.args = {arg[0]: arg[-1].lower() for arg in self.args if arg[0] != arg[-1]}
        self.args.setdefault('--limit-pages', 1)
        self.args.setdefault('--price-range', '')
        self.args.setdefault('--mode', 'list')
        if self.args['--price-range']:
            price_range = self.args['--price-range'].split(':')
            self.args['--price-range'] = [int(price) for price in price_range if price.isdigit()]
            self.args['--price-range'] = '?price[min]={}&price[max]={}'.format(*self.args['--price-range'])
        self.url = 'http://price.ua/catc839t14.html' + self.args['--price-range']
        self.page = int(self.args.get('--start-page', 1)) # Number of current page.
        self.item_list = []  # List with result
        self.item_counter = 0

    def get_url(self, page):
        """ Ruturn url for next scrape. """
        if page > 1:
            self.url = 'http://price.ua/catc839t14/page{}.html'.format(page)+ self.args['--price-range']
        return self.url

    def get_item_detail(self, item):
        """ Return data for every item in scrape list """
        price = item.find('div', {'class': 'price-wrap'})
        price = price.text.replace('\xa0', '')
        price = ''.join([i for i in price if i.isdigit()])

        name = item.find('a', {'class': {'model-name', }})
        if not name:
            name = item.find('div', {'class': {'photo-wrap', }}).find('a')
            print(name)
            name = name.get('title')
            print(name)
        try:            
            item_url = name.get('href')
        except AttributeError as e:
                print('\t Error Item URL for :', ' page :', self.page)
                print('It seems this item is from other host. Skipped!')
                return None
        if not item_url:  # product from other host
            name = 'Product from other host. Skipped!'
            return name, price, None, item_url, None
        name = name.text
        name_contains = self.args.get('--name-contains', False)
        if name_contains and name_contains not in name.lower():
            return None
        if self.args['--mode'].lower() == 'list':  # LIST mode
            description = str(item.find('div', {'class':'characteristics'}))
            item_photos = item.find('div', {'class':'photo-wrap'}).find('img').get('src')
        else:
            """ Open url for every item and scrape detailed data - FULL mode"""
            r_item = requests.get(item_url)  # Get item page
            item_full = BeautifulSoup(r_item.content, "html.parser")
            try:
                item_description_url = item_full.find('tr', {'class': 'tr-details_compare-link'})  # Get table row with URL to descript
                item_description_url = item_description_url.find('td', {'class': 'td-name'}).find('a').get('href')  # Get URL to descript
                r_item_description = requests.get(item_description_url)
            except BaseException as e:
                print('\t Error Item description URL for :', name, item_url, '\n\t : ', e)
                return None
            item_description = BeautifulSoup(r_item_description.content, "html.parser")
            description = str(item_description.find('div', {'class': 'full-desc', }))
            description = html2text.html2text(description).replace('(javascript:void\\', '').replace('[](0\\);)', '')
            item_photos = item_description.find('div', {'id': 'scrollable-gallery-photo'}).find_all('img')            
            item_photos = [item_photo.get_attribute_list('data-original')[0] for item_photo in item_photos]
        self.item_counter += 1
        print('\t',self.item_counter, ' : ', name, item_url, ' parsed')
        return name, price, description, item_url, item_photos

    def get_item_list(self):
        current_url = self.get_url(self.page)
        r = requests.get(current_url)
        print('URL to parse: ', current_url)
        if r.status_code != 200:
            return 'Error'
        bs = BeautifulSoup(r.content, "html.parser")
        items = bs.find_all('div', {'class': {'product-item', 'view-list'}})
        max_page = int(bs.find('span', {'id': 'top-paginator-max'}).text)
        for item in items:
            item_detail = self.get_item_detail(item)
            if item_detail:
                self.item_list.append(item_detail)
        print('Scanned {} page of {} pages (max pages for scan: {})'.format(self.page, max_page,
                                                                            self.args['--limit-pages']))
        if self.page < max_page and self.page < int(self.args['--limit-pages']):
            self.page += 1
            self.get_item_list()

        return self.item_list
