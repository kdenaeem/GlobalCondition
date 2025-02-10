from news_scraper.scrapers.newsdata_scraper import NewsDataScraper
from news_scraper.config import settings, setup_logging
from news_scraper.utils.article_formatter import ArticleFormatter
from pathlib import Path
from dotenv import load_dotenv
import os
import logging
from news_scraper.scrapers.newspaper_scraper import ManualScrape
from news_scraper.utils.article_manager import ArticleManager
from news_scraper.config.settings import Settings


def main():
    # logging
    setup_logging()
    logger = logging.getLogger(__name__)

    logger.info("Just set up logging, now settings")

    # settings
    settings = Settings()
    OUTPUT_DIR = settings.PROCESSED_DATA_DIR
    OUTPUT_FILE = settings.PROCESSED_ARTICLES_FILE
    logger.info(f"Output directory is {OUTPUT_DIR}")

    logger.info("Just set up logging, now settings")

    # Article tools
    article_formatter = ArticleFormatter()
    articleManager = ArticleManager(OUTPUT_DIR, OUTPUT_FILE)

    # Start logging
    logger.info("Strarted news scraping")

    try:
        # scraper = NewsDataScraper()
        # scraper.run(limit=15)
        # sample_article = [
        #     {
        #         "title": "Hello",
        #         "link": "https://www.bbc.co.uk/news/world-africa-12345678",
        #     }
        # ]

        # articleManager.save_articles(sample_article, article_formatter)

        scraper = ManualScrape()
        all_articles = scraper.fetch_bbc_urls()
        # articleManager.save_articles(all_articles)
        logger.info("Completed news scraping")
    except Exception as e:
        logger.error(f"Error in main scraping process {e}")
        raise


if __name__ == "__main__":
    main()
