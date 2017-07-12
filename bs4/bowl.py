import requests
import html2text
from bs4 import BeautifulSoup


class Soup:
    """ Class Soup - scrapper for site """

    def __init__(self):
        self.url = 'http://price.ua/catc839t14.html'

    def set_url(self, url):
        self.url = url

    def get_item_detail(self, item):
        price = item.find('div', {'class': 'price-wrap'})
        price = price.text.replace('\xa0', '')
        price = ''.join([i for i in price if i.isdigit()])

        name = item.find('a', {'class': {'model-name', }}).text

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
        r = requests.get(self.url)
        if r.status_code != 200:
            return 'Error'
        bs = BeautifulSoup(r.content, "html.parser")
        items = bs.find_all('div', {'class': {'product-item', 'view-list '}})
        return [self.get_item_detail(item) for item in items]
