import sys
from scrapy import cmdline

cmdline.execute("scrapy crawl price {}".format(' '.join(sys.argv[1:])).split())