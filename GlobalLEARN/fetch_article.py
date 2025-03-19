"""fetch articles for testing methodology"""

import json
import requests
from bs4 import BeautifulSoup
from newspaper import Article


def save_article_versions(article, filename):
    """Save all versions of an article to a text file"""
    with open(f"GlobalLEARN/{filename}.txt", "w", encoding="utf-8") as f:
        # Version 1: Headline only
        f.write("VERSION 1: HEADLINE ONLY\n")
        f.write("=" * 50 + "\n")
        f.write(headline_only(article))
        f.write("\n\n" + "=" * 50 + "\n\n")

        # Version 2: Headline + full content
        f.write("VERSION 2: HEADLINE + FULL CONTENT\n")
        f.write("=" * 50 + "\n")
        full_content = headline_content(article)
        f.write(json.dumps(full_content, indent=2))
        f.write("\n\n" + "=" * 50 + "\n\n")

        # Version 3: Headline + extract
        f.write("VERSION 3: HEADLINE + EXTRACT\n")
        f.write("=" * 50 + "\n")
        extract = headline_extract(article)
        f.write(json.dumps(extract, indent=2))


def extract_article_content(url):
    """extract content"""
    try:
        # Using newspaper3k library
        downloaded_article = Article(url)
        downloaded_article.download()
        downloaded_article.parse()

        return {
            "text": downloaded_article.text,
            "summary": downloaded_article.text[:300],  # First 500 chars
        }
    except Exception as e:
        print(f"Error extracting content from {url}: {e}")
        return None


def headline_only(h_article):
    """headline only"""
    return h_article["headline"]


def headline_content(hc_article):
    """headline and content"""
    content = extract_article_content(hc_article["link"], all=True)
    if content:
        return {"headline": hc_article["headline"], "content": content}
    return {"headline": hc_article["headline"], "content": None}


def headline_extract(handearticle):
    """headline and extract"""
    content = extract_article_content(handearticle["link"], all=False)
    if content:
        return {"headline": handearticle["headline"], "extract": content}
    return {"headline": handearticle["headline"], "extract": None}


# Load articles
with open("GlobalLEARN/sampled_articles.json", "r", encoding="utf-8") as f:
    sampled_articles = json.load(f)

target_articles = [
    "Iran Says It Has Broken Stockpile Limit Set By Nuclear Deal",
    "Canada Convinced Trump Will Pull Out Of NAFTA Deal: Report",
    "Happy 92nd Birthday, George H.W. Bush",
]

# print(
#     extract_article_content(
#         "https://www.huffpost.com/entry/vulnerable-house-dems-see-abortion-as-winning-campaign-theme_n_62e6847ee4b006483a9e59ea",
#     )
# )


from urllib.parse import urlparse
import re


def get_source_from_url(url: str) -> str:
    """
    Extract news source name from URL
    Args:
        url: News article URL
    Returns:
        str: Name of the news source
    """
    try:
        # Parse the URL
        parsed_url = urlparse(url)
        domain = parsed_url.netloc.lower()

        # Remove www. if present
        domain = domain.replace("www.", "")

        # If not in mapping, extract name from domain
        # Remove common TLDs and split by dots
        name = domain.replace(".com", "").replace(".org", "").replace(".net", "")
        name = name.split(".")[0]

        # Capitalize and clean up
        name = name.replace("-", " ").replace("_", " ")
        name = " ".join(word.capitalize() for word in name.split())

        return name
    except Exception as e:
        print(f"Error extracting source from URL: {e}")
        return "Unknown Source"
