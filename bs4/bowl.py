import requests
import csv
from bs4 import BeautifulSoup


class Soup:
    """ Class Soup - scrapper for site """

    def __init__(self, args):
        self.args = args
        self.args.setdefault('--limit-pages', 1)
        self.args.setdefault('--price-range', '10000:20000')
        if self.args['--price-range']:
            price_range = self.args['--price-range'].split(':')
            self.args['--price-range'] = [int(price) for price in price_range if price.isdigit()]
            self.args['--price-range'] = '?price[min]={}&price[max]={}'.format(*self.args['--price-range'])
        self.url = 'http://price.ua/catc839t14.html' + self.args['--price-range']
        self.base_url = 'http://price.ua'
        self.page = int(self.args.get('--start-page', 1))  # Current page.
        self.item_counter = 0
        self.page_counter = 0  # Total scanned pages
        self.output_file_name = 'scrape_data.csv'

    def store_data(self, row):
        """    Write data to a CSV file    """

        with open(self.output_file_name, "a") as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerow(row)

    def get_url(self, page):
        """ Return url for next scrape. """
        if page > 1:
            self.url = 'http://price.ua/catc839t14/page{}.html'.format(page) + self.args['--price-range']
        return self.url

    def get_item_detail(self, item):
        """ Return data for every item in scrape list """

        item_url = item.find('div', {'class': 'photo-wrap'}).find('a').get('onmousedown').replace(
            'this.href=', '').strip('"')
        price = item.find('div', {'class': 'price-wrap'}).find('span', {'price'})
        if not price:
            price = item.find('div', {'class': 'price-wrap'}).find('a', {'price'})
        price = price.text.replace('\xa0', '')
        price = ''.join([i for i in price if i.isdigit()])
        name_contains = self.args.get('--name-contains', False)
        name = item.find('a', {'class': {'model-name', }})
        if not name:  # Item is from other host
            name = item.find('div', {'photo-wrap'}).find('a').get('title').replace('Купить ', '')
            item_photo = item.find('div', {'photo-wrap'}).find('img').get('data-original')
            description = '!!! Warning! Item from other host!\n' + \
                          item.find('div', {'desc'}).find('span', {'wrap-descr'}).text
            description = description.replace('|', '\n')
        else:
            description = item.find('div', {'desc'}).find('div', {'characteristics'})
            if not description:
                description = item.find('div', {'desc'})
            description = description.text.replace('\n\n\n', '\n')
            item_photo = item.find('div', {'photo-wrap'}).find('div', {'hidden'}).get('data-big-image-url')
            name = name.text
        if item_url.startswith('/main/gate'):
            item_url = 'http://price.ua' + item_url
        if name_contains and name_contains not in name.lower():  # Check for matching --name-contains=<string>
            return None

        self.item_counter += 1
        print('\t', self.item_counter, ' : ', name, item_url, ' parsed')
        return name, price, description, item_url, item_photo

    def do_scraping(self):
        """ Get start parameters and scrape data until:
                                current page < max_page
                                        AND
                                scrapped_pages < limit_pages """
        while True:
            current_url = self.get_url(self.page)
            r = requests.get(current_url)
            print('URL to parse: ', current_url)
            if r.status_code != 200:
                print('Error :', r.status_code)
                return
            bs = BeautifulSoup(r.content, "html.parser")
            items = bs.find_all('div', {'class': {'product-item', 'view-list'}})  # create current page items list
            max_page = int(bs.find('span', {'id': 'top-paginator-max'}).text)
            for item in items:
                item_detail = self.get_item_detail(item)
                if item_detail:
                    self.store_data(item_detail)

            print('Scanned {} page of {} pages (max pages for scan: {})'.format(self.page, max_page,
                                                                                self.args['--limit-pages']))
            if self.page < max_page and self.page_counter < int(self.args['--limit-pages']) - 1:
                self.page += 1
                self.page_counter += 1
            else:
                break

        print('Data wrote in: {}\nTotal {} items.'.format(self.output_file_name, self.item_counter))
