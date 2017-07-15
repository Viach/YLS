"""        Application for scraping website with BeautifulSoup   
    
    Usage: python app.py [OPTION]... 
                                                            Default:
    Options:    --start-page=<number start page>            1               If it > max number pages App scrape last page
                --limit-pages=<number pages>                1
                --price-range=<min-price>:<max-pice>        10000:20000
                --name-contains=<string>
                --mode=[list|full]                          list            in list mode description field is encoded,
                                                                            full mode - is in hmtl format
                --output-format=[csv|sql]                   csv
                --help=[true|false]                         false


    Example: python app.py --limit-pages=10 --price-range=10000:20000 
                           --name-contains=Lenovo --mode=list --start-page=5

"""
import sys
from bowl import Soup, store_data


def main(args):
    args = [param.split('=') for param in args]
    args = {arg[0]: arg[-1].lower() for arg in args if arg[0] != arg[-1]}

    if 'true' == args.get('--help', False):
        print(__doc__)
        return

    soup = Soup(args)

    item_list = soup.get_item_list()
    print('Total items: ', len(item_list))

    store_data(args, item_list)
    print("\n\t\tThat's it!")


if __name__ == '__main__':
    main(sys.argv[1:])
