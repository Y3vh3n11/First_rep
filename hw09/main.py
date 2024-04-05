import scrapy
from scrapy.crawler import CrawlerProcess
import json
from connect import db
from datetime import datetime


dataQuotes = []
dataAuthors = []


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["http://quotes.toscrape.com/"]

    def parse(self, response):
        global dataQuotes
        for quote in response.xpath("/html//div[@class='quote']"):

            quotes = {
                "keywords": quote.xpath("div[@class='tags']/a/text()").extract(),
                "author": quote.xpath("span/small/text()").get(),
                "quote": str(quote.xpath("span[@class='text']/text()").get()).removeprefix("“").removesuffix("”"),
            }
            dataQuotes.append(quotes)

        for author in response.xpath("/html//div[@class='quote']/span/a/@href"):
            url = author.get()
            yield response.follow(url, self.parse_author)

        next_link = response.xpath("//li[@class='next']/a/@href").get()
        if next_link:
            yield scrapy.Request(url=self.start_urls[0] + next_link)

    def parse_author(self, response):
        global dataAuthors
        author = {
            "fullname": response.xpath('//div[@class="author-details"]/h3/text()').get(),
            "born_date": response.xpath('//div[@class="author-details"]/p/span[@class="author-born-date"]/text()').get(),
            "born_location": response.xpath('//div[@class="author-details"]/p/span[@class="author-born-location"]/text()').get(),
            "description": str(response.xpath('//div[@class="author-details"]/div[@class="author-description"]/text()').get()).strip(),
        }
        dataAuthors.append(author)


def save_data():
    with open("authors.json", "r", encoding="utf-8") as file:
        readjsonAuthor = json.load(file)

    with open("quotes.json", "r", encoding="utf-8") as file:
        readjsonQoutes = json.load(file)
    
    db.authors.drop()
    for author in readjsonAuthor:
        insrt = db.authors.insert_one(
            {
                "fullname": author["fullname"],
                "born_date": datetime.strptime(author["born_date"], "%B %d, %Y"),
                "born_location": author["born_location"],
                "description": author["description"],
            }
        )
        print(insrt.inserted_id)
    db.quotes.drop()
    for quote in readjsonQoutes:
        insrt = db.quotes.insert_one(
            {
                "keywords": quote["keywords"],
                "author": db.authors.find_one({"fullname": quote["author"]}),
                "quote": quote["quote"],
            }
        )
        print(insrt.inserted_id)



if __name__ == "__main__":
    # run spider
    process = CrawlerProcess()
    process.crawl(QuotesSpider)
    process.start()

    with open("quotes.json", "w", encoding="utf-8") as fileQ:
        json.dump(dataQuotes, fileQ, indent=4)
    
    with open("authors.json", "w", encoding="utf-8") as fileQ:
        json.dump(dataAuthors, fileQ, indent=4)

    save_data()
