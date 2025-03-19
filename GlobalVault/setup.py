from setuptools import setup, find_packages

setup(
    name="news_scraper",
    version="0.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "requests==2.31.0",
        "newspaper3k==0.2.8",
        "python-dotenv==1.0.0",
        "spacy==3.7.2",
        "pandas==2.1.4",
    ],
)
