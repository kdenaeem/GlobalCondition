import requests
import json
import logging
from typing import List, Dict
from news_scraper.config.logging_config import setup_logging
from news_scraper.config.settings import Settings

from utils.article_formatter import ArticleFormatter


class NewsDataScraper:
    """ "Class for scraping news data.io sources"""

    def __init__(self):
        setup_logging()
        self.logger = logging.getLogger(__name__)
        self.settings = Settings()
        self.formatter = ArticleFormatter()

        self.base_url = (
            "https://newsdata.io/api/1/latest?"
            f"apikey={self.settings.NEWSDATA_API_KEY}"
            "&prioritydomain=top"
            "&category=world"
            "&language=en"
            "&excludedomain=moneycontrol.com"
        )

        self.logger.info(f"API URL is : {self.base_url}")

        self.params = {
            "apikey": self.settings.NEWSDATA_API_KEY,
            "language": "en",
            "size": 10,
        }

    def fetch_articles(self, limit: int = 15):
        """fetch articles from newsdata.io api"""
        articles = []
        nextpage = None
        next_page = ""

        self.logger.info("Starting to fetch from NewsData.io")
        try:
            response = requests.get(self.base_url, params=self.params, timeout=10000)
            data = response.json()

            self.logger.info(data)

            while len(articles) < limit:
                if nextpage:
                    self.params["page"] = nextpage
                self.logger.debug(
                    f"Making API request, current articles: {len(articles)}"
                )
                response = requests.get(
                    self.base_url, params=self.params, timeout=100000
                )
                data = response.json()

                if "results" in data:
                    articles.extend(data["results"])
                    # next_page = data.get("nextPage")
                    self.logger.info(
                        f"Fetched batch of articles, total: {len(articles)}"
                    )
                else:
                    self.logger.error(f"Unexpected API response format : {data} ")
                    return []

                # if not next_page:
                #     self.logger.info("No more pages available")
                #     break

            self.logger.info(f"Finished fetching articles, total: {len(articles)}")
            self.logger.info(f"Raw articles: {articles[:2]}")
            return articles[:limit]  # Ensure we don't exceed the limit

        except Exception as e:
            self.logger.error(f"Error fetching articles: {str(e)}")
            return []

    def save_articles(self, articles: List[Dict]):
        """save articles in json file"""
        try:
            formatted_articles = self.formatter.format_articles(articles)

            output_path = (
                self.settings.PROCESSED_DATA_DIR / self.settings.PROCESSED_ARTICLES_FILE
            )

            # Load existing articles
            existing_articles = []
            if output_path.exists():
                with open(output_path, "r", encoding="utf-8") as f:
                    existing_articles = json.load(f)
                self.logger.info(f"Loaded {len(existing_articles)} existing articles")
            else:
                self.logger.warning(f"No existing articles file found at {output_path}")
            # Add new articles, avoiding duplicates by article_id
            existing_ids = {article["article_id"] for article in existing_articles}
            new_articles = [
                article
                for article in formatted_articles
                if article["article_id"] not in existing_ids
            ]

            # Combine and save
            all_articles = new_articles + existing_articles
            print(existing_articles)
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(all_articles, f, ensure_ascii=False, indent=4)

            self.logger.info(f"Added {len(new_articles)} new formatted articles")
            self.logger.info(f"Total articles in processed file: {len(all_articles)}")

        except Exception as e:
            self.logger.error(f"Error saving articles: {str(e)}")

    def run(self, limit: int = 15):
        """fetch and save articles"""

        self.logger.info("Started news scraping")
        articles = self.fetch_articles(limit)
        if articles:
            self.save_articles(articles)
        self.logger.info("Completed newsdata scraping")


def main():
    """Main newscraper"""
    scraper = NewsDataScraper()
    scraper.run(limit=20)


if __name__ == "__main__":
    main()
