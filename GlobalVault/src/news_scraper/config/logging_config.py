# src/news_scraper/config/logging_config.py
"""
Logging configuration when news scraping.
"""
import logging
from datetime import datetime
from pathlib import Path
from .settings import Settings
import os
from dotenv import load_dotenv


def setup_logging():
    """Configure logging for the application."""
    settings = Settings()

    # Create logs directory if it doesn't exist
    log_dir = settings.LOG_DIR
    log_dir.mkdir(parents=True, exist_ok=True)

    # Generate log filename with timestamp
    log_file = log_dir / f'news_scraper_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(),  # Console output
        ],
    )

    # Set specific logger levels
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("newspaper").setLevel(logging.WARNING)

    # Log initial startup message
    logging.info(f"Logging initialized. Log file: {log_file}")
