"""        Application for scraping website with BeautifulSoup    """
import sys
from bowl import Soup


def main(args):
    soup = Soup()

    items_list = soup.get_item_list()
    print(items_list[0], len(items_list))


if __name__ == '__main__':
    main(sys.argv[1:])
