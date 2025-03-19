import logging
import json


class ArticleManager:
    """class for saving articles, loading articles and checking for duplicates"""

    def __init__(self, output_dir, output_file):
        self.output_path = output_dir / output_file
        self.logger = logging.getLogger(__name__)

    def load_article(self):
        if self.output_path.exists():
            with open(self.output_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def save_articles(self, articles, formatter=None):
        try:
            existing_articles = self.load_article()
            self.logger.info(
                f"Loaded {len(existing_articles)} existing articles from files"
            )
            if formatter:
                format_articles = formatter.format_articles(articles)
                print(format_articles)
            else:
                format_articles = articles

            existing_ids = {article["article_id"] for article in existing_articles}

            unique_articles = [
                article
                for article in format_articles
                if article["article_id"] not in existing_ids
            ]

            all_articles = unique_articles + existing_articles
            self.logger.info(f"Added {len(unique_articles)} new formatted articles")
            with open(self.output_path, "w", encoding="utf-8") as f:
                json.dump(all_articles, f, ensure_ascii=False, indent=4)
            self.logger.info(f"Total articles in processed file: {len(all_articles)}")

            return len(unique_articles), len(all_articles)

        except Exception as e:
            self.logger.error(f"Error saving articles: {str(e)}")
            return 0, 0
