import requests
import html2text
import csv
from bs4 import BeautifulSoup


def store_data(args, data):
    """    Write data to a CSV file    """

    output_file_name = 'scrape_data.csv'
    with open(output_file_name, "w") as csv_file:
        writer = csv.writer(csv_file, delimiter=',')

        for line in data:
            writer.writerow(line)
        print('Data wrote in: ', output_file_name)


class Soup:
    """ Class Soup - scrapper for site """

    def __init__(self, args):
        self.args = args
        self.args.setdefault('--limit-pages', 1)
        self.args.setdefault('--price-range', '10000:20000')
        self.args.setdefault('--mode', 'list')
        if self.args['--price-range']:
            price_range = self.args['--price-range'].split(':')
            self.args['--price-range'] = [int(price) for price in price_range if price.isdigit()]
            self.args['--price-range'] = '?price[min]={}&price[max]={}'.format(*self.args['--price-range'])
        self.url = 'http://price.ua/catc839t14.html' + self.args['--price-range']
        self.base_url = 'http://price.ua'
        self.page = int(self.args.get('--start-page', 1))  # Number of current page.
        self.item_list = []  # List with result
        self.item_counter = 0
        self.page_counter = 0

    def get_url(self, page):
        """ Return url for next scrape. """
        if page > 1:
            self.url = 'http://price.ua/catc839t14/page{}.html'.format(page) + self.args['--price-range']
        return self.url

    def scrape_detail_js(self, item):
        """ If item is in JavaScript code block:
        scrape for item: name, description, item_url, item_photos from JS block code
        """

        block = item.find('div', {'class': {'photo-wrap', }}).find('a')  # for items from other hosts
        item_url = self.base_url + block.get('onmousedown').replace('this.href=', '').replace('"', '')
        name = block.get('title').replace('Купить ', '')
        description = 'item from other host!'
        item_photos = [block.find('img').get('src')]
        return name, description, item_url, item_photos

    def get_full_details(self, item_url):
        """ FULL mode. Open url for item and scrape detailed date:
        - all item photos
        - full description (in html format)
        """

        r_item = requests.get(item_url)  # Get item page
        item_full = BeautifulSoup(r_item.content, "html.parser")
        item_description_url = item_full.find('tr', {
            'class': 'tr-details_compare-link'})  # Get table row with URL to descript
        item_description_url = item_description_url.find('td', {'class': 'td-name'}).find('a').get(
            'href')  # Get URL to descript
        r_item_description = requests.get(item_description_url)
        item_description = BeautifulSoup(r_item_description.content, "html.parser")
        description = str(item_description.find('div', {'class': 'full-desc', }))
        item_photos = item_description.find('div', {'id': 'scrollable-gallery-photo'}).find_all('img')
        item_photos = [item_photo.get_attribute_list('data-original')[0] for item_photo in item_photos]
        return description, item_photos

    def get_item_detail(self, item):
        """ Return data for every item in scrape list """

        is_item_from_other_host = False
        price = item.find('div', {'class': 'price-wrap'})
        price = price.text.replace('\xa0', '')
        price = ''.join([i for i in price if i.isdigit()])
        name_contains = self.args.get('--name-contains', False)
        name = item.find('a', {'class': {'model-name', }})
        if not name:  # Item is from other host
            is_item_from_other_host = True
            name, description, item_url, item_photos = self.scrape_detail_js(item)
        else:
            item_url = name.get('href')
            name = name.text

        if name_contains and name_contains not in name.lower():  # Check for matching --name-contains=<string>
            return None

        if self.args['--mode'].lower() == 'list' or is_item_from_other_host:  # LIST mode
            description = str(item.find('div', {'class': 'characteristics'}))
            description = html2text.html2text(description).replace('(javascript:void\\', '').replace(
                '[ Подробнее ](0\\);', '').replace('\n\n', '\n').encode()
            item_photos = item.find('div', {'class': 'photo-wrap'}).find('img').get('src')
        else:  # FULL mode
            description, item_photos = self.get_full_details(item_url)

        self.item_counter += 1
        print('\t', self.item_counter, ' : ', name, item_url, ' parsed')
        return name, price, description, item_url, item_photos

    def get_item_list(self):
        """ Get start parameters and recursively scrape data """

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
        if self.page < max_page and self.page_counter < int(self.args['--limit-pages']) - 1:
            self.page += 1
            self.get_item_list()
            self.page_counter += 1
        return self.item_list
