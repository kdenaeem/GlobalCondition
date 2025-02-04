import news_scraper
from news_scraper.scrapers.newsdata_scraper import NewsDataScraper
from news_scraper.config import settings, setup_logging
import logging


def main():
  setup_logging()
  logger = logging.getLogger(__name__)

  logger.info("Started news scraping")

  try:

    scraper = NewsDataScraper()
    scraper.run(limit=15)

  except Exception as e:
    logger.error(f"Error in main scraping process")
    raise


if __name__  == "__main__":
  main()


