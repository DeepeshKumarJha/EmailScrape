import sys
from scrapy.crawler import CrawlerProcess
from escrape.spiders.mail import MailSpider


if __name__ == "__main__":

    # command line argument will be like python run.py -s <site> <site> -n <number of email>

    site = []
    for i in range(sys.argv.index('-s')+1, len(sys.argv)):

        if sys.argv[i] == '-n':
            break;
        else:
            site.append(sys.argv[i])
    
    print(site)

    # numb = sys.argv[2]

    process = CrawlerProcess()
    process.crawl(MailSpider, link=site)
    process.start()