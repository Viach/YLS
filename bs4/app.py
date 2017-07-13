"""        Application for scraping website with BeautifulSoup    """
import sys
from bowl import Soup


def main(args):
    soup = Soup(args)

    item_list = soup.get_item_list()
    print(item_list[0], len(item_list))


if __name__ == '__main__':
    main(sys.argv[1:])
