import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv('keys.env')  # Update path to your .env file

class Settings:
    """Application settings configuration."""

    def __init__(self):
        # API Keys
        self.NEWSDATA_API_KEY = os.getenv('NEWSDATA_API_KEY', '')

        # Directory setup - point to root level directories
        self.BASE_DIR = Path(__file__).parent.parent.parent.parent  # Go up to GlobalVault
        self.DATA_DIR = self.BASE_DIR / 'data'
        self.RAW_DATA_DIR = self.DATA_DIR / 'raw'
        self.PROCESSED_DATA_DIR = self.DATA_DIR / 'processed'
        self.LOG_DIR = self.BASE_DIR / 'logs'

        # File Names
        self.RAW_ARTICLES_FILE = 'news_articles.json'
        self.PROCESSED_ARTICLES_FILE = 'transformed_articles.json'

        # Create necessary directories
        self._create_directories()
        self.BBC_URLS = [
            "https://www.bbc.co.uk/news/world",
            "https://www.bbc.co.uk/news/world/africa",
            "https://www.bbc.co.uk/news/world/asia",
            "https://www.bbc.co.uk/news/world/australia",
            "https://www.bbc.co.uk/news/world/europe",
            "https://www.bbc.co.uk/news/world/latin_america",
            "https://www.bbc.co.uk/news/world/middle_east",
            "https://www.bbc.co.uk/news/world/us_and_canada"
        ]

        # Al Jazeera URLs
        self.ALJAZEERA_URLS = [
            "https://www.aljazeera.com/africa/",
            "https://www.aljazeera.com/middle-east/",
            "https://www.aljazeera.com/asia/",
            "https://www.aljazeera.com/europe/"
        ]


    def _create_directories(self):
        """Create necessary directories if they don't exist."""
        for directory in [self.DATA_DIR, self.RAW_DATA_DIR,
                         self.PROCESSED_DATA_DIR, self.LOG_DIR]:
            directory.mkdir(parents=True, exist_ok=True)
            
    def get_urls_by_source(self, source: str) -> list:
        """Get URLs for a specific news source."""
        sources = {
            'bbc': self.BBC_URLS,
            'aljazeera': self.ALJAZEERA_URLS
        }
        return sources.get(source.lower(), [])
