import hashlib
import re
import logging
from typing import Dict, List


class ArticleFormatter:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    @staticmethod
    def get_hash(url: str):
        hash_object = hashlib.sha256(url.encode())
        return hash_object.hexdigest()[:8]

    @staticmethod
    def clean_method(title: str):
        """Clean up the title by removing unwanted elements"""
        # Remove image URLs that end with .webp)
        title = re.sub(r"https://.*?\.webp\)", "", title)
        # Remove image markdown
        title = re.sub(r"!\[Image \d+: .*?\]", "", title)
        # Remove leading parentheses
        title = title.lstrip("(")
        # Remove "LIVE" tag
        title = re.sub(r"^\s*LIVE\s*", "", title)

        # Split at first occurrence of multiple dashes and keep only the title part
        parts = re.split(r"-{2,}", title)
        if parts:
            title = parts[0]

        # Remove multiple spaces
        title = " ".join(title.split())
        return title.strip()

    def format_article(self, article: Dict):
        try:
            return {
                "article_id": self.get_hash(article["link"]),
                "title": self.clean_method(article["title"]),
                "link": article["link"],
            }
        except Exception as e:
            self.logger.error(f"Error exception article : {e}")
            return None

    def format_articles(self, articles: List[Dict]):
        formatted_articles = []
        try:
            self.logger.info(f"Formatting {len(articles)} articles")
            for article in articles:
                formatted = self.format_article(
                    article
                )  # Fixed: now passing individual article
                if formatted:
                    formatted_articles.append(formatted)
        except Exception as e:
            self.logger.error(f"Error formatting multiple articles: {e}")
        return formatted_articles
