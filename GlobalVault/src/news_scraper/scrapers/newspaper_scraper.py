import newspaper
import pandas as pd
from datetime import datetime
import logging
from typing import List, Dict
from newspaper import Article, Source
import json

import newspaper

bbc_papers = newspaper.build("https://www.bbc.co.uk/news/world", number_threads=3)

article_urls = [article.url for article in bbc_papers.articles]
print(article_urls[10])
