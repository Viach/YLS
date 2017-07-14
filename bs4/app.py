"""        Application for scraping website with BeautifulSoup   
    
    Usage: python app.py [OPTION]... 

    Options:    --start-page=<number start page>
                --limit-pages=<number pages>
                --price-range=<min-price>:<max-pice>
                --name-contains=<string>
                --mode=[list|full]


    Example: python app.py --limit-pages=10 --price-range=10000:20000 
                           --name-contains=Samsung --mode=list

"""
import sys
from bowl import Soup


def main(args):    
    soup = Soup(args)

    item_list = soup.get_item_list()
    print(item_list[-1], len(item_list))


if __name__ == '__main__':
    main(sys.argv[1:])
