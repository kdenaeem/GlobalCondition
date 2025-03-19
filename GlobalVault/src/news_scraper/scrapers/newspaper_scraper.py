import newspaper
import pandas as pd
from datetime import datetime
import logging
from typing import List, Dict
from newspaper import Article, Source
import json
from newspaper import Article
import pandas as pd
from newspaper import build
from news_scraper.config import Settings, setup_logging
from news_scraper.utils.article_formatter import ArticleFormatter
from bs4 import BeautifulSoup
from newspaper import Article
import requests
import pandas as pd
import logging


class ManualScrape:
    def __init__(self):
        setup_logging()
        self.logger = logging.getLogger(__name__)
        self.settings = Settings()
        self.formatter = ArticleFormatter()
        self.all_articles = []
        self.logger.info("Starting manual scraping")

    def fetch_bbc_urls(self):
        all_urls = []
        # https://www.bbc.co.uk/news/world/asia/india
        # https://www.bbc.co.uk/news/world/asia
        # "https://www.bbc.co.uk/news/world/australia"
        # URL = "https://www.bbc.co.uk/news/world/middle_east"
        # URL = "https://www.aljazeera.com/africa/"
        # URL = "https://www.aljazeera.com/middle-east/"
        # URL = "https://www.aljazeera.com/europe/"
        URL = "https://news.yahoo.com/"

        all_articles = []  # List to store all articles
        response = requests.get(URL)
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract all potential article links
        article_links = set()
        print(soup.text)
        for link in soup.find_all("a", href=True):
            href = link["href"]
            print(href)
            # BBC article links usually start with "/news/"
            if href.startswith("/news/article") and "bbc.co.uk" not in href:
                full_url = f"https://www.bbc.co.uk{href}"
                article_links.add(full_url)

            if ("/news/202" in href or "/features/202" in href) and not href.startswith(
                "http"
            ):
                # Build full URL if it's a relative path
                full_url = f"https://www.aljazeera.com{href}"
                print(full_url)
                article_links.add(full_url)
        # Print extracted article links
        # for url in article_links:
        #     all_urls.append(url)
        # self.logger.info(f"Fetched {len(all_urls)} article links")
        # return self.process_articles(all_urls)

    def process_articles(self, url_list: List[str]):
        self.logger.info(f"Processing {len(url_list)} articles")
        data = []
        for url in url_list:
            try:
                self.logger.info(f"Processing {url}")
                article = Article(url)
                article.download()
                article.parse()
                data.append(
                    {
                        "link": url,
                        "title": article.title,
                    }
                )
                self.logger.info(f"Finished processing {url}")
            except Exception as e:
                print(f"Failed to scrape {url}: {e}")

        self.logger.info(f"Processed {len(data)} articles, now formatting")
        self.logger.info(f"Data: {data[:3]}")
        article_data = self.formatter.format_articles(data)
        self.logger.info(f"Formatted {len(article_data)} articles")
        self.logger.info(f"Formatted data: {article_data[:3]}")
        return article_data


# import newspaper

# bbc_papers = newspaper.build("https://www.bbc.co.uk/news/world", number_threads=3)

# article_urls = [article.url for article in bbc_papers.articles]
# print(article_urls[10])


# from newspaper import Article
# import pandas as pd

# # List of article URLs
# urls = [
#     "https://www.bbc.co.uk/news/articles/cx2pwjgp59do",
# ]


# Function to information from the article
# def process_articles(urls):
#     data = []
#     try:
#         article = Article(url)
#         article.download()
#         article.parse()
#         data.append(
#             {
#                 "url": url,
#                 "title": article.title,
#             }
#         )
#     except Exception as e:
#         print(f"Failed to scrape {url}: {e}")

#     all_articles.extend(data)


# Fetch the page


# # Save scraped data to CSV
