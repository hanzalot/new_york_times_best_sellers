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
        label = response.meta['label']
        print label
        bs_list = response.xpath("//*[@id='main']/div[1]/section[1]/ol/li/article")
        number = 1
        for entry in bs_list:
            title = response.xpath(".//div/h3[contains(title)]/text()").extract()
            print title[0]
            author = response.xpath(".//div/p[contains(author)]/text()").extract()
            print author[0]
            publisher = response.xpath(".//div/p[contains(publisher)]/text()").extract()
            print publisher[0]
            description = response.xpath(".//div/p[contains(description)]/text()").extract()
            print description[0]
            isbn = response.xpath(".//meta/@content").extract()
            print isbn[1]
            #print ",".join([label,number,title[0],author[0],publisher[0],description[0],isbn[1],isbn[0]])
            number+=1
        
        
        
process = CrawlerProcess()
process.crawl(NYTBSSpider)
process.start()
