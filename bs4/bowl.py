from bs4 import BeautifulSoup as bs

class Soup:
    """ Class Soup - scrapper for site """

    def __init__(self):
        self.url = 'http://http://quotes.toscrape.com/'

    def set_url(self, url):
        self.url = url

