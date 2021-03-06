# This is a template for a Python scraper on morph.io (https://morph.io)
# including some code snippets below that you should find helpful

# import scraperwiki
# import lxml.html
#
# # Read in a page
# html = scraperwiki.scrape("http://foo.com")
#
# # Find something on the page using css selectors
# root = lxml.html.fromstring(html)
# root.cssselect("div[align='left']")
#
# # Write out to the sqlite database using scraperwiki library
# scraperwiki.sqlite.save(unique_keys=['name'], data={"name": "susan", "occupation": "software developer"})
#
# # An arbitrary query against the database
# scraperwiki.sql.select("* from data where 'name'='peter'")

# You don't have to do things with the ScraperWiki and lxml libraries.
# You can use whatever libraries you want: https://morph.io/documentation/python
# All that matters is that your final data is written to an SQLite database
# called "data.sqlite" in the current working directory which has at least a table
# called "data".
import scrapy
from scrapy.crawler import CrawlerProcess
from datetime import datetime
import scraperwiki

class NYTBSSpider(scrapy.Spider):
    name = "nytbs"
    
    allowed_domains = ["nytimes.com"]
    start_urls = [
        "http://www.nytimes.com/books/best-sellers/"
    ]

    def parse(self, response):
        headers = response.xpath("//*[@id='subnavigation']/form/div")
        for header in headers:
            links = header.xpath(".//select/option")
            ident = header.xpath(".//@id").extract()
            for link in links:
                value = link.xpath(".//@value").extract()
                label = link.xpath(".//text()").extract()
                if len(value)>0:
                    url = response.urljoin(value[0])
                    request = scrapy.Request(url, callback=self.parse_best_seller_page)
                    request.meta['label'] = label[0]
                    yield request
    
    def parse_best_seller_page(self, response):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        label = response.meta['label'] or 'blank'
        bs_list = response.xpath("//*[@id='main']/div[1]/section[1]/ol/li/article")
        number = 1
        for entry in bs_list:
            try:
                title = entry.xpath(".//div/h2[contains(@class,'title')]/text()")[0].extract()
            except: 
                title = 'blank'
            try:
                author = entry.xpath(".//div/p[contains(@class,'author')]/text()")[0].extract()
            except:
                author = 'blank'
            try:
                publisher = entry.xpath(".//div/p[contains(@class,'publisher')]/text()")[0].extract()
            except:
                publisher = 'blank'
            try:
                description = entry.xpath(".//div/p[contains(@class,'description')]/text()")[0].extract()
            except:
                description = 'blank'
            isbn = entry.xpath(".//meta/@content").extract()
            if len(isbn)==2:
                isbn1 = isbn[1]
            else:
                isbn1 = ''
            output = ",".join([timestamp,response.url,label,str(number),str(isbn1),title,author,publisher,description])
            print output.encode('ascii','ignore')
            number+=1
        
        
        
process = CrawlerProcess()
process.crawl(NYTBSSpider)
process.start()
