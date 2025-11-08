# Use official Python 3.11 image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the FastAPI app
COPY service.py .

# Expose the port FastAPI will run on
EXPOSE 8080

# Use environment variable PORT (Cloud Run uses this)
ENV PORT=8080

# Start Uvicorn
CMD ["uvicorn", "service:app", "--host", "0.0.0.0", "--port", "8080"]
