"""Stratified Sampling of News Articles from Kaggle Dataset"""

import random
import json
from collections import defaultdict
from newspaper import Article


def get_sampling_categories(total_samples=10):
    """
    Sampling proportions for significance scoring dataset
    Primary: Politics/World News (high impact global events) - 60%
    Secondary: Business/Tech/Science (medium impact) - 25%
    Tertiary: Culture/Lifestyle (lower impact) - 15%
    """
    primary_categories = {
        "POLITICS": int(total_samples * 0.4),  # 40% (160 articles)
        "WORLD NEWS": int(total_samples * 0.2),  # 20% (80 articles)
    }

    secondary_categories = {
        "BUSINESS": int(total_samples * 0.1),  # 10% (40 articles)
        "TECH": int(total_samples * 0.075),  # 7.5% (30 articles)
        "SCIENCE": int(total_samples * 0.075),  # 7.5% (30 articles)
    }

    tertiary_categories = {
        "ENTERTAINMENT": int(total_samples * 0.05),  # 5% (20 articles)
        "SPORTS": int(total_samples * 0.05),  # 5% (20 articles)
        "BLACK VOICES": int(total_samples * 0.025),  # 2.5% (10 articles)
        "WELLNESS": int(total_samples * 0.025),  # 2.5% (10 articles)
    }

    # Verification of total
    return {**primary_categories, **secondary_categories, **tertiary_categories}


with open("GlobalLEARN/News_Category_Dataset_v3.json", "r", encoding="utf-8") as file:
    # Read the file line by line since it's JSON Lines format
    articles_by_category = defaultdict(list)
    for line in file:
        article = json.loads(line.strip())
        articles_by_category[article["category"]].append(article)

sampled_articles = []
sampled_counts = get_sampling_categories()

for category, count in sampled_counts.items():
    # sampled_articles[category] = articles_by_category[category][:count]
    sampled_articles.extend(articles_by_category[category][:count])


# sampled_articles = []  # Initialize as a list instead of dict
# for category, target_count in sampled_counts.items():
#     if category in articles_by_category:
#         # Sample articles from this category
#         category_samples = random.sample(articles_by_category[category], target_count)
#         # Extend the main list with these samples
#         sampled_articles.extend(category_samples)
#         print(f"Sampled {target_count} articles from {category}")

print(f"Total articles sampled: {len(sampled_articles)}")


print(sampled_articles)

for articles in sampled_articles:
    print(f"Sampled {len(articles)} articles from")

with open("GlobalLEARN/sampled_articles.json", "w", encoding="utf-8") as file:
    json.dump(sampled_articles, file, ensure_ascii=False, indent=2)
