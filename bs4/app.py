"""        Application for scraping website with BeautifulSoup    """
import sys
from bowl import Soup

def main(args):
    soup = Soup()
    print(soup.url)



if __name__ == '__main__':
    main(sys.argv[1:])
