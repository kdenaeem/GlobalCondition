# src/news_scraper/config/__init__.py

"""
Configuration package for the news scraper application.
"""

from .settings import Settings
from .logging_config import setup_logging

# Create a global settings instance
settings = Settings()

# Export these items when using 'from config import *'
__all__ = ['settings', 'Settings', 'setup_logging']
