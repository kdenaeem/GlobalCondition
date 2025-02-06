FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire src directory
COPY src/ ./src/

# Create necessary directories
RUN mkdir -p data/raw data/processed logs

# Set Python path
ENV PYTHONPATH=/app/src
ENV DOCKER_ENV = 1

# Command to run the scraper
CMD ["python", "src/news_scraper/main.py"]
