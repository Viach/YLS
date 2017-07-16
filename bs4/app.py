"""        Application for scraping website with BeautifulSoup   
    
    Usage: python app.py [OPTION]... 
                                                            Default:
    Options:    --start-page=<number start page>            1               If it > max number pages App scrape last page
                --limit-pages=<number pages>                1
                --price-range=<min-price>:<max-pice>        10000:20000
                --name-contains=<string>
                --help=[true|false]                         false


    Example: python app.py --limit-pages=10 --price-range=10000:20000 
                           --name-contains=Lenovo --start-page=5

"""
import sys
from bowl import Soup


def main(args):
    args = [param.split('=') for param in args]
    args = {arg[0]: arg[-1].lower() for arg in args if arg[0] != arg[-1]}

    if 'true' == args.get('--help', False):
        print(__doc__)
        return

    soup = Soup(args)

    item_list = soup.get_item_list()
    if item_list:
        print('Total items: ', len(item_list))
        soup.store_data()
        print("\n\t\tThat's it!")


if __name__ == '__main__':
    main(sys.argv[1:])
