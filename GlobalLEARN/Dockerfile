# Use Python 3.9 specifically
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
  git \
  && rm -rf /var/lib/apt/lists/*

# Copy requirements file and install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your Python script
COPY main.py .

# Force Python to run unbuffered
ENV PYTHONUNBUFFERED=1

# Command to run when starting the container
CMD ["python", "-u", "main.py"]

