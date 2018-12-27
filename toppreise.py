import warnings
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy import Selector

dctProductName = {}
dctProductPrice = {}
dctShippingCost = {}
dctRetailer = {}

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    
    def start_requests(self):
        with open('https://github.com/frooni/scrapytoppreise/blob/master/input_url.csv') as f:
            urls = f.read().strip().splitlines()
        urls.remove('urls')
        for url in urls:
            dctProductName[url] = []
            dctProductPrice[url] = []
            dctShippingCost[url] = []
            dctRetailer[url] = []
            yield scrapy.Request(url=url, callback=self.parse, meta={'url': url},headers={
                                 "Accept": "*/*",
                                 "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"})

    def parse(self, response):
        link = response.meta.get('url')
        data = response.css('tbody[class]')
        tempArray = []
        for i in range(1, len(data)):
            try:
                d = data[i].css('.altLinesOdd')[0]
            except:
                d = data[i].css('.altLinesEven')[0]
            details  = d.css('td')
            for x in range(0, len(details),2):
                if (x != 6):
                    temp = details[x].css('::text').extract()
                    if (len(temp) != 0):
                        if (x == 0):
                            dctProductName[link].append(temp[0])
                        elif (x == 2):
                            dctProductPrice[link].append(temp[0])
                        elif (x == 4):
                            dctShippingCost[link].append(temp[1])
                    temp = details[x].css('::attr(alt)').extract()
                    if (len(temp) != 0):
                        dctRetailer[link].append(temp[0])
        print("Length of product Name : ", len(dctProductName[link]))
        print("Length of product Price : ", len(dctProductPrice[link]))
        print("Length of shipping Cost : ", len(dctShippingCost[link]))
        print("Length of retailer : ", len(dctRetailer[link]))

warnings.filterwarnings('ignore')
process = CrawlerProcess()
process.crawl(QuotesSpider)
process.start()