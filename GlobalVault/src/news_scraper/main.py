from news_scraper.scrapers.newsdata_scraper import NewsDataScraper
from news_scraper.config import settings, setup_logging
from news_scraper.utils.article_formatter import ArticleFormatter
from pathlib import Path
from dotenv import load_dotenv
import os
import logging


def main():
    setup_logging()
    article_formatter = ArticleFormatter()
    logger = logging.getLogger(__name__)

    logger.info("Strarted news scraping")

    try:
        scraper = NewsDataScraper()
        scraper.run(limit=15)

    except Exception as e:
        logger.error(f"Error in main scraping process {e}")
        raise


if __name__ == "__main__":
    main()
