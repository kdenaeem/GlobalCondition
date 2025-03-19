import time
import json
from typing import Dict, List
from openai import OpenAI
from newspaper import Article
import pandas as pd
import re
import os


class NewsSignificanceCalculator:
    """Calculate the significance of news article"""

    def __init__(self):
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.prompt_template = """Return a score of each factor for the news article I have attached at the end (0-10 for each factor):

Factors and weights:
- scale : Global population impact (10=affects all humanity, 5=regional, 2=local)
- impact : Immediate effect strength on humanity's development
- potential : Future influence on human civilization
- legacy : Historical milestone for human progress
- novelty : Uniqueness in human history
- credibility : Source reliability
- positivity : Positive development for humanity

Scale scoring guideline:
10: Affects all of humanity directly
8: Major global impact
6: Multi-region impact
4: Regional impact
2: Local impact

Impact scoring guideline:
10: Immediate global emergency
8: Major global change
6: Significant regional change
4: Moderate regional effect
2: Local effect

YOU MUST RETURN ONLY A VALID JSON OBJECT IN THIS EXACT FORMAT:
    "scale": 0,
    "impact": 0,
    "potential": 0,
    "legacy": 0,
    "novelty": 0,
    "credibility": 0,
    "positivity": 0
Calibration Examples:
Global Impact (6.3/10): "Earth surpasses 1.5°C warming limit"
    "scale": 9,
    "impact": 8,
    "potential": 9,
    "legacy": 8,
    "novelty": 7,
    "credibility": 9,
    "positivity": 2

Regional Conflict (5.0/10): "Military escalation in ongoing war"
    "scale": 5,
    "impact": 6,
    "potential": 5,
    "legacy": 5,
    "novelty": 5,
    "credibility": 9,
    "positivity": 2

Local Event (2.2/10): "Regional sports championship"
    "scale": 2,
    "impact": 2,
    "potential": 1,
    "legacy": 1,
    "novelty": 2,
    "credibility": 8,
    "positivity": 8

Significance ranges:
High (6+): Major impact on human civilization
Medium (3-5): Regional/industry significance
Low (1-2): Local/minor impact

Below is the news article:
Source: {article_source}
Headline: {article_headline}
Article Content: {article_text}"""

    def calculate_final_score(self, scores: Dict[str, float]) -> float:
        """calculate final significance value"""
        weights = {
            "scale": 0.22,
            "impact": 0.21,
            "potential": 0.15,
            "legacy": 0.15,
            "novelty": 0.17,
            "credibility": 0.05,
            "positivity": 0.05,
        }

        weighted_scores = {}
        for factor, weight in weights.items():
            weighted_scores[factor] = scores[factor] * weight

        base_score = sum(weighted_scores.values())
        positivity_adjustment = 0.5 if scores["positivity"] >= 7 else 0

        return round(base_score + positivity_adjustment, 1)

    def get_scores(
        self, article_text: str, article_headline: str, articlesource: str
    ) -> Dict:
        """retrieve scores from the model"""

        try:
            prompt = self.prompt_template.format(
                article_headline=article_headline,
                article_text=article_text,
                article_source=articlesource,
            )

            print(prompt)

            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
            )
            response_text = response.choices[0].message.content.strip()
            response_text = (
                response_text.replace("```json", "").replace("```", "").strip()
            )
            try:
                # First attempt to parse the JSON directly
                scores = json.loads(response_text)
            except json.JSONDecodeError:
                # If direct parsing fails, try to extract JSON using regex

                json_pattern = r"\{[^{}]*\}"
                matches = re.findall(json_pattern, response_text)
                if matches:
                    scores = json.loads(matches[0])
                else:
                    raise Exception(
                        f"Could not find valid JSON in response: {response_text}"
                    )

            # Calculate final score
            final_score = self.calculate_final_score(scores)
            scores["final_score"] = final_score

            return scores
        except Exception as e:
            print(f"Error processing article: {article_headline}")
            print(f"Error details: {str(e)}")
            print(
                f"Response text: {response_text if 'response_text' in locals() else 'No response'}"
            )
            raise  # Re-raise the exception after logging

    def extract_article_content(self, url):
        """extract content"""
        try:
            # Using newspaper3k library
            downloaded_article = Article(url)
            downloaded_article.download()
            downloaded_article.parse()
            if not downloaded_article.text:
                print(f"No content extracted from {url}")
                return None
            text = downloaded_article.text.strip()
            text = " ".join(text.split())
            text = text.replace("LOADING ERROR LOADING", "")
            text = text.replace("Advertisement", "")  # Also remove advertisements
            text = text.replace("\n\n\n", "\n")  # Clean up multiple newlines
            print("removing ads and new lines")

            return {
                "text": text,
                "summary": downloaded_article.text[:300],  # First 500 chars
            }
        except Exception as e:
            print(f"Error extracting content from {url}: {e}")
            return None

    def process_batch(self, articles: List[Dict], batch_size: int = 2):
        """process batch of articles"""
        results = []

        for i in range(0, len(articles), batch_size):
            print(f"Processing batch {i + 1} - {i + batch_size}")
            batch = articles[i : i + batch_size]
            print(f"Processing batch {i + 1} - {i + batch_size}")
            for article in batch:
                print(f"Processing article: {article['headline']}")

                scores = self.get_scores(
                    self.extract_article_content(article["link"])["text"],
                    article["headline"],
                    "huffingtonpost",
                )

                if scores:
                    result = {
                        "title": article["headline"],
                        "url": article["link"],
                        "category": article["category"],
                        "scores": scores,
                    }
                    results.append(result)

                time.sleep(1)
            self.save_results(results, f"significance_scores_{i//batch_size + 1}.json")
        return results

    @staticmethod
    def save_results(results: List[Dict], filename: str):
        """ "save to json file"""
        batch_data = pd.DataFrame(results)
        batch_data.to_csv(f"GlobalLEARN/{filename}.csv", index=False)


def main():
    # article = {
    #     "title": "Happy 92nd Birthday, George H.W. Bush",
    #     "text": """KYIV (Reuters) - Russian troops have sharply stepped up their attacks in eastern Ukraine, Kyiv's military said on Sunday, as a NATO official predicted Moscow would increase the pace and intensity of its assaults with talks to end the war approaching.The main attacks were concentrated near the imperilled logistics hub of Pokrovsk, Kyiv said, with U.S. and Russian officials expected to hold talks in the coming days in Saudi Arabia and U.S President Donald Trump pushing for peace.Kyiv's military reported 261 combat engagements with Russia over a 24-hour period on Saturday, easily the largest number recorded this year and more than double the roughly 100 per day it reported in previous days.Today was the hardest day of 2025 at the front," the Ukrainian DeepState military blog wrote late on Saturday.Moscow's troops advanced steadily in the east for much of the second half 2024, announcing the capture of village after village, though the intensity of the fighting dropped in January this year, according to Ukrainian military data.""",
    #     "source": "huffingtonpost",
    # }

    with open("GlobalLEARN/sampled_articles.json", "r", encoding="utf-8") as f:
        articles = json.load(f)

    calculator = NewsSignificanceCalculator()

    # Process articles in batches
    results = calculator.process_batch(articles, batch_size=10)

    summary_data = []
    for result in results:
        summary_data.append(
            {
                "title": result["title"],
                "url": result["url"],
                "category": result["category"],
                "final_score": result["scores"]["final_score"],
                "impact": result["scores"]["impact"],
                "scale": result["scores"]["scale"],
                "potential": result["scores"]["potential"],
                "legacy": result["scores"]["legacy"],
                "novelty": result["scores"]["novelty"],
                "credibility": result["scores"]["credibility"],
                "positivity": result["scores"]["positivity"],
            }
        )

    summary_data = pd.DataFrame(summary_data)
    summary_data.to_csv("GlobalLEARN/summary_data.csv", index=False)

    print("prcessing complete")
    print(f"Processed {len(results)} articles")


if __name__ == "__main__":
    main()
