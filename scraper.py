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

class ToiletSpider(scrapy.Spider):
    name = "toilet"
    def start_requests(self):
        yield scrapy.Request('http://www.fehd.gov.hk/english/pleasant_environment/cleansing/list_of_public_toilets.php?district=NTIs')
        yield scrapy.Request('http://www.fehd.gov.hk/english/pleasant_environment/cleansing/list_of_public_toilets.php?district=HK')
        yield scrapy.Request('http://www.fehd.gov.hk/english/pleasant_environment/cleansing/list_of_public_toilets.php?district=KLN')

    def parse(self, response):
        tables = response.xpath("//table")
        print len(tables)
        for table in tables:
            rows = table.xpath("tr")
            district = rows[0].xpath("td/text()").extract()[0]
            for row in rows[2:]:
                texts = row.xpath("td/text()")
                name = texts[1].extract().replace("*", "")
                address = texts[2].extract()
                scraperwiki.sqlite.save(unique_keys=[], data={"district": district, "name": name, "address": address})
scraperwiki.sqlite.execute("DROP table data")
process = CrawlerProcess()
process.crawl(ToiletSpider)
process.start()
