import requests
import json
import logging
from typing import List, Dict
from news_scraper.config import settings, setup_logging


class NewsDataScraper:
    def __init__(self):
        setup_logging()
        self.logger = logging.getLogger(__name__)

        self.settings = settings

        self.base_url = (
            "https://newsdata.io/api/1/latest?"
            f"apikey={self.settings.NEWSDATA_API_KEY}"
            "&prioritydomain=top"
            "&category=world"
            "&language=en"
            "&excludedomain=moneycontrol.com"
        )

        self.params = {
            "apikey": self.settings.NEWSDATA_API_KEY,
            "language": "en",
            "size": 10,
        }

    def fetch_articles(self, limit: int = 15):
        articles = []
        nextpage = None

        self.logger.info("Starting to fetch from NewsData.io")
        try:
            while len(articles) < limit:
                if nextpage:
                    self.params["page"] = nextpage
                self.logger.debug(
                    f"Making API request, current articles: {len(articles)}"
                )
                response = requests.get(self.base_url, params=self.params)
                data = response.json()

                if "results" in data:
                    articles.extend(data["results"])
                    next_page = data.get("nextPage")
                    self.logger.info(
                        f"Fetched batch of articles, total: {len(articles)}"
                    )

                if not next_page:
                    self.logger.info("No more pages available")
                    break
                self.logger.info(f"Finished fetching articles, total: {len(articles)}")
                return articles[:limit]  # Ensure we don't exceed the limit

        except Exception as e:
            self.logger.error(f"Error fetching articles: {str(e)}")
            return []

    def save_articles(self, articles: List[Dict]):
        """save articles in json file"""
        try:
            output_path = self.settings.RAW_DATA_DIR / self.settings.RAW_ARTICLES_FILE
            print(output_path)
            # Load existing articles
            existing_articles = []
            if output_path.exists():
                with open(output_path, "r", encoding="utf-8") as f:
                    existing_articles = json.load(f)
                self.logger.info(f"Loaded {len(existing_articles)} existing articles")
            else:
                self.logger.warning(f"No existing articles file found at {output_path}")

            # Combine articles
            combined_articles = articles + existing_articles

            # Save combined articles
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(combined_articles, f, ensure_ascii=False, indent=4)

            self.logger.info(
                f"Saved {len(combined_articles)} articles to {output_path}"
            )

        except Exception as e:
            self.logger.error(f"Error saving articles: {str(e)}")

    def run(self, limit: int = 15):
        """fetch and save articles"""

        self.logger.info("started news scraping")
        articles = self.fetch_articles(limit)
        if articles:
            self.save_articles(articles)
        self.logger.info("Completed newsdata scraping")


def main():
    scraper = NewsDataScraper()
    scraper.run(limit=15)


if __name__ == "__main__":
    main()
