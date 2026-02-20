import scrapy
import pandas as pd
import logging
from datetime import datetime

class QuotesSpider(scrapy.Spider):
    name = "quotesclean"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["http://quotes.toscrape.com/"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Initialize an empty DataFrame
        self.df = pd.DataFrame(columns=[
            "quote_text", "author_name", "tags",
            "author_full_name", "date_of_birth", "place_of_birth"
        ])
        # Setup logging
        logging.basicConfig(
            filename='scraping.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        logging.info("Spider initialized")

    def parse(self, response):
        for quote in response.xpath("//div[@class='quote']"):
            quote_text = quote.xpath(".//span[@class='text']/text()").get()
            author_name = quote.xpath(".//small[@class='author']/text()").get()
            tags = quote.xpath(".//div[@class='tags']/a/text()").getall()
            author_link = quote.xpath(".//a[contains(text(),'about')]/@href").get()

            logging.info(f"Scraping quote by {author_name}")
            yield response.follow(author_link, callback=self.parse_author, meta={
                "quote_text": quote_text,
                "author_name": author_name,
                "tags": tags
            }, dont_filter=True)

        next_page = response.xpath("//li[@class='next']/a/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_author(self, response):
        # Extract author details
        raw_place = response.xpath("//span[@class='author-born-location']/text()").get()
        clean_place = raw_place.replace("in ", "").strip() if raw_place else None

        item = {
            "quote_text": response.meta["quote_text"],
            "author_name": response.meta["author_name"],
            "tags": ", ".join(response.meta["tags"]) if response.meta["tags"] else "",
            "author_full_name": response.xpath("//h3[@class='author-title']/text()").get().strip(),
            "date_of_birth": response.xpath("//span[@class='author-born-date']/text()").get(),
            "place_of_birth": clean_place,
        }

        # Convert date immediately
        try:
            item["date_of_birth"] = pd.to_datetime(item["date_of_birth"])
        except Exception as e:
            logging.warning(f"Failed to parse date for {item['author_name']}: {e}")
            item["date_of_birth"] = pd.NaT

        # Append to the DataFrame
        self.df = pd.concat([self.df, pd.DataFrame([item])], ignore_index=True)
        self.df.drop_duplicates(subset=["quote_text"], inplace=True)

        logging.info(f"Processed quote: {item['quote_text'][:50]}...")
        yield item

    def closed(self, reason):
        self.df.reset_index(drop=True, inplace=True)
        logging.info(f"Scraping finished, reason: {reason}")
        logging.info(f"Total quotes scraped: {len(self.df)}")
        self.df.to_csv("quotes_clean.csv", index=False)
        logging.info("Saved cleaned data to quotes_clean.csv")