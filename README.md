# GlobalLEARN: News Significance Analysis Framework

[![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python-390/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🌐 Overview

GlobalLEARN is an advanced framework for analyzing news articles and quantifying their global significance through AI-powered evaluation. This system helps identify high-impact news by measuring multiple dimensions of significance using large language models.

## 🚀 Features

- **Multi-dimensional Evaluation**: Assesses news articles across 7 critical factors:
  - **Scale**: Global population impact (10=affects all humanity, 5=regional, 2=local)
  - **Impact**: Immediate effect strength on humanity's development
  - **Potential**: Future influence on human civilization
  - **Legacy**: Historical milestone for human progress
  - **Novelty**: Uniqueness in human history
  - **Credibility**: Source reliability
  - **Positivity**: Positive development for humanity

- **Comprehensive Scoring**: Weighted algorithm calculating overall significance score
- **AI-powered Analysis**: Utilizes GPT-4o for nuanced content evaluation
- **Batch Processing**: Efficiently processes multiple articles in parallel
- **Content Extraction**: Automatic content scraping from article URLs
- **Results Management**: Saves analysis as structured data for further processing

## 📊 Example Output

```json
{
    "title": "Example News Article",
    "url": "https://example.com/article",
    "category": "POLITICS",
    "final_score": 6.7,
    "impact": 7,
    "scale": 8,
    "potential": 8,
    "legacy": 6,
    "novelty": 5,
    "credibility": 7,
    "positivity": 3
}
```

## 🔧 Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/GlobalLEARN.git

# Navigate to project directory
cd GlobalLEARN

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
export OPENAI_API_KEY="your_openai_api_key"
```

## 💡 Usage

### Basic Usage

```python
from openailabeling import NewsSignificanceCalculator

# Initialize calculator
calculator = NewsSignificanceCalculator()

# Extract and analyze a single article
article_content = calculator.extract_article_content("https://example.com/article")
scores = calculator.get_scores(
    article_content["text"],
    "Example Headline",
    "example_source"
)

print(f"Final significance score: {scores['final_score']}")
```

### Batch Processing

```python
# Load articles from JSON file
with open("articles.json", "r") as f:
    articles = json.load(f)

# Process articles in batches
results = calculator.process_batch(articles, batch_size=10)
```

## 🧠 AI Model Integration

The system leverages fine-tuned Transformer models (Llama 3.2 1B Instruct) for advanced text analysis. See `model1.ipynb` for implementation details on model loading and inference.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgements

- The CrossNER dataset for providing training data
- Hugging Face for transformer model implementations
- OpenAI for GPT-4o API

---

*Note: This project is part of ongoing research in natural language processing and information significance evaluation.*
# GlobalVault_Submission
